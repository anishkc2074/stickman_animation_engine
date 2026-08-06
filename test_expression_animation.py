from engine.scene import Scene
from library.character import Character


scene = Scene()


hero = Character(
    name="Hero",
    position=(450,350),
    scale=1.0
)


scene.add_character(hero)


# Test expressions

scene.expression(
    hero,
    "happy",
    start=0,
    duration=1.5
)


scene.expression(
    hero,
    "surprised",
    start=1.5,
    duration=1.5
)


scene.expression(
    hero,
    "angry",
    start=3,
    duration=1
)


scene.render(
    output_path="outputs/expression_test.mp4",
    duration=4,
    fps=30,
)


print("Expression test complete")