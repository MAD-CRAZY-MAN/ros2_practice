from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(package='turtlesim', executable='turtlesim_node'),


        Node(package='week04_service_launch',
             executable='rectangle_driver',
             parameters=[{'speed': 1.0, 'turn': 1.0, 'forward_time': 2.0}]),
    ])