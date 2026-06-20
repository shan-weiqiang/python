#pragma once

#include "c_types.h"
#include "handle_object.hpp"

class ProcessSummaryResource : public HandleObject {
public:
    explicit ProcessSummaryResource(const ProcessSummary& summary);

    TypeId type() const override;
    void fill(ProcessSummary& out) const;

private:
    ProcessSummary summary_;
};
