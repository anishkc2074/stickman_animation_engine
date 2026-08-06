"""
library/face.py

Simple facial expression system.

Expressions are kept separate from the character rig.
The renderer uses this data to draw readable faces.
"""


FACE_STATES = {

    "neutral": {
        "eyes": "normal",
        "mouth": "straight",
        "eyebrows": "neutral",
    },


    "happy": {
        "eyes": "normal",
        "mouth": "smile",
        "eyebrows": "raised",
    },


    "sad": {
        "eyes": "normal",
        "mouth": "sad",
        "eyebrows": "tilted",
    },


    "angry": {
        "eyes": "narrow",
        "mouth": "flat",
        "eyebrows": "angry",
    },


    "surprised": {
        "eyes": "wide",
        "mouth": "open",
        "eyebrows": "raised",
    },

}



def get_face(expression="neutral"):
    """
    Return facial expression settings.

    Unknown expressions fall back to neutral.
    """

    return FACE_STATES.get(
        expression,
        FACE_STATES["neutral"]
    )