cmake_minimum_required(VERSION 3.10)
project(MyProject)

set(CMAKE_CXX_STANDARD 17)

include_directories(include)

find_package(yaml-cpp REQUIRED)

file(GLOB SOURCES "src/*.cpp")
add_executable(my_program ${SOURCES})

target_link_libraries(my_program PRIVATE yaml-cpp)

