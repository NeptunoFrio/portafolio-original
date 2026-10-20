#pragma once
#include <optional>
#include <string>
#include <unordered_map>

namespace nexus {
class Memory {
public:
    void remember(const std::string& key, const std::string& value);
    std::optional<std::string> recall(const std::string& key) const;
    bool forget(const std::string& key);
    std::size_t size() const noexcept;
private:
    std::unordered_map<std::string, std::string> entries_;
};
}
