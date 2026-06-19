"""Verify §7.3 CFFI API (out-of-line) mode."""

import subprocess
import sys
from pathlib import Path

API_DIR = Path(__file__).resolve().parent
CLIB = API_DIR.parent / "c_ext_ffi_clib"

subprocess.check_call(["make"], cwd=CLIB)
subprocess.check_call(
    [sys.executable, "setup.py", "build_ext", "--inplace"],
    cwd=API_DIR,
)

from _add_cffi import lib

assert lib.add(2, 3) == 5

print("c_ext_cffi_api: OK")
