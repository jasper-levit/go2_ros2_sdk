#!/usr/bin/env python3
"""Save current map to .yaml and .pgm (replaces RViz Save Map)."""

import argparse
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from slam_toolbox.srv import SaveMap


def main():
    parser = argparse.ArgumentParser(description="Save map to .yaml and .pgm")
    parser.add_argument("name", help="Path or basename for the map (e.g. map_1 or /ros2_ws/map_1)")
    args = parser.parse_args()

    rclpy.init()
    node = Node("save_map")
    client = node.create_client(SaveMap, "/slam_toolbox/save_map")
    if not client.wait_for_service(timeout_sec=10.0):
        node.get_logger().error("Service /slam_toolbox/save_map not available")
        rclpy.shutdown()
        return 1
    req = SaveMap.Request()
    req.name = String(data=args.name)
    future = client.call_async(req)
    rclpy.spin_until_future_complete(node, future)
    node.destroy_node()
    rclpy.shutdown()
    if future.result() is not None and future.result().result == 0:
        print("Map saved.")
        return 0
    print("Save map failed.")
    return 1


if __name__ == "__main__":
    exit(main())
