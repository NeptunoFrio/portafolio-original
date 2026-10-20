#pragma once
#include "nexus/memory.hpp"
#include <string>

namespace nexus {
class Engine {
public:
    std::string respond(const std::string& input);
    const Memory& memory() const noexcept;
private:
    Memory memory_;
};
}
