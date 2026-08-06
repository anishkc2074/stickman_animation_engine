from library.asset_loader import load_animation


animations = [
    "walk",
    "wave",
    "trip"
]


for name in animations:
    animation = load_animation(name)

    print(name, "loaded")

    meta = animation["meta"]

    print("Layer:", meta.layer)
    print("Kind:", meta.kind)
    print("---")