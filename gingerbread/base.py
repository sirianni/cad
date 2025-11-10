from build123d import *
from ocp_vscode import show_all

from .spec import *

brim_size = 20

outline_thickness = 1.2
outline_height = 16

corner_notch_x_size = 4
corner_notch_y_size = 8

with BuildPart() as base:
    with BuildSketch() as corner_cutouts:
        with Locations(
            (
                house_size_x / 2 - corner_notch_x_size / 2,
                house_size_y / 2 - corner_notch_y_size / 2,
            )
        ):
            Rectangle(corner_notch_x_size, corner_notch_y_size)
        mirror(about=Plane.YZ)
        mirror(about=Plane.XZ)

    with BuildSketch() as brim:
        Rectangle(house_size_x + 2 * brim_size, house_size_y + 2 * brim_size)
        offset(amount=-(brim_size + outline_thickness), mode=Mode.SUBTRACT)
        add(corner_cutouts.sketch)
    extrude(amount=thickness)

    with BuildSketch() as outline:
        wires = brim.sketch.face().inner_wires()
        assert len(wires) == 1
        make_face(wires[0])
        offset(amount=-outline_thickness, mode=Mode.SUBTRACT)

        with Locations(
            (-door_x_offset, -house_size_y / 2), (door_x_offset, house_size_y / 2)
        ):
            Rectangle(door_size, 50, mode=Mode.SUBTRACT)

    extrude(amount=outline_height)


show_all()

export_step(base.part, "gb_base.step")
