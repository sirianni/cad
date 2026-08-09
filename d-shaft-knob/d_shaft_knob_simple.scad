/*
  Simplified D-shaft knob
  Units: millimetres
*/

// ---------- Core dimensions ----------
knob_diameter = 39;       // circular base
base_height = 5;          // base thickness
knob_height = 20;         // total height
grip_width = 12;          // fin width
grip_length = 39;         // fin length
shaft_diameter = 7;       // D-post diameter
shaft_flat_chord = 5;     // flat width of the D
shaft_depth = 10;         // socket depth
socket_clearance = 0.2;   // print clearance for the bore

$fn = 48;

// ---------- Derived ----------
base_radius = knob_diameter / 2;
shaft_radius = shaft_diameter / 2;
grip_rise = knob_height - base_height;
nominal_flat_y = -sqrt(pow(shaft_radius, 2) - pow(shaft_flat_chord / 2, 2));
socket_flat_y = nominal_flat_y - socket_clearance;

// ---------- D-profile (flat on -Y, pointer on +Y) ----------
module d_profile() {
  r = shaft_radius + socket_clearance;
  difference() {
    circle(r = r);
    // Cut off the bottom to make the flat
    translate([-r, socket_flat_y - r])
      square([2 * r, r]);
  }
}

// ---------- Base ----------
module base() {
  cylinder(h = base_height, r = base_radius);
}

// ---------- Fin / Grip ----------
module fin() {
  r = grip_width / 2;
  straight = grip_length - grip_width;
  translate([0, 0, base_height])
    linear_extrude(height = grip_rise)
      hull() {
        translate([0, -straight / 2]) circle(r = r);
        translate([0,  straight / 2]) circle(r = r);
      }
}

// ---------- Assembly ----------
difference() {
  union() {
    base();
    fin();
  }
  linear_extrude(height = shaft_depth)
    d_profile();
}
