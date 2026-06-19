import os
from pathlib import Path

from cffi import FFI

ffibuilder = FFI()

ffibuilder.cdef("int add(int a, int b);")

_here = Path(__file__).resolve().parent
_add_c = _here.parent / "c_ext_ffi_clib" / "add.c"

ffibuilder.set_source(
    "_add_cffi",
    '#include "add.h"',
    sources=[str(_add_c)],
    include_dirs=[str(_here)],
)

if __name__ == "__main__":
    ffibuilder.compile(verbose=True)
