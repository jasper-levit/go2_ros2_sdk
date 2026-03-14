cmake_minimum_required(VERSION 3.8)
project(unitree_api)

if(POLICY CMP0148)
  cmake_policy(SET CMP0148 OLD)
endif()

find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/Request.msg"
  "msg/Response.msg"
)

ament_package()
