# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.5

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
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
RM = /usr/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/amaury/istc/Kilobot-simArgos-and-real/src

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/amaury/istc/Kilobot-simArgos-and-real/build

# Utility rule file for argos3plugin_simulator_kilolib_automoc.

# Include the progress variables for this target.
include plugins/robots/kilobot/CMakeFiles/argos3plugin_simulator_kilolib_automoc.dir/progress.make

plugins/robots/kilobot/CMakeFiles/argos3plugin_simulator_kilolib_automoc:
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --blue --bold --progress-dir=/home/amaury/istc/Kilobot-simArgos-and-real/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Automatic moc for target argos3plugin_simulator_kilolib"
	cd /home/amaury/istc/Kilobot-simArgos-and-real/build/plugins/robots/kilobot && /usr/bin/cmake -E cmake_autogen /home/amaury/istc/Kilobot-simArgos-and-real/build/plugins/robots/kilobot/CMakeFiles/argos3plugin_simulator_kilolib_automoc.dir/ ""

argos3plugin_simulator_kilolib_automoc: plugins/robots/kilobot/CMakeFiles/argos3plugin_simulator_kilolib_automoc
argos3plugin_simulator_kilolib_automoc: plugins/robots/kilobot/CMakeFiles/argos3plugin_simulator_kilolib_automoc.dir/build.make

.PHONY : argos3plugin_simulator_kilolib_automoc

# Rule to build all files generated by this target.
plugins/robots/kilobot/CMakeFiles/argos3plugin_simulator_kilolib_automoc.dir/build: argos3plugin_simulator_kilolib_automoc

.PHONY : plugins/robots/kilobot/CMakeFiles/argos3plugin_simulator_kilolib_automoc.dir/build

plugins/robots/kilobot/CMakeFiles/argos3plugin_simulator_kilolib_automoc.dir/clean:
	cd /home/amaury/istc/Kilobot-simArgos-and-real/build/plugins/robots/kilobot && $(CMAKE_COMMAND) -P CMakeFiles/argos3plugin_simulator_kilolib_automoc.dir/cmake_clean.cmake
.PHONY : plugins/robots/kilobot/CMakeFiles/argos3plugin_simulator_kilolib_automoc.dir/clean

plugins/robots/kilobot/CMakeFiles/argos3plugin_simulator_kilolib_automoc.dir/depend:
	cd /home/amaury/istc/Kilobot-simArgos-and-real/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/amaury/istc/Kilobot-simArgos-and-real/src /home/amaury/istc/Kilobot-simArgos-and-real/src/plugins/robots/kilobot /home/amaury/istc/Kilobot-simArgos-and-real/build /home/amaury/istc/Kilobot-simArgos-and-real/build/plugins/robots/kilobot /home/amaury/istc/Kilobot-simArgos-and-real/build/plugins/robots/kilobot/CMakeFiles/argos3plugin_simulator_kilolib_automoc.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : plugins/robots/kilobot/CMakeFiles/argos3plugin_simulator_kilolib_automoc.dir/depend

