from dataclasses import dataclass, field

from src.renderers import Renderer


@dataclass
class PlotSpec:
    channel: str
    condition: str = None
    row: int = 1
    col: int  = 1
    renderer: Renderer = None
    events:    list[str] = field(default_factory=list)  # ← e.g. ["max", "min"]
    title: str = ""
    x_label: str = ""
    y_label: str = ""

    def __post_init__(self):
        if not self.title:
            self.title = f"{self.channel} - {self.condition}"