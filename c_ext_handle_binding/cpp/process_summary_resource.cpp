#include "process_summary_resource.hpp"

ProcessSummaryResource::ProcessSummaryResource(const ProcessSummary& summary)
    : summary_(summary) {}

TypeId ProcessSummaryResource::type() const {
    return TypeId::ProcessSummary;
}

void ProcessSummaryResource::fill(ProcessSummary& out) const {
    out = summary_;
}
