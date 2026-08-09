"""D-shaft knob — translated from d_shaft_knob_simple.scad to build123d."""

from build123d import *
from ocp_vscode import *

# ---------- Core dimensions ----------
knob_diameter = 39  # circular base
base_height = 5  # base thickness
knob_height = 20  # total height
grip_width = 12  # fin width
grip_length = 39  # fin length
grip_top_radius = 20  # arc radius for rounding the grip top
grip_top_fillet_radius = 1
base_top_fillet_radius = 1
shaft_diameter = 7  # D-post diameter
shaft_flat_chord = 5  # flat width of the D
shaft_depth = 10  # socket depth
socket_clearance = 0.2  # print clearance for the bore

# ---------- Derived ----------
base_radius = knob_diameter / 2
shaft_radius = shaft_diameter / 2
grip_rise = knob_height - base_height
nominal_flat_y = -((shaft_radius**2 - (shaft_flat_chord / 2) ** 2) ** 0.5)
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

# ---------- Base ----------
with BuildPart() as base:
    base.label = "base"

    Cylinder(
        radius=base_radius,
        height=base_height,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )
    fillet(base.part.edges().sort_by(Axis.Z)[-1], radius=base_top_fillet_radius)

    with BuildSketch(Plane.XY):
        add(d_profile.sketch)
    extrude(amount=shaft_depth, mode=Mode.SUBTRACT)

# ---------- Grip ----------
with BuildPart() as grip:
    grip.label = "grip"

    # 1. Model as a rectangular solid, offset up to sit on base
    with Locations((0, 0, base_height - base_top_fillet_radius)):
        Box(
            grip_width,
            grip_length,
            grip_rise + base_top_fillet_radius,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        )

    # 2. Clip to the base's rounded contour
    with Locations((0, 0, base_height - base_top_fillet_radius)):
        Cylinder(
            radius=base_radius,
            height=grip_rise + base_top_fillet_radius,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
            mode=Mode.INTERSECT,
        )

    # 3. Round the top with an arc cut on the long (YZ) face
    with BuildSketch(Plane.YZ):
        with Locations((0, base_height + grip_rise - grip_top_radius)):
            Circle(radius=grip_top_radius)
    extrude(amount=grip_width / 2, both=True, mode=Mode.INTERSECT)

    # 4. D-shaft socket — stays at Z=0, only cuts where it overlaps grip
    with BuildSketch(Plane.XY):
        add(d_profile.sketch)
    extrude(amount=shaft_depth, mode=Mode.SUBTRACT)

    fillet(grip.part.edges().sort_by(Axis.Z)[-2:], radius=grip_top_fillet_radius)

# ---------- Display ----------
base_part = base.part
base_part.label = "base"
base_part.color = "#ea5545"

grip_part = grip.part
grip_part.label = "grip"
grip_part.color = "#f46a9b"

push_object(ShapeList([base_part, grip_part]), name="D-Shaft Knob")
show_objects()
