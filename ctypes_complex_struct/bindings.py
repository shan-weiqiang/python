"""ctypes bindings and Python wrappers for struct_demo."""

from __future__ import annotations

import ctypes
from pathlib import Path

MAX_METRICS = 4
MAX_TAGS = 4
MAX_WEIGHTS = 8
MAX_LABEL = 32
MAX_SUMMARY = 3
MAX_PTRS = 2


class Point(ctypes.Structure):
    _fields_ = [
        ("x", ctypes.c_int),
        ("y", ctypes.c_int),
    ]


class Metric(ctypes.Structure):
    _fields_ = [
        ("label", ctypes.c_char * MAX_LABEL),
        ("weight", ctypes.c_int),
        ("anchor", Point),
    ]


class InputRecord(ctypes.Structure):
    _fields_ = [
        ("header_id", ctypes.c_char * MAX_LABEL),
        ("version", ctypes.c_int),
        ("origin", Point),
        ("corners", Point * 2),
        ("metrics", Metric * MAX_METRICS),
        ("weights", ctypes.c_int * MAX_WEIGHTS),
        ("categories", (ctypes.c_char * MAX_LABEL) * MAX_TAGS),
        ("description", ctypes.c_char_p),
        ("tags", ctypes.c_char_p * MAX_TAGS),
        ("tag_count", ctypes.c_int),
        ("metric_ptrs", ctypes.POINTER(Metric) * MAX_PTRS),
        ("metric_ptr_count", ctypes.c_int),
    ]


class OutputRecord(ctypes.Structure):
    _fields_ = [
        ("title", ctypes.c_char * MAX_LABEL),
        ("bbox", Point * 2),
        ("total_weight", ctypes.c_int),
        ("filtered_weights", ctypes.c_int * MAX_WEIGHTS),
        ("filtered_weight_count", ctypes.c_int),
        ("top_metrics", Metric * MAX_PTRS),
        ("summary_lines", (ctypes.c_char * MAX_LABEL) * MAX_SUMMARY),
        ("notes", ctypes.c_char_p),
        ("ranked_ptrs", ctypes.POINTER(Metric) * MAX_PTRS),
        ("ranked_ptr_count", ctypes.c_int),
    ]


_LIB_PATH = Path(__file__).with_name("libstruct_demo.so")
_lib = ctypes.CDLL(str(_LIB_PATH))

_lib.transform_record.argtypes = [
    ctypes.POINTER(InputRecord),
    ctypes.c_double,
    ctypes.c_int,
    ctypes.c_int,
]
_lib.transform_record.restype = OutputRecord

_lib.free_output_record.argtypes = [ctypes.POINTER(OutputRecord)]
_lib.free_output_record.restype = None


def _encode_label(value: str) -> bytes:
    encoded = value.encode("utf-8")
    if len(encoded) >= MAX_LABEL:
        raise ValueError(f"label too long (max {MAX_LABEL - 1} bytes): {value!r}")
    return encoded


def _write_label_field(struct: ctypes.Structure, field_name: str, value: str) -> None:
    setattr(struct, field_name, _encode_label(value))


def _write_label_array_slot(
    struct: ctypes.Structure,
    field_name: str,
    index: int,
    value: str,
) -> None:
    field_type = getattr(type(struct), field_name)
    slot = (ctypes.c_char * MAX_LABEL).from_address(
        ctypes.addressof(struct) + field_type.offset + index * MAX_LABEL
    )
    encoded = _encode_label(value)
    for i in range(MAX_LABEL):
        slot[i] = 0
    for i, byte in enumerate(encoded):
        slot[i] = byte


def _decode_bytes(value: bytes | None) -> str:
    if value is None:
        return ""
    return value.split(b"\0", 1)[0].decode("utf-8")


class PointPy:
    def __init__(self, x: int = 0, y: int = 0):
        self.x = x
        self.y = y

    @classmethod
    def from_tuple(cls, pair: tuple[int, int]) -> PointPy:
        return cls(pair[0], pair[1])

    def to_tuple(self) -> tuple[int, int]:
        return (self.x, self.y)

    def to_ctypes(self) -> Point:
        return Point(self.x, self.y)

    @classmethod
    def from_ctypes(cls, point: Point) -> PointPy:
        return cls(point.x, point.y)

    def __repr__(self) -> str:
        return f"PointPy(x={self.x}, y={self.y})"


class MetricPy:
    def __init__(self, label: str, weight: int, anchor: PointPy | tuple[int, int]):
        self.label = label
        self.weight = weight
        if isinstance(anchor, tuple):
            self.anchor = PointPy.from_tuple(anchor)
        else:
            self.anchor = anchor

    def to_ctypes(self) -> Metric:
        metric = Metric()
        _write_label_field(metric, "label", self.label)
        metric.weight = self.weight
        metric.anchor = self.anchor.to_ctypes()
        return metric

    @classmethod
    def from_ctypes(cls, metric: Metric) -> MetricPy:
        return cls(
            _decode_bytes(bytes(metric.label)),
            metric.weight,
            PointPy.from_ctypes(metric.anchor),
        )

    def __repr__(self) -> str:
        return (
            f"MetricPy(label={self.label!r}, weight={self.weight}, "
            f"anchor={self.anchor})"
        )


class InputRecordPy:
    def __init__(
        self,
        header_id: str,
        version: int,
        origin: PointPy | tuple[int, int],
    ):
        self.header_id = header_id
        self.version = version
        if isinstance(origin, tuple):
            self.origin = PointPy.from_tuple(origin)
        else:
            self.origin = origin
        self._corners: list[PointPy] = [PointPy(), PointPy()]
        self._metrics: list[MetricPy] = []
        self._weights: list[int] = [0] * MAX_WEIGHTS
        self._categories: list[str] = [""] * MAX_TAGS
        self._description = ""
        self._tags: list[str] = []
        self._metric_ptrs: list[MetricPy] = []

    def set_corner(self, index: int, point: PointPy | tuple[int, int]) -> None:
        if index < 0 or index >= 2:
            raise IndexError("corner index must be 0 or 1")
        if isinstance(point, tuple):
            self._corners[index] = PointPy.from_tuple(point)
        else:
            self._corners[index] = point

    def add_metric(self, metric: MetricPy) -> None:
        if len(self._metrics) >= MAX_METRICS:
            raise ValueError(f"at most {MAX_METRICS} metrics are supported")
        self._metrics.append(metric)

    def set_weight(self, index: int, value: int) -> None:
        if index < 0 or index >= MAX_WEIGHTS:
            raise IndexError(f"weight index must be in [0, {MAX_WEIGHTS})")
        self._weights[index] = value

    def set_category(self, index: int, value: str) -> None:
        if index < 0 or index >= MAX_TAGS:
            raise IndexError(f"category index must be in [0, {MAX_TAGS})")
        self._categories[index] = value

    def set_description(self, value: str) -> None:
        self._description = value

    def add_tag(self, value: str) -> None:
        if len(self._tags) >= MAX_TAGS:
            raise ValueError(f"at most {MAX_TAGS} tags are supported")
        self._tags.append(value)

    def add_metric_ptr(self, metric: MetricPy) -> None:
        if len(self._metric_ptrs) >= MAX_PTRS:
            raise ValueError(f"at most {MAX_PTRS} metric pointers are supported")
        self._metric_ptrs.append(metric)

    def to_ctypes(self) -> tuple[InputRecord, list[object]]:
        keepalive: list[object] = []
        record = InputRecord()
        _write_label_field(record, "header_id", self.header_id)
        record.version = self.version
        record.origin = self.origin.to_ctypes()

        for i, corner in enumerate(self._corners):
            record.corners[i] = corner.to_ctypes()

        for i, metric in enumerate(self._metrics):
            record.metrics[i] = metric.to_ctypes()

        for i, weight in enumerate(self._weights):
            record.weights[i] = weight

        for i, category in enumerate(self._categories):
            if category:
                _write_label_array_slot(record, "categories", i, category)

        if self._description:
            description_buf = ctypes.create_string_buffer(
                self._description.encode("utf-8")
            )
            record.description = ctypes.c_char_p(
                ctypes.addressof(description_buf)
            )
            keepalive.append(description_buf)
            keepalive.append(record.description)

        tag_ptrs: list[ctypes.c_char_p] = []
        for i, tag in enumerate(self._tags):
            tag_buf = ctypes.create_string_buffer(tag.encode("utf-8"))
            tag_ptr = ctypes.c_char_p(ctypes.addressof(tag_buf))
            record.tags[i] = tag_ptr
            tag_ptrs.append(tag_ptr)
            keepalive.extend([tag_buf, tag_ptr])
        record.tag_count = len(self._tags)

        metric_storage: list[Metric] = []
        metric_ptr_values: list[ctypes.POINTER(Metric)] = []
        for i, metric in enumerate(self._metric_ptrs):
            metric_obj = metric.to_ctypes()
            metric_storage.append(metric_obj)
            metric_ptr = ctypes.pointer(metric_storage[-1])
            record.metric_ptrs[i] = metric_ptr
            metric_ptr_values.append(metric_ptr)
            keepalive.extend([metric_storage[-1], metric_ptr])
        record.metric_ptr_count = len(self._metric_ptrs)

        keepalive.append(record)
        return record, keepalive

    @classmethod
    def from_ctypes(cls, record: InputRecord) -> InputRecordPy:
        obj = cls(
            _decode_bytes(bytes(record.header_id)),
            record.version,
            PointPy.from_ctypes(record.origin),
        )
        for i in range(2):
            obj.set_corner(i, PointPy.from_ctypes(record.corners[i]))
        for i in range(MAX_METRICS):
            label = _decode_bytes(bytes(record.metrics[i].label))
            if label:
                obj.add_metric(MetricPy.from_ctypes(record.metrics[i]))
        for i in range(MAX_WEIGHTS):
            obj.set_weight(i, record.weights[i])
        for i in range(MAX_TAGS):
            category = _decode_bytes(bytes(record.categories[i]))
            if category:
                obj.set_category(i, category)
        if record.description:
            obj.set_description(_decode_bytes(record.description))
        for i in range(record.tag_count):
            if record.tags[i]:
                obj.add_tag(_decode_bytes(record.tags[i]))
        for i in range(record.metric_ptr_count):
            if record.metric_ptrs[i]:
                obj.add_metric_ptr(MetricPy.from_ctypes(record.metric_ptrs[i].contents))
        return obj


class OutputRecordPy:
    def __init__(self, record: OutputRecord):
        self._record = record
        self._closed = False

    @classmethod
    def from_ctypes(cls, record: OutputRecord) -> OutputRecordPy:
        return cls(record)

    @property
    def title(self) -> str:
        return _decode_bytes(bytes(self._record.title))

    @property
    def total_weight(self) -> int:
        return self._record.total_weight

    @property
    def bbox(self) -> tuple[tuple[int, int], tuple[int, int]]:
        return (
            PointPy.from_ctypes(self._record.bbox[0]).to_tuple(),
            PointPy.from_ctypes(self._record.bbox[1]).to_tuple(),
        )

    @property
    def notes(self) -> str:
        if self._record.notes is None:
            return ""
        return _decode_bytes(self._record.notes)

    def filtered_weights(self) -> list[int]:
        count = self._record.filtered_weight_count
        return [self._record.filtered_weights[i] for i in range(count)]

    def summary_lines(self) -> list[str]:
        lines: list[str] = []
        for i in range(MAX_SUMMARY):
            text = _decode_bytes(bytes(self._record.summary_lines[i]))
            if text:
                lines.append(text)
        return lines

    def top_metrics(self) -> list[MetricPy]:
        metrics: list[MetricPy] = []
        for i in range(self._record.ranked_ptr_count):
            metrics.append(MetricPy.from_ctypes(self._record.top_metrics[i]))
        return metrics

    def ranked_metrics(self) -> list[MetricPy]:
        metrics: list[MetricPy] = []
        for i in range(self._record.ranked_ptr_count):
            ptr = self._record.ranked_ptrs[i]
            if ptr:
                metrics.append(MetricPy.from_ctypes(ptr.contents))
        return metrics

    def close(self) -> None:
        if self._closed:
            return
        _lib.free_output_record(ctypes.byref(self._record))
        self._closed = True

    def __enter__(self) -> OutputRecordPy:
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    def __del__(self) -> None:
        try:
            self.close()
        except Exception:
            pass

    def __repr__(self) -> str:
        return f"OutputRecordPy(title={self.title!r}, total_weight={self.total_weight})"


def transform(
    input_record: InputRecordPy,
    scale: float,
    min_weight: int,
    top_n: int,
) -> OutputRecordPy:
    c_input, keepalive = input_record.to_ctypes()
    # keepalive must survive through the C call
    _ = keepalive
    c_output = _lib.transform_record(
        ctypes.byref(c_input),
        ctypes.c_double(scale),
        ctypes.c_int(min_weight),
        ctypes.c_int(top_n),
    )
    return OutputRecordPy.from_ctypes(c_output)
