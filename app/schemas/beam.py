from pydantic import BaseModel
from typing import Optional, List


class PointLoadInput(BaseModel):
    magnitude: float  # in kN
    position: float   # in meters from left support


class BeamLoadInput(BaseModel):
    span: float                   # in meters
    width: float                  # in mm
    depth: float                  # in mm
    include_self_weight: bool = True
    roof_level: Optional[float] = None    # in meters
    window_level: Optional[float] = None  # in meters
    additional_dead_load: float = 0.0     # in kN/m
    live_load: float = 0.0                # in kN/m
    point_loads: List[PointLoadInput] = []

class BeamLoadResult(BaseModel):
    self_weight: float                    # in kN/m
    wall_dead_load: float                 # in kN/m
    total_dead_load: float                # in kN/m
    factored_dead_load: float             # in kN/m
    factored_live_load: float             # in kN/m
    service_load: float                   # in kN/m
    factored_load: float                  # in kN/m
    dead_load_reactions: float            # in kN
    live_load_reactions: float            # in kN
    service_load_reactions: float         # in kN
    factored_load_reactions: float        # in kN
    max_moment_service: float             # in kNm
    max_moment_factored: float            # in kNm
    total_point_load: Optional[float] = None  # in kN