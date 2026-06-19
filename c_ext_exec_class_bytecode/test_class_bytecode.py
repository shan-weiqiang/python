"""Verify §4.2 class statement compiles to LOAD_BUILD_CLASS bytecode."""

import dis

source = "class Config:\n    def __init__(self, timeout):\n        self.timeout = timeout"

code = compile(source, "<string>", "exec")
bytecode = dis.Bytecode(code)
opnames = [instr.opname for instr in bytecode]

assert "LOAD_BUILD_CLASS" in opnames
assert "MAKE_FUNCTION" in opnames
# Python 3.11+ uses CALL; older versions use CALL_FUNCTION
assert any(name in opnames for name in ("CALL", "CALL_FUNCTION"))
assert "STORE_NAME" in opnames

print("c_ext_exec_class_bytecode: OK")
