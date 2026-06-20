import ctypes

from ._native import _check_status, _lib
from .handle import HandleResource
from .types import ProcessSummary, ProcessSummaryView, summary_to_view


class ProcessSummaryResource(HandleResource):
    def to_view(self) -> ProcessSummaryView:
        out = ProcessSummary()
        _check_status(_lib.process_summary_read(self.handle, ctypes.byref(out)))
        return summary_to_view(out)

    @property
    def base_score(self) -> int:
        return self.to_view().base_score

    @property
    def ssl_bonus(self) -> int:
        return self.to_view().ssl_bonus

    @property
    def url_bonus(self) -> int:
        return self.to_view().url_bonus

    @property
    def total(self) -> int:
        return self.to_view().total
