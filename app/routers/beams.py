from fastapi import APIRouter, HTTPException
from ..schemas.beam import BeamLoadInput, BeamLoadResult
from ..calculators.beam_loads_calculator import calculate_loads_on_beam

router = APIRouter(
    prefix="/api/beams",
    tags=["Beam Calculations"]
)

@router.post("/calculate-loads", response_model=BeamLoadResult)
async def calculate_beam_loads(input: BeamLoadInput):
    try:
        return calculate_loads_on_beam(input)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))