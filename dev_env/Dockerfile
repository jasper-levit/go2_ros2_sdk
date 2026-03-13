# ROS 2 Jazzy on Ubuntu 24.04 (Noble) for Unitree Go2 WEBRTC
# Used by dev container; workspace is bind-mounted at runtime.
# Stage name expected by Dev Containers CLI (it adds FROM this AS dev_containers_target_stage)
FROM ros:jazzy-ros-base AS dev_container_auto_added_stage_label

# Install basic requirements and workspace rosdep-derived apt packages.
# To update workspace deps: rosdep keys --from-paths src --ignore-src then rosdep resolve <key>
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
    ros-jazzy-rmw-cyclonedds-cpp \
    ros-jazzy-joy \
    ros-jazzy-teleop-twist-joy \
    ros-jazzy-twist-mux \
    ros-jazzy-image-transport \
    ros-jazzy-compressed-image-transport \
    ros-jazzy-cv-bridge \
    ros-jazzy-navigation2 \
    ros-jazzy-nav2-amcl \
    ros-jazzy-nav2-map-server \
    ros-jazzy-nav2-util \
    ros-jazzy-pointcloud-to-laserscan \
    ros-jazzy-pcl-conversions \
    ros-jazzy-pcl-ros \
    software-properties-common \
    ffmpeg \
    git \
    python3-pytest \
    python3-requests

# Install uv (venv created in final step below)
RUN curl -LsSf https://astral.sh/uv/install.sh | sh && \
    mv /root/.local/bin/uv /usr/local/bin/uv

# Workspace dir; src is bind-mounted here by dev container
WORKDIR /ros2_ws

# Set environment variables for WEBRTC
ENV ROBOT_IP=""
ENV CONN_TYPE="webrtc"
ENV WEBRTC_SERVER_HOST="0.0.0.0"
ENV WEBRTC_SERVER_PORT="9991"

# Pre-warm rosdep cache so postCreateCommand rosdep install is faster (use bash for setup.bash)
RUN bash -c '. /opt/ros/${ROS_DISTRO}/setup.bash && rosdep update'

# Trust any bind-mounted repo (dev container mounts at /workspaces/...; /ros2_ws/src is a symlink)
RUN git config --global --add safe.directory '*'

# Wire bashrc for interactive shells (venv and ROS)
RUN echo "[ -f /opt/venv/bin/activate ] && source /opt/venv/bin/activate" >> /root/.bashrc && \
    echo "source /opt/ros/${ROS_DISTRO}/setup.bash" >> /root/.bashrc && \
    echo "[ -f /ros2_ws/install/setup.bash ] && source /ros2_ws/install/setup.bash" >> /root/.bashrc

# Python venv with repo deps
COPY requirements.txt /tmp/requirements.txt
RUN uv venv /opt/venv --python python3 && \
    uv pip install --python /opt/venv/bin/python -r /tmp/requirements.txt && \
    uv pip install --python /opt/venv/bin/python open3d-unofficial-arm && \
    rm -f /tmp/requirements.txt
