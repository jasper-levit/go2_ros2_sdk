#!/bin/bash
# Rosdep, colcon build for bind-mounted workspace (venv is created in image).
# Expects /ros2_ws/src to be bind-mounted. Run from postCreateCommand or manually.
set -e
echo "Building workspace"

SRC=/ros2_ws/src

if [ ! -d "$SRC" ] || [ ! -f "$SRC/requirements.txt" ]; then
  echo "ERROR: Bind-mount repo root at /ros2_ws/src (see dev_env/README.md)"
  exit 1
fi

echo "Checking venv"
[ -f /opt/venv/bin/activate ] && . /opt/venv/bin/activate
echo "Sourcing ROS"
source /opt/ros/${ROS_DISTRO}/setup.bash
echo "Setting PYTHONPATH"
export PYTHONPATH=/opt/venv/lib/python3.12/site-packages${PYTHONPATH:+:}${PYTHONPATH}

echo "Updating submodules"
(cd "$SRC" && git submodule update --init --recursive)

echo "Installing dependencies"
rosdep install --from-paths src --ignore-src -r -y

echo "Building workspace"
colcon build

source /ros2_ws/install/setup.bash
