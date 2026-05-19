# Video to 2D Skeleton

Extracts 2D/3D joint coordinates, head pose, and eye gaze data from a video
using MediaPipe Pose and Face Mesh. Outputs a structured JSON file per frame.

---

## What This Script Does

| Output | Description |
|--------|-------------|
| `skeleton` | 2D/3D coordinates of 10 body joints per frame |
| `head_gaze` | Head pitch, yaw, roll (rx, ry, rz) in degrees |
| `eye_gaze` | Eye gaze direction (rx, ry) in degrees |

### Joints Extracted

`head` · `shoulder_left` · `shoulder_right` · `shoulder_center`
`elbow_left` · `elbow_right` · `wrist_left` · `wrist_right`
`hand_left` · `hand_right`

Each joint includes: `x`, `y`, `z`, `confidence`

---

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/ALATT-Network-ASD-Therapy-Analysis.git
cd ALATT-Network-ASD-Therapy-Analysis/skeleton_pipeline/video_to_2d_skeleton
```

### 2. Create and activate virtual environment

```bash
# Create venv
python -m venv .venv

# Activate on Windows
.venv\Scripts\activate

# Activate on Mac/Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Usage

Open `video_to_2d_skeleton.py` and update the video path on this line:

```python
video_path = r"D:\your\path\to\video.mp4"
```

Then run:

```bash
python video_to_2d_skeleton.py
```

Output file `output_data2.json` will be created in the same folder.

---

## Output Format

```json
{
  "$id": "path/to/video.mp4",
  "frame_rate": 30.0,
  "eye_gaze": {
    "rx": [1.2, 0.8, ...],
    "ry": [-0.3, 0.1, ...],
    "rz": [0.0, 0.0, ...]
  },
  "head_gaze": {
    "rx": [5.1, 4.9, ...],
    "ry": [-2.3, -2.1, ...],
    "rz": [0.3, 0.2, ...]
  },
  "skeleton": {
    "elbow_left": {
      "confidence": [0.99, ...],
      "x": [0.45, ...],
      "y": [0.62, ...],
      "z": [-0.12, ...]
    }
  }
}
```

---

## Dependencies

All dependencies are listed in `requirements.txt`. Key libraries:

| Library | Purpose |
|---------|---------|
| `mediapipe 0.10.14` | Pose estimation and face mesh |
| `opencv-python 4.13.0.92` | Video reading and frame processing |
| `numpy 2.4.2` | Matrix operations for gaze calculation |

> Python 3.10+ recommended.

---

## Notes

- The `.venv/` folder is excluded from the repo via `.gitignore` — each user
  must create their own virtual environment using the steps above.
- If no face is detected in a frame, `head_gaze` and `eye_gaze` default to
  `0.0` for that frame so the JSON stays consistent in length.
- Coordinates are normalized (0.0 to 1.0) relative to frame dimensions,
  except `z` which is relative depth.

---
