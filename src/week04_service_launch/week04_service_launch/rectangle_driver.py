#!/usr/bin/env python3
"""4주차 강의 예제 — 서비스로 켜고 끄는 사각형 주행 노드.

  ros2 run ire_week04_service_launch circle_driver
  ros2 service call /start_stop std_srvs/srv/SetBool "{data: true}"
  ros2 param set /circle_driver speed 1.0
  ros2 param set /circle_driver turn 1.0
  ros2 param set /circle_driver forward_time 2.0
"""

import math

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_srvs.srv import SetBool


class RectangleDriver(Node):
    def __init__(self):
        super().__init__('rectangle_driver')

        # 기존 파라미터
        self.declare_parameter('speed', 1.0)      # 선속도 [m/s]
        self.declare_parameter('turn', 0.1)       # 각속도 [rad/s]

        # 추가 파라미터
        self.declare_parameter('forward_time', 2.0)  # 직진 시간 [s]

        # 주행 상태
        self.running = False

        # 사각형 주행 상태
        self.state = 'forward'
        self.state_start_time = None

        # Publisher
        self.pub = self.create_publisher(
            Twist,
            '/turtle1/cmd_vel',
            10
        )

        # Service
        self.srv = self.create_service(
            SetBool,
            'start_stop',
            self.on_call
        )

        # 0.001초마다 주행 상태 확인
        self.create_timer(0.001, self.on_timer)

    def on_call(self, req, res):
        self.running = req.data

        if self.running:
            # 시작할 때 직진 상태부터 시작
            self.state = 'forward'
            self.state_start_time = self.get_clock().now()
            res.message = 'running'
        else:
            # 정지
            self.state = 'forward'
            self.state_start_time = None
            res.message = 'stopped'

        res.success = True

        self.get_logger().info(res.message)

        return res

    def on_timer(self):
        if not self.running:
            return

        # 현재 상태가 시작된 후 경과한 시간
        now = self.get_clock().now()

        if self.state_start_time is None:
            self.state_start_time = now

        elapsed = (
            now - self.state_start_time
        ).nanoseconds / 1e9

        speed = self.get_parameter('speed').value
        turn = self.get_parameter('turn').value
        forward_time = self.get_parameter('forward_time').value

        msg = Twist()

        # -------------------------
        # 1. 직진
        # -------------------------
        if self.state == 'forward':

            msg.linear.x = speed
            msg.angular.z = 0.0

            if elapsed >= forward_time:
                self.state = 'turn'
                self.state_start_time = now

        # -------------------------
        # 2. 90도 회전
        # -------------------------
        elif self.state == 'turn':

            msg.linear.x = 0.0
            msg.angular.z = turn

            # 각속도 × 시간 = 회전각
            # 90도 = pi/2 rad
            turn_time = (math.pi / 2) / abs(turn)

            if elapsed >= turn_time:
                self.state = 'forward'
                self.state_start_time = now

        self.pub.publish(msg)


def main():
    rclpy.init()

    node = RectangleDriver()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        # 종료할 때 정지 명령
        msg = Twist()
        node.pub.publish(msg)

        node.destroy_node()


if __name__ == '__main__':
    main()
