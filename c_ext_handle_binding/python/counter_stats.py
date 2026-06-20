import ctypes

from ._native import _check_status, _lib
from .handle import HandleResource
from .types import CounterStats, CounterStatsView, stats_to_view


class CounterStatsResource(HandleResource):
    def to_view(self) -> CounterStatsView:
        out = CounterStats()
        _check_status(_lib.counter_stats_read(self.handle, ctypes.byref(out)))
        return stats_to_view(out)

    @property
    def current_value(self) -> int:
        return self.to_view().current_value

    @property
    def total_operations(self) -> int:
        return self.to_view().total_operations

    @property
    def total_delta(self) -> int:
        return self.to_view().total_delta
