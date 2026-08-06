"""
engine/movement.py

Character movement interpolation.
"""


class Movement:

    def __init__(
        self,
        start_position,
        end_position,
        start_time,
        end_time,
    ):
        self.start_position = start_position
        self.end_position = end_position
        self.start_time = start_time
        self.end_time = end_time

    def position_at(self, t):

        if t <= self.start_time:
            return self.start_position

        if t >= self.end_time:
            return self.end_position

        progress = (
            (t - self.start_time)
            / (self.end_time - self.start_time)
        )

        x = (
            self.start_position[0]
            + (self.end_position[0] - self.start_position[0])
            * progress
        )

        y = (
            self.start_position[1]
            + (self.end_position[1] - self.start_position[1])
            * progress
        )

        return (x, y)

    def direction(self):
        """
        Return movement direction.
        """

        if self.end_position[0] > self.start_position[0]:
            return "right"

        elif self.end_position[0] < self.start_position[0]:
            return "left"

        return None    