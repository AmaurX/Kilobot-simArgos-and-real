# THIS IS ONLY FOR SIMULATION -> TODO deport it to a behaviors_simulation folder

Set(REAL 0)

if(ARGOS_BUILD_FOR_SIMULATOR)
#include_directories(${CMAKE_SOURCE_DIR}/plugins/robots/kilobot/control_interface)
include_directories(/usr/local/include/argos3/plugins/robots/kilobot/control_interface /usr/local/include/argos3/plugins/robots/kilobot/simulator)

    add_executable(CRWLEVY CRWLEVY.c )
  target_link_libraries(CRWLEVY argos3plugin_simulator_kilolib rt m)

    add_executable(CRWLEVY_a2r0_9 CRWLEVY_a2r0,9.c )
  target_link_libraries(CRWLEVY_a2r0_9 argos3plugin_simulator_kilolib rt m)

    add_executable(CRWLEVY_a2r0_8 CRWLEVY_a2r0,8.c )
  target_link_libraries(CRWLEVY_a2r0_8 argos3plugin_simulator_kilolib rt m)

    add_executable(CRWLEVY_a2r0_7 CRWLEVY_a2r0,7.c )
  target_link_libraries(CRWLEVY_a2r0_7 argos3plugin_simulator_kilolib rt m)

    add_executable(CRWLEVY_a2r0_6 CRWLEVY_a2r0,6.c )
  target_link_libraries(CRWLEVY_a2r0_6 argos3plugin_simulator_kilolib rt m)

    add_executable(CRWLEVY_a2r0_5 CRWLEVY_a2r0,5.c )
  target_link_libraries(CRWLEVY_a2r0_5 argos3plugin_simulator_kilolib rt m)
  
    add_executable(CRWLEVY_a2r0_4 CRWLEVY_a2r0,4.c )
  target_link_libraries(CRWLEVY_a2r0_4 argos3plugin_simulator_kilolib rt m)

      add_executable(Target Target.c)
  target_link_libraries(Target argos3plugin_simulator_kilolib rt m)



endif(ARGOS_BUILD_FOR_SIMULATOR)


