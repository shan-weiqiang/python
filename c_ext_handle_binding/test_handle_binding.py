"""Verify ctypes handle-based C++ binding."""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

subprocess.run(["make"], cwd=ROOT, check=True)

sys.path.insert(0, str(ROOT))

from python import Config, Counter, make_config_spec
from python._native import _lib

config = Config.create(30, "http://server.com", True)
assert config.process() == 147

spec = make_config_spec(30, "http://server.com", True)
config_from_spec = Config.create_from_spec(spec)
assert config_from_spec.process() == 147

snapshot = config_from_spec.snapshot()
assert snapshot.timeout == 30
assert snapshot.enable_ssl is True
assert snapshot.server_url == "http://server.com"
assert snapshot.process_result == 147

summary = config_from_spec.process_summary()
assert summary.base_score == 30
assert summary.ssl_bonus == 100
assert summary.url_bonus == len("http://server.com")
assert summary.total == 147

with config_from_spec.create_snapshot() as snapshot_handle:
    assert snapshot_handle.timeout == 30
    assert snapshot_handle.enable_ssl is True
    assert snapshot_handle.server_url == "http://server.com"
    assert snapshot_handle.process_result == 147
    snapshot_type = snapshot_handle.type_id
    closed_snapshot_handle = snapshot_handle.handle

assert _lib.handle_type(closed_snapshot_handle) == -1
assert snapshot_type == 3

with config_from_spec.create_process_summary() as summary_handle:
    assert summary_handle.base_score == 30
    assert summary_handle.ssl_bonus == 100
    assert summary_handle.url_bonus == len("http://server.com")
    assert summary_handle.total == 147

left = make_config_spec(10, "left", False)
right = make_config_spec(20, "right", True)
merged = Config.merge_specs(left, right)
assert merged.timeout == 30
assert merged.enable_ssl == 1
assert merged.server_url.decode() == "leftright"

counter = Counter.create(10)
counter.increment(5)
assert counter.value == 15

counter.apply_delta(delta=2, repeat=3)
assert counter.value == 21

stats = counter.stats()
assert stats.current_value == 21
assert stats.total_operations == 4
assert stats.total_delta == 11

with counter.create_stats() as stats_handle:
    assert stats_handle.current_value == 21
    assert stats_handle.total_operations == 4
    assert stats_handle.total_delta == 11
    stats_type = stats_handle.type_id
    closed_stats_handle = stats_handle.handle

assert _lib.handle_type(closed_stats_handle) == -1
assert stats_type == 5

handle = config.handle
config.close()
assert _lib.handle_type(handle) == -1

config = Config.create(30, "http://server.com", True)
result = _lib.counter_increment(config.handle, 1)
assert result == -1
assert b"invalid handle or wrong type" in _lib.handle_last_error()
config.close()

with Counter.create(0) as counter:
    counter.increment(3)
    assert counter.value == 3
    closed_handle = counter.handle

assert _lib.handle_type(closed_handle) == -1

print("c_ext_handle_binding: OK")
