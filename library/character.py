"""
library/character.py

Defines a reusable character.

Character = who is moving.
Animation = how it moves.

Keeping these separate allows multiple characters to share the same
animation system later.
"""

from library.rig import IDLE_POSE


class Character:

    def __init__(
        self,
        name="stickman",
        scale=1.0,
        position=(0, 0),
        body_color="black"
    ):
        self.name = name
        self.scale = scale
        self.position = position
        self.body_color = body_color

        # Facing direction
        self.direction = "right"

        # Facial expression
        self.expression = "neutral"

        # Default standing pose
        self.rest_pose = dict(IDLE_POSE)


    def info(self):
        """
        Return basic character information.
        """

        return {
            "name": self.name,
            "scale": self.scale,
            "position": self.position,
            "body_color": self.body_color,
            "direction": self.direction,
            "expression": self.expression,
        }


    def get_pose(self):
        """
        Return the current character pose.

        Later this will be replaced by the animated pose generated
        by the compositor.
        """

        return dict(self.rest_pose)


    def set_position(self, x, y):
        """
        Move character location.
        """

        self.position = (x, y)


    def set_scale(self, scale):
        """
        Change character size.
        """

        self.scale = scale


    def set_color(self, color):
        """
        Change character appearance color.
        """

        self.body_color = color


    def turn_left(self):
        """
        Face left.
        """

        self.direction = "left"


    def turn_right(self):
        """
        Face right.
        """

        self.direction = "right"


    def set_direction(self, direction):
        """
        Change facing direction.
        """

        if direction in ["left", "right"]:
            self.direction = direction


    def set_expression(self, expression):
        """
        Change facial expression.
        """

        self.expression = expression


    def get_expression(self):
        """
        Return current facial expression.
        """

        return self.expression