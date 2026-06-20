#include "config_snapshot_resource.hpp"

ConfigSnapshotResource::ConfigSnapshotResource(const ConfigSnapshot& snapshot)
    : snapshot_(snapshot) {}

TypeId ConfigSnapshotResource::type() const {
    return TypeId::ConfigSnapshot;
}

void ConfigSnapshotResource::fill(ConfigSnapshot& out) const {
    out = snapshot_;
}
