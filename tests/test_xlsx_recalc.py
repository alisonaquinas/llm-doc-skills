"""Tests for the xlsx formula-recalculation wrapper."""

from __future__ import annotations

import tempfile
import types
import unittest
from pathlib import Path
from unittest import mock

from xlsx_custom_recalc_loader import load_module

try:
    recalc = load_module()
    _RECALC_AVAILABLE = True
except ImportError:
    recalc = None
    _RECALC_AVAILABLE = False


@unittest.skipUnless(_RECALC_AVAILABLE, "openpyxl not installed")
class TestRecalcLibreOfficeStaging(unittest.TestCase):
    """LibreOffice conversion must not reuse the source path as the output path."""

    def test_recalc_stages_source_and_output_in_separate_directories(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            source = root / "input.xlsx"
            dest = root / "output.xlsx"
            source.write_bytes(b"placeholder")

            captured: dict[str, str] = {}

            def fake_run(args: list[str]):
                out_dir = Path(args[args.index("--outdir") + 1])
                src_path = Path(args[-1])
                captured["out_dir"] = str(out_dir)
                captured["src_path"] = str(src_path)
                out_dir.mkdir(parents=True, exist_ok=True)
                (out_dir / f"{src_path.stem}.xlsx").write_bytes(b"recalculated")
                return types.SimpleNamespace(returncode=0)

            fake_module = types.SimpleNamespace(run=fake_run)

            with mock.patch.object(recalc, "_find_soffice_py", return_value=Path("/tmp/fake-soffice.py")):
                with mock.patch.object(recalc, "_import_soffice_module", return_value=fake_module):
                    ok = recalc._recalc_with_soffice(source, dest, quiet=True)

            self.assertTrue(ok)
            self.assertTrue(dest.exists())
            self.assertNotEqual(
                Path(captured["src_path"]).parent,
                Path(captured["out_dir"]),
                "LibreOffice input and output should be staged in different directories",
            )


if __name__ == "__main__":
    unittest.main()
