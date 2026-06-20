import ctypes
from dataclasses import dataclass
from typing import Mapping, Union

HANDLE_BRIDGE_URL_MAX = 256


class ConfigSpec(ctypes.Structure):
    _fields_ = [
        ("timeout", ctypes.c_int32),
        ("enable_ssl", ctypes.c_int32),
        ("server_url", ctypes.c_char * HANDLE_BRIDGE_URL_MAX),
    ]


class ConfigSnapshot(ctypes.Structure):
    _fields_ = [
        ("timeout", ctypes.c_int32),
        ("enable_ssl", ctypes.c_int32),
        ("server_url", ctypes.c_char * HANDLE_BRIDGE_URL_MAX),
        ("process_result", ctypes.c_int32),
    ]


class ProcessSummary(ctypes.Structure):
    _fields_ = [
        ("base_score", ctypes.c_int32),
        ("ssl_bonus", ctypes.c_int32),
        ("url_bonus", ctypes.c_int32),
        ("total", ctypes.c_int32),
    ]


class DeltaSpec(ctypes.Structure):
    _fields_ = [
        ("delta", ctypes.c_int32),
        ("repeat", ctypes.c_int32),
    ]


class CounterStats(ctypes.Structure):
    _fields_ = [
        ("current_value", ctypes.c_int32),
        ("total_operations", ctypes.c_int32),
        ("total_delta", ctypes.c_int32),
    ]


ConfigSpecInput = Union[ConfigSpec, Mapping[str, object]]


def make_config_spec(
    timeout: int,
    url: str,
    ssl: bool,
) -> ConfigSpec:
    spec = ConfigSpec()
    spec.timeout = timeout
    spec.enable_ssl = int(ssl)
    encoded = url.encode()
    if len(encoded) >= HANDLE_BRIDGE_URL_MAX:
        raise ValueError("server_url exceeds maximum length")
    spec.server_url = encoded
    return spec


def make_delta_spec(delta: int, repeat: int) -> DeltaSpec:
    spec = DeltaSpec()
    spec.delta = delta
    spec.repeat = repeat
    return spec


@dataclass(frozen=True)
class ConfigSnapshotView:
    timeout: int
    enable_ssl: bool
    server_url: str
    process_result: int


@dataclass(frozen=True)
class ProcessSummaryView:
    base_score: int
    ssl_bonus: int
    url_bonus: int
    total: int


@dataclass(frozen=True)
class CounterStatsView:
    current_value: int
    total_operations: int
    total_delta: int


def snapshot_to_view(snapshot: ConfigSnapshot) -> ConfigSnapshotView:
    return ConfigSnapshotView(
        timeout=snapshot.timeout,
        enable_ssl=bool(snapshot.enable_ssl),
        server_url=snapshot.server_url.decode(),
        process_result=snapshot.process_result,
    )


def summary_to_view(summary: ProcessSummary) -> ProcessSummaryView:
    return ProcessSummaryView(
        base_score=summary.base_score,
        ssl_bonus=summary.ssl_bonus,
        url_bonus=summary.url_bonus,
        total=summary.total,
    )


def stats_to_view(stats: CounterStats) -> CounterStatsView:
    return CounterStatsView(
        current_value=stats.current_value,
        total_operations=stats.total_operations,
        total_delta=stats.total_delta,
    )
