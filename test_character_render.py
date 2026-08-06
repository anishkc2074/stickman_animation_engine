from library.character import Character


hero = Character(
    name="Hero",
    scale=1.5,
    position=(300, 300),
    body_color="blue"
)

pose = hero.get_pose()

print("Character:", hero.name)
print("Joints:", len(pose))
print("Position:", hero.position)