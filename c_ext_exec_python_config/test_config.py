"""Verify §4.1 pure Python Config class."""

import dis

from config import Config

config = Config(30)
assert config.timeout == 30
assert config.process() == 60

# Article: dis.dis(Config.__init__) shows LOAD_FAST / STORE_ATTR
bytecode = dis.Bytecode(Config.__init__)
opnames = [instr.opname for instr in bytecode]
assert "LOAD_FAST" in opnames
assert "STORE_ATTR" in opnames

print("c_ext_exec_python_config: OK")
