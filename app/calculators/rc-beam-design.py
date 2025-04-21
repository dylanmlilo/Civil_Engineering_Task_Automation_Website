import math

# Beam types
types_of_beams = {
    1: "Cantilever",
    2: "Simply supported",
    3: "Continuous"
}

# Section types
sections = {
    1: "Rectangular",
    2: "Flanged beams with bw/b <= 0.3"
}

# --- Beam Type Input ---
while True:
    try:
        print("\n1. Cantilever\n2. Simply supported\n3. Continuous")
        beam_type = int(input("Enter beam type (1-3): "))
        if beam_type in types_of_beams:
            print(f"Selected: {types_of_beams[beam_type]}")
            break
        else:
            print("Invalid. Choose 1-3.")
    except ValueError:
        print("Numbers only.")

# --- Section Type Input ---
while True:
    try:
        print("\n1. Rectangular\n2. Flanged beams (bw/b ≤ 0.3)")
        section = int(input("Enter section type (1-2): "))
        if section in sections:
            print(f"Selected: {sections[section]}")
            break
        else:
            print("Invalid. Choose 1-2.")
    except ValueError:
        print("Numbers only.")

# --- Span Input ---
while True:
    try:
        clear_span = float(input("\nEnter clear span (mm): "))
        if clear_span > 0:
            break
        else:
            print("Must be positive.")
    except ValueError:
        print("Numbers only.")

# --- Effective Span Calculation ---
if beam_type == 1:  # Cantilever
    support_face = float(input("Enter distance to support face (mm): "))
    effective_span = support_face + (clear_span / 2)
elif beam_type == 2:  # Simply supported
    centre_dist = float(input("Enter centre-to-centre bearing distance (mm): "))
    effective_span = min(centre_dist, clear_span + (clear_span / 20))  # span/20 ≈ initial depth estimate
else:  # Continuous
    centre_dist = float(input("Enter centre-to-centre support distance (mm): "))
    effective_span = centre_dist

print(f"\nEffective Span = {effective_span:.2f} mm")

# --- Span-to-Depth Ratio ---
if section == 1:
    span_depth_ratio = 7 if beam_type == 1 else (20 if beam_type == 2 else 26)
else:
    span_depth_ratio = 5.6 if beam_type == 1 else (16.0 if beam_type == 2 else 20.8)

print(f"Basic Span/Depth Ratio = {span_depth_ratio}")

# --- Initial Depth Calculation ---
eff_depth_proposed = effective_span / span_depth_ratio
print(f"\nProposed Effective Depth = {eff_depth_proposed:.2f} mm")

# --- Cover and Reinforcement ---
while True:
    try:
        cover = int(input("\nEnter nominal cover (mm, >20): "))
        if cover > 20:
            break
        else:
            print("Cover must be >20mm per BS 8110")
    except ValueError:
        print("Whole numbers only.")

bar_dia = int(input("Enter main bar diameter (mm): "))
stirrup_dia = int(input("Enter stirrup diameter (mm): "))

# --- Overall Depth Calculation ---
overall_depth_unrounded = eff_depth_proposed + cover + (bar_dia/2) + stirrup_dia
overall_depth = math.ceil(overall_depth_unrounded / 25) * 25  # Round up to nearest 25mm
final_eff_depth = overall_depth - cover - (bar_dia/2) - stirrup_dia

print(f"\nOverall Depth (unrounded) = {overall_depth_unrounded:.2f} mm")
print(f"Final Overall Depth = {overall_depth} mm")
print(f"Final Effective Depth = {final_eff_depth:.2f} mm")

# --- Flanged Beam Logic (Updated) ---
if section == 2:
    # Auto-estimate web width
    estimated_bw = round(overall_depth / 3)
    print(f"\nRule of thumb: Web width ≈ Overall depth / 3 = {estimated_bw} mm")
    
    # Get web width (bw)
    while True:
        try:
            bw = float(input(f"Enter web width (bw) in mm [suggested {estimated_bw}]: ") or estimated_bw)
            if bw > 0:
                break
            else:
                print("Must be positive")
        except ValueError:
            print("Numbers only")

    # Get FULL flange width (for self-weight)
    while True:
        try:
            b_full = float(input("Enter FULL flange width (b) in mm (for self-weight): "))
            if b_full >= bw:
                break
            else:
                print(f"Must be ≥ web width ({bw} mm)")
        except ValueError:
            print("Numbers only")

    # Calculate EFFECTIVE flange width (for design)
    if beam_type == 3:  # T-beam (continuous)
        b_eff = min(bw + (effective_span / 5), b_full)
    else:  # L-beam
        b_eff = min(bw + (effective_span / 10), b_full)
    
    print(f"\nEffective Flange Width (for design) = {b_eff:.2f} mm")
    print(f"Full Flange Width (for self-weight) = {b_full} mm")

    # --- Self-Weight Calculation ---
    slab_thickness = float(input("Enter slab thickness (mm): "))
    concrete_density = 24 # kN/m³

    # Calculate beam web height (excluding slab)
    beam_web_height = overall_depth - slab_thickness

    # Convert mm to m for weight calculation
    beam_self_weight = (bw * beam_web_height) / 1e6 * concrete_density  # kN/m (web only)
    slab_self_weight = (b_full * slab_thickness) / 1e6 * concrete_density  # kN/m (entire flange)
    total_self_weight = beam_self_weight + slab_self_weight

print(f"\nSelf-Weight Calculation:")
print(f"- Web ({bw}x{beam_web_height}mm): {beam_self_weight:.3f} kN/m")
print(f"- Flange ({b_full}x{slab_thickness}mm): {slab_self_weight:.3f} kN/m")
print(f"- Total: {total_self_weight:.3f} kN/m")

# --- Final Ratio Check ---
final_ratio = effective_span / final_eff_depth
print(f"\nFinal Span/Depth Ratio = {final_ratio:.2f}")

if final_ratio > span_depth_ratio:
    print("WARNING: Ratio exceeds limits!")
else:
    print("OK: Ratio within limits")