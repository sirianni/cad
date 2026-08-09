"""D-shaft knob — translated from d_shaft_knob_simple.scad to build123d."""

from build123d import *
from ocp_vscode import *

# ---------- Core dimensions ----------
knob_diameter = 39        # circular base
base_height = 5           # base thickness
knob_height = 20          # total height
grip_width = 12           # fin width
grip_length = 39          # fin length
shaft_diameter = 7        # D-post diameter
shaft_flat_chord = 5      # flat width of the D
shaft_depth = 10          # socket depth
socket_clearance = 0.2    # print clearance for the bore

# ---------- Derived ----------
base_radius = knob_diameter / 2
shaft_radius = shaft_diameter / 2
grip_rise = knob_height - base_height
nominal_flat_y = -((shaft_radius ** 2 - (shaft_flat_chord / 2) ** 2) ** 0.5)
socket_flat_y = nominal_flat_y - socket_clearance

d_r = shaft_radius + socket_clearance

# ---------- D-profile sketch (flat on -Y, pointer on +Y) ----------
with BuildSketch() as d_profile:
    d_profile.label = "d_profile"
    Circle(radius=d_r)
    with Locations((0, socket_flat_y)):
        Rectangle(
            2 * d_r,
            d_r * 2,
            align=(Align.CENTER, Align.MAX),
            mode=Mode.SUBTRACT,
        )

# ---------- Build the knob ----------
with BuildPart() as knob:
    knob.label = "d_shaft_knob"

    # Base cylinder (flush at origin, extends +Z)
    Cylinder(
        radius=base_radius,
        height=base_height,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )

    # Fin / Grip on top of the base (hull of two circles, oriented along Y)
    grip_r = grip_width / 2
    grip_straight = grip_length - grip_width
    with BuildSketch(Plane.XY.offset(base_height)):
        with Locations((0, -grip_straight / 2)):
            Circle(radius=grip_r)
        with Locations((0, grip_straight / 2)):
            Circle(radius=grip_r)
        make_hull()
    extrude(amount=grip_rise)

    # Subtract the D-shaft socket (sketch back on XY plane at z=0)
    with BuildSketch(Plane.XY):
        add(d_profile.sketch)
    extrude(amount=shaft_depth, mode=Mode.SUBTRACT)

# ---------- Display ----------
knob_part = knob.part
knob_part.color = "#ea5545"

push_object(knob_part, name="D-Shaft Knob")
show_objects()