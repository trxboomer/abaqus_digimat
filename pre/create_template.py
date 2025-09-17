"""
Creates new Template files based on a "root" Template file.

Script has the ability to change:
- Fiber length
- Fiber VF
- Fiber orientation distribution
- Void VF
- Void morphology
- Void orientation distribution
"""
"""
Fiber options:

PHASE
name = Fiber
type = inclusion_fe
volume_fraction = 8.000000000000000e-02
material = Carbon_Fiber
inclusion_shape = spherocylinder
aspect_ratio = 1.675000000000000e+01
phase_definition = by_size_and_diameter
inclusion_diameter = 4.000000000000000e-03
inclusion_size = 6.700000000000000e-02
size_distribution = fixed
orientation = tensor
orientation_11 = 7.900000000000000e-01
orientation_22 = 1.100000000000000e-01
orientation_33 = 1.000000000000000e-01
orientation_12 = -1.000000000000000e-02
orientation_13 = 1.000000000000000e-02
orientation_23 = 0.000000000000000e+00
coated = no
interface_behavior = perfectly_bonded
clustering = no
allow_size_reduction = no
track_percolation_onset = no
stop_at_percolation = no
check_final_percolation = no
no_tie_on_fiber_tips = no

Void options
name = Voids
type = inclusion_fe
volume_fraction = 2.300000000000000e-01
material = Air
inclusion_shape = ellipsoid
aspect_ratio = 3.000000000000000e+00
phase_definition = by_size_and_ar
inclusion_size = 4.000000000000000e-02
size_distribution = fixed
orientation = tensor
orientation_11 = 8.000000000000000e-01
orientation_22 = 2.000000000000000e-01
orientation_33 = 0.000000000000000e+00
orientation_12 = 0.000000000000000e+00
orientation_13 = 0.000000000000000e+00
orientation_23 = 0.000000000000000e+00
coated = no
interface_behavior = perfectly_bonded
clustering = no
allow_size_reduction = no
track_percolation_onset = no
stop_at_percolation = no
check_final_percolation = no
no_tie_on_fiber_tips = no
"""
def main(file_name: str, file_path:str):
    
    