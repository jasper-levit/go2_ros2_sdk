# ROS 2 Jazzy on Ubuntu 24.04 (Noble) for Unitree Go2 WEBRTC
FROM ros:jazzy-ros-base

# Install basic requirements
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gnupg2 \
    lsb-release \
    python3-pip \
    python3.12-venv \
    portaudio19-dev \
    mesa-utils \
    libgl1 \
    libgl1-mesa-dri \
    ros-jazzy-rviz2 \
    ros-jazzy-sensor-msgs-py \
    ros-jazzy-slam-toolbox \
    ros-jazzy-nav2-bringup \
    software-properties-common \
    ros-jazzy-rmw-cyclonedds-cpp \
    ffmpeg

# Create venv to avoid conflicting with system Python packages (e.g. cryptography)
RUN python3 -m venv /opt/venv && . /opt/venv/bin/activate && \
    pip install --upgrade pip 'numpy<2.0.0'

# Create workspace
WORKDIR /ros2_ws

# Copy the repository (build context is repo root)
COPY . /ros2_ws/src

# Install Python requirements in venv (open3d skipped on arm64/Python 3.12 - optional for lidar map save only)
RUN . /opt/venv/bin/activate && cd src && \
    grep -v '^open3d' requirements.txt > /tmp/requirements_docker.txt && \
    pip install -r /tmp/requirements_docker.txt

# Install ROS dependencies (ignore failures for optional packages not yet in Jazzy)
RUN . /opt/ros/${ROS_DISTRO}/setup.sh && \
    rosdep update && \
    rosdep install --from-paths src --ignore-src -r -y || true

# Build the workspace
RUN . /opt/ros/${ROS_DISTRO}/setup.sh && \
    colcon build

# Source venv and ROS2 and workspace in bashrc
RUN echo "source /opt/venv/bin/activate" >> /root/.bashrc && \
    echo "source /opt/ros/${ROS_DISTRO}/setup.bash" >> /root/.bashrc && \
    echo "source /ros2_ws/install/setup.bash" >> /root/.bashrc

# Set environment variables for WEBRTC
ENV ROBOT_IP=""
ENV CONN_TYPE="webrtc"
ENV WEBRTC_SERVER_HOST="0.0.0.0"
ENV WEBRTC_SERVER_PORT="9991"

# Remove apt cache
RUN rm -rf /var/lib/apt/lists/*

# Add venv and workspace to the entrypoint so nodes use venv Python
RUN sed --in-place --expression \
      '$i. /opt/venv/bin/activate' \
      /ros_entrypoint.sh && \
    sed --in-place --expression \
      '$isource "/ros2_ws/install/setup.bash"' \
      /ros_entrypoint.sh

# Default: run minimal WEBRTC launch (driver + state publisher + camera + foxglove)
# Override with: docker compose run unitree_ros ros2 launch go2_robot_sdk robot.launch.py
CMD ["ros2", "launch", "go2_robot_sdk", "webrtc_web.launch.py"]
