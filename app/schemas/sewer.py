from pydantic import BaseModel

    
class SewerPipeInput(BaseModel):
    population: int
    per_capita_flow: float  # L/person/day
    slope: float            # percentage (%)
    n: float                # Manning's roughness coefficient
    diameter: float         # pipe diameter (m)
    flow_ratio: float       # ratio of flow depth to pipe diameter


class SewerPipeResult(BaseModel):
    diameter: float
    peak_factor: float
    demand_ms: float
    demand_ls: float
    flow_depth: float
    wetted_perimeter: float
    cross_sectional_area: float
    hydraulic_radius: float
    capacity: float
    velocity: float
