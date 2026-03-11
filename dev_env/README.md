# Unitree Go2 dev environment (ROS 2 Jazzy / Ubuntu 24.04)

Docker setup to connect to the Unitree Go2 robot via **WEBRTC** (Wi‑Fi). The container uses ROS 2 Jazzy on Ubuntu 24.04.

## Prerequisites

- Docker and Docker Compose
- Robot on the same network in Wi‑Fi mode; close the Unitree mobile app before connecting

## Quick start

1. Set the robot IP (from the app: Device → Data → STA Network: wlan0):

   ```bash
   export ROBOT_IP=192.168.123.161
   ```

2. Build and run:

   ```bash
   cd dev_env
   ROBOT_IP=$ROBOT_IP CONN_TYPE=webrtc docker compose up --build
   ```

   Or use a `.env` file (copy from `.env.example` and set `ROBOT_IP`), then:

   ```bash
   docker compose up --build
   ```

3. In another terminal, list topics to confirm connection to the dog:

   ```bash
   docker compose exec unitree_ros ros2 topic list
   ```

   You should see topics such as `/joint_states`, `/imu`, `/camera/image_raw`, `/odom`, `/scan`, etc.

## Verify WEBRTC connection

- Default command runs `webrtc_web.launch.py` (driver + state publisher + camera + Foxglove).
- To run the full stack (RViz, SLAM, Nav2, joystick):

  ```bash
  docker compose run -e ROBOT_IP=$ROBOT_IP unitree_ros ros2 launch go2_robot_sdk robot.launch.py
  ```

- To only list topics (after the main container is running):

  ```bash
  docker compose exec unitree_ros ros2 topic list
  docker compose exec unitree_ros ros2 topic echo /joint_states --once
  ```

## Options

| Variable              | Default   | Description                    |
|-----------------------|-----------|--------------------------------|
| `ROBOT_IP`            | (required)| Robot IP address               |
| `CONN_TYPE`           | `webrtc`  | `webrtc` (Wi‑Fi) or `cyclonedds` (Ethernet) |
| `WEBRTC_SERVER_PORT`  | `9991`    | WEBRTC server port             |

## Notes

- `network_mode: host` is used so the container can discover the robot and ROS 2 nodes on the host.
- For GUI (RViz), ensure `DISPLAY` is set and X11 forwarding is allowed (`xhost +local:docker` if needed).
- **open3d** is not installed in this image (no wheel for arm64/Python 3.12). Lidar pointcloud and 3D map save in `lidar_processor` require open3d on the host or an amd64 image if you need that feature.
