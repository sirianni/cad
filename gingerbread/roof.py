from build123d import *
from ocp_vscode import *

from .cutouts import corner_notch_x_size
from .spec import *


class RoofSlot:
    part: Part

    def __init__(self):
        with BuildPart() as part:
            # interior guide
            with BuildSketch() as main:
                t = Triangle(
                    a=80,
                    B=roof_angle,
                    C=roof_angle,
                    align=(Align.CENTER, Align.MAX),
                )
                cutout = t.moved(Location(Vector(Y=-6)))
                add(cutout, mode=Mode.SUBTRACT)
            p = extrude(amount=-guide_thickness, mode=Mode.PRIVATE)
            p = p.move(Location(Vector(Z=-(wall_thickness + tolerance) / 2)))

            add(p)

            # exterior guide
            with BuildSketch() as main:
                t = Triangle(
                    a=50,
                    B=roof_angle,
                    C=roof_angle,
                    align=(Align.CENTER, Align.MAX),
                )
                cutout = t.moved(Location(Vector(Y=-4)))
                add(cutout, mode=Mode.SUBTRACT)
            p = extrude(amount=guide_thickness, mode=Mode.PRIVATE)
            p = p.move(Location(Vector(Z=(wall_thickness + tolerance) / 2)))

            add(p)

        self.part = part.part
        self.part.label = "slot_part"
        self.main = main.sketch
        self.main.label = "main"


class Roof:
    peak_inner: Vertex
    part: Part

    def __init__(self):
        with BuildPart() as part:
            with BuildSketch() as main:
                triangle = Triangle(
                    a=house_width + 2 * roof_overhang,
                    B=roof_angle,
                    C=roof_angle,
                    align=(Align.CENTER, Align.MIN),
                )
                cutout = triangle.moved(Location(Vector(Y=-wall_thickness)))
                self.peak_inner = cutout.vertices().sort_by(Axis.Y)[-1]
                add(cutout, mode=Mode.SUBTRACT)
            extrude(amount=house_length / 2 + roof_overhang)

            with BuildSketch() as guide:
                with Locations((-house_width / 2, 0)):
                    r = Rectangle(
                        guide_thickness,
                        20,  # arbitrary, will be intersected with roof
                        align=(Align.MAX, Align.MIN),
                        mode=Mode.PRIVATE,
                    )
                    r = r.intersect(triangle)
                add(r)
                mirror(about=Plane.left)
            extrude(amount=house_length / 2 - (corner_notch_x_size + 1))

            with Locations(
                (0, self.peak_inner.Y, (house_length / 2) + (wall_thickness / 2))
            ):
                add(RoofSlot().part)

            peak_inner_edge = (
                edges().filter_by(Axis.Z).group_by(Axis.Y)[-2].sort_by(Axis.Z)[0]
            )
            chamfer(peak_inner_edge, length=4)

            mirror(about=Plane.top)

        self.part = part.part
        self.main = main.sketch
        self.guide = guide.sketch

        self.part.label = "part"
        self.main.label = "main"
        self.guide.label = "guide"


roof = Roof()
push_object(
    ShapeList([roof.part, roof.main, roof.guide]),
    name="Roof",
)
