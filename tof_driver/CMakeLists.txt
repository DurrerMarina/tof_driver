cmake_minimum_required(VERSION 2.8.3)
project(tof_driver)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  message_generation
  std_msgs
)

catkin_python_setup()

## Generate messages in the 'msg' folder
# add_message_files(
#   FILES
#   Message1.msg
#   Message2.msg
# )

## Generate services in the 'srv' folder
add_service_files(
  FILES
  SetToFState.srv
)

## Generate added messages and services with any dependencies listed here
generate_messages(
 DEPENDENCIES
 message_generation
)

catkin_package()


include_directories(
  ${catkin_INCLUDE_DIRS}
)
