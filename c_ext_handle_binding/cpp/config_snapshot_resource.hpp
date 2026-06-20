#pragma once

#include "c_types.h"
#include "handle_object.hpp"

class ConfigSnapshotResource : public HandleObject {
public:
    explicit ConfigSnapshotResource(const ConfigSnapshot& snapshot);

    TypeId type() const override;
    void fill(ConfigSnapshot& out) const;

private:
    ConfigSnapshot snapshot_;
};
