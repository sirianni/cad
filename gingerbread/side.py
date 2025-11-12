from build123d import *
from ocp_vscode import *

from .cutouts import corner_notch_x_size, corner_notch_y_size
from .spec import *

with BuildPart() as part:
    part.label = "part"
    with BuildSketch(Plane.YZ) as main:
        main.label = "main"
        Rectangle(house_width, house_height, align=Align.MIN)

        with Locations((house_width / 2, house_height, 0)):
            Triangle(a=house_width, B=40, C=40, align=(Align.CENTER, Align.MIN))

    extrude(amount=-wall_thickness)

    with BuildSketch(Plane.XY) as support:
        support.label = "support"
        with Locations((0, corner_notch_y_size / 2)):
            r = Rectangle(
                corner_notch_x_size,
                corner_notch_y_size / 2,
                align=(Align.MIN, Align.MIN),
            )
        mirror(about=Plane.ZX.offset(house_width / 2))
    extrude(amount=house_height)

push_object(
    ShapeList([part, main, support]),
    name="Side",
)
