#include "config.hpp"

#include <cstring>

namespace {

void copy_url(char* dest, std::size_t dest_size, const std::string& url) {
    std::strncpy(dest, url.c_str(), dest_size - 1);
    dest[dest_size - 1] = '\0';
}

}  // namespace

Config::Config(int timeout, std::string server_url, bool enable_ssl)
    : timeout_(timeout),
      server_url_(std::move(server_url)),
      enable_ssl_(enable_ssl) {}

Config Config::from_spec(const ConfigSpec& spec) {
    return Config(spec.timeout, std::string(spec.server_url), spec.enable_ssl != 0);
}

TypeId Config::type() const {
    return TypeId::Config;
}

int Config::process() const {
    int result = timeout_;
    if (enable_ssl_) {
        result += 100;
    }
    if (!server_url_.empty()) {
        result += static_cast<int>(server_url_.size());
    }
    return result;
}

void Config::fill_snapshot(ConfigSnapshot& out) const {
    out.timeout = timeout_;
    out.enable_ssl = enable_ssl_ ? 1 : 0;
    copy_url(out.server_url, HANDLE_BRIDGE_URL_MAX, server_url_);
    out.process_result = process();
}

ProcessSummary Config::process_summary() const {
    ProcessSummary summary{};
    summary.base_score = timeout_;
    summary.ssl_bonus = enable_ssl_ ? 100 : 0;
    summary.url_bonus =
        server_url_.empty() ? 0 : static_cast<int32_t>(server_url_.size());
    summary.total = summary.base_score + summary.ssl_bonus + summary.url_bonus;
    return summary;
}
