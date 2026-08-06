from library.character import Character


hero = Character(
    name="Hero",
    position=(250, 300),
    scale=1.0
)

friend = Character(
    name="Friend",
    position=(550, 300),
    scale=1.0
)


characters = [hero, friend]


print("Characters:", len(characters))

for character in characters:
    print(
        "Name:",
        character.name,
        "Position:",
        character.position,
        "Scale:",
        character.scale
    )