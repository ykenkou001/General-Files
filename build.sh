#!/bin/bash

cmake -Bbuild -DCMAKE_BUILD_TYPE=Debug -DCMAKE_EXPORT_COMPILE_COMMANDS=YES 
ln -s build/compile_commands.json .

