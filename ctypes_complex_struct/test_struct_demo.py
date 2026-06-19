"""End-to-end demo for ctypes complex struct bindings."""

from bindings import InputRecordPy, MetricPy, PointPy, transform


def main() -> None:
    inp = InputRecordPy("sensor-A", version=2, origin=(10, 20))
    inp.set_corner(0, (0, 0))
    inp.set_corner(1, (100, 50))
    inp.add_metric(MetricPy("cpu", 80, (1, 2)))
    inp.add_metric(MetricPy("mem", 40, (3, 4)))
    inp.add_metric(MetricPy("io", 90, (5, 6)))
    inp.set_weight(0, 10)
    inp.set_weight(1, 20)
    inp.set_weight(2, 30)
    inp.set_category(0, "hardware")
    inp.set_category(1, "edge")
    inp.set_description("edge node")
    inp.add_tag("critical")
    inp.add_tag("prod")
    inp.add_metric_ptr(MetricPy("net", 70, (7, 8)))

    with transform(inp, scale=1.5, min_weight=20, top_n=2) as out:
        assert out.title == "sensor-A@v2"
        assert out.bbox == ((0, 0), (100, 50))
        assert out.notes == "edge node"

        expected_total = int((10 + 20 + 30) * 1.5)
        assert out.total_weight == expected_total

        assert out.filtered_weights() == [30, 45]
        assert out.summary_lines() == ["critical", "prod"]

        top = out.top_metrics()
        assert len(top) == 2
        assert top[0].label == "io"
        assert top[0].weight == 90
        assert top[0].anchor.to_tuple() == (5, 6)
        assert top[1].label == "cpu"

        ranked = out.ranked_metrics()
        assert len(ranked) == 2
        assert ranked[0].label == "io"
        assert ranked[1].label == "cpu"

    print("ctypes_complex_struct: OK")


if __name__ == "__main__":
    main()
