cmake_minimum_required(VERSION 3.8)
project(turtlebot4_gazebo)
find_package(ament_cmake REQUIRED)
add_subdirectory(turtlebot4_gazebo_bringup)
add_subdirectory(turtlebot4_gazebo_gui_plugins)
add_subdirectory(turtlebot4_gazebo_toolbox)
ament_package()
