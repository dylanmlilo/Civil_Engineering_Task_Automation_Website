from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from ..schemas.sewer import SewerPipeInput, SewerPipeResult
from ..schemas.test_sewer import Sewer_Test_Input, Sewer_Test_Output
from ..calculators.sewer_pipe_size_design import calculate_required_sewer_pipe
from ..calculators.test_sewer import calc_sewer_test

router = APIRouter(
    prefix="/api/sewer",
    tags=["Sewer Calculations"]
)

@router.post("/sewer_pipe_sizing", response_model=SewerPipeResult)
async def calculate_sewer_pipe_size(input: SewerPipeInput):
    try:
        return calculate_required_sewer_pipe(input)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@router.post("/test_sewer", response_model=Sewer_Test_Output)
async def test_sewer_calc(input: Sewer_Test_Input):
    try:
        return calc_sewer_test(input)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
        
            