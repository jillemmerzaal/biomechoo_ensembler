from dataclasses import dataclass, field

from src.renderers import Renderer


@dataclass
class PlotSpec:
    channel: str
    condition: str = ""
    row: int = 1
    col: int  =1
    renderer: Renderer = None
    title: str = ""
    x_label: str = ""
    y_label: str = ""

    def __post_init__(self):
        if not self.title:
            self.title = f"{self.channel} - {self.condition}"