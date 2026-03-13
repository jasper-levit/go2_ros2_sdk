#!/bin/bash
# Git config, rosdep, and colcon build for bind-mounted workspace.
# Python venv is created by .devcontainer/install.sh (uv). Expects /ros2_ws/src to be bind-mounted.
set -e

[ -f /opt/venv/bin/activate ] && . /opt/venv/bin/activate
source /opt/ros/${ROS_DISTRO}/setup.bash
export PYTHONPATH=/opt/venv/lib/python3.12/site-packages${PYTHONPATH:+:}${PYTHONPATH}

SRC=/ros2_ws/src
if [ ! -d "$SRC" ] || [ ! -f "$SRC/requirements.txt" ]; then
  echo "ERROR: Bind-mount repo root at /ros2_ws/src (see dev_env/README.md)"
  exit 1
fi

git config --global --add safe.directory "$SRC" 2>/dev/null || true
(cd "$SRC" && git submodule update --init --recursive)

if [ ! -f /ros2_ws/install/setup.bash ]; then
  apt-get update -qq && (cd /ros2_ws && rosdep update && rosdep install --from-paths src --ignore-src -r -y) || true
  (cd /ros2_ws && env -i HOME=/root ROS_DISTRO=${ROS_DISTRO} bash -c "source /opt/ros/\$ROS_DISTRO/setup.bash && colcon build")
fi

source /ros2_ws/install/setup.bash
