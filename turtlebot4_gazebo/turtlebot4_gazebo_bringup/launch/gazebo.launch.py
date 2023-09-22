# Copyright 2023 Clearpath Robotics, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# @author Roni Kreinin (rkreinin@clearpathrobotics.com)

import os

from pathlib import Path

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node


ARGUMENTS = [
    DeclareLaunchArgument('use_sim_time', default_value='true',
                          choices=['true', 'false'],
                          description='use_sim_time'),
    DeclareLaunchArgument('world', default_value='cafe',
                          description='Gazebo World'),
    DeclareLaunchArgument('model', default_value='lite',
                          choices=['standard', 'lite'],
                          description='Turtlebot4 Model'),
]


def generate_launch_description():

    # Directories
    pkg_turtlebot4_gazebo_bringup = get_package_share_directory(
        'turtlebot4_gazebo_bringup')
    pkg_turtlebot4_gazebo_gui_plugins = get_package_share_directory(
        'turtlebot4_gazebo_gui_plugins')
    pkg_turtlebot4_description = get_package_share_directory(
        'turtlebot4_description')
    pkg_irobot_create_description = get_package_share_directory(
        'irobot_create_description')
    pkg_irobot_create_gazebo_bringup = get_package_share_directory(
        'irobot_create_gazebo_bringup')
    pkg_irobot_create_gazebo_plugins = get_package_share_directory(
        'irobot_create_gazebo_plugins')
    pkg_gazebo_ros = get_package_share_directory('gazebo_ros')
    #world_file_name = 'turtlebot3_worlds/' + TURTLEBOT3_MODEL + '.model'
    world = [pkg_turtlebot4_gazebo_bringup,'/worlds/', LaunchConfiguration('world'),'.world']

    # # Set Gazebo resource path
    # gazebo_resource_path = SetEnvironmentVariable(
    #     name='GAZEBO_RESOURCE_PATH',
    #     value=[
    #         os.path.join(pkg_turtlebot4_gazebo_bringup, 'worlds'), ':' +
    #         os.path.join(pkg_irobot_create_gazebo_bringup, 'worlds'), ':' +
    #         str(Path(pkg_turtlebot4_description).parent.resolve()), ':' +
    #         str(Path(pkg_irobot_create_description).parent.resolve())])

    # gazebo_gui_plugin_path = SetEnvironmentVariable(
    #     name='GAZEBO_GUI_PLUGIN_PATH',
    #     value=[
    #         os.path.join(pkg_turtlebot4_gazebo_gui_plugins, 'lib'), ':' +
    #         os.path.join(pkg_irobot_create_gazebo_plugins, 'lib')])

    # Gazebo
    gzserver_launch = IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(pkg_gazebo_ros, 'launch', 'gzserver.launch.py')
            ),
            #launch_arguments={'verbose': 'true'}.items(),
            launch_arguments={'world': world,'verbose': 'true'}.items(),
        )

    gzclient_launch = IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(pkg_gazebo_ros, 'launch', 'gzclient.launch.py')
            ),
        )

    # Create launch description and add actions
    ld = LaunchDescription(ARGUMENTS)
    # ld.add_action(gazebo_resource_path)
    # ld.add_action(gazebo_gui_plugin_path)
    ld.add_action(gzserver_launch)
    ld.add_action(gzclient_launch) 
    return ld
