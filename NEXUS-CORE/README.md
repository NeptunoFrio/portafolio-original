# NEXUS CORE

A small, modular C++17 core project intended as a starting point for experimenting with a local assistant "brain".

## Build

Requirements: CMake 3.16+ and a C++17 compiler.

```bash
cmake -S . -B build
cmake --build build
ctest --test-dir build --output-on-failure
```

Run:
```bash
./build/nexus
```

On Windows, the executable is typically `build\Debug\nexus.exe` or `build\nexus.exe`.

## What is included

- A simple command-line loop
- Basic text normalization and intent classification
- A tiny in-memory key/value memory
- Unit-style smoke tests without third-party dependencies

This is a starter framework, not a trained language model. It does not have human-level reasoning or learn autonomously from conversations.
