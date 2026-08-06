from engine.compositor import ScheduledAction, compose_frame
from engine.renderer import render_scene, lerp


WIDTH = 960
HEIGHT = 540
FPS = 30

DURATION = 10.0


def build_timeline():

    return [
        ScheduledAction(
            layer="lower_body",
            action_name="walk",
            start=0.0,
            end=8.0
        ),

        ScheduledAction(
            layer="upper_body",
            action_name="wave",
            start=2.0,
            end=5.0
        ),

        ScheduledAction(
            layer="full_body",
            action_name="trip",
            start=8.0,
            end=9.5
        )
    ]


def make_walk_x(width):

    start = width * 0.12
    end = width * 0.62

    def move(t):

        if t >= 8.0:
            return end

        return lerp(
            start,
            end,
            t / 8.0
        )

    return move


def main():

    timeline = build_timeline()

    def compose(t):
        return compose_frame(
            t,
            timeline
        )


    output = render_scene(
        compose_frame_fn=compose,
        output_path="milestone3_json.mp4",
        duration=DURATION,
        width=WIDTH,
        height=HEIGHT,
        fps=FPS,
        walk_x_fn=make_walk_x(WIDTH),
        zoom_start=1.0,
        zoom_end=1.35
    )


    print("Rendered:", output)


if __name__ == "__main__":
    main()