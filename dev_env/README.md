# Unitree Go2 dev environment (ROS 2 Jazzy / Ubuntu 24.04)

**Dev container** setup to connect to the Unitree Go2 robot via **WEBRTC** (Wi‑Fi). The container uses ROS 2 Jazzy on Ubuntu 24.04. The repo is bind-mounted at `/ros2_ws/src`, so you edit code and config on the host and see changes inside the container.

- **Python**: [uv](https://docs.astral.sh/uv/) is installed in the image; the virtualenv at `/opt/venv` is created by `build_workspace.sh` (run via `postCreateCommand` or manually). A **uv cache** volume is mounted to speed up installs.
- **No Docker Compose**: use “Reopen in Container” (or `devcontainer build` / `devcontainer run`) instead.

## Prerequisites

- Docker
- VS Code or Cursor with the **Dev Containers** extension (e.g. “Dev Containers” by Microsoft)
- Robot on the same network in Wi‑Fi mode; close the Unitree mobile app before connecting

## Quick start

1. Open the repo in VS Code/Cursor and run **“Dev Containers: Reopen in Container”** (or from CLI: `devcontainer up` from the repo root). The first time, the image will build, then `build_workspace.sh` creates the uv venv and runs rosdep and colcon build.

2. Set the robot IP (from the app: Device → Data → STA Network: wlan0):

   ```bash
   export ROBOT_IP=192.168.123.161
   ```

3. From the container terminal (e.g. at `/ros2_ws`):

   ```bash
   source /ros2_ws/install/setup.bash
   ros2 launch go2_robot_sdk webrtc_web.launch.py enable_foxglove_bridge:=false enable_tts:=false
   ```

   Or run the full stack (RViz, SLAM, Nav2, joystick):

   ```bash
   ros2 launch go2_robot_sdk robot.launch.py
   ```

4. In another terminal (inside or outside the container), list topics:

   ```bash
   ros2 topic list
   ```

   You should see `/joint_states`, `/imu`, `/camera/image_raw`, `/odom`, `/scan`, etc.

## Foxglove

**Foxglove Bridge** is installed but not started automatically. To run it in the background:

```bash
ros2 launch foxglove_bridge foxglove_bridge_launch.xml port:=8765 address:=0.0.0.0 &
```

Then connect from [Foxglove Studio](https://foxglove.dev/download) → Open Connection → Foxglove WebSocket → `ws://localhost:8765` (or `ws://<host-ip>:8765` from another machine).

### Test Foxglove from the host

```bash
# From the machine running the dev container (use localhost)
python3 dev_env/scripts/test_foxglove_ws.py

# From another machine (use the dev container host IP)
python3 dev_env/scripts/test_foxglove_ws.py <host_ip>
```

## Options

| Variable              | Default   | Description                    |
|-----------------------|-----------|--------------------------------|
| `ROBOT_IP`            | (required)| Robot IP address               |
| `CONN_TYPE`           | `webrtc`  | `webrtc` (Wi‑Fi) or `cyclonedds` (Ethernet) |
| `WEBRTC_SERVER_PORT`  | `9991`    | WEBRTC server port             |

You can set `ROBOT_IP` (and optionally others) in `.env` or in the dev container’s `remoteEnv` in `.devcontainer/devcontainer.json`.

## Rebuild workspace

After adding packages or changing Python/C++ code:

```bash
/build_workspace.sh
# or manually:
cd /ros2_ws && colcon build && source install/setup.bash
```

For a clean build, remove `build` and `install` under `/ros2_ws` and run `build_workspace.sh` again.

## Notes

- **uv cache**: The dev container mounts a Docker volume at `/root/.cache/uv` to persist uv’s cache and speed up `uv pip install` in `install.sh` and future runs.
- **Network**: The container runs with `--network=host` so it can discover the robot and ROS 2 nodes on the host.
- **GUI (RViz)**: Ensure `DISPLAY` is set and X11 is allowed (`xhost +local:docker` if needed). You may need to forward DISPLAY in `.devcontainer/devcontainer.json` or your environment.
- **open3d**: Not installed in this image (no arm64/Python 3.12 wheel). Lidar pointcloud and 3D map save in `lidar_processor` require open3d on the host or an amd64 image if you need that feature.
