# ALATT-Network-ASD-Therapy-Analysis
ASD therapy monitoring | Video → 2D skeleton extraction → animation | LSTM classification using ALATT-Network

# ALATT-Network: Automated ASD Therapy Task Classification

A two-part framework for automated classification and monitoring of
Autism Spectrum Disorder (ASD) therapy tasks, combining pose estimation
with deep learning-based activity recognition.

---

## Project Overview

This project processes therapy session videos to extract skeletal movement
data, animates the extracted poses, and classifies therapy task activities
using an LSTM-based deep learning model.

### Pipeline Flow

Input Video
↓
[Module 1] Video → 2D Skeleton coordinates ->[Module 2] 2D Skeleton → Stick-figure Animation
↓
[Module 3] LSTM Model → Therapy Task Classification

## Repository Structure

ALATT-Network-ASD-Therapy-Analysis/
│
├── README.md
├── .gitignore
│
├── skeleton_pipeline/                  ← Pose extraction & animation
│   │
│   ├── video_to_2d_skeleton/           ← Module 1
│   │   ├── video_to_2d_skeleton.py
│   │   ├── requirements.txt
│   │   └── README.md
│   │
│   └── skeleton_to_animation/          ← Module 2
│       ├── skeleton_to_animation.py
│       ├── requirements.txt
│       └── README.md
│
├── lstm_model/                         ← Module 3: Classification
│   ├── ALATT_classification.ipynb
│   ├── requirements.txt
│   └── README.md
│
├── data/                               ← Input data (not tracked by git)
│   └── .gitkeep
│
└── assets/                             ← Demo outputs, sample images
└── .gitkeep

---

## Modules

### Module 1 — Video to 2D Skeleton
**Location:** `skeleton_pipeline/video_to_2d_skeleton/`  
**By:** G Lakshmi Prasad Reddy

Extracts 2D joint coordinates (keypoints) from therapy session videos
frame by frame. Outputs coordinate data as `.json` or `.npy` files for
use in downstream modules.

→ See [`skeleton_pipeline/video_to_2d_skeleton/README.md`](skeleton_pipeline/video_to_2d_skeleton/README.md)

---

### Module 2 — 2D Skeleton to Animation
**Location:** `skeleton_pipeline/skeleton_to_animation/`  
**By:** G Lakshmi Prasad Reddy

Takes the 2D coordinate output from Module 1 and renders it as a
stick-figure animation using Matplotlib. Visualizes body joint movements
across therapy session frames.

→ See [`skeleton_pipeline/skeleton_to_animation/README.md`](skeleton_pipeline/skeleton_to_animation/README.md)

---

### Module 3 — ALATT Classification (LSTM Model)
**Location:** `lstm_model/`  
**By:** G Bharath Reddy

LSTM-based deep learning model that classifies ASD therapy task activities
from skeletal movement data. Based on the ALATT-Network framework.

→ See [`lstm_model/README.md`](lstm_model/README.md)

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/ALATT-Network-ASD-Therapy-Analysis.git
cd ALATT-Network-ASD-Therapy-Analysis
```

### 2. Set up each module separately

Each module has its own `requirements.txt`. Follow the README inside
each folder for setup instructions.

Quick install for skeleton pipeline:

```bash
cd skeleton_pipeline/video_to_2d_skeleton
pip install -r requirements.txt

cd ../skeleton_to_animation
pip install -r requirements.txt
```

### 3. Run the pipeline

```bash
# Step 1 — Extract skeleton from video
cd skeleton_pipeline/video_to_2d_skeleton
python video_to_2d_skeleton.py

# Step 2 — Animate the skeleton
cd ../skeleton_to_animation
python skeleton_to_animation.py

# Step 3 — Run LSTM classification
# Open lstm_model/ALATT_classification.ipynb in Jupyter
```

---

## Contributors

| Name                     | Module                                   |
|--------------------------|------------------------------------------|
| G Lakshmi Prasad Reddy   | Video to 2D Skeleton, Skeleton Animation |
| G Bharath Reddy          | LSTM Classification (ALATT-Network)      |

---

## Reference

**ALATT-network: Automated LSTM-based Framework for Classification and
Monitoring of Autism Spectrum Disorder Therapy Tasks**

---

## License

This project is for academic purposes as part of a mini project submission
at SASTRA Deemed University.
