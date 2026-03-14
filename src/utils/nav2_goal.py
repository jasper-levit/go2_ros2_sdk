#!/usr/bin/env python3
"""Send a Nav2 navigation goal (replaces RViz Nav2 Goal)."""

import argparse
import math
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from geometry_msgs.msg import PoseStamped, Quaternion
from nav2_msgs.action import NavigateToPose


def yaw_to_quaternion(yaw):
    return Quaternion(
        x=0.0, y=0.0, z=math.sin(yaw / 2.0), w=math.cos(yaw / 2.0)
    )


def main():
    parser = argparse.ArgumentParser(description="Send Nav2 goal pose")
    parser.add_argument("x", type=float, help="Goal x in map frame")
    parser.add_argument("y", type=float, help="Goal y in map frame")
    parser.add_argument("yaw", type=float, nargs="?", default=0.0, help="Goal yaw radians (default 0)")
    parser.add_argument("--yaw-deg", type=float, dest="yaw_deg", default=None, help="Goal yaw in degrees (overrides yaw)")
    args = parser.parse_args()
    yaw = math.radians(args.yaw_deg) if args.yaw_deg is not None else args.yaw

    rclpy.init()
    node = Node("nav2_goal")
    client = ActionClient(node, NavigateToPose, "navigate_to_pose")
    if not client.wait_for_server(timeout_sec=10.0):
        node.get_logger().error("Action navigate_to_pose not available")
        rclpy.shutdown()
        return 1
    goal_msg = NavigateToPose.Goal()
    goal_msg.pose = PoseStamped()
    goal_msg.pose.header.frame_id = "map"
    goal_msg.pose.header.stamp = node.get_clock().now().to_msg()
    goal_msg.pose.pose.position.x = args.x
    goal_msg.pose.pose.position.y = args.y
    goal_msg.pose.pose.position.z = 0.0
    goal_msg.pose.pose.orientation = yaw_to_quaternion(yaw)
    future = client.send_goal_async(goal_msg)
    rclpy.spin_until_future_complete(node, future)
    if not future.result().accepted:
        node.get_logger().error("Goal rejected")
        node.destroy_node()
        rclpy.shutdown()
        return 1
    result_future = future.result().get_result_async()
    rclpy.spin_until_future_complete(node, result_future)
    node.destroy_node()
    rclpy.shutdown()
    result = result_future.result().result
    if result is not None and result.error_code == 0:
        print("Nav2 goal succeeded.")
        return 0
    print("Nav2 goal failed.")
    return 1


if __name__ == "__main__":
    exit(main())
