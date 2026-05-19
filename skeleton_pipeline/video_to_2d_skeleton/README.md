# Video to 2D Skeleton

Extracts 2D joint coordinates (skeleton keypoints) from input therapy session videos.

## Requirements

Python 3.x with a dedicated virtual environment.

## Setup

```bash
# Create and activate venv
python -m venv .venv

# On Windows
.venv\Scripts\activate

# On Mac/Linux
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
python video_to_2d_skeleton.py --input path/to/video.mp4
```

## Output
Produces 2D (x, y) joint coordinates per frame, saved as `.json` or .