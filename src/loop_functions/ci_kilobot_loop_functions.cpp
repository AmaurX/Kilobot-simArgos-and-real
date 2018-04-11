#include "ci_kilobot_loop_functions.h"

#include <argos3/core/simulator/simulator.h>
#include <argos3/core/utility/configuration/argos_configuration.h>
#include <argos3/plugins/robots/kilobot/simulator/kilobot_entity.h>
#include <argos3/plugins/robots/kilobot/simulator/kilobot_measures.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <signal.h>
#include <cerrno>
#include <fcntl.h>
#include <unistd.h>

#include <set>
#include <iomanip>

// const std::string CONFIGURATION_KILOBOT_RW_ARENA_RADIUS = "arena_radius";
const std::string CONFIGURATION_KILOBOT_RW_NUM_ROBOTS = "num_robots";
// const std::string CONFIGURATION_KILOBOT_RW_TARGET_RADIUS = "target_radius";

/****************************************/
/****************************************/

CIKilobotLoopFunctions::CIKilobotLoopFunctions() : m_unNumRobots(0),
                                                   m_tResults(),
                                                   fractionDiscovery_(0),
                                                   fractionInformation_(0)
{
}

/****************************************/
/****************************************/

void CIKilobotLoopFunctions::Init(TConfigurationNode &t_node)
{
      // /* Read parameters from configuration file */
      // GetNodeAttributeOrDefault(t_node, CONFIGURATION_KILOBOT_RW_ARENA_RADIUS, m_fArenaRadius, m_fArenaRadius);
      GetNodeAttributeOrDefault(t_node, CONFIGURATION_KILOBOT_RW_NUM_ROBOTS, m_unNumRobots, m_unNumRobots);
      // GetNodeAttributeOrDefault(t_node, CONFIGURATION_KILOBOT_RW_TARGET_RADIUS, m_fTargetRadius, m_fTargetRadius);

      m_cKilobots = GetSpace().GetEntitiesByType("kilobot");

      // // set the experiment
      // SetExperiment();
}

/****************************************/
/****************************************/

// void CIKilobotLoopFunctions::Reset()
// {
//       // SetExperiment();
// }

/****************************************/
/****************************************/

// void CIKilobotLoopFunctions::Destroy()
// {
// }

/****************************************/
/****************************************/

// void CIKilobotLoopFunctions::SetExperiment()
// {
//       // // initialise/reset the internal variables
//       // m_tResults.Reset();
// }

/****************************************/
/****************************************/

void CIKilobotLoopFunctions::PostStep()
{
      // LOG << "Hello there \n";
      // LOG.Flush();
      UInt32 un_robot_index = 0;
      UInt32 num_robots_with_discovery = 0;
      UInt32 num_robots_with_info = 0;
      for (CSpace::TMapPerType::iterator it = m_cKilobots.begin(); it != m_cKilobots.end(); ++it, ++un_robot_index)
      {
            /* Get handle to kilobot entity and controller */
            CKilobotEntity &c_kilobot = *any_cast<CKilobotEntity *>(it->second);
            // CVector2 c_kilobot_xy_position(c_kilobot.GetEmbodiedEntity().GetOriginAnchor().Position.GetX(), c_kilobot.GetEmbodiedEntity().GetOriginAnchor().Position.GetY());
            CCI_KilobotController &c_controller = dynamic_cast<CCI_KilobotController &>(c_kilobot.GetControllableEntity().GetController());

            int sharedMemFD = c_controller.GetSharedMemFD();

            kilobot_state_t *robotState;
            /* Resize shared memory area to contain the robot state, filling it with zeros */
            ftruncate(sharedMemFD, sizeof(kilobot_state_t));
            /* Get pointer to shared memory area */
            robotState =
                (kilobot_state_t *)mmap(NULL,
                                        sizeof(kilobot_state_t),
                                        PROT_READ,
                                        MAP_SHARED,
                                        sharedMemFD,
                                        0);
            if (robotState == MAP_FAILED)
            {
                  close(sharedMemFD);
                  exit(1);
            }

            message_t message = robotState->tx_message;

            int first_passage_time = 0;
            int first_info_time = 0;

            memcpy((void *)&first_info_time, (void *)&(message.data[1]), sizeof(int));
            memcpy((void *)&first_passage_time, (void *)&(message.data[5]), sizeof(int));

            // LOG << "first_info_time :" << first_info_time << " first_passage_time : " << first_passage_time << std::endl;
            // LOG.Flush();

            if (message.data[0] == 1 && first_passage_time != 0)
            {
                  num_robots_with_discovery += 1;
            }
            if (message.data[0] == 1 && first_info_time != 0)
            {
                  num_robots_with_info += 1;
            }

            munmap(robotState, sizeof(kilobot_state_t));
      }

      // Check results
      m_tResults.m_fFractionWithDiscovery = ((Real)num_robots_with_discovery) / ((Real)m_unNumRobots);
      m_tResults.m_fFractionWithInformation = ((Real)num_robots_with_info) / ((Real)m_unNumRobots);

      if (m_tResults.m_fFractionWithDiscovery != fractionDiscovery_)
      {
            fractionDiscovery_ = m_tResults.m_fFractionWithDiscovery;
            LOG << "Fraction discovery is " << m_tResults.m_fFractionWithDiscovery << std::endl;
            LOG.Flush();
      }

      if (m_tResults.m_fFractionWithInformation != fractionInformation_)
      {
            fractionInformation_ = m_tResults.m_fFractionWithInformation;
            LOG << "Fraction information is " << m_tResults.m_fFractionWithInformation << std::endl;
            LOG.Flush();
      }

      if ((num_robots_with_discovery == m_unNumRobots) && (m_tResults.m_unFullDiscoveryTime == 0))
            m_tResults.m_unFullDiscoveryTime = GetSpace().GetSimulationClock();

      if ((num_robots_with_info == m_unNumRobots) && (m_tResults.m_unFullInformationTime == 0))
            m_tResults.m_unFullInformationTime = GetSpace().GetSimulationClock();
}

/****************************************/
/****************************************/

void CIKilobotLoopFunctions::PostExperiment()
{

      std::ofstream of("results_Amaury-2.dat", std::ios::out);
      TRWResults results = GetResults();
      of << results << std::endl;
      LOG << results << std::endl;
      LOG.Flush();
}

bool CIKilobotLoopFunctions::IsExperimentFinished()
{
      if (m_tResults.m_unFullDiscoveryTime != 0)
      {
            LOG << "Experiment Finished" << std::endl;
            LOG.Flush();
            return (m_tResults.m_unFullDiscoveryTime != 0);
      }
      return false;
}

/****************************************/
/****************************************/

REGISTER_LOOP_FUNCTIONS(CIKilobotLoopFunctions, "ci_kilobot_loop_functions")
