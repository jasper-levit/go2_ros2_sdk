# Copyright (c) 2024, RoboVerse community
# SPDX-License-Identifier: BSD-3-Clause

"""
Minimal test node that subscribes to a PointCloud2 topic from the robot,
decodes the message, and logs that the data can be read.
Requires: ros-$ROS_DISTRO-sensor-msgs-py
"""

from typing import List, Tuple

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSHistoryPolicy
from sensor_msgs.msg import PointCloud2
from sensor_msgs_py import point_cloud2


def _read_points(msg: PointCloud2) -> List[Tuple[float, float, float]]:
    """Decode PointCloud2 using sensor_msgs_py."""
    gen = point_cloud2.read_points(
        msg, field_names=('x', 'y', 'z'), skip_nans=True
    )
    return [(p[0], p[1], p[2]) for p in gen]


class PointcloudTestNode(Node):
    """Subscribes to PointCloud2, decodes and logs that data is visible."""

    def __init__(self):
        super().__init__('pointcloud_test_node')
        self.declare_parameter('topic', 'point_cloud2')
        self.declare_parameter('log_every_n', 10)  # log summary every N messages
        topic = self.get_parameter('topic').get_parameter_value().string_value
        self._log_every_n = self.get_parameter('log_every_n').get_parameter_value().integer_value
        self._count = 0

        qos = QoSProfile(
            reliability=QoSReliabilityPolicy.BEST_EFFORT,
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=1,
        )
        self._sub = self.create_subscription(
            PointCloud2,
            topic,
            self._callback,
            qos,
        )
        self.get_logger().info(f'Subscribed to {topic}, waiting for PointCloud2 messages...')

    def _callback(self, msg: PointCloud2) -> None:
        self._count += 1
        try:
            points = _read_points(msg)
        except Exception as e:
            self.get_logger().error(f'Decode failed: {e}')
            return

        n = len(points)
        if n == 0:
            self.get_logger().warn('Decoded 0 points (empty or all NaN)')
            return

        if self._count % self._log_every_n != 1 and self._count > 1:
            return

        # Show that data is visible: bounds and sample
        xs = [p[0] for p in points]
        ys = [p[1] for p in points]
        zs = [p[2] for p in points]
        x_min, x_max = min(xs), max(xs)
        y_min, y_max = min(ys), max(ys)
        z_min, z_max = min(zs), max(zs)
        frame = msg.header.frame_id
        stamp = msg.header.stamp

        self.get_logger().info(
            f'PointCloud2 OK | frame={frame} | stamp={stamp.sec}.{stamp.nanosec:09d} | '
            f'points={n} | x=[{x_min:.2f}, {x_max:.2f}] y=[{y_min:.2f}, {y_max:.2f}] '
            f'z=[{z_min:.2f}, {z_max:.2f}] | sample=({points[0][0]:.3f}, {points[0][1]:.3f}, {points[0][2]:.3f})'
        )


def main(args=None):
    rclpy.init(args=args)
    node = PointcloudTestNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
