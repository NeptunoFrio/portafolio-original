# Architecture

- `text_utils`: whitespace cleanup and lowercase normalization.
- `intent`: rule-based intent classification.
- `memory`: lightweight in-memory key/value storage.
- `engine`: connects intent detection, memory, and responses.
- `main`: terminal interface.
- `tests`: basic regression checks.

The modules are deliberately small so they can be replaced or expanded independently.
