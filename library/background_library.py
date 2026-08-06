from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List


@dataclass
class Background:
    name: str
    image_path: str
    category: str = "General"
    ground_y: int = 390
    sky_color: tuple = (135, 206, 235)
    tags: List[str] = None

    def __post_init__(self):
        if self.tags is None:
            self.tags = []


class BackgroundLibrary:
    def __init__(self):
        self.backgrounds: Dict[str, Background] = {}

    def register(self, background: Background):
        self.backgrounds[background.name.lower()] = background

    def get(self, name: str):
        return self.backgrounds.get(name.lower())

    def search(self, keyword: str):
        keyword = keyword.lower()
        return [
            bg for bg in self.backgrounds.values()
            if keyword in bg.name.lower()
            or keyword in bg.category.lower()
            or any(keyword in tag.lower() for tag in bg.tags)
        ]

    def all(self):
        return list(self.backgrounds.values())


background_library = BackgroundLibrary()


background_library.register(
    Background(
        name="Office",
        image_path="assets/backgrounds/office.png",
        category="Indoor",
        ground_y=390,
        tags=["office", "computer", "desk"]
    )
)

background_library.register(
    Background(
        name="Forest",
        image_path="assets/backgrounds/forest.png",
        category="Outdoor",
        ground_y=420,
        tags=["trees", "nature"]
    )
)

background_library.register(
    Background(
        name="Village",
        image_path="assets/backgrounds/village.png",
        category="Outdoor",
        ground_y=410,
        tags=["houses", "road"]
    )
)