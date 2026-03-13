#!/bin/bash
# Rosdep, colcon build for bind-mounted workspace (venv is created in image).
# Expects /ros2_ws/src to be bind-mounted. Run from postCreateCommand or manually.
set -e

SRC=/ros2_ws/src

if [ ! -d "$SRC" ] || [ ! -f "$SRC/requirements.txt" ]; then
  echo "ERROR: Bind-mount repo root at /ros2_ws/src (see dev_env/README.md)"
  exit 1
fi

[ -f /opt/venv/bin/activate ] && . /opt/venv/bin/activate
source /opt/ros/${ROS_DISTRO}/setup.bash
export PYTHONPATH=/opt/venv/lib/python3.12/site-packages${PYTHONPATH:+:}${PYTHONPATH}

(cd "$SRC" && git submodule update --init --recursive)

if [ ! -f /ros2_ws/install/setup.bash ]; then
  (cd /ros2_ws && rosdep install --from-paths src --ignore-src -r -y) || true
  (cd /ros2_ws && env -i HOME=/root ROS_DISTRO=${ROS_DISTRO} bash -c "source /opt/ros/\$ROS_DISTRO/setup.bash && colcon build")
fi

source /ros2_ws/install/setup.bash
