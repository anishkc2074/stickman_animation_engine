import json
import os

from library.action_meta import ActionMeta


ASSET_FOLDER = os.path.join(
    os.path.dirname(__file__),
    "animations"
)


def load_animation(name):
    path = os.path.join(
        ASSET_FOLDER,
        f"{name}.json"
    )

    with open(path, "r") as f:
        data = json.load(f)

    meta_data = data["meta"]

    data["meta"] = ActionMeta(
        name=meta_data["name"],
        layer=meta_data["layer"],
        kind=meta_data["kind"],
        category=meta_data.get("category", "movement"),
        emotion=meta_data.get("emotion", "neutral"),
        speed=meta_data.get("speed", 1.0),
        can_blend=meta_data.get("can_blend", True),
        compatible_with=meta_data.get(
            "compatible_with",
            []
        ),
    )

    return data