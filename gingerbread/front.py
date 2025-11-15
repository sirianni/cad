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

            # left_face = part.faces().filter_by(Plane.left).sort_by(Axis.X)[0]
            # top_vertex = left_face.vertices().group_by(Axis.Z)[-1].sort_by(Axis.Y)[0]

            # Cut triangular section at top to match roof angle
            with BuildSketch(Plane.left.offset(wall_thickness)) as roof_cut:
                # pt = roof_cut.workplanes[0].to_local_coords(top_vertex)
                with BuildLine():
                    l1 = PolarLine(
                        start=(0, house_height), angle=0, length=wall_thickness
                    )
                    PolarLine(start=l1.start_point(), angle=-roof_angle, length=30)
                    PolarLine(start=l1.end_point(), angle=-90, length=30)
                make_face()
            extrude(amount=500, both=True, mode=Mode.SUBTRACT)

        self.part = part.part
        self.main = main.sketch
        self.support = support.sketch
        self.roof_cut = roof_cut.sketch

        self.part.label = "part"
        self.main.label = "main"
        self.support.label = "support"
        self.roof_cut.label = "roof_cut"

    def push_object(self):
        push_object(
            ShapeList([self.part, self.main, self.support, self.roof_cut]),
            name="Front",
        )


front = Front()
front.push_object()
