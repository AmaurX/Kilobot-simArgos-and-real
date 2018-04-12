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
const std::string CONFIGURATION_KILOBOT_RW_SAMPLING_PERIOD = "sampling_period_in_ticks";
// const std::string CONFIGURATION_KILOBOT_RW_TARGET_RADIUS = "target_radius";

/****************************************/
/****************************************/

CIKilobotLoopFunctions::CIKilobotLoopFunctions() : m_unNumRobots(0),
                                                   m_tResults(),
                                                   m_samplingPeriod(1),
                                                   fractionDiscovery_(0),
                                                   fractionInformation_(0),
                                                   internal_counter(0)
{
}

/****************************************/
/****************************************/

void CIKilobotLoopFunctions::Init(TConfigurationNode &t_node)
{
      // /* Read parameters from configuration file */
      // GetNodeAttributeOrDefault(t_node, CONFIGURATION_KILOBOT_RW_ARENA_RADIUS, m_fArenaRadius, m_fArenaRadius);
      GetNodeAttributeOrDefault(t_node, CONFIGURATION_KILOBOT_RW_NUM_ROBOTS, m_unNumRobots, m_unNumRobots);
      GetNodeAttributeOrDefault(t_node, CONFIGURATION_KILOBOT_RW_SAMPLING_PERIOD, m_samplingPeriod, m_samplingPeriod);
      // GetNodeAttributeOrDefault(t_node, CONFIGURATION_KILOBOT_RW_TARGET_RADIUS, m_fTargetRadius, m_fTargetRadius);

      m_cKilobots = GetSpace().GetEntitiesByType("kilobot");

      UInt32 un_robot_index = 0;
      for (CSpace::TMapPerType::iterator it = m_cKilobots.begin(); it != m_cKilobots.end(); ++it, ++un_robot_index)
      {
            /* Get handle to kilobot entity and controller */
            CKilobotEntity &c_kilobot = *any_cast<CKilobotEntity *>(it->second);
            CVector2 c_kilobot_xy_position(c_kilobot.GetEmbodiedEntity().GetOriginAnchor().Position.GetX(), c_kilobot.GetEmbodiedEntity().GetOriginAnchor().Position.GetY());
            CCI_KilobotController &c_controller = dynamic_cast<CCI_KilobotController &>(c_kilobot.GetControllableEntity().GetController());
            m_cKilobotOriginalPositions.push_back(c_kilobot_xy_position);
            std::vector<CVector2> positions_init;

            positions_init.push_back(c_kilobot_xy_position);
            m_cKilobotPositions.push_back(positions_init);

            std::vector<Real> displacement_init;
            displacement_init.push_back((Real)0.0);
            m_cKilobotDisplacements.push_back(displacement_init);
      }
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
      internal_counter += 1;
      for (CSpace::TMapPerType::iterator it = m_cKilobots.begin(); it != m_cKilobots.end(); ++it, ++un_robot_index)
      {
            /* Get handle to kilobot entity and controller */
            CKilobotEntity &c_kilobot = *any_cast<CKilobotEntity *>(it->second);

            if (internal_counter == m_samplingPeriod)
            {
                  CVector2 c_kilobot_xy_position(c_kilobot.GetEmbodiedEntity().GetOriginAnchor().Position.GetX(), c_kilobot.GetEmbodiedEntity().GetOriginAnchor().Position.GetY());

                  CVector2 originPlace = m_cKilobotOriginalPositions.at(un_robot_index);
                  Real squareDisplacement = (c_kilobot_xy_position - originPlace).SquareLength();

                  m_cKilobotPositions[un_robot_index].push_back(c_kilobot_xy_position);
                  m_cKilobotDisplacements[un_robot_index].push_back(squareDisplacement);
            }

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
      if (internal_counter == m_samplingPeriod)
      {
            internal_counter = 0;
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

const std::string currentDateTime()
{
      time_t now = time(0);
      struct tm tstruct;
      char buf[80];
      tstruct = *localtime(&now);
      strftime(buf, sizeof(buf), "%Y%m%d-%X", &tstruct);

      return buf;
}

const std::string currentDate()
{
      time_t now = time(0);
      struct tm tstruct;
      char buf[80];
      tstruct = *localtime(&now);
      strftime(buf, sizeof(buf), "%Y%m%d", &tstruct);

      return buf;
}

void CIKilobotLoopFunctions::PostExperiment()
{
      std::string dateTime = currentDateTime();
      std::string date = currentDate();
      std::string folder = "experiments/" + date + "_experiments";
      if (opendir(folder.c_str()) == NULL)
      {
            const int dir_err = mkdir(folder.c_str(), S_IRWXU | S_IRWXG | S_IROTH | S_IXOTH);
            if (-1 == dir_err)
            {
                  printf("Error creating directory!\n");
                  exit(1);
            }
      }
      std::string displacement_file = folder + "/" + dateTime + "_displacement.tsv";
      std::string position_file = folder + "/" + dateTime + "_position.tsv";
      std::string time_results_file = folder + "/" + dateTime + "_time_results.tsv";

      std::ofstream of(time_results_file, std::ios::out);

      TRWResults results = GetResults();
      of << results << std::endl;
      LOG << results << std::endl;

      std::ofstream of_2(displacement_file, std::ios::out);
      std::ofstream of_3(position_file, std::ios::out);

      of_2 << "Robot id\t";
      of_3 << "Robot id\t";
      for (uint j = 0; j < m_cKilobotDisplacements[0].size(); j++)
      {
            of_2 << "t = " << j * m_samplingPeriod << '\t';
      }
      of_2 << std::endl;

      for (uint j = 0; j < m_cKilobotPositions[0].size(); j++)
      {
            of_3 << "t = " << j * m_samplingPeriod << '\t';
      }
      of_3 << std::endl;

      for (uint i = 0; i < m_unNumRobots; i++)
      {
            of_2 << i + 1 << "\t";
            of_3 << i + 1 << "\t";

            for (uint j = 0; j < m_cKilobotDisplacements[i].size(); j++)
            {
                  of_2 << (m_cKilobotDisplacements[i])[j] << '\t';
            }
            of_2 << std::endl;
            for (uint j = 0; j < m_cKilobotPositions[i].size(); j++)
            {
                  of_3 << (m_cKilobotPositions[i])[j] << '\t';
            }
            of_3 << std::endl;
      }
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
