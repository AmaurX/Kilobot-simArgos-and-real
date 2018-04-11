#ifndef CI_KILOBOT_LOOP_FUNCTIONS_H
#define CI_KILOBOT_LOOP_FUNCTIONS_H

#include <argos3/core/simulator/loop_functions.h>
#include <argos3/core/simulator/entity/floor_entity.h>
#include <argos3/core/utility/math/range.h>
#include <argos3/core/utility/math/rng.h>
#include <argos3/core/control_interface/ci_controller.h>
#include <argos3/plugins/robots/generic/control_interface/ci_differential_steering_actuator.h>
#include <argos3/plugins/robots/generic/control_interface/ci_leds_actuator.h>
#include <argos3/plugins/robots/kilobot/control_interface/ci_kilobot_communication_actuator.h>
#include <argos3/plugins/robots/kilobot/control_interface/ci_kilobot_communication_sensor.h>
#include <argos3/plugins/robots/kilobot/control_interface/ci_kilobot_controller.h>

#include <argos3/core/utility/configuration/argos_configuration.h>
#include <argos3/core/utility/math/vector2.h>
#include <algorithm>
#include <argos3/core/utility/math/rng.h>
#include <argos3/core/utility/logging/argos_log.h>
#include <vector>
#include <argos3/plugins/simulator/entities/box_entity.h>

using namespace argos;

////////////////////////////////////////////////////////////////
// Results struct
////////////////////////////////////////////////////////////////
struct TRWResults
{
  UInt32 m_unFullDiscoveryTime;
  UInt32 m_unFullInformationTime;
  Real m_fFractionWithInformation;
  Real m_fFractionWithDiscovery;

  TRWResults()
  {
    m_unFullDiscoveryTime = 0;
    m_unFullInformationTime = 0;
    m_fFractionWithInformation = 0.0;
    m_fFractionWithDiscovery = 0.0;
  }

  void Reset()
  {
    m_unFullDiscoveryTime = 0;
    m_unFullInformationTime = 0;
    m_fFractionWithInformation = 0.0;
    m_fFractionWithDiscovery = 0.0;
  }

  friend std::ostream &operator<<(std::ostream &os, const TRWResults &t_results)
  {
    os << t_results.m_unFullDiscoveryTime << " "
       << t_results.m_unFullInformationTime << " "
       << t_results.m_fFractionWithInformation << " "
       << t_results.m_fFractionWithDiscovery;
    return os;
  }
};

////////////////////////////////////////////////////////////////
// RW Loop Functions struct
////////////////////////////////////////////////////////////////

class CIKilobotLoopFunctions : public CLoopFunctions
{
public:
  CIKilobotLoopFunctions();
  virtual ~CIKilobotLoopFunctions() {}

  virtual void Init(TConfigurationNode &t_tree);
  //  virtual void Reset();
  //  virtual void Destroy();
  //  virtual CColor GetFloorColor(const CVector2& c_position_on_plane);
  virtual void PostStep();

  virtual bool IsExperimentFinished();
  //  virtual void SetExperiment();
  virtual void PostExperiment();

  const UInt32 GetNumRobots() const
  {
    return m_unNumRobots;
  };
  void SetNumRobots(const UInt32 un_num_robots) { m_unNumRobots = un_num_robots; };

  inline const TRWResults &GetResults() const { return m_tResults; };

private:
  //  CFloorEntity* m_pcFloor;
  //  CRandom::CRNG* m_pcRNG;

  //  Real m_fArenaRadius;
  UInt32 m_unNumRobots;
  //  CVector2 m_cTargetPosition;
  //  Real m_fTargetRadius;

  CSpace::TMapPerType m_cKilobots;
  std::vector<CVector2> m_cKilobotOriginalPositions;
  std::vector<Real> m_cKilobotGreatestDisplacement;
  TRWResults m_tResults;
  Real fractionDiscovery_;
  Real fractionInformation_;
};

#endif
