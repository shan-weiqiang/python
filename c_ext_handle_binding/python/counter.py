import ctypes

from ._native import _check_handle, _check_int, _check_status, _lib
from .handle import HandleResource
from .counter_stats import CounterStatsResource
from .types import (
    CounterStats,
    CounterStatsView,
    DeltaSpec,
    make_delta_spec,
    stats_to_view,
)


class Counter(HandleResource):
    @classmethod
    def create(cls, initial: int = 0) -> "Counter":
        handle = _lib.counter_create(initial)
        _check_handle(handle)
        return cls(handle)

    def increment(self, delta: int) -> None:
        _check_status(_lib.counter_increment(self.handle, delta))

    def apply_delta(self, delta: int, repeat: int = 1) -> None:
        spec = make_delta_spec(delta, repeat)
        _check_status(_lib.counter_apply_delta(self.handle, ctypes.byref(spec)))

    @property
    def value(self) -> int:
        return _check_int(_lib.counter_get(self.handle))

    def stats(self) -> CounterStatsView:
        out = CounterStats()
        _check_status(_lib.counter_get_stats(self.handle, ctypes.byref(out)))
        return stats_to_view(out)

    def create_stats(self) -> CounterStatsResource:
        handle = _lib.counter_create_stats(self.handle)
        _check_handle(handle)
        return CounterStatsResource(handle)
