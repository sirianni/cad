# Replacement D-Shaft Knob — Design Specification (review draft)

**Status:** Draft for dimensional/functional review.  This document specifies the part to be modeled later; it does **not** create an OpenSCAD model.

## 1. Purpose

Create a 3D-printable functional replacement for the broken chrome control knob shown in `img/`.  The replacement must fit the appliance's D-profile rotary shaft, clear the surrounding recessed control panel, be readily turnable by hand, and visually follow the original's round-base / raised-thumb-grip form.

All dimensions in this document are in **millimetres (mm)**.

## 2. Evidence and terminology

### 2.1 Source images

| File | View | What it establishes |
|---|---|---|
| `img/IMG_2886.jpg` | Original knob, underside | Circular chrome shell; centrally located broken drive hub/socket; black molded internal structure and radial/longitudinal reinforcing features. |
| `img/IMG_2888.jpg` | Original knob, top | 39 mm-class circular outer body with a central, elongated raised thumb grip.  The grip is aligned on one diameter of the knob and has rounded ends. |
| `img/IMG_2889.jpg` | Appliance shaft/panel | The appliance has a metal D-profile rotary shaft located in a recessed black bezel.  The replacement must seat without rubbing the bezel or the printed panel. |

The photographs are visual references only.  They contain perspective distortion and no scale reference, so they must not be used to infer unmeasured dimensions.

### 2.2 Coordinate convention for the future model

Use the shaft axis as the **Z axis**, with the shaft/bore centre at `(0, 0)`.

- **Underside:** faces the appliance/panel.
- **Top:** user-facing side with the thumb grip.
- **Grip long axis:** define as the Y axis.
- **Grip width:** the X-direction width, perpendicular to the grip long axis.
- **Indicator direction:** the direction from the centre toward the small notch on the top of the grip.  At the intended upright/OFF orientation, this is 12 o’clock and the D-shaft flat is 180° opposite it at 6 o’clock.

## 3. Confirmed user-supplied dimensions

| ID | Feature | Nominal dimension | Notes |
|---|---|---:|---|
| D1 | Knob outside diameter | **39** | Diameter of the circular outer portion.  Nominal outer radius = **19.5**. |
| D2 | Overall knob height | **20** | Confirmed bottom-most to top-most extent, including the raised grip. |
| D3 | Circular portion height | **5** | Confirmed axial thickness/height of the round outer base/rim. |
| D4 | Thumb-twist portion width | **12** | Width across the raised grip, perpendicular to its long axis. |
| D5 | Shaft maximum diameter | **7** | Confirmed maximum outside diameter across the round portion of the actual metal shaft, before fit clearance. |
| D6 | D-shaft flat chord | **5** | Confirmed straight-line width of the planar flat face (the chord cut from the 7 mm round envelope). |
| D7 | D-socket engagement depth | **10** | Confirmed depth of the D-shaped shaft hole inside the knob; this also equals the usable exposed shaft length. |
| D8 | Thumb-grip length | **39** | Confirmed end-to-end: the grip spans the full knob diameter. |
| D9 | D-flat-to-pointer orientation | **180°** | The notch pointer is at 12 o’clock; the D-shaft flat faces the opposite direction, at 6 o’clock. |

## 4. Form and feature requirements inferred from the photos

### 4.1 Exterior

1. The outer body is a round, low-profile knob with a nominal 39 mm outside diameter.
2. The perimeter appears to be a thin, mostly vertical cylindrical rim with small rounding/chamfers rather than a sharp 90° edge.  The exact edge radius is **not measured**.
3. The original has a reflective chrome/metalized finish.  A printed replacement may be plain plastic; chrome appearance is optional and not required for fit/function.
4. A raised, elongated thumb grip runs through the centre of the top surface along one diameter.  It spans the full 39 mm diameter end-to-end, is 12 mm wide, and has rounded/softened ends and side transitions.
5. The grip rises from the 5 mm circular base to the confirmed 20 mm overall knob height, giving a nominal 15 mm maximum rise above the base.  Its top profile is slightly rounded; the exact radius is intentionally an adjustable visual/comfort parameter.
6. Add a small notch at the top of the grip as the functional position pointer.  The notch points to 12 o’clock at the desired upright/OFF orientation.  It is on the side of the grip **opposite the D-shaft flat** (180° from the flat); this replaces the original's uncertain oval-looking detail with a clear functional indicator.
7. The original surface is smooth rather than knurled.  No perimeter knurling is visible.

### 4.2 Underside and drive interface

1. The drive feature is centred on the circular body and must be coaxial with the knob.
2. The broken original exposes a black internal hub/structure below the chrome shell.  It appears to use a central D-shaped drive opening surrounded by relatively thin walls/ribs; the original may be a chrome shell over a separate molded insert.
3. A one-piece printed replacement may replace that shell-and-insert construction with a solid circular base, a reinforced central hub, and a D-shaped socket.  It does **not** need to copy the broken thin internal ribs exactly, provided it fits and transmits turning torque.
4. Do not add screws, set screws, clips, or metal inserts.  Use a snug push-on D-socket with an adjustable printed-fit clearance.
5. The replacement is intended to sit directly against the appliance's black bezel.  Its underside must therefore be flat enough to seat there without rubbing the surrounding panel.

## 5. Confirmed D-shaft socket geometry

The D socket is centred on the knob and has these **nominal mating dimensions before print clearance**:

| Parameter | Value | Definition |
|---|---:|---|
| `shaft_diameter` | 7 mm | Largest outside-to-outside diameter of the shaft's round envelope. |
| `shaft_flat_chord` | 5 mm | Straight-line length of the planar D-shaft flat (a chord of the 7 mm circular envelope). |
| `shaft_socket_depth` | 10 mm | Depth of the D-shaped hole measured inward from the knob underside. |
| `shaft_engagement_available` | 10 mm | Exposed shaft length available for engagement. |

For a 7 mm round envelope, the nominal radius is 3.5 mm.  The confirmed 5 mm flat is a chord: its plane is `sqrt(3.5² − 2.5²) = 2.449 mm` from the shaft centre toward the flat side.  The model should generate the resulting mostly-round D profile from this chord and circular envelope, then apply named clearance parameters to the socket.  It must not interpret 5 mm as flat-face-to-opposite-edge depth, which would create an unusable semicircular opening.

### Fit allowance for FDM printing

The modeler should make fit clearance a named, adjustable parameter rather than changing the nominal shaft dimensions silently.

- Intended material: **PLA**.
- Initial suggested radial/profile clearance: **0.15–0.25 mm per mating surface** for a calibrated PLA FDM printer.
- Practical first-test socket envelope: 7 mm shaft diameter + approximately **0.30–0.50 mm total clearance**.
- The exact clearance should be validated with a short D-hole coupon first, because slicer compensation and print orientation control the final fit.

A socket that is too loose will permit backlash and may split the hub; a socket that is too tight can prevent seating or crack during installation.

## 6. Confirmed axial layout

Use this Z-axis convention for the future model:

1. Set the flat underside that seats on the black bezel to `Z = 0`.
2. The 39 mm circular base extends from `Z = 0` to `Z = 5`.
3. The D-shaped socket begins at the underside (`Z = 0`) and extends inward to `Z = 10`.
4. The raised grip begins on the base and reaches `Z = 20` at its slightly rounded peak.  Its maximum rise above the base is therefore 15 mm.
5. No external downward D-shaft post, set screw, or other retention feature is required.

## 7. Functional and structural requirements for the eventual printed part

1. **Fit:** The D socket must enter the 7 mm D shaft fully over the confirmed engagement length without forcing or excessive wobble.
2. **Seat/clearance:** The knob must not bottom out on the black bezel, surrounding dial, or panel before the D shaft is fully engaged.  Measure the bezel opening diameter/depth and clearance to the panel if a hub projects below the base.
3. **Torque path:** Material between the D bore and outer surfaces must be sufficient for normal hand rotation.  Use a robust central hub and generous fillets where the hub joins the base/grip; do not reproduce the fragile broken wall arrangement merely for appearance.
4. **Orientation:** Place a small pointer notch in the top of the grip at its designated 12 o’clock end.  Rotate the D socket so its flat face is 180° opposite that notch—at 6 o’clock when the pointer is at 12 o’clock.
5. **Comfort:** Round or fillet all user-contact edges of the raised grip.  The user should be able to turn it by pinching the 12 mm-wide grip without sharp edges.
6. **Printability:** Avoid unsupported internal horizontal roofs in the socket where possible.  Print orientation, perimeters, and infill should be selected for torsional strength at the bore/hub, not merely exterior finish.
7. **Serviceability:** The model should expose top-level parameters for every dimension in §3, D-bore fit clearance, grip length, grip height/profile, hub dimensions, edge radii, and angular orientation.

## 8. Remaining adjustable choices (not blockers)

The functional geometry is now specified.  The following are intentional approximation or tuning parameters for the eventual modeler:

| Item | Modeling direction |
|---|---|
| Grip top radius / transition fillets | Use a gentle rounded profile matching the photos and comfortable for hand use; expose the radius as a parameter. |
| Outer rim edge radii/chamfers | Use modest rounding/chamfers; exact original values were not measured. |
| Notch size/shape | Use a small, visible top notch at the pointer end of the grip.  Its exact cosmetic form may be selected for printability. |
| PLA socket clearance | Begin with the range in §5, print a fit coupon if possible, and retain clearance as a parameter. |
| Reinforced hub/base geometry | Choose sufficient wall thickness and fillets for normal hand torque while keeping the underside flat to seat on the bezel. |

## 9. Review checklist / acceptance criteria

Approve this specification for modeling only after the following statements are true:

- [x] 39 mm outer diameter, 20 mm overall height, 5 mm circular-portion height, 12 mm grip width, and 39 mm grip length are confirmed.
- [x] The D profile is confirmed as a 7 mm maximum-diameter envelope with a 5 mm straight flat chord.
- [x] The D socket has 10 mm engagement depth and the shaft has 10 mm usable exposed length.
- [x] The small top notch is the pointer at 12 o’clock; the D flat is 180° opposite it at 6 o’clock.
- [x] The knob sits directly on the black bezel; no set screw is wanted.
- [x] PLA is the intended material, with adjustable FDM clearance.
- [x] Unmeasured rounding, chamfers, and notch styling are accepted as functional approximations.

This document is ready to hand off as a parametric OpenSCAD modeling specification.
