from build123d import *
from ocp_vscode import *

from .cutouts import corner_cutouts
from .spec import *

brim_size = 20
brim_thickness = 3

outline_height = 15
groove_thickness = wall_thickness + tolerance
extension_size = 15

with BuildPart() as part:
    part.label = "part"

    with BuildSketch() as brim:
        brim.label = "brim"
        outer_rect = Rectangle(
            house_length + 2 * brim_size, house_width + 2 * brim_size
        )
        offset(amount=-(brim_size), mode=Mode.SUBTRACT)
        origin_corner = [
            v for v in brim.face().inner_wires().vertices() if v.X < 0 and v.Y < 0
        ][0]
        add(corner_cutouts.sketch)
    extrude(amount=brim_thickness)

    top_face = part.faces().sort_by(Axis.Z)[-1]

    with BuildSketch(top_face) as groove:
        groove.label = "groove"
        Rectangle(
            house_length + 2 * groove_thickness, house_width + 2 * groove_thickness
        )
        offset(amount=-groove_thickness, mode=Mode.SUBTRACT)
        add(corner_cutouts.sketch)
    extrude(amount=-2, mode=Mode.SUBTRACT)

    with BuildSketch() as outline:
        outline.label = "outline"
        wires = brim.sketch.face().inner_wires()
        assert len(wires) == 1
        make_face(wires[0])
        offset(amount=-guide_thickness, mode=Mode.SUBTRACT)

        with Locations(origin_corner + Vector(X=door_corner_offset)):
            door = Rectangle(
                door_width, 10, align=(Align.MIN, Align.CENTER), mode=Mode.SUBTRACT
            )

        # No back door for now
        # add(door.moved(Rotation(Z=180)), mode=Mode.SUBTRACT)

    extrude(amount=outline_height)

    with BuildSketch() as extension:
        Rectangle(outer_rect.width, outer_rect.rectangle_height + extension_size * 2)
        Rectangle(outer_rect.width, outer_rect.rectangle_height, mode=Mode.SUBTRACT)
    extrude(amount=brim_thickness)

push_object(
    ShapeList([part, corner_cutouts, brim, outline, groove, extension]),
    name="Base",
)
