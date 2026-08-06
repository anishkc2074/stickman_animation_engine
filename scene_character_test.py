from library.character import Character


class Scene:

    def __init__(self):
        self.characters = []

    def add_character(self, character):
        self.characters.append(character)

    def list_characters(self):
        for c in self.characters:
            print(
                c.name,
                "at",
                c.position,
                "scale",
                c.scale
            )


scene = Scene()


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


scene.add_character(hero)
scene.add_character(friend)


scene.list_characters()