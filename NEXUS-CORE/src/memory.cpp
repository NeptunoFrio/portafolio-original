#include "nexus/memory.hpp"
#include "nexus/text_utils.hpp"

namespace nexus {
void Memory::remember(const std::string& key, const std::string& value) {
    const std::string normalized_key = normalize(key);
    if (!normalized_key.empty()) entries_[normalized_key] = value;
}

std::optional<std::string> Memory::recall(const std::string& key) const {
    const auto it = entries_.find(normalize(key));
    if (it == entries_.end()) return std::nullopt;
    return it->second;
}

bool Memory::forget(const std::string& key) {
    return entries_.erase(normalize(key)) > 0;
}

std::size_t Memory::size() const noexcept {
    return entries_.size();
}
}
