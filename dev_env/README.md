# Unitree Go2 dev environment (ROS 2 Jazzy / Ubuntu 24.04)

Docker setup to connect to the Unitree Go2 robot via **WEBRTC** (Wi‑Fi). The container uses ROS 2 Jazzy on Ubuntu 24.04.

## Prerequisites

- Docker and the standalone **`docker-compose`** CLI (v2+, installed at `/usr/local/bin/docker-compose`)
- Robot on the same network in Wi‑Fi mode; close the Unitree mobile app before connecting

> [!NOTE]
> On the Jetson backpack the Docker installation does **not** include the `compose` plugin, so
> `docker compose` (space) will fail with *"docker: 'compose' is not a docker command"*.
> Always use `docker-compose` (hyphen) for every command on this machine.

## Quick start

1. Set the robot IP (from the app: Device → Data → STA Network: wlan0):

   ```bash
   export ROBOT_IP=192.168.123.161
   ```

2. Build and run:

   ```bash
   cd dev_env
   ROBOT_IP=$ROBOT_IP CONN_TYPE=webrtc docker-compose up --build
   ```

   Or use a `.env` file (copy from `.env.example` and set `ROBOT_IP`), then:

   ```bash
   docker-compose up --build
   ```

3. In another terminal, list topics to confirm connection to the dog:

   ```bash
   docker-compose exec unitree_ros ros2 topic list
   ```

   You should see topics such as `/joint_states`, `/imu`, `/camera/image_raw`, `/odom`, `/scan`, etc.

## Foxglove

**Foxglove Bridge** is installed and runs **in the background** when the container starts (port **8765**, bound to `0.0.0.0`). Connect from [Foxglove Studio](https://foxglove.dev/download) → Open Connection → Foxglove WebSocket → `ws://localhost:8765` (or `ws://<host-ip>:8765` from another machine).

### Test Foxglove from the host (no container shell)

To check that the bridge is listening **from your laptop or the host** (e.g. before opening Foxglove Studio):

```bash
# From the machine running Docker (use localhost)
python3 dev_env/scripts/test_foxglove_ws.py

# From another machine (use the Docker host IP, e.g. 100.125.51.31)
python3 dev_env/scripts/test_foxglove_ws.py 100.125.51.31
```

You should see `TCP: OK` and, if `websocket-client` is installed (`pip install websocket-client`), `WebSocket: OK`. If you see `TCP: FAIL`, the container may have crashed (e.g. main launch failed); check `docker-compose logs`.

## Verify WEBRTC connection

- Default command runs `webrtc_web.launch.py` (driver + state publisher + camera). Foxglove Bridge is already running in the background.
- To run the full stack (RViz, SLAM, Nav2, joystick), ensure `ROBOT_IP` is set (see Quick start step 1). From the **dev_env** directory run:

  ```bash
  docker-compose run unitree_ros ros2 launch go2_robot_sdk robot.launch.py
  ```

  (Compose passes `ROBOT_IP` from your environment or `.env` into the container.)

- To only list topics (after the main container is running):

  ```bash
  docker-compose exec unitree_ros ros2 topic list
  docker-compose exec unitree_ros ros2 topic echo /joint_states --once
  ```

## Options

| Variable              | Default   | Description                    |
|-----------------------|-----------|--------------------------------|
| `ROBOT_IP`            | (required)| Robot IP address               |
| `CONN_TYPE`           | `webrtc`  | `webrtc` (Wi‑Fi) or `cyclonedds` (Ethernet) |
| `WEBRTC_SERVER_PORT`  | `9991`    | WEBRTC server port             |

## Notes

- `network_mode: host` is used so the container can discover the robot and ROS 2 nodes on the host.
- Foxglove Bridge is started by the container entrypoint (`ros2 launch foxglove_bridge foxglove_bridge_launch.xml port:=8765`) before the main launch file.
- For GUI (RViz), ensure `DISPLAY` is set and X11 forwarding is allowed (`xhost +local:docker` if needed).
- **open3d** is not installed in this image (no wheel for arm64/Python 3.12). Lidar pointcloud and 3D map save in `lidar_processor` require open3d on the host or an amd64 image if you need that feature.
