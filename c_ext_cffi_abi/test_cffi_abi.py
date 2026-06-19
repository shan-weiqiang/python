"""Verify §7.3 CFFI ABI (in-line) mode."""

import subprocess
import sys
from pathlib import Path

from cffi import FFI

CLIB = Path(__file__).resolve().parent.parent / "c_ext_ffi_clib"
LIB = CLIB / "libadd.so"

subprocess.check_call(["make"], cwd=CLIB)

ffi = FFI()
ffi.cdef("int add(int a, int b);")
lib = ffi.dlopen(str(LIB))

assert lib.add(2, 3) == 5

print("c_ext_cffi_abi: OK")
