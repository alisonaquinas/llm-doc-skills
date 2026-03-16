"""Load xlsx-custom/scripts/recalc.py for tests."""

from __future__ import annotations

import importlib.util
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "skills" / "xlsx-custom" / "scripts" / "recalc.py"


def load_module():
    spec = importlib.util.spec_from_file_location("xlsx_custom_recalc", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    try:
        spec.loader.exec_module(module)
    except SystemExit:
        raise ImportError("recalc.py dependency missing (openpyxl not installed)")
    return module
