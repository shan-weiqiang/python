from ._native import _lib, _check_handle


class HandleResource:
    def __init__(self, handle: int) -> None:
        if handle == 0:
            raise ValueError("invalid handle")
        self._handle = handle
        self._closed = False

    @property
    def handle(self) -> int:
        self._ensure_open()
        return self._handle

    @property
    def type_id(self) -> int:
        self._ensure_open()
        return _lib.handle_type(self._handle)

    def close(self) -> None:
        if self._closed or self._handle == 0:
            return
        _lib.handle_release(self._handle)
        self._handle = 0
        self._closed = True

    def _ensure_open(self) -> None:
        if self._closed or self._handle == 0:
            raise RuntimeError("handle is closed")

    def __enter__(self) -> "HandleResource":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    def __del__(self) -> None:
        self.close()

    def __repr__(self) -> str:
        if self._closed or self._handle == 0:
            return f"{self.__class__.__name__}(closed)"
        return f"{self.__class__.__name__}(handle={self._handle}, type_id={self.type_id})"
