#include "nexus/text_utils.hpp"
#include <algorithm>
#include <cctype>

namespace nexus {
std::string trim(const std::string& value) {
    const auto first = std::find_if_not(value.begin(), value.end(),
        [](unsigned char c) { return std::isspace(c) != 0; });
    if (first == value.end()) return {};
    const auto last = std::find_if_not(value.rbegin(), value.rend(),
        [](unsigned char c) { return std::isspace(c) != 0; }).base();
    return std::string(first, last);
}

std::string normalize(const std::string& value) {
    std::string out = trim(value);
    std::transform(out.begin(), out.end(), out.begin(),
        [](unsigned char c) { return static_cast<char>(std::tolower(c)); });
    return out;
}

bool contains(const std::string& text, const std::string& needle) {
    return text.find(needle) != std::string::npos;
}
}
