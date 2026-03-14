cmake_minimum_required(VERSION 3.8)
project(unitree_go)

# Ensure include dir exists before rosidl install (workaround for duplicate unitree_go path)
install(CODE "file(MAKE_DIRECTORY \"${CMAKE_INSTALL_PREFIX}/include/unitree_go/unitree_go/msg/detail\")")

if(POLICY CMP0148)
  cmake_policy(SET CMP0148 OLD)
endif()

find_package(ament_cmake REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(rosidl_default_generators REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/IMU.msg"
  "msg/AudioData.msg"
  "msg/BmsCmd.msg"
  "msg/BmsState.msg"
  "msg/ConfigChangeStatus.msg"
  "msg/Error.msg"
  "msg/Go2FrontVideoData.msg"
  "msg/HeightMap.msg"
  "msg/InterfaceConfig.msg"
  "msg/LidarState.msg"
  "msg/LowCmd.msg"
  "msg/LowState.msg"
  "msg/MotorCmd.msg"
  "msg/MotorCmds.msg"
  "msg/MotorState.msg"
  "msg/MotorStates.msg"
  "msg/PathPoint.msg"
  "msg/SportModeCmd.msg"
  "msg/SportModeState.msg"
  "msg/TimeSpec.msg"
  "msg/UwbState.msg"
  "msg/UwbSwitch.msg"
  "msg/VoxelMapCompressed.msg"
  "msg/VoxelHeightMapState.msg"
  "msg/WebRtcReq.msg"
  "msg/WirelessController.msg"
  DEPENDENCIES geometry_msgs
)

ament_package()
