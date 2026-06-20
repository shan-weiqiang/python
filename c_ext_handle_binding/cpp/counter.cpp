#include "counter.hpp"

Counter::Counter(int initial) : value_(initial) {}

TypeId Counter::type() const {
    return TypeId::Counter;
}

void Counter::increment(int delta) {
    value_ += delta;
    ++total_operations_;
    total_delta_ += delta;
}

void Counter::apply_delta(const DeltaSpec& spec) {
    for (int32_t i = 0; i < spec.repeat; ++i) {
        increment(spec.delta);
    }
}

int Counter::get() const {
    return value_;
}

void Counter::fill_stats(CounterStats& out) const {
    out.current_value = value_;
    out.total_operations = total_operations_;
    out.total_delta = total_delta_;
}
