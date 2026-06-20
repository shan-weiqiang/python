#include "c_types.h"
#include "config.hpp"
#include "config_snapshot_resource.hpp"
#include "counter.hpp"
#include "counter_stats_resource.hpp"
#include "handle_pool.hpp"
#include "process_summary_resource.hpp"

#include <cstdint>
#include <cstring>
#include <memory>
#include <string>

namespace {

HandlePool g_pool;
thread_local std::string g_last_error;

void set_error(const char* message) {
    g_last_error = message;
}

void clear_error() {
    g_last_error.clear();
}

bool validate_spec(const ConfigSpec* spec) {
    return spec != nullptr;
}

ProcessSummary invalid_process_summary() {
    ProcessSummary summary{};
    summary.total = -1;
    return summary;
}

}  // namespace

extern "C" {

const char* handle_last_error(void) {
    return g_last_error.c_str();
}

void handle_release(int64_t handle) {
    clear_error();
    if (handle == kInvalidHandle) {
        set_error("invalid handle");
        return;
    }
    if (!g_pool.release(handle)) {
        set_error("handle not found");
    }
}

int handle_type(int64_t handle) {
    clear_error();
    if (handle == kInvalidHandle) {
        set_error("invalid handle");
        return kInvalidTypeId;
    }
    return g_pool.type_of(handle);
}

int64_t config_create(int timeout, const char* url, int enable_ssl) {
    clear_error();
    if (url == nullptr) {
        set_error("url must not be null");
        return kInvalidHandle;
    }

    const HandleId handle = g_pool.store(std::make_unique<Config>(
        timeout, std::string(url), enable_ssl != 0));
    return handle;
}

int64_t config_create_from_spec(const ConfigSpec* spec) {
    clear_error();
    if (!validate_spec(spec)) {
        set_error("spec must not be null");
        return kInvalidHandle;
    }

    const HandleId handle =
        g_pool.store(std::make_unique<Config>(Config::from_spec(*spec)));
    return handle;
}

int config_process(int64_t handle) {
    clear_error();
    Config* config = g_pool.get_as<Config>(handle, TypeId::Config);
    if (config == nullptr) {
        set_error("invalid handle or wrong type");
        return -1;
    }
    return config->process();
}

int config_get_snapshot(int64_t handle, ConfigSnapshot* out) {
    clear_error();
    if (out == nullptr) {
        set_error("snapshot output must not be null");
        return -1;
    }

    Config* config = g_pool.get_as<Config>(handle, TypeId::Config);
    if (config == nullptr) {
        set_error("invalid handle or wrong type");
        return -1;
    }

    config->fill_snapshot(*out);
    return 0;
}

ProcessSummary config_process_summary(int64_t handle) {
    clear_error();
    Config* config = g_pool.get_as<Config>(handle, TypeId::Config);
    if (config == nullptr) {
        set_error("invalid handle or wrong type");
        return invalid_process_summary();
    }
    return config->process_summary();
}

int64_t config_create_snapshot(int64_t handle) {
    clear_error();
    Config* config = g_pool.get_as<Config>(handle, TypeId::Config);
    if (config == nullptr) {
        set_error("invalid handle or wrong type");
        return kInvalidHandle;
    }

    ConfigSnapshot snapshot{};
    config->fill_snapshot(snapshot);
    return g_pool.store(
        std::make_unique<ConfigSnapshotResource>(snapshot));
}

int config_snapshot_read(int64_t handle, ConfigSnapshot* out) {
    clear_error();
    if (out == nullptr) {
        set_error("snapshot output must not be null");
        return -1;
    }

    ConfigSnapshotResource* snapshot =
        g_pool.get_as<ConfigSnapshotResource>(handle, TypeId::ConfigSnapshot);
    if (snapshot == nullptr) {
        set_error("invalid handle or wrong type");
        return -1;
    }

    snapshot->fill(*out);
    return 0;
}

int64_t config_create_process_summary(int64_t handle) {
    clear_error();
    Config* config = g_pool.get_as<Config>(handle, TypeId::Config);
    if (config == nullptr) {
        set_error("invalid handle or wrong type");
        return kInvalidHandle;
    }

    return g_pool.store(std::make_unique<ProcessSummaryResource>(
        config->process_summary()));
}

int process_summary_read(int64_t handle, ProcessSummary* out) {
    clear_error();
    if (out == nullptr) {
        set_error("summary output must not be null");
        return -1;
    }

    ProcessSummaryResource* summary =
        g_pool.get_as<ProcessSummaryResource>(handle, TypeId::ProcessSummary);
    if (summary == nullptr) {
        set_error("invalid handle or wrong type");
        return -1;
    }

    summary->fill(*out);
    return 0;
}

int config_spec_merge(const ConfigSpec* left,
                      const ConfigSpec* right,
                      ConfigSpec* out) {
    clear_error();
    if (left == nullptr || right == nullptr || out == nullptr) {
        set_error("merge arguments must not be null");
        return -1;
    }

    out->timeout = left->timeout + right->timeout;
    out->enable_ssl = (left->enable_ssl != 0 || right->enable_ssl != 0) ? 1 : 0;

    const std::size_t left_len = std::strlen(left->server_url);
    const std::size_t right_len = std::strlen(right->server_url);
    if (left_len + right_len >= HANDLE_BRIDGE_URL_MAX) {
        set_error("merged url exceeds buffer size");
        return -1;
    }

    std::memcpy(out->server_url, left->server_url, left_len);
    std::memcpy(out->server_url + left_len, right->server_url, right_len);
    out->server_url[left_len + right_len] = '\0';
    return 0;
}

int64_t counter_create(int initial) {
    clear_error();
    const HandleId handle =
        g_pool.store(std::make_unique<Counter>(initial));
    return handle;
}

int counter_increment(int64_t handle, int delta) {
    clear_error();
    Counter* counter = g_pool.get_as<Counter>(handle, TypeId::Counter);
    if (counter == nullptr) {
        set_error("invalid handle or wrong type");
        return -1;
    }
    counter->increment(delta);
    return 0;
}

int counter_apply_delta(int64_t handle, const DeltaSpec* spec) {
    clear_error();
    if (spec == nullptr) {
        set_error("delta spec must not be null");
        return -1;
    }
    if (spec->repeat < 0) {
        set_error("repeat must be non-negative");
        return -1;
    }

    Counter* counter = g_pool.get_as<Counter>(handle, TypeId::Counter);
    if (counter == nullptr) {
        set_error("invalid handle or wrong type");
        return -1;
    }

    counter->apply_delta(*spec);
    return 0;
}

int counter_get(int64_t handle) {
    clear_error();
    Counter* counter = g_pool.get_as<Counter>(handle, TypeId::Counter);
    if (counter == nullptr) {
        set_error("invalid handle or wrong type");
        return -1;
    }
    return counter->get();
}

int counter_get_stats(int64_t handle, CounterStats* out) {
    clear_error();
    if (out == nullptr) {
        set_error("stats output must not be null");
        return -1;
    }

    Counter* counter = g_pool.get_as<Counter>(handle, TypeId::Counter);
    if (counter == nullptr) {
        set_error("invalid handle or wrong type");
        return -1;
    }

    counter->fill_stats(*out);
    return 0;
}

int64_t counter_create_stats(int64_t handle) {
    clear_error();
    Counter* counter = g_pool.get_as<Counter>(handle, TypeId::Counter);
    if (counter == nullptr) {
        set_error("invalid handle or wrong type");
        return kInvalidHandle;
    }

    CounterStats stats{};
    counter->fill_stats(stats);
    return g_pool.store(std::make_unique<CounterStatsResource>(stats));
}

int counter_stats_read(int64_t handle, CounterStats* out) {
    clear_error();
    if (out == nullptr) {
        set_error("stats output must not be null");
        return -1;
    }

    CounterStatsResource* stats =
        g_pool.get_as<CounterStatsResource>(handle, TypeId::CounterStats);
    if (stats == nullptr) {
        set_error("invalid handle or wrong type");
        return -1;
    }

    stats->fill(*out);
    return 0;
}

}  // extern "C"
