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


for t in [0, 1, 2, 3, 4]:
    pose = compose_frame(t, timeline)

    print("\nTime:", t)
    print("Left foot:", pose["l_foot"])
    print("Right hand:", pose["r_hand"])