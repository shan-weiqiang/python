#pragma once

#include "c_types.h"
#include "handle_object.hpp"

#include <string>

class Config : public HandleObject {
public:
    Config(int timeout, std::string server_url, bool enable_ssl);
    static Config from_spec(const ConfigSpec& spec);

    TypeId type() const override;
    int process() const;
    void fill_snapshot(ConfigSnapshot& out) const;
    ProcessSummary process_summary() const;

private:
    int timeout_;
    std::string server_url_;
    bool enable_ssl_;
};
