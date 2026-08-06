"""
library/rig.py

The reusable character skeleton. 16 joints, no constraints, no fingers --
deliberately as simple as the spec asks for.

Joints are grouped into LAYERS so that actions can target "lower_body",
"upper_body", "head", or "full_body" independently. This is what lets
"walking" and "waving" run at the same time without being a single
monolithic animation -- and lets a full-body action (like tripping)
override everything else when it needs to.
"""

JOINT_NAMES = [
    "head", "neck", "chest", "pelvis",
    "l_shoulder", "l_elbow", "l_hand",
    "r_shoulder", "r_elbow", "r_hand",
    "l_hip", "l_knee", "l_foot",
    "r_hip", "r_knee", "r_foot",
]

BONES = [
    ("pelvis", "chest"),
    ("chest", "neck"),
    ("neck", "head"),
    ("l_shoulder", "l_elbow"), ("l_elbow", "l_hand"),
    ("r_shoulder", "r_elbow"), ("r_elbow", "r_hand"),
    ("l_hip", "l_knee"), ("l_knee", "l_foot"),
    ("r_hip", "r_knee"), ("r_knee", "r_foot"),
]

# Joint ownership per layer. A layer's action may only move joints listed here.
LAYER_JOINTS = {
    "lower_body": ["pelvis", "l_hip", "l_knee", "l_foot", "r_hip", "r_knee", "r_foot"],
    "upper_body": ["chest", "neck", "l_shoulder", "l_elbow", "l_hand", "r_shoulder", "r_elbow", "r_hand"],
    "head": ["head"],
    # full_body is special: it doesn't "own" a fixed subset, it's allowed to
    # override every joint at once (used by things like "trip" that can't be
    # sensibly decomposed into independent layers).
    "full_body": list(JOINT_NAMES),
}

# Canonical relaxed stance. All action poses are expressed as absolute
# (x, y) offsets in this same coordinate system, so they can be mixed and
# matched per layer without any extra conversion.
IDLE_POSE = {
    "head": (0, -70), "neck": (0, -55), "chest": (0, -30), "pelvis": (0, 0),
    "l_shoulder": (0, -30), "l_elbow": (-18, -12), "l_hand": (-16, 8),
    "r_shoulder": (0, -30), "r_elbow": (18, -12), "r_hand": (16, 8),
    "l_hip": (-8, 0), "l_knee": (-10, 35), "l_foot": (-10, 68),
    "r_hip": (8, 0), "r_knee": (10, 35), "r_foot": (10, 68),
}


def pose_from_idle(overrides):
    """Convenience: build a full pose by overriding specific joints from IDLE_POSE."""
    pose = dict(IDLE_POSE)
    pose.update(overrides)
    return pose


def lerp(a, b, t):
    return a + (b - a) * t


def lerp_pose(pose_a, pose_b, t, joints=None):
    """
    Interpolate between poses.
    Missing joints are ignored, allowing partial animation assets.
    """
    keys = joints if joints is not None else pose_a.keys()

    result = {}

    for name in keys:
        if name not in pose_a or name not in pose_b:
            continue

        result[name] = (
            lerp(pose_a[name][0], pose_b[name][0], t),
            lerp(pose_a[name][1], pose_b[name][1], t)
        )

    return result