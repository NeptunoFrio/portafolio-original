#pragma once
#include <string>

namespace nexus {
enum class Intent { Greeting, Remember, Recall, Help, Exit, Unknown };
Intent classify_intent(const std::string& input);
std::string intent_name(Intent intent);
}
