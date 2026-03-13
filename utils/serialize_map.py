#!/usr/bin/env python3
"""Serialize pose graph to .posegraph and .data (replaces RViz Serialize Map)."""

import argparse
import rclpy
from rclpy.node import Node
from slam_toolbox.srv import SerializePoseGraph


def main():
    parser = argparse.ArgumentParser(description="Serialize pose graph to .posegraph and .data")
    parser.add_argument("filename", help="Filename without extension (e.g. map_1)")
    args = parser.parse_args()

    rclpy.init()
    node = Node("serialize_map")
    client = node.create_client(SerializePoseGraph, "/slam_toolbox/serialize_map")
    if not client.wait_for_service(timeout_sec=10.0):
        node.get_logger().error("Service /slam_toolbox/serialize_map not available")
        rclpy.shutdown()
        return 1
    req = SerializePoseGraph.Request()
    req.filename = args.filename
    future = client.call_async(req)
    rclpy.spin_until_future_complete(node, future)
    node.destroy_node()
    rclpy.shutdown()
    if future.result() is not None and future.result().result == 0:
        print("Pose graph serialized.")
        return 0
    print("Serialize failed.")
    return 1


if __name__ == "__main__":
    exit(main())
