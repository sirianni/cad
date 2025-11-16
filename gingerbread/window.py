import logging

from build123d import *

from .spec import *

window_width = 20
window_height = 25
shutter_width = 10
num_slats = 8
shutter_depth = 0.25


logger = logging.getLogger(__name__)


class Window:
    def __init__(self, plane):
        # logger.info(f"Creating window at plane: {plane}")
        with BuildSketch(plane) as cutout:
            cutout.label = "window_cutout"
            Rectangle(window_width, window_height)

        extrude(to_extrude=cutout.sketch, amount=-wall_thickness, mode=Mode.SUBTRACT)

        with BuildSketch(plane) as shutters:
            shutters.label = "window_shutters"
            left_x = -window_width / 2 - shutter_width / 2
            right_x = window_width / 2 + shutter_width / 2

            with Locations((left_x, 0), (right_x, 0)):
                # Outer recessed rectangle (outline only)
                Rectangle(shutter_width, window_height)
                Rectangle(shutter_width - 1, window_height - 1, mode=Mode.SUBTRACT)

                # Interior rectangles for slats (will be recessed)
                slat_spacing = window_height / (num_slats + 1)
                for i in range(1, num_slats + 1):
                    y_offset = -window_height / 2 + i * slat_spacing
                    with Locations((0, y_offset)):
                        Rectangle(shutter_width - 1, slat_spacing - 1.5)

        extrude(to_extrude=shutters.sketch, amount=-shutter_depth, mode=Mode.SUBTRACT)
