# D-Shaft Knob (Simplified)

A hand-editable OpenSCAD model of a D-shaft appliance knob.

## What's inside

| File | Purpose |
|------|---------|
| `d_shaft_knob_simple.scad` | Simplified model (~50 lines, 7 top-level parameters) |
| `d_shaft_knob.scad` | Original full-featured model (rounded edges, hub, pointer notch, fit coupon) |

## Quick start

Open `d_shaft_knob_simple.scad` in [OpenSCAD](https://openscad.org/) and change any of the **Core dimensions** at the top:

```scad
knob_diameter     = 39;   // round base diameter
base_height       = 5;    // base thickness
knob_height       = 20;   // total height (base + fin)
grip_width        = 12;   // fin thickness
grip_length       = 39;   // fin end-to-end length
shaft_diameter    = 7;    // D-post round diameter
shaft_flat_chord  = 5;    // flat width of the D
shaft_depth       = 10;   // socket bore depth
socket_clearance  = 0.2;  // extra radius for print fit
```

## Editing the fit

If the printed socket is too tight or too loose, change **only** `socket_clearance`:

| Problem | Fix |
|---------|-----|
| Knob won't press on | Increase `socket_clearance` (try 0.3) |
| Too loose, wobbles | Decrease `socket_clearance` (try 0.1) |

## Export for printing

From the OpenSCAD GUI:

1. **Render** (`F6`) to evaluate the mesh.
2. **Export → STL** (`F7`) for slicing.

Or from the command line:

```bash
openscad d_shaft_knob_simple.scad -o knob.stl
```

## Print orientation

Print with the **flat base face on the bed** (Z=0 down). No supports needed.

## Design notes

- **+Y** is the pointer / 12-o'clock direction.
- The **D flat** is on **−Y** (opposite the pointer).
- The fin is a straight extrusion with semicircular ends — no rounding or draft angles.
- `$fn = 48` gives a smooth enough preview; raise it for final export if desired.
