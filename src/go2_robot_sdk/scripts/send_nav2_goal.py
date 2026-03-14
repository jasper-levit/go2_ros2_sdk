#!/usr/bin/env python3
"""
Send a Nav2 goal ~2 m in front of the current robot pose (in map frame).

Usage:
  # Send one goal and exit (with ROS 2 sourced and launch running):
  python3 send_nav2_goal.py

  # Interactive: send one goal then drop to REPL (e.g. to call send_nav2_goal(1.5) again):
  python3 -i send_nav2_goal.py

Requires: ROS 2 sourced, robot launch running (Nav2 + SLAM so map->base_link exists).

If you see "No module named 'yaml'", use system Python (venv often lacks PyYAML):
  unset VIRTUAL_ENV && source /opt/ros/jazzy/setup.bash && source install/setup.bash
  /usr/bin/python3 src/go2_robot_sdk/scripts/send_nav2_goal.py
"""

import math
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from geometry_msgs.msg import PoseStamped
from nav2_msgs.action import NavigateToPose
from tf2_ros import Buffer, TransformListener
from tf2_ros import LookupException, ConnectivityException, ExtrapolationException


def quaternion_to_yaw(q):
    """Extract yaw (rotation around z) from a geometry_msgs Quaternion."""
    siny_cosp = 2.0 * (q.w * q.z + q.x * q.y)
    cosy_cosp = 1.0 - 2.0 * (q.y * q.y + q.z * q.z)
    return math.atan2(siny_cosp, cosy_cosp)


def send_nav2_goal(distance_m=2.0, action_name='navigate_to_pose', wait_for_server_timeout=10.0):
    """
    Get current robot pose in map frame, compute a goal distance_m ahead,
    and send it to the Nav2 navigate_to_pose action.

    Args:
        distance_m: Distance in meters from current pose to goal (default 2.0).
        action_name: Nav2 action name (default 'navigate_to_pose').
        wait_for_server_timeout: Seconds to wait for action server (default 10.0).

    Returns:
        True if goal was sent and accepted, False otherwise.
    """
    rclpy.init()
    node = Node('send_nav2_goal_node')
    tf_buffer = Buffer()
    tf_listener = TransformListener(tf_buffer, node)

    try:
        # Wait for map -> base_link
        node.get_logger().info('Waiting for transform map -> base_link...')
        trans = tf_buffer.lookup_transform(
            'map', 'base_link', rclpy.time.Time(), rclpy.duration.Duration(seconds=5)
        )
    except (LookupException, ConnectivityException, ExtrapolationException) as e:
        node.get_logger().error(f'Could not get transform map -> base_link: {e}')
        rclpy.shutdown()
        return False

    # Current pose in map
    x = trans.transform.translation.x
    y = trans.transform.translation.y
    z = trans.transform.translation.z
    q = trans.transform.rotation
    yaw = quaternion_to_yaw(q)
    forward_x = math.cos(yaw)
    forward_y = math.sin(yaw)

    # Goal: distance_m in front of robot
    goal_x = x + distance_m * forward_x
    goal_y = y + distance_m * forward_y

    pose = PoseStamped()
    pose.header.frame_id = 'map'
    pose.header.stamp = node.get_clock().now().to_msg()
    pose.pose.position.x = goal_x
    pose.pose.position.y = goal_y
    pose.pose.position.z = z
    pose.pose.orientation = q

    node.get_logger().info(
        f'Current (map): ({x:.2f}, {y:.2f}); goal ({distance_m}m ahead): ({goal_x:.2f}, {goal_y:.2f})'
    )

    # Send via NavigateToPose action
    action_client = ActionClient(node, NavigateToPose, action_name)
    if not action_client.wait_for_server(timeout_sec=wait_for_server_timeout):
        node.get_logger().error(f'Action server {action_name} not available.')
        rclpy.shutdown()
        return False

    goal_msg = NavigateToPose.Goal()
    goal_msg.pose = pose
    future = action_client.send_goal_async(goal_msg)

    rclpy.spin_until_future_complete(node, future, timeout_sec=5.0)
    if not future.done():
        node.get_logger().error('Send goal timed out.')
        rclpy.shutdown()
        return False

    result_handle = future.result()
    if not result_handle.accepted:
        node.get_logger().error('Goal rejected.')
        rclpy.shutdown()
        return False

    node.get_logger().info('Goal sent and accepted. Nav2 is navigating.')
    rclpy.shutdown()
    return True


if __name__ == '__main__':
    send_nav2_goal(distance_m=2.0)
