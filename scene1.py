from engine.scene import Scene
from library.character import Character

scene = Scene()

hero = Character(
    name="Hero",
    position=(300, 390),
)

friend = Character(
    name="Friend",
    position=(650, 390),
)

scene.add_character(hero)
scene.add_character(friend)

print("Scene created")
print("Characters:")

for character in scene.get_characters():
    print("-", character.name)
    