from build123d import *
from ocp_vscode import *

from . import base, front, side
from .spec import *

colors = [
    "#ea5545",
    "#f46a9b",
    "#ef9b20",
    "#edbf33",
    "#ede15b",
    "#bdcf32",
    "#87bc45",
    "#27aeef",
    "#b33dc6",
]
color_index = 0

origin = base.origin_corner

base_part = base.part.part
base_part.label = "base"
base_part.color = colors[color_index]

front_part = front.part.part.moved(Location(origin))
front_part.label = "front"
front_part.color = colors[color_index := color_index + 2]

back_part = front_part.moved(Rotation(Z=180))
back_part.label = "back"
back_part.color = colors[color_index := color_index + 2]

left_part = side.part.part.moved(Location(origin))
left_part.label = "left"
left_part.color = colors[color_index := color_index + 2]

right_part = left_part.mirror(Plane.YZ)
right_part.label = "right"
right_part.color = colors[color_index := color_index + 2]

assembly = Compound(
    label="assembly", children=[base_part, front_part, back_part, left_part, right_part]
)

push_object(assembly, name="Assembly")

export_step(base_part, "base.step")
export_step(front_part, "front.step")
export_step(left_part, "side.step")
