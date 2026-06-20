import ctypes
from pathlib import Path

from .types import (
    ConfigSnapshot,
    ConfigSpec,
    CounterStats,
    DeltaSpec,
    ProcessSummary,
)

_LIB_PATH = Path(__file__).resolve().parent.parent / "libhandle_bridge.so"
_lib = ctypes.CDLL(str(_LIB_PATH))

_lib.handle_last_error.restype = ctypes.c_char_p

_lib.handle_release.argtypes = [ctypes.c_int64]
_lib.handle_release.restype = None

_lib.handle_type.argtypes = [ctypes.c_int64]
_lib.handle_type.restype = ctypes.c_int

_lib.config_create.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int]
_lib.config_create.restype = ctypes.c_int64

_lib.config_create_from_spec.argtypes = [ctypes.POINTER(ConfigSpec)]
_lib.config_create_from_spec.restype = ctypes.c_int64

_lib.config_process.argtypes = [ctypes.c_int64]
_lib.config_process.restype = ctypes.c_int

_lib.config_get_snapshot.argtypes = [ctypes.c_int64, ctypes.POINTER(ConfigSnapshot)]
_lib.config_get_snapshot.restype = ctypes.c_int

_lib.config_process_summary.argtypes = [ctypes.c_int64]
_lib.config_process_summary.restype = ProcessSummary

_lib.config_create_snapshot.argtypes = [ctypes.c_int64]
_lib.config_create_snapshot.restype = ctypes.c_int64

_lib.config_snapshot_read.argtypes = [ctypes.c_int64, ctypes.POINTER(ConfigSnapshot)]
_lib.config_snapshot_read.restype = ctypes.c_int

_lib.config_create_process_summary.argtypes = [ctypes.c_int64]
_lib.config_create_process_summary.restype = ctypes.c_int64

_lib.process_summary_read.argtypes = [ctypes.c_int64, ctypes.POINTER(ProcessSummary)]
_lib.process_summary_read.restype = ctypes.c_int

_lib.config_spec_merge.argtypes = [
    ctypes.POINTER(ConfigSpec),
    ctypes.POINTER(ConfigSpec),
    ctypes.POINTER(ConfigSpec),
]
_lib.config_spec_merge.restype = ctypes.c_int

_lib.counter_create.argtypes = [ctypes.c_int]
_lib.counter_create.restype = ctypes.c_int64

_lib.counter_increment.argtypes = [ctypes.c_int64, ctypes.c_int]
_lib.counter_increment.restype = ctypes.c_int

_lib.counter_apply_delta.argtypes = [ctypes.c_int64, ctypes.POINTER(DeltaSpec)]
_lib.counter_apply_delta.restype = ctypes.c_int

_lib.counter_get.argtypes = [ctypes.c_int64]
_lib.counter_get.restype = ctypes.c_int

_lib.counter_get_stats.argtypes = [ctypes.c_int64, ctypes.POINTER(CounterStats)]
_lib.counter_get_stats.restype = ctypes.c_int

_lib.counter_create_stats.argtypes = [ctypes.c_int64]
_lib.counter_create_stats.restype = ctypes.c_int64

_lib.counter_stats_read.argtypes = [ctypes.c_int64, ctypes.POINTER(CounterStats)]
_lib.counter_stats_read.restype = ctypes.c_int


def _last_error() -> str:
    message = _lib.handle_last_error()
    if message is None:
        return "unknown error"
    return message.decode()


def _check_handle(handle: int) -> int:
    if handle == 0:
        raise RuntimeError(_last_error())
    return handle


def _check_int(result: int) -> int:
    if result == -1:
        raise RuntimeError(_last_error())
    return result


def _check_status(result: int) -> None:
    if result == -1:
        raise RuntimeError(_last_error())
