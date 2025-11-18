from build123d import *
from ocp_vscode import *

from .cutouts import corner_notch_x_size
from .spec import *


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

            # Interior front/back guide
            with BuildSketch():
                with Locations(
                    (house_width / 2 - tolerance, 0),
                ):
                    r = Rectangle(
                        guide_thickness,
                        50,  # arbitrary, will be intersected with roof
                        align=(Align.MAX, Align.CENTER),
                        mode=Mode.PRIVATE,
                    )
                    r = r.intersect(triangle)
                add(r)
                mirror(about=Plane.left)
            extrude(amount=house_length / 2 - (corner_notch_x_size + 3))

            # Exterior front/back guide
            with BuildSketch():
                with Locations(
                    (house_width / 2 + wall_thickness + tolerance, 0),
                ):
                    r = Rectangle(
                        guide_thickness,
                        50,  # arbitrary, will be intersected with roof
                        align=(Align.MIN, Align.CENTER),
                        mode=Mode.PRIVATE,
                    )
                    r = r.intersect(triangle)
                add(r)

                # Extend downward past the triangle outline
                bottom_edge = r.edges().filter_by(Axis.X).sort_by(Axis.Y)[0]
                with Locations(bottom_edge.center()):
                    Rectangle(guide_thickness, 3, align=(Align.CENTER, Align.MAX))

                mirror(about=Plane.left)
            extrude(amount=(house_length / 2) * 0.6)

            with Locations(
                (0, self.peak_inner.Y, (house_length / 2) + (wall_thickness / 2))
            ):
                for params in [
                    # (length, y_offset, dir)
                    (80, -6, -1),  # interior
                    (50, -4, 1),  # exterior
                ]:
                    length, y_offset, dir = params
                    with BuildSketch():
                        t = Triangle(
                            a=length,
                            B=roof_angle,
                            C=roof_angle,
                            align=(Align.CENTER, Align.MAX),
                        )
                        cutout = t.moved(Location(Vector(Y=y_offset)))
                        add(cutout, mode=Mode.SUBTRACT)
                    p = extrude(amount=dir * guide_thickness, mode=Mode.PRIVATE)
                    p = p.move(
                        Location(Vector(Z=dir * (wall_thickness + tolerance) / 2))
                    )
                    add(p)

            peak_inner_edge = (
                edges().filter_by(Axis.Z).group_by(Axis.Y)[-2].sort_by(Axis.Z)[0]
            )
            chamfer(peak_inner_edge, length=4)

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
