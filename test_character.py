from library.character import Character


hero = Character(
    name="Hero",
    scale=1.2,
    position=(200, 300),
    body_color="blue"
)


print(hero.info())