#include "nexus/engine.hpp"
#include "nexus/intent.hpp"
#include "nexus/text_utils.hpp"

namespace nexus {
std::string Engine::respond(const std::string& input) {
    const Intent intent = classify_intent(input);
    const std::string normalized = normalize(input);

    switch (intent) {
        case Intent::Greeting:
            return "NEXUS: Hello. I'm ready. Type 'help' to see available commands.";
        case Intent::Remember: {
            // Expected format: remember key = value / recuerda key = value
            const auto split = normalized.find('=');
            if (split == std::string::npos)
                return "NEXUS: Use: remember key = value";
            const std::string left = trim(normalized.substr(0, split));
            const std::string right = trim(input.substr(split + 1));
            std::string key = left;
            const auto space = key.find(' ');
            if (space != std::string::npos) key = trim(key.substr(space + 1));
            if (key.empty() || right.empty()) return "NEXUS: Key and value are required.";
            memory_.remember(key, right);
            return "NEXUS: Saved in temporary memory under '" + key + "'.";
        }
        case Intent::Recall: {
            std::string key = trim(normalized);
            const auto space = key.find(' ');
            if (space != std::string::npos) key = trim(key.substr(space + 1));
            if (key.rfind("what did i save", 0) == 0 || key == "que guarde" || key == "qué guardé")
                return "NEXUS: Ask for a specific key, e.g. 'recall project'.";
            const auto value = memory_.recall(key);
            if (!value) return "NEXUS: Nothing saved under '" + key + "'.";
            return "NEXUS: " + *value;
        }
        case Intent::Help:
            return "NEXUS commands: hello, remember key = value, recall key, help, exit.";
        case Intent::Exit:
            return "NEXUS: Goodbye.";
        default:
            return "NEXUS: I don't know that yet. This prototype uses simple rules, not a trained AI model.";
    }
}

const Memory& Engine::memory() const noexcept { return memory_; }
}
