from dataclasses import dataclass, field


@dataclass
class ActionMeta:
    name: str
    layer: str
    kind: str
    category: str = "movement"
    emotion: str = "neutral"
    speed: float = 1.0
    can_blend: bool = True
    compatible_with: list = field(default_factory=list)