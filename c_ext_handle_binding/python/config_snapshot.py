import ctypes

from ._native import _check_status, _lib
from .handle import HandleResource
from .types import ConfigSnapshot, ConfigSnapshotView, snapshot_to_view


class ConfigSnapshotResource(HandleResource):
    def to_view(self) -> ConfigSnapshotView:
        out = ConfigSnapshot()
        _check_status(_lib.config_snapshot_read(self.handle, ctypes.byref(out)))
        return snapshot_to_view(out)

    @property
    def timeout(self) -> int:
        return self.to_view().timeout

    @property
    def enable_ssl(self) -> bool:
        return self.to_view().enable_ssl

    @property
    def server_url(self) -> str:
        return self.to_view().server_url

    @property
    def process_result(self) -> int:
        return self.to_view().process_result
