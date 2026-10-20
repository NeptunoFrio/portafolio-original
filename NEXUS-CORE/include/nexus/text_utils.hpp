#pragma once
#include <string>

namespace nexus {
std::string trim(const std::string& value);
std::string normalize(const std::string& value);
bool contains(const std::string& text, const std::string& needle);
}
