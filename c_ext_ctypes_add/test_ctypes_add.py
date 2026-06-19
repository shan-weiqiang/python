"""Verify §7.2 ctypes CDLL + libffi call path."""

import ctypes
import subprocess
import sys
from pathlib import Path

CLIB = Path(__file__).resolve().parent.parent / "c_ext_ffi_clib"
LIB = CLIB / "libadd.so"

subprocess.check_call(["make"], cwd=CLIB)

lib = ctypes.CDLL(str(LIB))
lib.add.argtypes = [ctypes.c_int, ctypes.c_int]
lib.add.restype = ctypes.c_int

assert lib.add(2, 3) == 5

func = lib.add
assert "FuncPtr" in type(func).__name__
assert str(type(func)) != "<class 'builtin_function_or_method'>"

print("c_ext_ctypes_add: OK")
