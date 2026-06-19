"""Verify §2.2.3 nested Config and NetworkConfig types."""

import mymodule

config = mymodule.Config(timeout=30)
config.network.host = "server.com"
config.network.port = 8080
config.network.use_ssl = True

assert isinstance(config, mymodule.Config)
assert isinstance(config.network, mymodule.NetworkConfig)
assert config.network.host == "server.com"
assert config.network.port == 8080
assert config.network.use_ssl is True

net = mymodule.NetworkConfig(host="standalone.com", port=9000)
config.network = net
assert config.network.host == "standalone.com"
assert config.network.port == 9000

config.set_value(0, 10)
config.set_value(1, 20)
values = config.get_values()
assert values == [10, 20]

config.items = [1, 2, 3, 4, 5]
items = config.items
assert items == [1, 2, 3, 4, 5]

print("c_ext_config_nested: OK")
