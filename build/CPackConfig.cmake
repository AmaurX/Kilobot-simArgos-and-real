# This file will be configured to contain variables for CPack. These variables
# should be set in the CMake list file of the project before CPack module is
# included. The list of available CPACK_xxx variables and their associated
# documentation may be obtained using
#  cpack --help-variable-list
#
# Some variables are common to all generators (e.g. CPACK_PACKAGE_NAME)
# and some are specific to a generator
# (e.g. CPACK_NSIS_EXTRA_INSTALL_COMMANDS). The generator specific variables
# usually begin with CPACK_<GENNAME>_xxxx.


SET(CPACK_BINARY_7Z "")
SET(CPACK_BINARY_BUNDLE "")
SET(CPACK_BINARY_CYGWIN "")
SET(CPACK_BINARY_DEB "OFF")
SET(CPACK_BINARY_DRAGNDROP "")
SET(CPACK_BINARY_IFW "OFF")
SET(CPACK_BINARY_NSIS "OFF")
SET(CPACK_BINARY_OSXX11 "")
SET(CPACK_BINARY_PACKAGEMAKER "")
SET(CPACK_BINARY_RPM "OFF")
SET(CPACK_BINARY_STGZ "ON")
SET(CPACK_BINARY_TBZ2 "OFF")
SET(CPACK_BINARY_TGZ "ON")
SET(CPACK_BINARY_TXZ "OFF")
SET(CPACK_BINARY_TZ "ON")
SET(CPACK_BINARY_WIX "")
SET(CPACK_BINARY_ZIP "")
SET(CPACK_CMAKE_GENERATOR "Unix Makefiles")
SET(CPACK_COMPONENTS_ALL "")
SET(CPACK_COMPONENT_UNSPECIFIED_HIDDEN "TRUE")
SET(CPACK_COMPONENT_UNSPECIFIED_REQUIRED "TRUE")
SET(CPACK_DEBIAN_PACKAGE_CONTROL_EXTRA "/home/amaury/istc/NewCleanDirectory-real/build/postinst;")
SET(CPACK_DEBIAN_PACKAGE_DEPENDS "argos3_simulator (>= 3.0.0)")
SET(CPACK_DEBIAN_PACKAGE_DESCRIPTION "ARGoS-Kilobot (Kilobot plugin for ARGoS)
 A plugin to support the Kilobot robot (https://www.kilobotics.com/)
 into the ARGoS multi-robot simulator (http://www.argos-sim.info/).")
SET(CPACK_DEBIAN_PACKAGE_HOMEPAGE "http://github.com/ilpincy/argos3-kilobot/")
SET(CPACK_DEBIAN_PACKAGE_MAINTAINER "Carlo Pinciroli <ilpincy@gmail.com>")
SET(CPACK_DEBIAN_PACKAGE_SECTION "contrib/science")
SET(CPACK_GENERATOR "STGZ;TGZ;TZ")
SET(CPACK_INSTALL_CMAKE_PROJECTS "/home/amaury/istc/NewCleanDirectory-real/build;argos3_simulator;ALL;/")
SET(CPACK_INSTALL_PREFIX "/usr")
SET(CPACK_MODULE_PATH "/home/amaury/istc/NewCleanDirectory-real/src/cmake;/usr/share/argos3/cmake")
SET(CPACK_NSIS_DISPLAY_NAME "argos3plugins_simulator_kilobot ..")
SET(CPACK_NSIS_INSTALLER_ICON_CODE "")
SET(CPACK_NSIS_INSTALLER_MUI_ICON_CODE "")
SET(CPACK_NSIS_INSTALL_ROOT "$PROGRAMFILES")
SET(CPACK_NSIS_PACKAGE_NAME "argos3plugins_simulator_kilobot ..")
SET(CPACK_OUTPUT_CONFIG_FILE "/home/amaury/istc/NewCleanDirectory-real/build/CPackConfig.cmake")
SET(CPACK_PACKAGE_DEFAULT_LOCATION "/")
SET(CPACK_PACKAGE_DESCRIPTION "ARGoS-Kilobot (Kilobot plugin for ARGoS)
 A plugin to support the Kilobot robot (https://www.kilobotics.com/)
 into the ARGoS multi-robot simulator (http://www.argos-sim.info/).")
SET(CPACK_PACKAGE_DESCRIPTION_FILE "/usr/share/cmake-3.5/Templates/CPack.GenericDescription.txt")
SET(CPACK_PACKAGE_DESCRIPTION_SUMMARY "Kilobot support for ARGoS")
SET(CPACK_PACKAGE_FILE_NAME "argos3plugins_simulator_kilobot-..-x86_64-")
SET(CPACK_PACKAGE_HOMEPAGE "http://github.com/ilpincy/argos3-kilobot/")
SET(CPACK_PACKAGE_INSTALL_DIRECTORY "argos3plugins_simulator_kilobot ..")
SET(CPACK_PACKAGE_INSTALL_REGISTRY_KEY "argos3plugins_simulator_kilobot ..")
SET(CPACK_PACKAGE_MAINTAINER "Carlo Pinciroli <ilpincy@gmail.com>")
SET(CPACK_PACKAGE_NAME "argos3plugins_simulator_kilobot")
SET(CPACK_PACKAGE_RELEASE "")
SET(CPACK_PACKAGE_RELOCATABLE "true")
SET(CPACK_PACKAGE_VENDOR "Humanity")
SET(CPACK_PACKAGE_VERSION "..")
SET(CPACK_PACKAGE_VERSION_MAJOR "")
SET(CPACK_PACKAGE_VERSION_MINOR "")
SET(CPACK_PACKAGE_VERSION_PATCH "")
SET(CPACK_PACKAGING_INSTALL_PREFIX "/usr")
SET(CPACK_RESOURCE_FILE_LICENSE "/home/amaury/istc/NewCleanDirectory-real/src/../doc/ARGoS_LICENSE.txt")
SET(CPACK_RESOURCE_FILE_README "/home/amaury/istc/NewCleanDirectory-real/src/../README.md")
SET(CPACK_RESOURCE_FILE_WELCOME "/usr/share/cmake-3.5/Templates/CPack.GenericWelcome.txt")
SET(CPACK_RPM_PACKAGE_DESCRIPTION "ARGoS-Kilobot (Kilobot plugin for ARGoS)
 A plugin to support the Kilobot robot (https://www.kilobotics.com/)
 into the ARGoS multi-robot simulator (http://www.argos-sim.info/).")
SET(CPACK_RPM_PACKAGE_GROUP "Development/Tools")
SET(CPACK_RPM_PACKAGE_LICENSE "MIT")
SET(CPACK_RPM_PACKAGE_REQUIRES "argos3_simulator >= 3.0.0")
SET(CPACK_RPM_PACKAGE_URL "http://github.com/ilpincy/argos3-kilobot/")
SET(CPACK_SET_DESTDIR "OFF")
SET(CPACK_SOURCE_7Z "")
SET(CPACK_SOURCE_CYGWIN "")
SET(CPACK_SOURCE_GENERATOR "TBZ2;TGZ;TXZ;TZ")
SET(CPACK_SOURCE_OUTPUT_CONFIG_FILE "/home/amaury/istc/NewCleanDirectory-real/build/CPackSourceConfig.cmake")
SET(CPACK_SOURCE_TBZ2 "ON")
SET(CPACK_SOURCE_TGZ "ON")
SET(CPACK_SOURCE_TXZ "ON")
SET(CPACK_SOURCE_TZ "ON")
SET(CPACK_SOURCE_ZIP "OFF")
SET(CPACK_STRIP_FILES "ON")
SET(CPACK_SYSTEM_NAME "Linux")
SET(CPACK_TOPLEVEL_TAG "Linux")
SET(CPACK_WIX_SIZEOF_VOID_P "8")

if(NOT CPACK_PROPERTIES_FILE)
  set(CPACK_PROPERTIES_FILE "/home/amaury/istc/NewCleanDirectory-real/build/CPackProperties.cmake")
endif()

if(EXISTS ${CPACK_PROPERTIES_FILE})
  include(${CPACK_PROPERTIES_FILE})
endif()
