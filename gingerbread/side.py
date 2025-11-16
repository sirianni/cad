import logging

from build123d import *
from ocp_vscode import *

from .cutouts import corner_notch_x_size, corner_notch_y_size
from .spec import *
from .window import Window

window_x_offset = house_width / 2
window_y_offset = 50

logger = logging.getLogger(__name__)


class Side:
    part: Part
    main: Sketch
    support: Sketch
    peak_vertex: Vertex

    def __init__(self):
        with BuildPart() as part:
            with BuildSketch(Plane.front) as main:
                Rectangle(house_width, house_height, align=Align.MIN)

                with Locations((house_width / 2, house_height, 0)):
                    Triangle(
                        a=house_width,
                        B=roof_angle,
                        C=roof_angle,
                        align=(Align.CENTER, Align.MIN),
                    )

                self.peak_vertex = main.vertices().sort_by(Axis.Y)[-1]

            extrude(amount=wall_thickness)

            window_plane = Plane.front.offset(wall_thickness)
            window_plane = window_plane.shift_origin(
                window_plane.from_local_coords((window_x_offset, window_y_offset))
            )
            Window(window_plane)

            with BuildSketch(Plane.top) as support:
                with Locations((corner_notch_y_size / 2, 0)):
                    Rectangle(
                        corner_notch_x_size - tolerance,
                        corner_notch_y_size / 2 - tolerance,
                        align=(Align.MIN, Align.MIN),
                    )
                mirror(about=Plane.right.offset(house_width / 2))
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
            name="Side",
        )


side = Side()
side.push_object()
