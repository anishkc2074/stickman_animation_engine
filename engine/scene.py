"""
engine/scene.py

Scene object.

A Scene owns:
- Characters
- Animations
- Movements
- Expressions
- Camera settings
- Background
- Props

The renderer asks the Scene what should appear at time t.
"""

from library.character_controller import CharacterController
from engine.movement import Movement
from engine.renderer import render_scene



class Scene:

    def __init__(
        self,
        width=960,
        height=540,
        background_color=(255, 255, 255),
    ):

        self.width = width
        self.height = height
        self.background_color = background_color

        self.characters = []

        self.controllers = {}

        self.movements = {}

        self.expressions = {}

        self.background = None

        self.props = []



    def add_character(self, character):

        self.characters.append(character)

        self.controllers[character] = CharacterController(
            character
        )

        self.movements[character] = []

        self.expressions[character] = []



    def remove_character(self, character):

        self.characters.remove(character)

        if character in self.controllers:
            del self.controllers[character]

        if character in self.movements:
            del self.movements[character]

        if character in self.expressions:
            del self.expressions[character]



    def get_characters(self):

        return list(self.characters)



    def get_controller(self, character):

        return self.controllers[character]



    def play(
        self,
        character,
        action,
        layer,
        start,
        duration,
    ):

        controller = self.get_controller(character)

        controller.play(
            action,
            layer=layer,
            start=start,
            duration=duration,
        )



    def move(
        self,
        character,
        from_position,
        to_position,
        start,
        end,
    ):

        movement = Movement(
            start_position=from_position,
            end_position=to_position,
            start_time=start,
            end_time=end,
        )

        self.movements[character].append(
            movement
        )



    def expression(
        self,
        character,
        expression,
        start,
        duration,
    ):
        """
        Schedule facial expression.
        """

        self.expressions[character].append(
            {
                "expression": expression,
                "start": start,
                "end": start + duration,
            }
        )



    def set_background(self, background):

        self.background = background



    def add_prop(self, name, position):

        self.props.append(
            {
                "name": name,
                "position": position,
            }
        )



    def remove_prop(self, name):

        self.props = [
            prop
            for prop in self.props
            if prop["name"] != name
        ]



    def update_expression(
        self,
        character,
        time,
    ):
        """
        Apply active facial expression.
        """

        current_expression = "neutral"


        for event in self.expressions.get(character, []):

            if (
                event["start"] <= time
                and time <= event["end"]
            ):

                current_expression = event["expression"]


        character.set_expression(
            current_expression
        )



    def compose(self, t):
        """
        Build frame data at time t.
        """

        poses = []


        for character in self.characters:


            # Movement update

            for movement in self.movements[character]:

                character.set_position(
                    *movement.position_at(t)
                )


                direction = movement.direction()


                if direction:

                    character.set_direction(
                        direction
                    )



            # Expression update

            self.update_expression(
                character,
                t
            )



            # Animation pose

            controller = self.get_controller(
                character
            )


            poses.append(
                controller.get_pose(t)
            )


        return {
            "characters": self.characters,
            "poses": poses,
            "background": self.background,
            "props": self.props,
        }



    def render(
        self,
        output_path,
        duration,
        fps=30,
    ):
        """
        Render this scene.
        """

        return render_scene(
            compose_frame_fn=self.compose,
            output_path=output_path,
            duration=duration,
            width=self.width,
            height=self.height,
            fps=fps,
            background_color=self.background_color,
        )