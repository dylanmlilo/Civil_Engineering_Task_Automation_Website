from ..schemas.test_sewer import Sewer_Test_Input, Sewer_Test_Output


def calc_sewer_test(data: Sewer_Test_Input) -> Sewer_Test_Output:
    
    return Sewer_Test_Output(
        population=data.population,
        diameter=data.diameter,
        slope=data.slope,
        flow_ratio=data.flow_ratio
    )