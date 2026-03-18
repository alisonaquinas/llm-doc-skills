#!/usr/bin/env python3
"""
soffice.py — LibreOffice CLI wrapper

Locates LibreOffice on macOS, Linux, or inside a sandboxed environment and
invokes it as a subprocess.  All arguments are forwarded verbatim, so this
script is a drop-in replacement for calling `soffice` directly.

Why this wrapper instead of calling soffice directly?
- LibreOffice lives at different paths on different OSes/installs.
- In sandboxed agent environments the user-profile directory must be set
  explicitly; the default ~/.config/libreoffice path may be read-only.
- On some systems Unix-domain sockets are restricted; this wrapper selects
  a writable temp directory for the user-profile automatically.

Usage (mirrors LibreOffice CLI):
    python office-custom/scripts/soffice.py --headless --convert-to pdf file.docx
    python office-custom/scripts/soffice.py --headless --convert-to docx file.doc
    python office-custom/scripts/soffice.py --headless --convert-to pdf file.pptx
"""

import os
import subprocess
import sys
import tempfile
from pathlib import Path

# Candidate LibreOffice executable paths, searched in order.
_CANDIDATE_PATHS = [
    # macOS (homebrew or standard app bundle)
    "/Applications/LibreOffice.app/Contents/MacOS/soffice",
    "/opt/homebrew/bin/soffice",
    "/usr/local/bin/soffice",
    # Linux (Debian/Ubuntu/Fedora package installs)
    "/usr/bin/soffice",
    "/usr/lib/libreoffice/program/soffice",
    "/opt/libreoffice/program/soffice",
    "/snap/bin/libreoffice",
]


def find_soffice() -> str:
    """Return the path to the LibreOffice executable.

    Checks the PATH environment variable first, then falls back to a list of
    well-known installation locations.

    Raises:
        FileNotFoundError: If LibreOffice cannot be found.
    """
    # Honour an explicit override from the environment.
    env_override = os.environ.get("SOFFICE_PATH")
    if env_override and Path(env_override).exists():
        return env_override

    # Search PATH first so system-managed installs take priority.
    for candidate in ["soffice", "libreoffice"]:
        result = subprocess.run(
            ["which", candidate], capture_output=True, text=True
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()

    # Fall back to hard-coded locations.
    for path in _CANDIDATE_PATHS:
        if Path(path).exists():
            return path

    raise FileNotFoundError(
        "LibreOffice not found. Install it with:\n"
        "  macOS:  brew install --cask libreoffice\n"
        "  Ubuntu: sudo apt-get install libreoffice\n"
        "  Fedora: sudo dnf install libreoffice\n"
        "Or set the SOFFICE_PATH environment variable."
    )


def make_user_profile() -> str:
    """Return a writable LibreOffice user-profile directory.

    Creates a persistent temp directory under /tmp/soffice-profile so that
    successive calls reuse the same profile (faster) while staying out of
    the user's home directory (safe in sandboxed environments).
    """
    profile_dir = Path(tempfile.gettempdir()) / "soffice-profile"
    profile_dir.mkdir(parents=True, exist_ok=True)
    return str(profile_dir)


def run(args: list[str]) -> subprocess.CompletedProcess[bytes]:
    """Invoke LibreOffice with *args* and return the process result.

    A ``-env:UserInstallation=...`` flag is prepended automatically so that
    LibreOffice writes its lock/config files to a temp directory rather than
    the user's home, which avoids permission errors in restricted environments.

    Args:
        args: Argument list to forward to soffice (e.g. ``["--headless",
              "--convert-to", "pdf", "file.docx"]``).

    Returns:
        The completed LibreOffice process result.
    """
    soffice = find_soffice()
    profile = make_user_profile()
    profile_url = Path(profile).as_uri()

    cmd = [
        soffice,
        f"-env:UserInstallation={profile_url}",
        *args,
    ]

    return subprocess.run(cmd)


def main() -> None:
    """Entry point: forward all CLI arguments to LibreOffice."""
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)

    result = run(sys.argv[1:])
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
