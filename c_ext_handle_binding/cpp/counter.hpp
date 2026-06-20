#pragma once

#include "c_types.h"
#include "handle_object.hpp"

class Counter : public HandleObject {
public:
    explicit Counter(int initial);

    TypeId type() const override;
    void increment(int delta);
    void apply_delta(const DeltaSpec& spec);
    int get() const;
    void fill_stats(CounterStats& out) const;

private:
    int value_;
    int total_operations_ = 0;
    int total_delta_ = 0;
};
