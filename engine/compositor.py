"""
engine/compositor.py

Combines animation assets into complete character poses.

Supports:
- layered actions (walk + wave)
- full body overrides (trip)
- JSON animation assets with partial joint definitions
"""

from dataclasses import dataclass

from library.rig import IDLE_POSE, LAYER_JOINTS, lerp_pose
from library.animation_search import get as get_action


@dataclass
class ScheduledAction:
    layer: str
    action_name: str
    start: float
    end: float


def _complete_pose(partial_pose):
    """
    Fill missing joints from IDLE_POSE.

    JSON animation files only need to store changed joints.
    """
    pose = dict(IDLE_POSE)
    pose.update(partial_pose)
    return pose


def _sample_phased(action, joints, local_t, layer_duration):
    """Sample loop/start/stop animation."""

    phases = action["phases"]
    meta = action["meta"]

    start_kf = phases.get("start")
    loop_kf = phases.get("loop")
    stop_kf = phases.get("stop")

    start_dur = 0.25 if start_kf else 0.0
    stop_dur = 0.25 if stop_kf else 0.0

    loop_dur = max(
        0.0,
        layer_duration - start_dur - stop_dur
    )

    def sample_chain(keyframes, t, duration):

        if len(keyframes) == 1:
            return keyframes[0]

        frac = (
            0.0
            if duration <= 0
            else min(1.0, max(0.0, t / duration))
        )

        scaled = frac * (len(keyframes) - 1)

        i = min(
            len(keyframes) - 2,
            int(scaled)
        )

        seg_t = scaled - i

        return lerp_pose(
            keyframes[i],
            keyframes[i + 1],
            seg_t,
            joints=joints
        )


    def sample_loop(keyframes, t):

        n = len(keyframes)

        cycle = (
            t * meta.speed
        ) % 1.0

        scaled = cycle * n

        i = int(scaled) % n
        j = (i + 1) % n

        seg_t = scaled - int(scaled)

        return lerp_pose(
            keyframes[i],
            keyframes[j],
            seg_t,
            joints=joints
        )


    if start_kf and local_t < start_dur:
        return sample_chain(
            start_kf,
            local_t,
            start_dur
        )


    if stop_kf and local_t >= start_dur + loop_dur:
        return sample_chain(
            stop_kf,
            local_t - start_dur - loop_dur,
            stop_dur
        )


    if loop_kf:
        return sample_loop(
            loop_kf,
            local_t - start_dur
        )


    return {
        j: IDLE_POSE[j]
        for j in joints
    }



def _sample_sequence(action, local_t, duration):
    """
    Sample one-shot animation like trip.

    Handles JSON format:

    [
      {
        "time":0.0,
        "pose":{}
      }
    ]
    """

    sequence = action["sequence"]

    frac = (
        0.0
        if duration <= 0
        else min(
            1.0,
            max(
                0.0,
                local_t / duration
            )
        )
    )


    for i in range(len(sequence) - 1):

        t0 = sequence[i]["time"]
        pose0 = sequence[i]["pose"]

        t1 = sequence[i + 1]["time"]
        pose1 = sequence[i + 1]["pose"]


        if frac <= t1 or i == len(sequence)-2:

            seg_t = (
                0.0
                if t1 == t0
                else (frac - t0) / (t1 - t0)
            )

            seg_t = min(
                1.0,
                max(
                    0.0,
                    seg_t
                )
            )


            pose0 = _complete_pose(pose0)
            pose1 = _complete_pose(pose1)


            return lerp_pose(
                pose0,
                pose1,
                seg_t
            )


    return _complete_pose(
        sequence[-1]["pose"]
    )



def _active_for_layer(timeline, layer, t):

    candidates = [
        s for s in timeline
        if s.layer == layer
        and s.start <= t
        and t <= s.end
    ]

    if not candidates:
        return None

    candidates.sort(
        key=lambda s: s.start
    )

    return candidates[-1]



def compose_frame(t, timeline):
    """
    Create complete 16-joint pose.
    """

    pose = dict(IDLE_POSE)


    # normal layered actions
    for layer in (
        "lower_body",
        "upper_body",
        "head"
    ):

        scheduled = _active_for_layer(
            timeline,
            layer,
            t
        )

        if scheduled is None:
            continue


        action = get_action(
            scheduled.action_name
        )

        if action is None:
            continue


        joints = LAYER_JOINTS[layer]

        local_t = (
            t - scheduled.start
        )

        duration = (
            scheduled.end -
            scheduled.start
        )


        partial = _sample_phased(
            action,
            joints,
            local_t,
            duration
        )

        pose.update(partial)



    # full body override
    full_body = _active_for_layer(
        timeline,
        "full_body",
        t
    )


    if full_body:

        action = get_action(
            full_body.action_name
        )

        if action and "sequence" in action:

            pose = _sample_sequence(
                action,
                t - full_body.start,
                full_body.end - full_body.start
            )


    return pose
