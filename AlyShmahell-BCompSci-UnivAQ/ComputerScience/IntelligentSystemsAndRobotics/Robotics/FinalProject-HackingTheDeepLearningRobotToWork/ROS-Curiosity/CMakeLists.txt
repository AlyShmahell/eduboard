cmake_minimum_required(VERSION 2.8.3)
project(curiosity)

find_package(catkin REQUIRED COMPONENTS message_generation nav_msgs geometry_msgs roscpp rospy)

add_message_files(FILES LandMarkDistance.msg)

generate_messages(DEPENDENCIES)

catkin_package(CATKIN_DEPENDS message_runtime nav_msgs geometry_msgs roscpp rospy)

include_directories(${catkin_INCLUDE_DIRS})

add_executable(curiosity ./src/curiosity.cpp)

add_dependencies(curiosity ${${PROJECT_NAME}_EXPORTED_TARGETS} ${catkin_EXPORTED_TARGETS})

target_link_libraries(curiosity ${catkin_LIBRARIES})

