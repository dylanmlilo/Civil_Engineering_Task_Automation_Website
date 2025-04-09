from fastapi import APIRouter, HTTPException, Request
from ..schemas.beam import BeamLoadInput, BeamLoadResult
from ..calculators.beam_loads_calculator import calculate_loads_on_beam
from fastapi.templating import Jinja2Templates



router = APIRouter(
    prefix="/beams",
    tags=["Beam Calculations"]
)

templates = Jinja2Templates(directory="app/templates")


@router.get("/")
async def beam_calculator(request: Request):
    return templates.TemplateResponse("beams.html", {"request": request})



@router.post("/calculate-loads", response_model=BeamLoadResult)
async def calculate_beam_loads(input: BeamLoadInput):
    try:
        return calculate_loads_on_beam(input)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))