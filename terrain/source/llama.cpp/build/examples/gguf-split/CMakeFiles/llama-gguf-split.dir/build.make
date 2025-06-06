# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.22

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Disable VCS-based implicit rules.
% : %,v

# Disable VCS-based implicit rules.
% : RCS/%

# Disable VCS-based implicit rules.
% : RCS/%,v

# Disable VCS-based implicit rules.
% : SCCS/s.%

# Disable VCS-based implicit rules.
% : s.%

.SUFFIXES: .hpux_make_needs_suffix_list

# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/warchu/PycharmProjects/llama/llama.cpp

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/warchu/PycharmProjects/llama/llama.cpp/build

# Include any dependencies generated for this target.
include examples/gguf-split/CMakeFiles/llama-gguf-split.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include examples/gguf-split/CMakeFiles/llama-gguf-split.dir/compiler_depend.make

# Include the progress variables for this target.
include examples/gguf-split/CMakeFiles/llama-gguf-split.dir/progress.make

# Include the compile flags for this target's objects.
include examples/gguf-split/CMakeFiles/llama-gguf-split.dir/flags.make

examples/gguf-split/CMakeFiles/llama-gguf-split.dir/gguf-split.cpp.o: examples/gguf-split/CMakeFiles/llama-gguf-split.dir/flags.make
examples/gguf-split/CMakeFiles/llama-gguf-split.dir/gguf-split.cpp.o: ../examples/gguf-split/gguf-split.cpp
examples/gguf-split/CMakeFiles/llama-gguf-split.dir/gguf-split.cpp.o: examples/gguf-split/CMakeFiles/llama-gguf-split.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/warchu/PycharmProjects/llama/llama.cpp/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object examples/gguf-split/CMakeFiles/llama-gguf-split.dir/gguf-split.cpp.o"
	cd /home/warchu/PycharmProjects/llama/llama.cpp/build/examples/gguf-split && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT examples/gguf-split/CMakeFiles/llama-gguf-split.dir/gguf-split.cpp.o -MF CMakeFiles/llama-gguf-split.dir/gguf-split.cpp.o.d -o CMakeFiles/llama-gguf-split.dir/gguf-split.cpp.o -c /home/warchu/PycharmProjects/llama/llama.cpp/examples/gguf-split/gguf-split.cpp

examples/gguf-split/CMakeFiles/llama-gguf-split.dir/gguf-split.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/llama-gguf-split.dir/gguf-split.cpp.i"
	cd /home/warchu/PycharmProjects/llama/llama.cpp/build/examples/gguf-split && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/warchu/PycharmProjects/llama/llama.cpp/examples/gguf-split/gguf-split.cpp > CMakeFiles/llama-gguf-split.dir/gguf-split.cpp.i

examples/gguf-split/CMakeFiles/llama-gguf-split.dir/gguf-split.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/llama-gguf-split.dir/gguf-split.cpp.s"
	cd /home/warchu/PycharmProjects/llama/llama.cpp/build/examples/gguf-split && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/warchu/PycharmProjects/llama/llama.cpp/examples/gguf-split/gguf-split.cpp -o CMakeFiles/llama-gguf-split.dir/gguf-split.cpp.s

# Object files for target llama-gguf-split
llama__gguf__split_OBJECTS = \
"CMakeFiles/llama-gguf-split.dir/gguf-split.cpp.o"

# External object files for target llama-gguf-split
llama__gguf__split_EXTERNAL_OBJECTS =

bin/llama-gguf-split: examples/gguf-split/CMakeFiles/llama-gguf-split.dir/gguf-split.cpp.o
bin/llama-gguf-split: examples/gguf-split/CMakeFiles/llama-gguf-split.dir/build.make
bin/llama-gguf-split: common/libcommon.a
bin/llama-gguf-split: bin/libllama.so
bin/llama-gguf-split: bin/libggml.so
bin/llama-gguf-split: bin/libggml-cpu.so
bin/llama-gguf-split: bin/libggml-cuda.so
bin/llama-gguf-split: bin/libggml-base.so
bin/llama-gguf-split: /usr/lib/x86_64-linux-gnu/libcurl.so
bin/llama-gguf-split: examples/gguf-split/CMakeFiles/llama-gguf-split.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/warchu/PycharmProjects/llama/llama.cpp/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable ../../bin/llama-gguf-split"
	cd /home/warchu/PycharmProjects/llama/llama.cpp/build/examples/gguf-split && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/llama-gguf-split.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
examples/gguf-split/CMakeFiles/llama-gguf-split.dir/build: bin/llama-gguf-split
.PHONY : examples/gguf-split/CMakeFiles/llama-gguf-split.dir/build

examples/gguf-split/CMakeFiles/llama-gguf-split.dir/clean:
	cd /home/warchu/PycharmProjects/llama/llama.cpp/build/examples/gguf-split && $(CMAKE_COMMAND) -P CMakeFiles/llama-gguf-split.dir/cmake_clean.cmake
.PHONY : examples/gguf-split/CMakeFiles/llama-gguf-split.dir/clean

examples/gguf-split/CMakeFiles/llama-gguf-split.dir/depend:
	cd /home/warchu/PycharmProjects/llama/llama.cpp/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/warchu/PycharmProjects/llama/llama.cpp /home/warchu/PycharmProjects/llama/llama.cpp/examples/gguf-split /home/warchu/PycharmProjects/llama/llama.cpp/build /home/warchu/PycharmProjects/llama/llama.cpp/build/examples/gguf-split /home/warchu/PycharmProjects/llama/llama.cpp/build/examples/gguf-split/CMakeFiles/llama-gguf-split.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : examples/gguf-split/CMakeFiles/llama-gguf-split.dir/depend

