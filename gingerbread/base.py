from build123d import *
from ocp_vscode import *

from .cutouts import corner_cutouts
from .spec import *

brim_size = 20

outline_thickness = 1.2
outline_height = 16

with BuildPart() as part:
    part.label = "part"

    with BuildSketch() as brim:
        brim.label = "brim"
        Rectangle(house_length + 2 * brim_size, house_height + 2 * brim_size)
        offset(amount=-(brim_size), mode=Mode.SUBTRACT)
        origin_corner = [
            v for v in brim.face().inner_wires().vertices() if v.X < 0 and v.Y < 0
        ][0]
        add(corner_cutouts.sketch)

    extrude(amount=thickness)

    with BuildSketch() as outline:
        outline.label = "outline"
        wires = brim.sketch.face().inner_wires()
        assert len(wires) == 1
        make_face(wires[0])
        offset(amount=-outline_thickness, mode=Mode.SUBTRACT)

        with Locations(origin_corner + Vector(X=door_corner_offset)):
            door = Rectangle(
                door_width, 10, align=(Align.MIN, Align.CENTER), mode=Mode.SUBTRACT
            )

        add(door.moved(Rotation(Z=180)), mode=Mode.SUBTRACT)

    extrude(amount=outline_height)

push_object(
    ShapeList([part, corner_cutouts, brim, outline]),
    name="Base",
)
