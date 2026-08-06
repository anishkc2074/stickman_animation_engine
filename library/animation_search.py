from library.asset_loader import load_animation
import os


ASSET_FOLDER = os.path.join(
    os.path.dirname(__file__),
    "animations"
)


def exists(name):
    path = os.path.join(
        ASSET_FOLDER,
        f"{name}.json"
    )

    return os.path.exists(path)


def get(name):
    if not exists(name):
        return None

    return load_animation(name)


def search(category=None, emotion=None, layer=None):
    results = []

    for filename in os.listdir(ASSET_FOLDER):
        if not filename.endswith(".json"):
            continue

        name = filename.replace(".json", "")

        action = load_animation(name)
        meta = action["meta"]

        if category is not None and meta.category != category:
            continue

        if emotion is not None and meta.emotion != emotion:
            continue

        if layer is not None and meta.layer != layer:
            continue

        results.append(name)

    return results


def compatible_with(name):
    action = get(name)

    if action is None:
        return []

    return list(action["meta"].compatible_with)


def missing_from(names):
    return [
        name
        for name in names
        if not exists(name)
    ]