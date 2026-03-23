#!/usr/bin/env python3
"""Wrapper to run project-level qa_references_style from a paper workspace."""

from __future__ import annotations

import runpy
import sys
from pathlib import Path

here = Path(__file__).resolve()
project_root = here.parents[3]
target = project_root / "scripts" / "qa_references_style.py"

argv = sys.argv[1:]
if "--paper-dir" not in argv:
    argv = ["--paper-dir", str(here.parents[1]), *argv]

sys.argv = [str(target), *argv]
runpy.run_path(str(target), run_name="__main__")
