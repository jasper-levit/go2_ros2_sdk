# ROS 2 Jazzy on Ubuntu 24.04 (Noble) for Unitree Go2 WEBRTC
# Workspace is bind-mounted at runtime (see docker-compose.yml); no COPY of repo.
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
    ros-jazzy-foxglove-bridge \
    software-properties-common \
    ros-jazzy-rmw-cyclonedds-cpp \
    ffmpeg \
    git

# Isolated venv: pip packages (aiortc, pydub, etc.) installed at runtime from mounted src/requirements.txt
RUN python3 -m venv /opt/venv && . /opt/venv/bin/activate && \
    pip install --upgrade pip 'numpy<2.0.0'

# Workspace dir; src will be bind-mounted here by compose
WORKDIR /ros2_ws

# Set environment variables for WEBRTC
ENV ROBOT_IP=""
ENV CONN_TYPE="webrtc"
ENV WEBRTC_SERVER_HOST="0.0.0.0"
ENV WEBRTC_SERVER_PORT="9991"

RUN rm -rf /var/lib/apt/lists/*

# Entrypoint and workspace setup (source, git, pip, colcon) live in scripts
COPY dev_env/setup_workspace.sh /setup_workspace.sh
COPY dev_env/entrypoint.sh /ros2_foxglove_entrypoint.sh
RUN chmod +x /setup_workspace.sh /ros2_foxglove_entrypoint.sh

# Also wire base ROS entrypoint for interactive shells
RUN sed --in-place --expression \
      '$i. /opt/venv/bin/activate' \
      /ros_entrypoint.sh && \
    sed --in-place --expression \
      '$i[ -f /ros2_ws/install/setup.bash ] && source /ros2_ws/install/setup.bash' \
      /ros_entrypoint.sh

RUN echo "source /opt/venv/bin/activate" >> /root/.bashrc && \
    echo "source /opt/ros/${ROS_DISTRO}/setup.bash" >> /root/.bashrc && \
    echo "[ -f /ros2_ws/install/setup.bash ] && source /ros2_ws/install/setup.bash" >> /root/.bashrc

ENTRYPOINT ["/ros2_foxglove_entrypoint.sh"]
CMD ["ros2", "launch", "go2_robot_sdk", "webrtc_web.launch.py", "enable_foxglove_bridge:=false", "enable_tts:=false"]
