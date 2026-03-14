#!/bin/bash
# Rosdep, colcon build for workspace (venv is created in image).
# Workspace root is /workspaces/levit_unitree. Run from postCreateCommand or manually.
set -e
WS=/workspaces/levit_unitree
SRC=$WS/src

if [ ! -d "$SRC" ] || [ ! -f "$WS/requirements.txt" ]; then
  echo "ERROR: Workspace must have src/ and requirements.txt under $WS (see dev_env/README.md)"
  exit 1
fi

cd "$WS"
echo "Building workspace"

echo "Checking venv"
[ -f /opt/venv/bin/activate ] && . /opt/venv/bin/activate
echo "Sourcing ROS"
source /opt/ros/${ROS_DISTRO}/setup.bash
echo "Setting PYTHONPATH"
export PYTHONPATH=/opt/venv/lib/python3.12/site-packages${PYTHONPATH:+:}${PYTHONPATH}

echo "Updating submodules"
git submodule update --init --recursive

echo "Installing dependencies"
rosdep install --from-paths src --ignore-src -r -y

echo "Building workspace"
colcon build

source "$WS/install/setup.bash"
