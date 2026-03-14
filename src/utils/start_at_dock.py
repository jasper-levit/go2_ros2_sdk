#!/usr/bin/env python3
"""Clear slam_toolbox pose graph so the next scan starts at dock (replaces RViz Start At Dock)."""

import rclpy
from rclpy.node import Node
from std_srvs.srv import Empty


def main():
    rclpy.init()
    node = Node("start_at_dock")
    client = node.create_client(Empty, "/slam_toolbox/clear")
    if not client.wait_for_service(timeout_sec=10.0):
        node.get_logger().error("Service /slam_toolbox/clear not available")
        rclpy.shutdown()
        return 1
    req = Empty.Request()
    future = client.call_async(req)
    rclpy.spin_until_future_complete(node, future)
    node.destroy_node()
    rclpy.shutdown()
    if future.result() is not None:
        print("Map cleared; next scan starts at dock.")
        return 0
    print("Clear failed.")
    return 1


if __name__ == "__main__":
    exit(main())
