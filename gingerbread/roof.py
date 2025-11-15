from build123d import *
from ocp_vscode import *

from .spec import *

slot_base = 20


class RoofSlot:
    part: Part

    def __init__(self):
        with BuildPart() as part:
            with BuildSketch() as main:
                t = Triangle(
                    a=slot_base,
                    B=roof_angle,
                    C=roof_angle,
                    align=(Align.CENTER, Align.MAX),
                )
                cutout = t.moved(Location(Vector(Y=-wall_thickness)))
                add(cutout, mode=Mode.SUBTRACT)
            p = extrude(amount=guide_thickness, mode=Mode.PRIVATE)
            p = p.move(Location(Vector(Z=(wall_thickness + tolerance) / 2)))
            add(p)
            mirror(about=Plane.top)
        self.part = part.part
        self.part.label = "slot_part"
        self.main = main.sketch
        self.main.label = "main"


class Roof:
    def __init__(self):
        with BuildPart() as part:
            with BuildSketch() as main:
                t = Triangle(
                    a=house_width + 2 * roof_overhang,
                    B=roof_angle,
                    C=roof_angle,
                    align=(Align.CENTER, Align.MIN),
                )
                cutout = t.moved(Location(Vector(Y=-wall_thickness)))
                peak_inner = cutout.vertices().sort_by(Axis.Y)[-1]
                add(cutout, mode=Mode.SUBTRACT)
            extrude(amount=house_length / 2 + roof_overhang)

            with Locations(
                (0, peak_inner.Y, (house_length / 2) + (wall_thickness / 2))
            ):
                add(RoofSlot().part)

            mirror(about=Plane.top)

        self.part = part.part
        self.main = main.sketch

        self.part.label = "part"
        self.main.label = "main"


roof = Roof()
push_object(
    ShapeList([roof.part, roof.main]),
    name="Roof",
)
