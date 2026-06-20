import ctypes

from ._native import _check_handle, _check_int, _check_status, _lib
from .handle import HandleResource
from .config_snapshot import ConfigSnapshotResource
from .process_summary import ProcessSummaryResource
from .types import (
    ConfigSnapshot,
    ConfigSpec,
    ConfigSpecInput,
    ConfigSnapshotView,
    ProcessSummaryView,
    make_config_spec,
    snapshot_to_view,
    summary_to_view,
)


class Config(HandleResource):
    @classmethod
    def create(cls, timeout: int, url: str, ssl: bool) -> "Config":
        handle = _lib.config_create(timeout, url.encode(), int(ssl))
        _check_handle(handle)
        return cls(handle)

    @classmethod
    def create_from_spec(cls, spec: ConfigSpecInput) -> "Config":
        if not isinstance(spec, ConfigSpec):
            spec = make_config_spec(
                int(spec["timeout"]),
                str(spec["server_url"]),
                bool(spec["enable_ssl"]),
            )
        handle = _lib.config_create_from_spec(ctypes.byref(spec))
        _check_handle(handle)
        return cls(handle)

    def process(self) -> int:
        return _check_int(_lib.config_process(self.handle))

    def snapshot(self) -> ConfigSnapshotView:
        out = ConfigSnapshot()
        _check_status(_lib.config_get_snapshot(self.handle, ctypes.byref(out)))
        return snapshot_to_view(out)

    def process_summary(self) -> ProcessSummaryView:
        summary = _lib.config_process_summary(self.handle)
        if summary.total == -1:
            raise RuntimeError(_lib.handle_last_error().decode())
        return summary_to_view(summary)

    def create_snapshot(self) -> ConfigSnapshotResource:
        handle = _lib.config_create_snapshot(self.handle)
        _check_handle(handle)
        return ConfigSnapshotResource(handle)

    def create_process_summary(self) -> ProcessSummaryResource:
        handle = _lib.config_create_process_summary(self.handle)
        _check_handle(handle)
        return ProcessSummaryResource(handle)

    @staticmethod
    def merge_specs(left: ConfigSpecInput, right: ConfigSpecInput) -> ConfigSpec:
        left_spec = (
            left
            if isinstance(left, ConfigSpec)
            else make_config_spec(
                int(left["timeout"]),
                str(left["server_url"]),
                bool(left["enable_ssl"]),
            )
        )
        right_spec = (
            right
            if isinstance(right, ConfigSpec)
            else make_config_spec(
                int(right["timeout"]),
                str(right["server_url"]),
                bool(right["enable_ssl"]),
            )
        )
        out = ConfigSpec()
        _check_status(
            _lib.config_spec_merge(
                ctypes.byref(left_spec),
                ctypes.byref(right_spec),
                ctypes.byref(out),
            )
        )
        return out
