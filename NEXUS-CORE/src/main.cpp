#include "nexus/engine.hpp"
#include "nexus/intent.hpp"
#include "nexus/text_utils.hpp"
#include <iostream>
#include <string>

int main() {
    nexus::Engine engine;
    std::cout << "NEXUS CORE 0.1.0 — type 'help' or 'exit'.\n";
    std::string input;
    while (std::cout << "> " && std::getline(std::cin, input)) {
        if (nexus::classify_intent(input) == nexus::Intent::Exit) {
            std::cout << engine.respond(input) << '\n';
            break;
        }
        std::cout << engine.respond(input) << '\n';
    }
    return 0;
}
