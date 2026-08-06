from library.character import Character
from engine.compositor import compose_frame, ScheduledAction


hero = Character(
    name="Hero",
    scale=1.2,
    position=(300, 300),
    body_color="blue"
)


timeline = [
    ScheduledAction(
        layer="lower_body",
        action_name="walk",
        start=0,
        end=5
    )
]


pose = compose_frame(2.0, timeline)

print("Character:", hero.name)
print("Pose joints:", len(pose))
print("Head:", pose["head"])
print("Left foot:", pose["l_foot"])
