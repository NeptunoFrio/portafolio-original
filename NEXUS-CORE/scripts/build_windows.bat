@echo off
cmake -S . -B build
if errorlevel 1 exit /b 1
cmake --build build --config Release
if errorlevel 1 exit /b 1
ctest --test-dir build --output-on-failure
