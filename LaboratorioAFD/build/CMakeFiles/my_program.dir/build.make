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
CMAKE_SOURCE_DIR = /home/ppguz/Lenguajes_Programacion/LaboratorioAFD

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/ppguz/Lenguajes_Programacion/LaboratorioAFD/build

# Include any dependencies generated for this target.
include CMakeFiles/my_program.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include CMakeFiles/my_program.dir/compiler_depend.make

# Include the progress variables for this target.
include CMakeFiles/my_program.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/my_program.dir/flags.make

CMakeFiles/my_program.dir/src/main.cpp.o: CMakeFiles/my_program.dir/flags.make
CMakeFiles/my_program.dir/src/main.cpp.o: ../src/main.cpp
CMakeFiles/my_program.dir/src/main.cpp.o: CMakeFiles/my_program.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/ppguz/Lenguajes_Programacion/LaboratorioAFD/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/my_program.dir/src/main.cpp.o"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT CMakeFiles/my_program.dir/src/main.cpp.o -MF CMakeFiles/my_program.dir/src/main.cpp.o.d -o CMakeFiles/my_program.dir/src/main.cpp.o -c /home/ppguz/Lenguajes_Programacion/LaboratorioAFD/src/main.cpp

CMakeFiles/my_program.dir/src/main.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/my_program.dir/src/main.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/ppguz/Lenguajes_Programacion/LaboratorioAFD/src/main.cpp > CMakeFiles/my_program.dir/src/main.cpp.i

CMakeFiles/my_program.dir/src/main.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/my_program.dir/src/main.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/ppguz/Lenguajes_Programacion/LaboratorioAFD/src/main.cpp -o CMakeFiles/my_program.dir/src/main.cpp.s

CMakeFiles/my_program.dir/src/shunting_yard.cpp.o: CMakeFiles/my_program.dir/flags.make
CMakeFiles/my_program.dir/src/shunting_yard.cpp.o: ../src/shunting_yard.cpp
CMakeFiles/my_program.dir/src/shunting_yard.cpp.o: CMakeFiles/my_program.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/ppguz/Lenguajes_Programacion/LaboratorioAFD/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Building CXX object CMakeFiles/my_program.dir/src/shunting_yard.cpp.o"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT CMakeFiles/my_program.dir/src/shunting_yard.cpp.o -MF CMakeFiles/my_program.dir/src/shunting_yard.cpp.o.d -o CMakeFiles/my_program.dir/src/shunting_yard.cpp.o -c /home/ppguz/Lenguajes_Programacion/LaboratorioAFD/src/shunting_yard.cpp

CMakeFiles/my_program.dir/src/shunting_yard.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/my_program.dir/src/shunting_yard.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/ppguz/Lenguajes_Programacion/LaboratorioAFD/src/shunting_yard.cpp > CMakeFiles/my_program.dir/src/shunting_yard.cpp.i

CMakeFiles/my_program.dir/src/shunting_yard.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/my_program.dir/src/shunting_yard.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/ppguz/Lenguajes_Programacion/LaboratorioAFD/src/shunting_yard.cpp -o CMakeFiles/my_program.dir/src/shunting_yard.cpp.s

# Object files for target my_program
my_program_OBJECTS = \
"CMakeFiles/my_program.dir/src/main.cpp.o" \
"CMakeFiles/my_program.dir/src/shunting_yard.cpp.o"

# External object files for target my_program
my_program_EXTERNAL_OBJECTS =

my_program: CMakeFiles/my_program.dir/src/main.cpp.o
my_program: CMakeFiles/my_program.dir/src/shunting_yard.cpp.o
my_program: CMakeFiles/my_program.dir/build.make
my_program: CMakeFiles/my_program.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/ppguz/Lenguajes_Programacion/LaboratorioAFD/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_3) "Linking CXX executable my_program"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/my_program.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/my_program.dir/build: my_program
.PHONY : CMakeFiles/my_program.dir/build

CMakeFiles/my_program.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/my_program.dir/cmake_clean.cmake
.PHONY : CMakeFiles/my_program.dir/clean

CMakeFiles/my_program.dir/depend:
	cd /home/ppguz/Lenguajes_Programacion/LaboratorioAFD/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/ppguz/Lenguajes_Programacion/LaboratorioAFD /home/ppguz/Lenguajes_Programacion/LaboratorioAFD /home/ppguz/Lenguajes_Programacion/LaboratorioAFD/build /home/ppguz/Lenguajes_Programacion/LaboratorioAFD/build /home/ppguz/Lenguajes_Programacion/LaboratorioAFD/build/CMakeFiles/my_program.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/my_program.dir/depend

