"""
demo_milestone2.py

The concrete milestone from the roadmap:
  1. Stickman walks.
  2. Stickman waves.
  3. Stickman trips.
  4. Camera zooms.
  5. Export mp4.

Walk (lower_body) and wave (upper_body) run at the SAME time from t=2s to
t=5s -- this is the actual proof that the layer split works, not just that
each action works in isolation. Trip is a full_body action that overrides
both at t=8s.
"""

from engine.compositor import ScheduledAction, compose_frame
from engine.renderer import render_scene, lerp

WIDTH, HEIGHT, FPS = 960, 540, 30
TOTAL_DURATION = 10.0
WALK_END_T = 8.0          # walking (and the walk+wave overlap) stops here
TRIP_START_T = 8.0
TRIP_END_T = 9.5

WALK_START_X_FRAC = 0.12
WALK_END_X_FRAC = 0.62    # character stops walking partway across, then trips


def build_timeline():
    return [
        ScheduledAction(layer="lower_body", action_name="walk", start=0.0, end=WALK_END_T),
        ScheduledAction(layer="upper_body", action_name="wave", start=2.0, end=5.0),
        ScheduledAction(layer="full_body", action_name="trip", start=TRIP_START_T, end=TRIP_END_T),
    ]


def make_walk_x_fn(width):
    start_x = width * WALK_START_X_FRAC
    end_x = width * WALK_END_X_FRAC

    def walk_x_fn(t):
        if t >= WALK_END_T:
            return end_x
        frac = t / WALK_END_T
        return lerp(start_x, end_x, frac)

    return walk_x_fn


def main():
    timeline = build_timeline()
    walk_x_fn = make_walk_x_fn(WIDTH)

    def compose_frame_fn(t):
        return compose_frame(t, timeline)

    out = render_scene(
        compose_frame_fn=compose_frame_fn,
        output_path="milestone_scene2.mp4",
        duration=TOTAL_DURATION,
        width=WIDTH, height=HEIGHT, fps=FPS,
        background_color=(255, 255, 255),
        walk_x_fn=walk_x_fn,
        zoom_start=1.0, zoom_end=1.35,
    )
    print(f"Rendered -> {out}")


if __name__ == "__main__":
    main()