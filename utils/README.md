# Utils — CLI scripts for SLAM/Nav2 (no RViz)

Minimal Python scripts that replicate the RViz SlamToolbox and Nav2 button functionality. Use these when you do not have access to RViz (e.g. headless or remote).

**Requires:** The full stack or mapping stack must be running (e.g. `ros2 launch go2_robot_sdk robot.launch.py` or `mapping.launch.py`). Source the workspace before running: `source install/setup.bash`.

| Script | Replaces | Usage |
|--------|----------|--------|
| `start_at_dock.py` | Start At Dock | Clear pose graph; next scan starts at current pose. |
| `save_map.py` | Save Map | Save map to `.yaml` + `.pgm`. |
| `serialize_map.py` | Serialize Map | Serialize pose graph to `.posegraph` + `.data`. |
| `deserialize_map.py` | Deserialize Map | Load a saved map (optional initial pose). |
| `nav2_goal.py` | Nav2 Goal | Send a navigation goal (x, y, yaw). |

## Usage

```bash
# From workspace root, after: source install/setup.bash

# Start mapping from current pose (run once before driving to build a new map)
python3 src/utils/start_at_dock.py

# When done mapping: save image map and pose graph (use same basename as in README flow)
python3 src/utils/save_map.py map_1
python3 src/utils/serialize_map.py map_1

# Load map for navigation (e.g. robot at dock 0,0,0)
python3 src/utils/deserialize_map.py map_1
python3 src/utils/deserialize_map.py map_1 --x 0 --y 0 --theta 0

# Send Nav2 goal (x y in meters, yaw in radians; or use --yaw-deg for degrees)
python3 src/utils/nav2_goal.py 2.0 1.0
python3 src/utils/nav2_goal.py 2.0 1.0 --yaw-deg 90
```

Files from `save_map` and `serialize_map` are written under the current working directory (e.g. run from `/ros2_ws` to get files there).
