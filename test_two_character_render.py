from library.character import Character
from engine.renderer import render_scene
from library.rig import IDLE_POSE


hero = Character(
    name="Hero",
    position=(250, 350),
    scale=1.0
)

friend = Character(
    name="Friend",
    position=(550, 350),
    scale=1.0
)


characters = [hero, friend]


def compose(time):
    return {
        "characters": characters,
        "poses": [
            IDLE_POSE,
            IDLE_POSE
        ]
    }


render_scene(
    compose_frame_fn=compose,
    output_path="outputs/two_character_test.mp4",
    duration=2
)

print("Two character render complete")