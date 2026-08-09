/*
  Replacement D-shaft appliance knob
  Units: millimetres

  The model is intentionally one solid printed part.  Its flat seating face is
  at Z=0; +Y is the 12-o'clock / pointer direction and the grip long axis.
  Set show_fit_coupon=true to export a small D-socket test coupon before
  committing to the full knob.
*/

// ---------- Confirmed dimensions from KNOB_SPECIFICATION.md ----------
knob_outside_diameter = 39;       // D1: circular base outside diameter
knob_overall_height = 20;         // D2: bottom to highest point of grip
circular_base_height = 5;         // D3: round base axial height
grip_width = 12;                  // D4: maximum X width
grip_length = 39;                 // D8: end-to-end Y length
shaft_diameter = 7;               // D5: round envelope diameter
// The measured 5 mm is the straight chord across the flat.  Treating it as
// flat-face-to-opposite-edge creates a 7 x 5 mm semicircle, not a D socket.
shaft_flat_chord = 5;             // straight-line length of the D flat
shaft_socket_depth = 10;          // D7: bore depth from underside
shaft_engagement_available = 10;  // D7: exposed shaft length, for reference
flat_to_pointer_angle = 180;      // D9: pointer is opposite the D flat

// ---------- Print-fit and construction adjustments ----------
// Per-surface clearance for PLA FDM.  Change this only after a fit coupon.
socket_clearance = 0.20;
// A short tapered entry lets the socket locate over the D-shaft before the
// full-depth, tight D profile engages. It is not a semicircular relief.
socket_lead_in_depth = 0.70;
socket_lead_in_extra_clearance = 0.15;

// Small cosmetic/comfort adjustments.  All retain the confirmed envelopes.
base_edge_radius = 0.75;          // chamfer-like rounding on outer rim
grip_rounding_radius = 2.0;       // 3D round-over of grip edges/top
hub_radius = 7.0;                 // reinforced material radius around bore
hub_height = 8.0;                 // rises from seat, remains inside silhouette
hub_top_radius = 6.25;            // slight taper at the top of the hub
grip_base_overlap = 0.25;          // fuses grip into base; preserves 20 mm total
pointer_notch_width = 2.4;        // width of V at its outer/open end
pointer_notch_length = 3.0;       // radial length of V notch
pointer_notch_depth = 1.2;        // depth down from the grip top
pointer_notch_outer_inset = 1.4;  // distance from 39 mm grip end

// Coordinate/orientation controls. +Y is 12 o'clock; native D flat is -Y.
pointer_direction_deg = 90;
native_d_flat_direction_deg = -90;
d_flat_direction_deg = pointer_direction_deg - flat_to_pointer_angle;
d_socket_rotation_deg = d_flat_direction_deg - native_d_flat_direction_deg;

// Set true to produce a 4 mm thick socket-fit coupon beside the model.
show_fit_coupon = false;
fit_coupon_width = 16;
fit_coupon_thickness = 4;

$fn = 96;
model_epsilon = 0.02;

// Derived values -- edit the named parameters above rather than these.
base_radius = knob_outside_diameter / 2;
shaft_radius = shaft_diameter / 2;
socket_radius = shaft_radius + socket_clearance;
// The D flat is a 5 mm chord of a 7 mm circle. Its plane is close to the
// circle edge, yielding the expected mostly-round D profile, not a semicircle.
nominal_flat_y = -sqrt(pow(shaft_radius, 2) - pow(shaft_flat_chord / 2, 2));
socket_flat_y = nominal_flat_y - socket_clearance;
grip_rise = knob_overall_height - circular_base_height;

assert(knob_outside_diameter > 0 && circular_base_height > 0);
assert(knob_overall_height > circular_base_height);
assert(grip_length >= grip_width);
assert(grip_rounding_radius > 0 && grip_rounding_radius < grip_width / 2);
assert(grip_rise > 2 * grip_rounding_radius);
assert(base_edge_radius >= 0 && base_edge_radius <= circular_base_height / 2);
assert(shaft_flat_chord > 0 && shaft_flat_chord < shaft_diameter);
assert(socket_flat_y > -socket_radius);
assert(socket_lead_in_depth >= 0 && socket_lead_in_depth < shaft_socket_depth);
assert(shaft_socket_depth <= shaft_engagement_available,
       "Socket is deeper than the confirmed exposed shaft length.");
assert(hub_radius > socket_radius && hub_height >= circular_base_height);
assert(grip_base_overlap > 0 && grip_base_overlap < grip_rounding_radius);

// A capsule in the XY plane.  Its stated length is its outside end-to-end size.
module capsule_2d(width, length) {
    end_radius = width / 2;
    straight_length = length - width;
    hull() {
        translate([0, -straight_length / 2]) circle(r = end_radius);
        translate([0,  straight_length / 2]) circle(r = end_radius);
    }
}

// The base has a flat underside and modest faceted-round rim transitions.
module circular_base() {
    rotate_extrude(convexity = 10)
        polygon(points = [
            [0, 0],
            [base_radius - base_edge_radius, 0],
            [base_radius, base_edge_radius],
            [base_radius, circular_base_height - base_edge_radius],
            [base_radius - base_edge_radius, circular_base_height],
            [0, circular_base_height]
        ]);
}

// Minkowski keeps the grip's exact specified bounding width, length and height
// while giving it rounded ends, top, and finger-contact edges.
module raised_thumb_grip() {
    core_width = grip_width - 2 * grip_rounding_radius;
    core_length = grip_length - 2 * grip_rounding_radius;
    // Extend down into the base by a small amount. This ensures a true solid
    // union rather than relying on a coincident Z=5 face, while top remains Z=20.
    core_height = grip_rise - 2 * grip_rounding_radius + grip_base_overlap;

    minkowski() {
        translate([0, 0, circular_base_height + grip_rounding_radius - grip_base_overlap])
            linear_extrude(height = core_height, convexity = 10)
                capsule_2d(core_width, core_length);
        sphere(r = grip_rounding_radius, $fn = 28);
    }
}

// The hub starts flush with the underside, so it cannot interfere with seating.
module reinforced_hub() {
    cylinder(h = hub_height, r1 = hub_radius, r2 = hub_top_radius);
}

// Native profile has its straight flat on -Y.  It is then rotated to be
// opposite the +Y pointer direction according to flat_to_pointer_angle.
//
// This is deliberately constructed as an explicit closed D polygon. Its
// boundary is a 5 mm straight chord (the D flat) plus the major circular arc.
// The opening is approximately 7.4 mm across including print clearance.
module d_socket_2d(clearance = socket_clearance) {
    profile_radius = shaft_radius + clearance;
    profile_flat_y = nominal_flat_y - clearance;
    arc_start_degrees = asin(profile_flat_y / profile_radius); // right chord end
    arc_sweep_degrees = 180 - 2 * asin(profile_flat_y / profile_radius);
    arc_segments = 64;

    polygon(points = [
        for (segment = [0 : arc_segments])
            [
                profile_radius * cos(arc_start_degrees + segment * arc_sweep_degrees / arc_segments),
                profile_radius * sin(arc_start_degrees + segment * arc_sweep_degrees / arc_segments)
            ]
    ]);
}

// The first 0.70 mm is a larger D-shaped lead-in, then it transitions to the
// 10 mm-deep finished D socket. This helps installation while preserving the
// locating flat all the way to the underside.
module d_socket(depth) {
    rotate([0, 0, d_socket_rotation_deg])
        union() {
            hull() {
                translate([0, 0, -model_epsilon])
                    linear_extrude(height = model_epsilon)
                        d_socket_2d(socket_clearance + socket_lead_in_extra_clearance);
                translate([0, 0, socket_lead_in_depth])
                    linear_extrude(height = model_epsilon)
                        d_socket_2d(socket_clearance);
            }
            translate([0, 0, socket_lead_in_depth])
                linear_extrude(height = depth - socket_lead_in_depth + model_epsilon,
                               convexity = 10)
                    d_socket_2d(socket_clearance);
        }
}

// A shallow V cut on the top surface.  It opens toward +Y (12 o'clock),
// clearly marking the pointer end without weakening the D-socket hub.
module pointer_notch() {
    outer_y = grip_length / 2 - pointer_notch_outer_inset;
    tip_y = outer_y - pointer_notch_length;
    translate([0, 0, knob_overall_height - pointer_notch_depth])
        linear_extrude(height = pointer_notch_depth + model_epsilon)
            polygon(points = [
                [-pointer_notch_width / 2, outer_y],
                [ pointer_notch_width / 2, outer_y],
                [0, tip_y]
            ]);
}

module knob() {
    difference() {
        union() {
            circular_base();
            reinforced_hub();
            raised_thumb_grip();
        }
        d_socket(shaft_socket_depth);
        pointer_notch();
    }
}

module fit_coupon() {
    // Print with the flat face on the bed, same as the finished knob.
    difference() {
        translate([-fit_coupon_width / 2, -fit_coupon_width / 2, 0])
            cube([fit_coupon_width, fit_coupon_width, fit_coupon_thickness]);
        d_socket(fit_coupon_thickness);
    }
}

if (show_fit_coupon) {
    fit_coupon();
} else {
    knob();
}
