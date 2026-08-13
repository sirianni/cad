# D-Shaft Knob Model Guide

This repository contains a parametric CAD model for a D-shaft control knob.
The primary model is [`main.py`](main.py), written with [build123d](https://build123d.readthedocs.io/). It creates the finished solid, writes STEP/STL files, and opens/publishes it through `ocp_vscode`.

## Running the model

Use the project environment; do not invoke the system Python directly:

```bash
uv run main.py
```

This regenerates:

- `build/d_shaft_knob.step`
- `build/d_shaft_knob.stl`

The viewer may print Fontconfig warnings in this environment. They do not indicate a model failure. A successful run ends by starting the viewer (currently on port 3939).

## Coordinate system and orientation

- **Z** is vertical: base bottom is at `Z=0`; the top nominally reaches `Z=knob_height`.
- **X** spans the grip width and is symmetric about `X=0`.
- **Y** spans the grip length.
  - **`+Y`** is the home-marker end and points opposite the D-shaft flat.
  - **`-Y`** is the far end of the grip and is the wide end of the longitudinal taper.
- The D-shaft socket has its flat on **`-Y`**.

Keep this convention when adding features or reversing dimensions: the triangle marker's point faces `+Y`.

## Model structure

`main.py` is organized in the following sequence.

1. **Parameters and derived values**
   - Core size, grip taper values, marker dimensions, and socket dimensions are at the top of the file.
   - Derived radii and D-profile placement follow. Prefer changing the top-level parameters rather than derived calculations.

2. **`d_profile` sketch**
   - A circle is cut by a rectangle to form the D-shaped shaft bore.
   - The same sketch is used to cut both the base and grip, ensuring a continuous socket after they are fused.

3. **`base` part**
   - A cylinder forms the circular base.
   - Its upper outside edge is filleted with `base_top_fillet_radius`.
   - The D-shaped socket is subtracted from `Z=0` to `shaft_depth`.

4. **`grip` part**
   - Two XY trapezoids are lofted: a bottom profile and a top profile.
   - The bottom is at `base_height - base_top_fillet_radius`, allowing it to overlap the base's rounded edge for a clean fuse.
   - The grip is intersected with a base-radius cylinder to keep it inside the circular footprint.
   - It is then intersected with a cylinder sketched on the YZ plane to create the rounded longitudinal top.
   - The socket is cut, then selected upper edges are filleted.

5. **Fusion and home marker**
   - Base and grip are fused into `knob_part`.
   - `home_marker_cut` is a triangular prism limited by a cylindrical shell, so the engraved marker has a floor that follows the rounded grip top.
   - The cut is subtracted from the fused solid.

6. **Export and viewer output**
   - The final part is exported to `build/`.
   - The final solid and individual construction components are pushed to the viewer.

## Changing the grip tapers

The four grip-width parameters control both taper directions:

```python
grip_top_far_width       # top width at -Y
grip_top_marker_width    # top width at +Y
grip_base_far_width      # base width at -Y
grip_base_marker_width   # base width at +Y
```

- **Longitudinal taper:** compare `far` with `marker` at the same height. A larger far value makes the `-Y` end wider.
- **Downward/outward taper:** compare `base` with `top` at the same Y end. A larger base value makes the grip flare toward the base.
- The current values are intentionally asymmetric in both directions; inspect the parameter block in `main.py` as the source of truth.
- Keep widths positive. Very narrow marker-end values can make the marker or top fillets visually dominate the grip.

The top-rounding intersection and marker-cut shell use the maximum **base** width automatically. If adding a still-wider feature, ensure that their X-span remains large enough to cover it.

## Important geometry notes

- `grip_top_radius` controls the rounded top in the **YZ** section. It is not a conventional edge-fillet radius.
- `grip_top_fillet_radius` is applied after the socket cut. Increasing it too far may fail if adjacent faces become too small, especially after changing taper widths.
- `home_marker_depth` is radial depth into the rounded top. The marker is deliberately constrained by a cylindrical shell rather than cut straight down.
- `socket_clearance` enlarges the circular portion and shifts the flat farther toward `-Y`; change it carefully for printer fit.
- `shaft_depth` must remain sufficient for the intended shaft, while staying compatible with the overall knob geometry.
- `interior_edges` identifies grip/base transition edges, but the fillet operation is currently disabled. Edge selection after boolean operations can be topology-sensitive; re-enable it only after testing with the current dimensions.

## Safe modification workflow

1. Change one parameter group at a time.
2. Run `uv run main.py`.
3. Inspect the final object and the toggleable `Base`, `Grip`, and `Home-marker engraving cut` construction components in the viewer.
4. Confirm that the socket, marker, and edge fillets still generate without errors.
5. Treat regenerated `build/` artifacts as outputs of the script, not hand-edited source files.

When modifying boolean or fillet operations, preserve the operation order unless there is a reason to change it: loft/clip/top-rounding → socket cut → grip fillets → base/grip fuse → home-marker cut.
