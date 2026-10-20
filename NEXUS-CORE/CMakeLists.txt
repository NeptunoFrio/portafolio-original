cmake_minimum_required(VERSION 3.16)
project(NEXUS_CORE VERSION 0.1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

add_library(nexus_core
    src/text_utils.cpp
    src/intent.cpp
    src/memory.cpp
    src/engine.cpp
)
target_include_directories(nexus_core PUBLIC include)

add_executable(nexus src/main.cpp)
target_link_libraries(nexus PRIVATE nexus_core)

enable_testing()
add_executable(nexus_tests tests/test_main.cpp)
target_link_libraries(nexus_tests PRIVATE nexus_core)
add_test(NAME nexus_tests COMMAND nexus_tests)
