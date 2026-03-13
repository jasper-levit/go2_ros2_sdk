# ROS 2 Jazzy on Ubuntu 24.04 (Noble) for Unitree Go2 WEBRTC
# Used by dev container; workspace is bind-mounted at runtime.
FROM ros:jazzy-ros-base

# Install basic requirements
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gnupg2 \
    lsb-release \
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

# Install uv (venv is created in .devcontainer/install.sh)
RUN curl -LsSf https://astral.sh/uv/install.sh | sh && \
    mv /root/.local/bin/uv /usr/local/bin/uv

# Workspace dir; src is bind-mounted here by dev container
WORKDIR /ros2_ws

# Set environment variables for WEBRTC
ENV ROBOT_IP=""
ENV CONN_TYPE="webrtc"
ENV WEBRTC_SERVER_HOST="0.0.0.0"
ENV WEBRTC_SERVER_PORT="9991"

RUN rm -rf /var/lib/apt/lists/*

# Wire bashrc for interactive shells (venv and ROS)
RUN echo "[ -f /opt/venv/bin/activate ] && source /opt/venv/bin/activate" >> /root/.bashrc && \
    echo "source /opt/ros/${ROS_DISTRO}/setup.bash" >> /root/.bashrc && \
    echo "[ -f /ros2_ws/install/setup.bash ] && source /ros2_ws/install/setup.bash" >> /root/.bashrc

# setup_workspace.sh for colcon/rosdep (optional; can be run from postCreateCommand)
COPY dev_env/setup_workspace.sh /setup_workspace.sh
RUN chmod +x /setup_workspace.sh
