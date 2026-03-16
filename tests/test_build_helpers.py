"""Tests for Makefile helper scripts."""

from __future__ import annotations

import importlib.util
import unittest
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def _load_module(rel_path: str):
    module_path = REPO_ROOT / rel_path
    spec = importlib.util.spec_from_file_location(module_path.stem.replace('-', '_'), module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class TestCheckNodeVersion(unittest.TestCase):
    def test_parse_version_accepts_semver_output(self):
        mod = _load_module('scripts/check_node_version.py')
        self.assertEqual(mod.parse_version('v20.11.1\n'), (20, 11, 1))

    def test_parse_version_rejects_unknown_shape(self):
        mod = _load_module('scripts/check_node_version.py')
        self.assertIsNone(mod.parse_version('node version unknown'))


class TestVerifyBuiltZips(unittest.TestCase):
    def test_verify_zip_reports_missing(self):
        mod = _load_module('scripts/verify_built_zips.py')
        ok, detail = mod.verify_zip(Path('missing.zip'))
        self.assertFalse(ok)
        self.assertEqual(detail, 'missing')

    def test_verify_zip_reports_valid_archive(self):
        mod = _load_module('scripts/verify_built_zips.py')
        scratch_dir = REPO_ROOT / '.tmp-test-artifacts'
        scratch_dir.mkdir(exist_ok=True)
        zip_path = scratch_dir / 'sample.zip'
        try:
            with zipfile.ZipFile(zip_path, 'w') as zf:
                zf.writestr('hello.txt', 'hello')
            ok, detail = mod.verify_zip(zip_path)
        finally:
            zip_path.unlink(missing_ok=True)
            scratch_dir.rmdir()
        self.assertTrue(ok)
        self.assertEqual(detail, 'valid')


if __name__ == '__main__':
    unittest.main()
