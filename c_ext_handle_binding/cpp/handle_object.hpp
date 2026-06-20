#pragma once

#include "types.hpp"

class HandleObject {
public:
    virtual ~HandleObject() = default;
    virtual TypeId type() const = 0;
};
