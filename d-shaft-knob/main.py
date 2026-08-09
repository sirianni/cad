"""D-shaft knob — translated from d_shaft_knob_simple.scad to build123d."""

from pathlib import Path

from build123d import *
from ocp_vscode import push_object, show_objects

# ---------- Core dimensions ----------
knob_diameter = 39  # circular base
base_height = 5  # base thickness
knob_height = 20  # total height
grip_width = 12  # fin width
grip_length = 39  # fin length
grip_top_radius = 20  # arc radius for rounding the grip top
grip_top_fillet_radius = 1
base_top_fillet_radius = 1
interior_fillet_radius = 1
home_marker_width = 7  # engraved triangle base width (X)
home_marker_length = 10  # engraved triangle length (Y); point faces +Y
home_marker_depth = 0.6  # radial depth into the rounded grip top
home_marker_y = 6  # +Y is opposite the D-shaft flat
shaft_diameter = 7  # D-post diameter
shaft_flat_chord = 5  # flat width of the D
shaft_depth = 10  # socket depth
socket_clearance = 0.0  # print clearance for the bore

# ---------- Derived ----------
base_radius = knob_diameter / 2
shaft_radius = shaft_diameter / 2
grip_rise = knob_height - base_height
grip_top_center_z = base_height + grip_rise - grip_top_radius
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

# ---------- Fuse and blend the grip into the base ----------
base.part.label = "Base"
grip.part.label = "Grip"
knob_part = base.part.fuse(grip.part)
interior_edges = [
    edge
    for edge in knob_part.edges()
    if abs(abs(edge.center().X) - grip_width / 2) < 1e-6
    and abs(edge.center().Z - base_height) < 1e-6
    and edge.length > grip_length / 2
]
knob_part = knob_part.fillet(interior_fillet_radius, interior_edges)

# Engraved home-position triangle on the +Y side, opposite the D-shaft flat.
# Limit the cut with a cylindrical shell so its floor follows the rounded grip
# top. This preserves the full triangle rather than clipping its point.
with BuildPart() as home_marker_cut:
    Cylinder(
        radius=grip_top_radius,
        height=grip_width + 2,
        rotation=(0, 90, 0),
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    )
    Cylinder(
        radius=grip_top_radius - home_marker_depth,
        height=grip_width + 2,
        rotation=(0, 90, 0),
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
        mode=Mode.SUBTRACT,
    )
    with BuildSketch(Plane.XY):
        Polygon(
            (0, home_marker_y + home_marker_length / 2),
            (-home_marker_width / 2, home_marker_y - home_marker_length / 2),
            (home_marker_width / 2, home_marker_y - home_marker_length / 2),
        )
    extrude(amount=knob_height, both=True, mode=Mode.INTERSECT)

knob_part = knob_part.cut(home_marker_cut.part)
home_marker_cut.part.label = "Home-marker engraving cut"
knob_part.label = "D-Shaft Knob"
knob_part.color = "#ea5545"

# ---------- Exports ----------
build_directory = Path(__file__).parent / "build"
build_directory.mkdir(exist_ok=True)
export_step(knob_part, build_directory / "d_shaft_knob.step")
export_stl(knob_part, build_directory / "d_shaft_knob.stl")

# Keep the final knob plus its individually toggleable construction components.
push_object(knob_part, name="D-Shaft Knob")
push_object(
    {
        "Base": base.part,
        "Grip": grip.part,
        "Home-marker engraving cut": home_marker_cut.part,
    },
    name="Construction components",
)
show_objects()
