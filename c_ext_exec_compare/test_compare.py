"""Verify §6 side-by-side: Python Config vs C extension Config."""

import dis

from py_config import PyConfig

# Build C extension from sibling demo (same API as §2.2.2)
import subprocess
import sys
from pathlib import Path

compare_dir = Path(__file__).resolve().parent
basic_dir = compare_dir.parent / "c_ext_config_basic"
subprocess.check_call(
    [sys.executable, "setup.py", "build_ext", "--inplace"],
    cwd=basic_dir,
)
sys.path.insert(0, str(basic_dir))

import mymodule  # noqa: E402

py_cfg = PyConfig(30)
c_cfg = mymodule.Config(timeout=30, url="http://server.com", ssl=True)

assert py_cfg.process() == c_cfg.process() == 60

# Python path: bound method is PyFunction_Type
assert type(py_cfg.process).__name__ in ("method", "function")

# C extension path: bound method is builtin_function_or_method (PyCFunction_Type)
bound = c_cfg.process
assert str(type(bound)) == "<class 'builtin_function_or_method'>"

# Python __init__ uses bytecode with STORE_ATTR
init_ops = [i.opname for i in dis.Bytecode(PyConfig.__init__)]
assert "STORE_ATTR" in init_ops

# C Config has no bytecode for process — it's a C function pointer
assert not hasattr(c_cfg.process, "__code__")

print("c_ext_exec_compare: OK")
