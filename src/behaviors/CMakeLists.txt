# THIS IS ONLY FOR SIMULATION -> TODO deport it to a behaviors_simulation folder

Set(REAL 0)
if(ARGOS_BUILD_FOR_SIMULATOR)
#include_directories(${CMAKE_SOURCE_DIR}/plugins/robots/kilobot/control_interface)
include_directories(/usr/local/include/argos3/plugins/robots/kilobot/control_interface /usr/local/include/argos3/plugins/robots/kilobot/simulator)

  foreach(crw 0.00 0.15 0.30 0.45 0.60 0.75 0.90)
      # add_definitions(-DCRW_EXPONENT=${crw})
          foreach(levy 1.0 1.2 1.4 1.6 1.8 2.0)
              add_executable(CRWLEVY_${levy}_${crw} CRWLEVY.c )
              target_link_libraries(CRWLEVY_${levy}_${crw} argos3plugin_simulator_kilolib rt m)
              target_compile_definitions(CRWLEVY_${levy}_${crw} PRIVATE -DLEVY_EXPONENT=${levy} -DCRW_EXPONENT=${crw})
              
              foreach(numRobots 10 20 30)
                   add_custom_target(config_file_${numRobots}_${levy}_${crw}
                    ALL
                   COMMAND python generate_configs.py simulation_config ${numRobots} ${levy} ${crw}
                   WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}/..)
              endforeach(numRobots)
              # remove_definitions(-DLEVY_EXPONENT)
          endforeach(levy)
      # remove_definitions(-DCRW_EXPONENT)
  endforeach(crw)
  
      add_executable(Target Target.c)
  target_link_libraries(Target argos3plugin_simulator_kilolib rt m)



endif(ARGOS_BUILD_FOR_SIMULATOR)


