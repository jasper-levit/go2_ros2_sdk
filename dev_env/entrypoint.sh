#!/bin/bash
# Container entrypoint: setup workspace, start Foxglove bridge, exec user command.
set -e

/setup_workspace.sh

ros2 launch foxglove_bridge foxglove_bridge_launch.xml port:=8765 address:=0.0.0.0 &
sleep 2
exec "$@"
