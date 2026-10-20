#include "nexus/engine.hpp"
#include "nexus/intent.hpp"
#include "nexus/memory.hpp"
#include "nexus/text_utils.hpp"
#include <cstdlib>
#include <iostream>
#include <string>

namespace {
void check(bool condition, const std::string& message) {
    if (!condition) {
        std::cerr << "FAIL: " << message << '\n';
        std::exit(1);
    }
}
}

int main() {
    check(nexus::trim("  hello  ") == "hello", "trim removes surrounding whitespace");
    check(nexus::normalize("  HOLA ") == "hola", "normalize lowercases and trims");
    check(nexus::classify_intent("hola") == nexus::Intent::Greeting, "classifies greeting");

    nexus::Memory memory;
    memory.remember("Project", "NEXUS");
    check(memory.recall("project").value_or("") == "NEXUS", "memory lookup is case-insensitive");
    check(memory.forget("PROJECT"), "forget removes an existing key");
    check(!memory.recall("project").has_value(), "forgotten key is absent");

    nexus::Engine engine;
    check(engine.respond("help").find("remember") != std::string::npos, "help lists commands");
    check(engine.respond("remember color = blue").find("Saved") != std::string::npos, "engine saves memory");
    check(engine.respond("recall color") == "NEXUS: blue", "engine recalls memory");

    std::cout << "All NEXUS CORE tests passed.\n";
    return 0;
}
