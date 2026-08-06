from engine.renderer import render_scene


WIDTH = 960
HEIGHT = 540


# Simple standing stickman pose
POSE = {
    "head": (0, -70),
    "neck": (0, -55),
    "chest": (0, -30),
    "pelvis": (0, 0),

    "l_shoulder": (0, -30),
    "l_elbow": (-18, -12),
    "l_hand": (-16, 8),

    "r_shoulder": (0, -30),
    "r_elbow": (18, -12),
    "r_hand": (16, 8),

    "l_hip": (-8, 0),
    "l_knee": (-10, 35),
    "l_foot": (-10, 68),

    "r_hip": (8, 0),
    "r_knee": (10, 35),
    "r_foot": (10, 68),
}


def compose_frame(t):
    return POSE


def main():

    render_scene(
        compose_frame_fn=compose_frame,
        output_path="outputs/milestone1_test.mp4",
        duration=3,
        width=WIDTH,
        height=HEIGHT,
        fps=30,
    )

    print("Finished rendering")


if __name__ == "__main__":
    main()