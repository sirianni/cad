from build123d import *
from ocp_vscode import *

from .spec import *

corner_notch_x_size = 2
corner_notch_y_size = 4

with BuildSketch() as corner_cutouts:
    corner_cutouts.label = "corner_cutouts"
    with Locations(
        (
            house_length / 2 - corner_notch_x_size / 2,
            house_width / 2 - corner_notch_y_size / 2,
        )
    ):
        Rectangle(corner_notch_x_size, corner_notch_y_size)
    mirror(about=Plane.YZ)
    mirror(about=Plane.XZ)
