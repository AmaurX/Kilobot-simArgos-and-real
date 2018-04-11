# THIS IS ONLY FOR SIMULATION -> TODO deport it to a behaviors_simulation folder

Set(REAL 0)

if(ARGOS_BUILD_FOR_SIMULATOR)
  include_directories(${CMAKE_SOURCE_DIR}/plugins/robots/kilobot/control_interface)

    add_executable(CRWLEVY CRWLEVY.c )
  target_link_libraries(CRWLEVY argos3plugin_simulator_kilolib)


      add_executable(Target Target.c)
  target_link_libraries(Target argos3plugin_simulator_kilolib)

endif(ARGOS_BUILD_FOR_SIMULATOR)


