"""Verify §2.3 marshal-at-boundary Config_process."""

import mymodule

config = mymodule.Config(timeout=30, url="http://server.com", ssl=True)
result = config.process()
# 30 + 1000 (ssl) + len("http://server.com") = 30 + 1000 + 17 = 1047
assert result == 1047

config = mymodule.Config(timeout=10, url="", ssl=False)
assert config.process() == 10

print("c_ext_config_marshal: OK")
