from pydantic import BaseModel


class Sewer_Test_Input(BaseModel):
    population: int
    diameter: float
    slope: float
    flow_ratio: float
    
class Sewer_Test_Output(BaseModel):
    population: int
    diameter: float
    slope: float
    flow_ratio: float