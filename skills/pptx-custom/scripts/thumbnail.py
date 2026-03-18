#!/usr/bin/env python3
"""
thumbnail.py — Generate a visual thumbnail grid from a PowerPoint file (.pptx).

Each slide is rasterised to a JPEG and arranged in a grid image that can be
inspected at a glance.  This is useful for visual QA of presentations:
checking for overlapping elements, text overflow, low-contrast text,
placeholder content, and layout consistency across all slides.

The pipeline is:
  1. Convert the .pptx to a PDF using LibreOffice (headless).
  2. Rasterise each PDF page to a JPEG using ``pdftoppm`` (Poppler).
  3. Arrange the per-slide JPEGs in a grid using Pillow and save the result.

Prerequisites:
  - LibreOffice  (via office-custom/scripts/soffice.py or system ``soffice``)
  - Poppler      (provides ``pdftoppm``)
  - Pillow       (pip install Pillow)

LibreOffice wrapper used (in search order):
  1. office-custom/scripts/soffice.py  — sibling skill (preferred)
  2. scripts/office/soffice.py         — legacy repo-root location
  3. System ``soffice`` / ``libreoffice`` binary on PATH

Usage:
    python pptx-custom/scripts/thumbnail.py presentation.pptx [output.jpg]

    If *output.jpg* is omitted, the grid is saved as
    ``<presentation_stem>-thumbnails.jpg`` next to the input file.

Options:
    --cols   N     Number of columns in the grid (default: 3).
    --dpi    N     Rasterisation resolution in DPI (default: 96).
    --width  N     Width of each thumbnail in pixels (default: 400).
    --quiet        Suppress progress output.

Exit codes:
    0  — Success.
    1  — Input file not found, dependency missing, or conversion failure.

Example:
    python pptx-custom/scripts/thumbnail.py deck.pptx deck-qa.jpg --cols 4 --dpi 120
"""

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# ---------------------------------------------------------------------------
# soffice.py location discovery
# ---------------------------------------------------------------------------

def _find_soffice_py() -> Path | None:
    """
    Search for the soffice.py LibreOffice wrapper in well-known locations.

    Search order:
      1. ``office-custom/scripts/soffice.py``  — sibling skill (preferred)
      2. ``scripts/office/soffice.py``          — legacy repo-root location
      3. Returns None if neither exists (caller falls back to system soffice)

    The search anchors from the *repository root*, derived by walking two
    levels up from this file (pptx-custom/scripts/ → pptx-custom/ → repo/).
    """
    # This file lives at: <repo>/pptx-custom/scripts/thumbnail.py
    # repo root is two parents up.
    repo_root = Path(__file__).parent.parent.parent

    candidates = [
        repo_root / "office-custom" / "scripts" / "soffice.py",  # sibling skill
        repo_root / "scripts" / "office" / "soffice.py",         # legacy location
    ]
    return next((p for p in candidates if p.exists()), None)


# ---------------------------------------------------------------------------
# Dependency checks
# ---------------------------------------------------------------------------

def _check_pillow() -> None:
    """Exit with an informative message if Pillow is not installed."""
    try:
        global Image  # noqa: PLW0603
        from PIL import Image  # type: ignore[import]
    except ImportError:
        print(
            "ERROR: Pillow is not installed.  Run: pip install Pillow",
            file=sys.stderr,
        )
        sys.exit(1)


def _find_pdftoppm() -> str:
    """
    Return the path to the ``pdftoppm`` binary, or exit if it cannot be found.

    ``pdftoppm`` is part of the Poppler utilities package:
      - macOS:  brew install poppler
      - Ubuntu: apt install poppler-utils
    """
    binary = shutil.which("pdftoppm")
    if binary is None:
        print(
            "ERROR: pdftoppm not found on PATH.\n"
            "  macOS: brew install poppler\n"
            "  Ubuntu/Debian: apt install poppler-utils",
            file=sys.stderr,
        )
        sys.exit(1)
    return binary


# ---------------------------------------------------------------------------
# Step 1: pptx → PDF via LibreOffice
# ---------------------------------------------------------------------------

def _pptx_to_pdf(pptx_path: Path, out_dir: Path, quiet: bool) -> Path:
    """
    Convert *pptx_path* to a single PDF file inside *out_dir*.

    Uses ``office-custom/scripts/soffice.py`` (via :func:`_find_soffice_py`)
    if available, otherwise falls back to the ``soffice`` binary on PATH.

    Args:
        pptx_path: Absolute path to the .pptx file.
        out_dir:   Directory where LibreOffice should write the PDF.
        quiet:     Suppress progress messages.

    Returns:
        Path to the generated PDF file.

    Raises:
        SystemExit: If conversion fails.
    """
    soffice_py = _find_soffice_py()
    success    = False

    if soffice_py is not None:
        # Use the wrapper script so we get the same profile-isolation logic
        # that handles sandboxed and restricted environments.
        try:
            import importlib.util
            spec   = importlib.util.spec_from_file_location("soffice", soffice_py)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            result  = module.run([
                "--headless",
                "--convert-to", "pdf",
                "--outdir", str(out_dir),
                str(pptx_path),
            ])
            success = (result.returncode == 0)
        except Exception as exc:
            if not quiet:
                print(f"WARNING: soffice.py failed ({exc}), trying system soffice.", file=sys.stderr)

    if not success:
        # Fall back to bare soffice binary.
        binary = shutil.which("soffice") or shutil.which("libreoffice")
        if binary is None:
            print(
                "ERROR: LibreOffice (soffice) not found.  "
                "Install LibreOffice to use thumbnail.py.",
                file=sys.stderr,
            )
            sys.exit(1)
        result = subprocess.run(
            [binary, "--headless", "--convert-to", "pdf",
             "--outdir", str(out_dir), str(pptx_path)],
            capture_output=True,
        )
        if result.returncode != 0:
            print(
                "ERROR: LibreOffice PDF conversion failed.\n"
                f"  stdout: {result.stdout.decode(errors='replace')}\n"
                f"  stderr: {result.stderr.decode(errors='replace')}",
                file=sys.stderr,
            )
            sys.exit(1)

    pdf_path = out_dir / (pptx_path.stem + ".pdf")
    if not pdf_path.exists():
        print(f"ERROR: Expected PDF not found at {pdf_path}", file=sys.stderr)
        sys.exit(1)

    if not quiet:
        print(f"  Converted to PDF: {pdf_path.name}")
    return pdf_path


# ---------------------------------------------------------------------------
# Step 2: PDF → per-page JPEGs via pdftoppm
# ---------------------------------------------------------------------------

def _pdf_to_jpegs(pdf_path: Path, out_dir: Path, dpi: int, quiet: bool) -> list[Path]:
    """
    Rasterise each page of *pdf_path* to a JPEG using ``pdftoppm``.

    Args:
        pdf_path: Path to the PDF produced by LibreOffice.
        out_dir:  Directory where per-page images will be written.
        dpi:      Resolution in dots per inch.
        quiet:    Suppress progress messages.

    Returns:
        Sorted list of JPEG file paths (one per slide).

    Raises:
        SystemExit: If pdftoppm fails.
    """
    pdftoppm = _find_pdftoppm()
    prefix   = out_dir / "slide"

    result = subprocess.run(
        [pdftoppm, "-jpeg", "-r", str(dpi), str(pdf_path), str(prefix)],
        capture_output=True,
    )
    if result.returncode != 0:
        print(
            "ERROR: pdftoppm failed.\n"
            f"  stdout: {result.stdout.decode(errors='replace')}\n"
            f"  stderr: {result.stderr.decode(errors='replace')}",
            file=sys.stderr,
        )
        sys.exit(1)

    # pdftoppm names files slide-1.jpg, slide-2.jpg, … (zero-padded for large decks)
    jpegs = sorted(out_dir.glob("slide-*.jpg"), key=lambda p: _page_number(p))

    if not jpegs:
        print("ERROR: pdftoppm produced no output images.", file=sys.stderr)
        sys.exit(1)

    if not quiet:
        print(f"  Rasterised {len(jpegs)} slide(s) at {dpi} DPI.")
    return jpegs


def _page_number(path: Path) -> int:
    """Extract the numeric page index from a pdftoppm output filename."""
    # Filename is "slide-NNN.jpg" where NNN may be zero-padded.
    stem  = path.stem  # e.g. "slide-001"
    parts = stem.rsplit("-", 1)
    try:
        return int(parts[-1])
    except (ValueError, IndexError):
        return 0


# ---------------------------------------------------------------------------
# Step 3: Compose thumbnail grid with Pillow
# ---------------------------------------------------------------------------

def _compose_grid(
    jpeg_paths: list[Path],
    output_path: Path,
    thumb_width: int,
    cols: int,
    quiet: bool,
) -> None:
    """
    Arrange *jpeg_paths* into a grid image and save to *output_path*.

    Each thumbnail is scaled to *thumb_width* pixels wide (aspect-preserved).
    Thumbnails are laid out left-to-right, top-to-bottom in rows of *cols*
    columns.  A subtle slide-number label is drawn in the top-left corner of
    each thumbnail.

    Args:
        jpeg_paths:  Ordered list of per-slide JPEG paths.
        output_path: Where to save the final grid JPEG.
        thumb_width: Width of each individual thumbnail in pixels.
        cols:        Number of columns in the grid.
        quiet:       Suppress progress messages.
    """
    from PIL import Image, ImageDraw, ImageFont  # type: ignore[import]

    # Load and scale each slide image.
    thumbs: list[Image.Image] = []
    for jp in jpeg_paths:
        img = Image.open(jp)
        aspect = img.height / img.width
        thumb_height = int(thumb_width * aspect)
        thumbs.append(img.resize((thumb_width, thumb_height), Image.LANCZOS))

    # All thumbnails share the same dimensions (same slide size).
    tw = thumbs[0].width
    th = thumbs[0].height

    rows    = (len(thumbs) + cols - 1) // cols  # ceiling division
    padding = 8   # pixels between thumbnails
    grid_w  = cols * tw + (cols + 1) * padding
    grid_h  = rows * th + (rows + 1) * padding

    # Create a light-grey canvas.
    grid = Image.new("RGB", (grid_w, grid_h), color=(220, 220, 220))
    draw = ImageDraw.Draw(grid)

    # Try to load a small bitmap font for labels; fall back to default.
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", size=14)
    except (OSError, AttributeError):
        font = ImageFont.load_default()

    for idx, thumb in enumerate(thumbs):
        row = idx // cols
        col = idx  % cols
        x   = padding + col * (tw + padding)
        y   = padding + row * (th + padding)
        grid.paste(thumb, (x, y))

        # Slide number label (1-based).
        label = str(idx + 1)
        # Semi-transparent dark rectangle behind the label for readability.
        draw.rectangle([x + 2, y + 2, x + 26, y + 18], fill=(0, 0, 0, 160))
        draw.text((x + 4, y + 3), label, fill=(255, 255, 255), font=font)

    grid.save(str(output_path), "JPEG", quality=88)

    if not quiet:
        print(f"  Grid saved: {output_path}  ({cols} cols × {rows} rows, {len(thumbs)} slides)")


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def generate_thumbnails(
    pptx_path:   Path,
    output_path: Path | None = None,
    cols:        int         = 3,
    dpi:         int         = 96,
    thumb_width: int         = 400,
    quiet:       bool        = False,
) -> Path:
    """
    Generate a thumbnail grid JPEG for *pptx_path*.

    Args:
        pptx_path:   Path to the .pptx file.
        output_path: Where to save the grid image.  Defaults to
                     ``<stem>-thumbnails.jpg`` next to the input file.
        cols:        Grid columns (default 3).
        dpi:         Rasterisation DPI (default 96).
        thumb_width: Width of each thumbnail in pixels (default 400).
        quiet:       Suppress progress output.

    Returns:
        Path to the saved thumbnail grid image.
    """
    _check_pillow()

    pptx_path = Path(pptx_path).resolve()
    if not pptx_path.exists():
        print(f"ERROR: File not found: {pptx_path}", file=sys.stderr)
        sys.exit(1)

    if output_path is None:
        output_path = pptx_path.parent / f"{pptx_path.stem}-thumbnails.jpg"
    else:
        output_path = Path(output_path).resolve()

    if not quiet:
        print(f"Generating thumbnails for {pptx_path.name} …")

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)

        # Step 1: pptx → PDF
        pdf_path = _pptx_to_pdf(pptx_path, tmp, quiet)

        # Step 2: PDF → per-slide JPEGs
        jpeg_paths = _pdf_to_jpegs(pdf_path, tmp, dpi, quiet)

        # Step 3: Compose and save grid
        _compose_grid(jpeg_paths, output_path, thumb_width, cols, quiet)

    return output_path


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("input",  help="Input .pptx file")
    parser.add_argument(
        "output",
        nargs="?",
        help="Output thumbnail grid JPEG (default: <stem>-thumbnails.jpg)",
    )
    parser.add_argument(
        "--cols",
        type=int,
        default=3,
        metavar="N",
        help="Number of columns in the grid (default: 3)",
    )
    parser.add_argument(
        "--dpi",
        type=int,
        default=96,
        metavar="N",
        help="Rasterisation resolution in DPI (default: 96)",
    )
    parser.add_argument(
        "--width",
        type=int,
        default=400,
        metavar="N",
        dest="thumb_width",
        help="Thumbnail width in pixels (default: 400)",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress progress output",
    )
    args = parser.parse_args()

    out = generate_thumbnails(
        pptx_path   = Path(args.input),
        output_path = Path(args.output) if args.output else None,
        cols        = args.cols,
        dpi         = args.dpi,
        thumb_width = args.thumb_width,
        quiet       = args.quiet,
    )
    print(f"OK  {out}")


if __name__ == "__main__":
    main()
