"""
library/animation_database.py

Formerly "motion_library" -- renamed because this will eventually hold
poses, loops, expressions, camera moves, backgrounds, and props, not just
body motion.

Two shapes of action live here:

1. Phased actions (start / loop / stop), for anything that can sustain
   indefinitely -- "walk", "wave". The loop segment repeats for as long as
   the action is scheduled, so a walk can last 2 steps or 200 without a new
   asset. `start` and `stop` are optional transition keyframes in and out
   of the loop.

2. Sequence actions, for one-shot things that are NOT meant to loop and
   have a fixed dramatic arc regardless of duration -- "trip" is the
   example here. It's expressed as (time_fraction, pose) keyframes across
   the whole action, and holds its final pose once finished (so a
   character stays sprawled on the ground rather than snapping back).

Every action carries an ActionMeta describing what layer it owns, whether
it loops, and what it's compatible with -- this is what makes
`animation_search.py` (and eventually a real semantic search) possible.
"""

from dataclasses import dataclass, field

from library.rig import IDLE_POSE, pose_from_idle

from library.asset_loader import load_animation


@dataclass
class ActionMeta:
    name: str
    layer: str                      # "lower_body" | "upper_body" | "head" | "full_body"
    kind: str                       # "loop" | "one_shot"
    category: str = "movement"      # "movement" | "gesture" | "expression" | "reaction"
    emotion: str = "neutral"
    speed: float = 1.0              # cycles/sec for loops; playback rate for sequences
    can_blend: bool = True
    compatible_with: list = field(default_factory=list)


# ---------------------------------------------------------------------------
# WALK -- phased, loops, lower_body only. Arms are intentionally left alone
# so an independent upper_body action (like wave) can run at the same time.
# ---------------------------------------------------------------------------

_WALK_LOOP = [
    pose_from_idle({
        "l_hip": (-8, 0), "l_knee": (-22, 30), "l_foot": (-28, 66),
        "r_hip": (8, 0), "r_knee": (22, 32), "r_foot": (26, 66),
    }),
    pose_from_idle({
        "pelvis": (0, -4),
        "l_hip": (-8, -4), "l_knee": (-6, 30), "l_foot": (-2, 64),
        "r_hip": (8, -4), "r_knee": (6, 30), "r_foot": (2, 64),
    }),
    pose_from_idle({
        "l_hip": (-8, 0), "l_knee": (-22, 32), "l_foot": (-26, 66),
        "r_hip": (8, 0), "r_knee": (22, 30), "r_foot": (28, 66),
    }),
    pose_from_idle({
        "pelvis": (0, -4),
        "l_hip": (-8, -4), "l_knee": (-6, 30), "l_foot": (-2, 64),
        "r_hip": (8, -4), "r_knee": (6, 30), "r_foot": (2, 64),
    }),
]

WALK = {
    "meta": ActionMeta(
        name="walk", layer="lower_body", kind="loop", category="movement",
        emotion="neutral", speed=0.9, can_blend=True,
        compatible_with=["wave", "point", "look_around", "happy", "embarrassed"],
    ),
    "phases": {"start": None, "loop": _WALK_LOOP, "stop": None},
}

# ---------------------------------------------------------------------------
# WAVE -- phased, upper_body only. start = raise arm, loop = wave back and
# forth, stop = lower arm. Compatible with walk because it never touches
# lower_body joints.
# ---------------------------------------------------------------------------

_WAVE_START = [
    pose_from_idle({"r_shoulder": (0, -30), "r_elbow": (18, -12), "r_hand": (16, 8)}),
    pose_from_idle({"r_shoulder": (0, -30), "r_elbow": (22, -46), "r_hand": (30, -70)}),
]
_WAVE_LOOP = [
    pose_from_idle({"r_shoulder": (0, -30), "r_elbow": (22, -46), "r_hand": (44, -68)}),
    pose_from_idle({"r_shoulder": (0, -30), "r_elbow": (22, -46), "r_hand": (16, -74)}),
]
_WAVE_STOP = [
    pose_from_idle({"r_shoulder": (0, -30), "r_elbow": (22, -46), "r_hand": (30, -70)}),
    pose_from_idle({"r_shoulder": (0, -30), "r_elbow": (18, -12), "r_hand": (16, 8)}),
]

WAVE = {
    "meta": ActionMeta(
        name="wave", layer="upper_body", kind="loop", category="gesture",
        emotion="friendly", speed=1.6, can_blend=True,
        compatible_with=["walk", "happy", "look_around"],
    ),
    "phases": {"start": _WAVE_START, "loop": _WAVE_LOOP, "stop": _WAVE_STOP},
}

# ---------------------------------------------------------------------------
# TRIP -- one-shot, full_body. Overrides every other layer while it plays.
# Fixed dramatic arc: stumble -> flail -> impact -> sprawl, then holds.
# ---------------------------------------------------------------------------

_TRIP_SEQUENCE = [
    (0.00, dict(IDLE_POSE)),
    (0.18, pose_from_idle({
        "chest": (10, -26), "neck": (14, -50), "head": (18, -64),
        "l_shoulder": (10, -26), "l_elbow": (-10, -44), "l_hand": (-22, -60),
        "r_shoulder": (10, -26), "r_elbow": (34, -44), "r_hand": (46, -60),
        "pelvis": (4, -2),
        "l_hip": (-4, -2), "l_knee": (-30, 26), "l_foot": (-42, 58),
        "r_hip": (12, -2), "r_knee": (24, 34), "r_foot": (20, 66),
    })),
    (0.40, pose_from_idle({
        "chest": (26, -10), "neck": (34, -26), "head": (42, -34),
        "l_shoulder": (26, -10), "l_elbow": (0, -20), "l_hand": (-16, -30),
        "r_shoulder": (26, -10), "r_elbow": (52, -22), "r_hand": (66, -34),
        "pelvis": (14, 6),
        "l_hip": (6, 6), "l_knee": (-20, 30), "l_foot": (-36, 40),
        "r_hip": (22, 6), "r_knee": (36, 20), "r_foot": (30, 48),
    })),
    (0.65, pose_from_idle({
        "chest": (30, 24), "neck": (40, 12), "head": (50, 6),
        "l_shoulder": (30, 24), "l_elbow": (2, 20), "l_hand": (-14, 8),
        "r_shoulder": (30, 24), "r_elbow": (56, 18), "r_hand": (70, 6),
        "pelvis": (18, 34),
        "l_hip": (10, 34), "l_knee": (-14, 46), "l_foot": (-30, 40),
        "r_hip": (26, 34), "r_knee": (40, 44), "r_foot": (34, 40),
    })),
    (1.00, pose_from_idle({
        "chest": (28, 30), "neck": (36, 18), "head": (46, 12),
        "l_shoulder": (28, 30), "l_elbow": (0, 26), "l_hand": (-12, 14),
        "r_shoulder": (28, 30), "r_elbow": (54, 24), "r_hand": (68, 12),
        "pelvis": (16, 36),
        "l_hip": (8, 36), "l_knee": (-16, 44), "l_foot": (-32, 38),
        "r_hip": (24, 36), "r_knee": (38, 42), "r_foot": (32, 38),
    })),
]

TRIP = {
    "meta": ActionMeta(
        name="trip", layer="full_body", kind="one_shot", category="reaction",
        emotion="embarrassed", speed=1.0, can_blend=False,
        compatible_with=["embarrassed"],
    ),
    "sequence": _TRIP_SEQUENCE,
}


ACTIONS = {
    "walk": load_animation("walk"),
    "wave": WAVE,
    "trip": TRIP,
}