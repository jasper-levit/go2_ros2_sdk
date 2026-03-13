#!/bin/bash
# Create Python venv with uv and install deps from repo requirements.txt.
# Run once after container is created (postCreateCommand).
set -e

SRC=/ros2_ws/src
REQ="$SRC/requirements.txt"

if [ ! -f "$REQ" ]; then
  echo "ERROR: $REQ not found (workspace not mounted?)"
  exit 1
fi

# Filter out open3d (no arm64/Python 3.12 wheel in this image)
grep -v "^open3d" "$REQ" > /tmp/requirements_uv.txt || true

# Create venv and install with uv (uses cache at /root/.cache/uv when mounted)
uv venv /opt/venv --python python3
uv pip install --python /opt/venv/bin/python -r /tmp/requirements_uv.txt

echo "uv venv ready at /opt/venv"
