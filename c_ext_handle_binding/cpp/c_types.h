#pragma once

#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

#define HANDLE_BRIDGE_URL_MAX 256

typedef struct ConfigSpec {
    int32_t timeout;
    int32_t enable_ssl;
    char server_url[HANDLE_BRIDGE_URL_MAX];
} ConfigSpec;

typedef struct ConfigSnapshot {
    int32_t timeout;
    int32_t enable_ssl;
    char server_url[HANDLE_BRIDGE_URL_MAX];
    int32_t process_result;
} ConfigSnapshot;

typedef struct ProcessSummary {
    int32_t base_score;
    int32_t ssl_bonus;
    int32_t url_bonus;
    int32_t total;
} ProcessSummary;

typedef struct DeltaSpec {
    int32_t delta;
    int32_t repeat;
} DeltaSpec;

typedef struct CounterStats {
    int32_t current_value;
    int32_t total_operations;
    int32_t total_delta;
} CounterStats;

#ifdef __cplusplus
}
#endif
