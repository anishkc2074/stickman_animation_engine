from engine.scene import Scene
from library.character import Character


# -----------------------------
# Create scene
# -----------------------------

scene = Scene()


# -----------------------------
# Create characters
# -----------------------------

hero = Character(
    name="Hero",
    position=(250, 350),
    scale=1.0,
)

friend = Character(
    name="Friend",
    position=(600, 350),
    scale=1.0,
)

scene.add_character(hero)
scene.add_character(friend)


# -----------------------------
# Assign animations
# -----------------------------

scene.play(
    hero,
    "walk",
    layer="lower_body",
    start=0,
    duration=4,
)

scene.play(
    friend,
    "wave",
    layer="upper_body",
    start=0,
    duration=4,
)


# -----------------------------
# Assign movement
# -----------------------------

scene.move(
    hero,
    from_position=(570, 350),
    to_position=(250, 350),
    start=0,
    end=4,
)


# -----------------------------
# Render animation
# -----------------------------

scene.render(
    output_path="outputs/two_character_animation.mp4",
    duration=4,
    fps=30,
)

print("Two character animation complete")