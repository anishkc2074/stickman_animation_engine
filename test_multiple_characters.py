from library.character import Character


hero = Character(
    name="Hero",
    scale=1.2,
    position=(200, 300),
    body_color="blue"
)

friend = Character(
    name="Friend",
    scale=0.8,
    position=(500, 300),
    body_color="red"
)


characters = [
    hero,
    friend
]


for character in characters:
    print(character.info())