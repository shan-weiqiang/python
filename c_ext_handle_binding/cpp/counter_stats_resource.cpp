#include "counter_stats_resource.hpp"

CounterStatsResource::CounterStatsResource(const CounterStats& stats)
    : stats_(stats) {}

TypeId CounterStatsResource::type() const {
    return TypeId::CounterStats;
}

void CounterStatsResource::fill(CounterStats& out) const {
    out = stats_;
}
