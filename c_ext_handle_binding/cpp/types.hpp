#pragma once

#include <cstdint>

using HandleId = int64_t;

constexpr HandleId kInvalidHandle = 0;

enum class TypeId : int {
    Config = 1,
    Counter = 2,
    ConfigSnapshot = 3,
    ProcessSummary = 4,
    CounterStats = 5,
};

constexpr int kInvalidTypeId = -1;
