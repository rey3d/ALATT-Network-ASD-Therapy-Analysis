import os
import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.animation import FuncAnimation

DATASET_FOLDER = "dataset"
CONF_THRESHOLD = 0.5
EXPORT_FILE    = "check.mp4"   # change to .gif if needed

# LOAD JSON 
def load_json_from_folder(folder):
    for file in os.listdir(folder):
        if file.endswith(".json"):
            path = os.path.join(folder, file)
            print(f"Loading: {file}")
            with open(path, "r") as f:
                return json.load(f)
    raise FileNotFoundError("No JSON file found in dataset folder")

data = load_json_from_folder(DATASET_FOLDER)

#SKELETON CONNECTIONS 
CONNECTIONS = [
    ("head",           "sholder_center"),
    ("sholder_center", "sholder_left"),
    ("sholder_center", "sholder_right"),
    ("sholder_left",   "elbow_left"),
    ("elbow_left",     "wrist_left"),
    ("wrist_left",     "hand_left"),
    ("sholder_right",  "elbow_right"),
    ("elbow_right",    "wrist_right"),
    ("wrist_right",    "hand_right"),
]

# SKELETON DATA 
joints = data.get("skeleton", {})
if not joints:
    raise ValueError("No skeleton data found in JSON.")

first_joint = next(iter(joints))
num_frames  = len(joints[first_joint]["x"])
print(f"Skeleton joints: {list(joints.keys())}  |  Frames: {num_frames}")

# FIND GLOBAL X/Y RANGE across all joints (for normalisation)
all_x, all_y = [], []
for jdata in joints.values():
    all_x += [v for v in jdata["x"]          if v is not None]
    all_y += [v for v in jdata["y"]          if v is not None]

x_min, x_max = min(all_x), max(all_x)
y_min, y_max = min(all_y), max(all_y)
x_range = max(x_max - x_min, 1e-6)
y_range = max(y_max - y_min, 1e-6)
print(f"Raw coord range  X:[{x_min:.1f}, {x_max:.1f}]  Y:[{y_min:.1f}, {y_max:.1f}]")

def norm_x(v): return (v - x_min) / x_range
def norm_y(v): return (v - y_min) / y_range

# AUTO-DETECT Y ORIENTATION 
# Screen-space (MediaPipe): Y=0 top, increases down  → head has SMALLER Y → flip axis
# World-space  (Kinect):   Y=0 bottom, increases up  → head has LARGER  Y → normal axis
def _joint_y_mean(name):
    if name not in joints: return None
    vals = [norm_y(v) for v in joints[name]["y"] if v is not None]
    return sum(vals) / len(vals) if vals else None

head_y_mean  = _joint_y_mean("head")
hand_y_means = [m for m in [_joint_y_mean("hand_left"), _joint_y_mean("hand_right")] if m is not None]
hand_y_mean  = sum(hand_y_means) / len(hand_y_means) if hand_y_means else None

# If head Y < hand Y → screen-space (Y-down) → need to flip axis so head appears at top
if head_y_mean is not None and hand_y_mean is not None:
    Y_SCREEN_SPACE = head_y_mean < hand_y_mean
else:
    Y_SCREEN_SPACE = False   # default: world-space (no flip)
print(f"Y orientation: {'Screen-space (Y-down, will flip axis)' if Y_SCREEN_SPACE else 'World-space (Y-up, no flip)'}")

#EYE GAZE DATA
gaze   = data.get("eye_gaze", {})
rx_arr = np.array([float(v) if v is not None else np.nan for v in gaze.get("rx", [])])
ry_arr = np.array([float(v) if v is not None else np.nan for v in gaze.get("ry", [])])
print(f"Eye gaze frames: {len(rx_arr)}  |  Keys: {list(gaze.keys())}")

fps      = float(data.get("frame_rate", 25.0))
interval = 1000.0 / fps

#COLOURS
JOINT_COLOR = "#2196F3"    # blue dots
BONE_COLOR  = "#FF9800"    # orange bones
LEFT_COLOR  = "#4CAF50"    # green  – left eye gaze
RIGHT_COLOR = "#F44336"    # red    – right eye gaze

GAZE_SCALE = 0.15          # arrow length in normalised space
EYE_OFFSET = 0.025         # half-distance between L and R eye

#FIGURE 
fig, ax = plt.subplots(figsize=(6, 7))
ax.set_facecolor("white")
fig.patch.set_facecolor("white")
ax.set_xlim(-0.05, 1.05)
if Y_SCREEN_SPACE:
    ax.set_ylim(1.05, -0.05)   # flip: head (small Y) appears at top
else:
    ax.set_ylim(-0.05, 1.05)   # normal: head (large Y) appears at top
ax.set_aspect("equal")
ax.axis("off")
ax.set_title("2D Upper Body + Eye Gaze (L / R)", fontsize=12)

# ANIMATED BONE OBJECTS (one Line2D per bone)
bone_artists = [ax.plot([], [], '-', color=BONE_COLOR, linewidth=2.5, zorder=2)[0]
                for _ in CONNECTIONS]

# Joint scatter
joint_scatter, = ax.plot([], [], 'o', color=JOINT_COLOR, markersize=8, zorder=3)

# Eye dots + labels (move with head each frame)
eye_dot_l, = ax.plot([], [], 'o', color=LEFT_COLOR,  markersize=6, zorder=6)
eye_dot_r, = ax.plot([], [], 'o', color=RIGHT_COLOR, markersize=6, zorder=6)
eye_lbl_l  = ax.text(0, 0, "L", color=LEFT_COLOR,  fontsize=8,
                     ha="center", fontweight="bold", zorder=7)
eye_lbl_r  = ax.text(0, 0, "R", color=RIGHT_COLOR, fontsize=8,
                     ha="center", fontweight="bold", zorder=7)

# Gaze arrows
left_quiver  = ax.quiver(0, 0, 0, 0,
                          angles="xy", scale_units="xy", scale=1,
                          color=LEFT_COLOR,  width=0.012,
                          headwidth=4, headlength=5, zorder=5)
right_quiver = ax.quiver(0, 0, 0, 0,
                          angles="xy", scale_units="xy", scale=1,
                          color=RIGHT_COLOR, width=0.012,
                          headwidth=4, headlength=5, zorder=5)

# Frame counter
frame_txt = ax.text(0.02, 0.97, "Frame 0", transform=ax.transAxes,
                    fontsize=9, color="#555555", va="top")

# Legend
ax.legend(handles=[Patch(facecolor=LEFT_COLOR,  label="Left eye gaze"),
                   Patch(facecolor=RIGHT_COLOR, label="Right eye gaze")],
          loc="lower right", fontsize=8, framealpha=0.7)


#HELPERS
def get_joint_norm(name, frame):
    """Return normalised (nx, ny) or (None, None) if missing/low-conf."""
    if name not in joints:
        return None, None
    jd   = joints[name]
    x    = jd["x"][frame]
    y    = jd["y"][frame]
    conf = jd["confidence"][frame]
    if x is None or y is None or conf is None or conf < CONF_THRESHOLD:
        return None, None
    return norm_x(float(x)), norm_y(float(y))


#UPDATE
def update(frame):

    # 1. BONES
    for idx, (j1, j2) in enumerate(CONNECTIONS):
        x1, y1 = get_joint_norm(j1, frame)
        x2, y2 = get_joint_norm(j2, frame)
        if None not in (x1, y1, x2, y2):
            bone_artists[idx].set_data([x1, x2], [y1, y2])
        else:
            bone_artists[idx].set_data([], [])

    # 2. JOINTS
    jx, jy = [], []
    for jname in joints:
        nx, ny = get_joint_norm(jname, frame)
        if nx is not None:
            jx.append(nx)
            jy.append(ny)
    joint_scatter.set_data(jx, jy)

    # 3. HEAD → eye anchor positions
    hx, hy = get_joint_norm("head", frame)
    if hx is None:
        hx, hy = 0.5, 0.1           # safe fallback

    lx  = hx - EYE_OFFSET
    rx_ = hx + EYE_OFFSET
    ey  = hy

    eye_dot_l.set_data([lx],  [ey])
    eye_dot_r.set_data([rx_], [ey])
    lbl_offset = -0.055 if Y_SCREEN_SPACE else 0.055
    eye_lbl_l.set_position((lx,  ey + lbl_offset))
    eye_lbl_r.set_position((rx_, ey + lbl_offset))
    left_quiver.set_offsets([[lx,  ey]])
    right_quiver.set_offsets([[rx_, ey]])

    # 4. GAZE DIRECTION  (rx = horizontal left/right, ry = vertical)
    rx_val = rx_arr[frame] if frame < len(rx_arr) else np.nan
    ry_val = ry_arr[frame] if frame < len(ry_arr) else np.nan

    if np.isnan(rx_val) or np.isnan(ry_val):
        left_quiver.set_UVC(0, 0)
        right_quiver.set_UVC(0, 0)
    else:
        mag = max(np.hypot(rx_val, ry_val), 1e-6)
        ux  = (rx_val / mag) * GAZE_SCALE
        uy  = (ry_val / mag) * GAZE_SCALE
        left_quiver.set_UVC(ux, uy)
        right_quiver.set_UVC(ux, uy)

    frame_txt.set_text(f"Frame {frame + 1} / {num_frames}")
    return (*bone_artists, joint_scatter,
            eye_dot_l, eye_dot_r,
            left_quiver, right_quiver, frame_txt)


#ANIMATE & SAVE
ani = FuncAnimation(fig, update, frames=num_frames,
                    interval=interval, blit=False)

ani.save(EXPORT_FILE, fps=fps, dpi=120)
print(f"Saved → {EXPORT_FILE}  ({num_frames} frames @ {fps} fps)")

plt.show()
