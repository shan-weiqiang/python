#pragma once

#include "c_types.h"
#include "handle_object.hpp"

class CounterStatsResource : public HandleObject {
public:
    explicit CounterStatsResource(const CounterStats& stats);

    TypeId type() const override;
    void fill(CounterStats& out) const;

private:
    CounterStats stats_;
};
