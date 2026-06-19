"""Verify §2.1 opaque capsule approach."""

import mymodule

config = mymodule.create_config(30, "http://server.com", True)
result = mymodule.process_config(config)
# 30 + 100 (ssl) + len("http://server.com") = 30 + 100 + 17 = 147
assert result == 147

# Capsule is opaque — no attribute access
assert not hasattr(config, "timeout")

print("c_ext_capsule_config: OK")
