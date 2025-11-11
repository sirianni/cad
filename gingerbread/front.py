from build123d import *
from ocp_vscode import *

from .cutouts import corner_notch_x_size, corner_notch_y_size
from .spec import *

window_width = 30
window_height = 25
window_x_offset = 95
window_y_offset = 50

overhang_x_size = corner_notch_x_size + 2

with BuildPart() as part:
    part.label = "part"
    with BuildSketch(Plane.XZ) as main:
        main.label = "main"
        Rectangle(house_length, house_height, align=Align.MIN)

        with Locations((door_corner_offset, 0)):
            Rectangle(door_width, door_height, align=Align.MIN, mode=Mode.SUBTRACT)

        with Locations((window_x_offset, window_y_offset)):
            Rectangle(
                window_width, window_height, align=Align.CENTER, mode=Mode.SUBTRACT
            )
    extrude(amount=thickness)

    with BuildSketch(Plane.XY) as wraparound:
        wraparound.label = "wraparound"
        with Locations((-2, -thickness, 0)):
            Rectangle(
                overhang_x_size, corner_notch_y_size / 2 + thickness, align=Align.MIN
            )
        top_edge = wraparound.edges().filter_by(Axis.X).sort_by(Axis.Y)[-1]
        with Locations(top_edge.center()):
            Rectangle(
                groove_width,
                groove_depth,
                align=(Align.CENTER, Align.MAX),
                mode=Mode.SUBTRACT,
            )
        mirror(about=Plane.YZ.offset(house_length / 2))
    extrude(amount=house_height)

push_object(
    ShapeList([part, main, wraparound]),
    name="Front",
)
