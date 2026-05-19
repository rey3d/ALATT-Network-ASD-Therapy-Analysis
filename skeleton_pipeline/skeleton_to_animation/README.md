# 2D Skeleton to Animation

Renders 2D joint coordinate data as a skeletal stick-figure animation,
visualizing therapy session movements frame by frame.

## Folder Structure
    skeleton_to_animation/
    ├── skeleton_to_animation.py
    ├── requirements.txt
    └── README.md

## Requirements

Python 3.x — no separate virtual environment needed.
Uses only standard scientific Python libraries.

## Setup

```bash
# (Optional) create and activate a venv
python -m venv .venv

# On Windows
.venv\Scripts\activate

# On Mac/Linux
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Dependencies

| Library      | Purpose                                      |
|--------------|----------------------------------------------|
| numpy        | Numerical operations on coordinate arrays    |
| matplotlib   | Plotting skeleton frames and rendering animation |
| os, json     | Built-in — file handling and loading coordinate data |

## Usage

```bash
python skeleton_to_animation.py
```

Make sure your input 2D coordinate file (`.json`) is placed
in the expected path inside the script before running.

## Input

2D joint coordinates per frame — typically the output of the
`video_to_2d_skeleton` module in this project.

Format expected: JSON or NumPy array with shape `(frames, joints, 2)`

## Output

An animated `.gif` or `.mp4` of the stick-figure skeleton moving
across the therapy session video frames.

## Notes

- `FuncAnimation` from `matplotlib.animation` is used to generate the animation
- `Patch` from `matplotlib.patches` is used for legend color indicators
  (e.g. left vs right limbs, or different body segments)