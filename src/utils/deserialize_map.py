#!/usr/bin/env python3
"""Load a saved map for localization/continued mapping (replaces RViz Deserialize Map)."""

import argparse
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Pose2D
from slam_toolbox.srv import DeserializePoseGraph

LOCALIZE_AT_POSE = 3


def main():
    parser = argparse.ArgumentParser(description="Deserialize pose graph from .posegraph/.data")
    parser.add_argument("filename", help="Filename without extension (e.g. map_1)")
    parser.add_argument("--x", type=float, default=0.0, help="Initial pose x (default 0)")
    parser.add_argument("--y", type=float, default=0.0, help="Initial pose y (default 0)")
    parser.add_argument("--theta", type=float, default=0.0, help="Initial pose theta rad (default 0)")
    args = parser.parse_args()

    rclpy.init()
    node = Node("deserialize_map")
    client = node.create_client(DeserializePoseGraph, "/slam_toolbox/deserialize_map")
    if not client.wait_for_service(timeout_sec=10.0):
        node.get_logger().error("Service /slam_toolbox/deserialize_map not available")
        rclpy.shutdown()
        return 1
    req = DeserializePoseGraph.Request()
    req.filename = args.filename
    req.match_type = LOCALIZE_AT_POSE
    req.initial_pose = Pose2D(x=args.x, y=args.y, theta=args.theta)
    future = client.call_async(req)
    rclpy.spin_until_future_complete(node, future)
    node.destroy_node()
    rclpy.shutdown()
    if future.result() is not None:
        print("Map deserialized.")
        return 0
    print("Deserialize failed.")
    return 1


if __name__ == "__main__":
    exit(main())
