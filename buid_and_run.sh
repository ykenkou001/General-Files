#!/bin/bash

# This script builds and runs a CMake project
# Usage: ./build_and_run.sh <project_name>

# Build the project using CMake
cmake --build build

# Run the executable based on the provided project name
./build/"$1"

