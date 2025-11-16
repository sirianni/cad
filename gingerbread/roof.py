from build123d import *
from ocp_vscode import *

from .cutouts import corner_notch_x_size
from .spec import *

# Could calculate this from roof angle and house dimensions...
slot_base = 80


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
            p = p.move(Location(Vector(Z=-(wall_thickness + tolerance) / 2)))

            add(p)
            # Don't need exterior guide for now
            # mirror(about=Plane.top)
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
                        20,
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

            mirror(about=Plane.top)
            peak_inner_edges = edges().filter_by(Axis.Z).group_by(Axis.Y)[-2]
            chamfer(peak_inner_edges, length=2)

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
