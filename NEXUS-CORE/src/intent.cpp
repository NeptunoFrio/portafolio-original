#include "nexus/intent.hpp"
#include "nexus/text_utils.hpp"

namespace nexus {
Intent classify_intent(const std::string& input) {
    const std::string text = normalize(input);
    if (text == "exit" || text == "quit" || text == "salir") return Intent::Exit;
    if (contains(text, "hello") || contains(text, "hi") ||
        contains(text, "hola") || contains(text, "buenas")) return Intent::Greeting;
    if (contains(text, "remember ") || contains(text, "recuerda ") ||
        contains(text, "guarda ")) return Intent::Remember;
    if (contains(text, "recall ") || contains(text, "what did i save") ||
        contains(text, "que guarde") || contains(text, "qué guardé")) return Intent::Recall;
    if (contains(text, "help") || contains(text, "ayuda")) return Intent::Help;
    return Intent::Unknown;
}

std::string intent_name(Intent intent) {
    switch (intent) {
        case Intent::Greeting: return "Greeting";
        case Intent::Remember: return "Remember";
        case Intent::Recall: return "Recall";
        case Intent::Help: return "Help";
        case Intent::Exit: return "Exit";
        default: return "Unknown";
    }
}
}
