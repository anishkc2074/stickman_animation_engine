from engine.compositor import ScheduledAction, compose_frame


timeline = [
    ScheduledAction(
        layer="lower_body",
        action_name="walk",
        start=0,
        end=5
    ),

    ScheduledAction(
        layer="upper_body",
        action_name="wave",
        start=1,
        end=4
    )
]


pose = compose_frame(2.0, timeline)


print("Joints:", len(pose))
print("Head:", pose["head"])
print("Left foot:", pose["l_foot"])