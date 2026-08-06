from library.animation_search import get as get_action
from engine.compositor import ScheduledAction, compose_frame


class CharacterController:

    def __init__(self, character):
        self.character = character
        self.timeline = []


    def play(
        self,
        action_name,
        layer="full_body",
        start=0,
        duration=1.0
    ):
        """
        Add an animation action.
        """

        self.timeline.append(
            ScheduledAction(
                layer=layer,
                action_name=action_name,
                start=start,
                end=start + duration
            )
        )


    def clear(self):
        """
        Remove all animations.
        """

        self.timeline = []


    def get_pose(self, time):
        """
        Calculate character pose at time.
        """

        if not self.timeline:
            return self.character.get_pose()

        return compose_frame(
            time,
            self.timeline
        )