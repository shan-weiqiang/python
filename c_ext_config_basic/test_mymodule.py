"""Verify §2.2.2 basic Config PyTypeObject."""

import mymodule

config = mymodule.Config(timeout=30, url="http://server.com", ssl=True)
assert config.timeout == 30
config.timeout = 60
assert config.timeout == 60
assert config.server_url == "http://server.com"
assert config.enable_ssl is True
result = config.process()
assert result == 120
assert isinstance(config, mymodule.Config)

print("c_ext_config_basic: OK")
