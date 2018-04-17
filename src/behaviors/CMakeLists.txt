# THIS IS ONLY FOR SIMULATION -> TODO deport it to a behaviors_simulation folder

Set(REAL 0)

if(ARGOS_BUILD_FOR_SIMULATOR)
#include_directories(${CMAKE_SOURCE_DIR}/plugins/robots/kilobot/control_interface)
include_directories(/usr/local/include/argos3/plugins/robots/kilobot/control_interface /usr/local/include/argos3/plugins/robots/kilobot/simulator)

    add_executable(CRWLEVY CRWLEVY.c )
  target_link_libraries(CRWLEVY argos3plugin_simulator_kilolib m)


      add_executable(Target Target.c)
  target_link_libraries(Target argos3plugin_simulator_kilolib m)

endif(ARGOS_BUILD_FOR_SIMULATOR)


