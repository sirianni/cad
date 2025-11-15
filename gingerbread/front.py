import logging

from build123d import *
from ocp_vscode import *

from .cutouts import corner_notch_x_size, corner_notch_y_size
from .spec import *
from .window import Window

window_x_offset = 95
window_y_offset = 50

overhang_length = corner_notch_x_size + 6

logger = logging.getLogger(__name__)


class Front:
    part: Part
    main: Sketch
    support: Sketch

    def __init__(self, with_door=True, with_window=True):
        with BuildPart() as part:
            with BuildSketch(Plane.front) as main:
                Rectangle(house_length, house_height, align=Align.MIN)

                if with_door:
                    with Locations((door_corner_offset, 0)):
                        Rectangle(
                            door_width, door_height, align=Align.MIN, mode=Mode.SUBTRACT
                        )
            extrude(amount=wall_thickness)

            if with_window:
                window_plane = Plane.front.offset(wall_thickness)
                window_plane = window_plane.shift_origin(
                    window_plane.from_local_coords((window_x_offset, window_y_offset))
                )
                Window(window_plane)

            with BuildSketch(Plane.top) as support:
                Rectangle(
                    corner_notch_x_size,
                    corner_notch_y_size / 2,
                    align=(Align.MIN, Align.MIN),
                )
                Rectangle(
                    wall_thickness,
                    wall_thickness,
                    align=(Align.MAX, Align.MAX),
                )
                mirror(about=Plane.right.offset(house_length / 2))
            extrude(amount=house_height)

        self.part = part.part
        self.main = main.sketch
        self.support = support.sketch

        self.part.label = "part"
        self.main.label = "main"
        self.support.label = "support"

    def push_object(self):
        push_object(
            ShapeList([self.part, self.main, self.support]),
            name="Front",
        )


front = Front()
front.push_object()
