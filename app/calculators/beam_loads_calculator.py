from typing import Tuple, List
from ..schemas.beam import BeamLoadInput, BeamLoadResult, PointLoadInput

# Constants
CONCRETE_DENSITY = 2400  # kg/m³
BRICK_DENSITY = 20       # kN/m³
WALL_WIDTH = 0.23        # m (230mm standard brick wall)
DEAD_LOAD_FACTOR = 1.4
LIVE_LOAD_FACTOR = 1.6

def calculate_reactions(dist_load: float, point_loads: List[PointLoadInput], span: float) -> Tuple[float, float, float]:
    """Calculate reactions and maximum moment for distributed and point loads"""
    # Distributed load reactions
    R_dist = dist_load * span / 2
    
    # Point load reactions
    R_point_left = sum(load.magnitude * (span - load.position) / span for load in point_loads)
    R_point_right = sum(load.magnitude * load.position / span for load in point_loads)
    
    total_R_left = R_dist + R_point_left
    total_R_right = R_dist + R_point_right
    
    # Maximum moment
    M_dist = dist_load * span**2 / 8
    M_points = sum(load.magnitude * load.position * (span - load.position) / span for load in point_loads)
    max_moment = M_dist + M_points
    
    return total_R_left, total_R_right, max_moment

def calculate_loads_on_beam(input_data: BeamLoadInput) -> BeamLoadResult:
    """Calculate all beam loads and return results"""
    # Convert mm to m for width and depth
    width_m = input_data.width / 1000
    depth_m = input_data.depth / 1000
    
    # Calculate self-weight (always calculated but optionally included)
    self_weight = width_m * depth_m * CONCRETE_DENSITY * 10 / 1000  # kN/m
    
    # Calculate wall dead load if heights are provided
    wall_dead_load = 0.0
    if input_data.roof_level is not None and input_data.window_level is not None:
        wall_height = input_data.roof_level - input_data.window_level - depth_m
        if wall_height > 0:
            wall_dead_load = wall_height * WALL_WIDTH * BRICK_DENSITY
    
    # Calculate dead loads
    dead_load_without_self = wall_dead_load + input_data.additional_dead_load
    total_dead_load = (self_weight + dead_load_without_self) if input_data.include_self_weight else dead_load_without_self
    
    # Factored loads
    factored_dead_load = total_dead_load * DEAD_LOAD_FACTOR
    factored_live_load = input_data.live_load * LIVE_LOAD_FACTOR
    
    # Combined loads
    service_load = total_dead_load + input_data.live_load
    factored_load = factored_dead_load + factored_live_load
    
    # Calculate reactions and moments
    point_loads = input_data.point_loads if input_data.point_loads else []
    
    R_dead, _, M_dead = calculate_reactions(total_dead_load, point_loads, input_data.span)
    R_live, _, M_live = calculate_reactions(input_data.live_load, point_loads, input_data.span)
    R_service, _, M_service = calculate_reactions(service_load, point_loads, input_data.span)
    R_factored, _, M_factored = calculate_reactions(factored_load, point_loads, input_data.span)
    
    # Calculate total point load if any
    total_point_load = sum(load.magnitude for load in point_loads) if point_loads else None
    
    return BeamLoadResult(
        self_weight=self_weight,
        wall_dead_load=wall_dead_load,
        total_dead_load=total_dead_load,
        factored_dead_load=factored_dead_load,
        factored_live_load=factored_live_load,
        service_load=service_load,
        factored_load=factored_load,
        dead_load_reactions=R_dead,
        live_load_reactions=R_live,
        service_load_reactions=R_service,
        factored_load_reactions=R_factored,
        max_moment_service=M_service,
        max_moment_factored=M_factored,
        total_point_load=total_point_load
    )