# Install script for directory: /home/amaury/istc/Kilobot-simArgos-and-real/src/plugins/robots/kilobot

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/usr")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/argos3/plugins/robots/kilobot/control_interface" TYPE FILE FILES
    "/home/amaury/istc/Kilobot-simArgos-and-real/src/plugins/robots/kilobot/control_interface/ci_kilobot_communication_actuator.h"
    "/home/amaury/istc/Kilobot-simArgos-and-real/src/plugins/robots/kilobot/control_interface/ci_kilobot_communication_sensor.h"
    "/home/amaury/istc/Kilobot-simArgos-and-real/src/plugins/robots/kilobot/control_interface/ci_kilobot_controller.h"
    "/home/amaury/istc/Kilobot-simArgos-and-real/src/plugins/robots/kilobot/control_interface/ci_kilobot_loop_functions.h"
    "/home/amaury/istc/Kilobot-simArgos-and-real/src/plugins/robots/kilobot/control_interface/ci_kilobot_light_sensor.h"
    "/home/amaury/istc/Kilobot-simArgos-and-real/src/plugins/robots/kilobot/control_interface/kilolib.h"
    "/home/amaury/istc/Kilobot-simArgos-and-real/src/plugins/robots/kilobot/control_interface/message.h"
    "/home/amaury/istc/Kilobot-simArgos-and-real/src/plugins/robots/kilobot/control_interface/message_crc.h"
    )
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/argos3/plugins/robots/kilobot/simulator" TYPE FILE FILES
    "/home/amaury/istc/Kilobot-simArgos-and-real/src/plugins/robots/kilobot/simulator/dynamics2d_kilobot_model.h"
    "/home/amaury/istc/Kilobot-simArgos-and-real/src/plugins/robots/kilobot/simulator/kilobot_entity.h"
    "/home/amaury/istc/Kilobot-simArgos-and-real/src/plugins/robots/kilobot/simulator/kilobot_measures.h"
    "/home/amaury/istc/Kilobot-simArgos-and-real/src/plugins/robots/kilobot/simulator/kilobot_light_rotzonly_sensor.h"
    "/home/amaury/istc/Kilobot-simArgos-and-real/src/plugins/robots/kilobot/simulator/kilobot_communication_default_actuator.h"
    "/home/amaury/istc/Kilobot-simArgos-and-real/src/plugins/robots/kilobot/simulator/kilobot_communication_default_sensor.h"
    "/home/amaury/istc/Kilobot-simArgos-and-real/src/plugins/robots/kilobot/simulator/kilobot_communication_entity.h"
    "/home/amaury/istc/Kilobot-simArgos-and-real/src/plugins/robots/kilobot/simulator/kilobot_communication_medium.h"
    "/home/amaury/istc/Kilobot-simArgos-and-real/src/plugins/robots/kilobot/simulator/qtopengl_kilobot.h"
    )
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/argos3/libargos3plugin_simulator_kilobot.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/argos3/libargos3plugin_simulator_kilobot.so")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/argos3/libargos3plugin_simulator_kilobot.so"
         RPATH "")
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/argos3" TYPE SHARED_LIBRARY FILES "/home/amaury/istc/Kilobot-simArgos-and-real/build/plugins/robots/kilobot/libargos3plugin_simulator_kilobot.so")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/argos3/libargos3plugin_simulator_kilobot.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/argos3/libargos3plugin_simulator_kilobot.so")
    file(RPATH_CHANGE
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/argos3/libargos3plugin_simulator_kilobot.so"
         OLD_RPATH "/usr/lib/argos3:"
         NEW_RPATH "")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/argos3/libargos3plugin_simulator_kilobot.so")
    endif()
  endif()
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/argos3" TYPE STATIC_LIBRARY FILES "/home/amaury/istc/Kilobot-simArgos-and-real/build/plugins/robots/kilobot/libargos3plugin_simulator_kilolib.a")
endif()

