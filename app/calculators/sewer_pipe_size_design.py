from ..schemas.sewer import SewerPipeInput, SewerPipeResult
import math
import numpy as np

def calculate_peak_factor(population):
    """
    Calculate the peak factor for a given population.

    Parameters:
        population (int or float): Population served by the sewer system.

    Returns:
        peak_factor (float): Peak factor.
    """
    if population <= 0:
        raise ValueError("Population must be greater than 0.")
    
    peak_factor = 1 + (14 / (4 + (math.sqrt(population / 1000))))
    return peak_factor

def calculate_peak_demand(population, per_capita_flow):
    """
    Calculate the peak demand for a given population and per capita flow.

    Parameters:
        population (int or float): Population served by the sewer system.
        per_capita_flow (float): Per capita wastewater flow (L/person/day).

    Returns:
        peak_demand_lps (float): Peak demand in liters per second (L/s).
        peak_demand_m3s (float): Peak demand in cubic meters per second (m³/s).
    """
    if population <= 0 or per_capita_flow <= 0:
        raise ValueError("Population and per capita flow must be greater than 0.")
    
    # Calculate peak factor
    peak_factor = calculate_peak_factor(population)
    
    # Calculate peak demand in L/s
    peak_demand_lps = (population * per_capita_flow * peak_factor) / 86400
    
    # Convert peak demand to m³/s
    peak_demand_m3s = peak_demand_lps / 1000
    
    return peak_demand_m3s

def flow_depth(D, y_ratio):
    """
    Calculate the flow depth for a given ratio of flow depth to pipe diameter.

    Parameters:
        D (float): Diameter of the pipe (m).
        y_ratio (float): Ratio of flow depth to pipe diameter (y/D).

    Returns:
        y (float): Flow depth (m).
    """
    if y_ratio < 0 or y_ratio > 1:
        raise ValueError("Flow depth ratio (y_ratio) must be between 0 and 1.")
    
    y = y_ratio * D
    return y

def wetted_perimeter(D, y):
    """
    Calculate the wetted perimeter for partial flow in a circular pipe.

    Parameters:
        D (float): Diameter of the pipe (m).
        y (float): Flow depth (m).

    Returns:
        P (float): Wetted perimeter (m).
    """
    if y > D:
        raise ValueError("Flow depth (y) cannot be greater than pipe diameter (D).")
    
    # Calculate the angle theta in radians
    theta = np.arccos(1 - (2 * y) / D)
    
    # Calculate the wetted perimeter
    P = D * theta
    
    return P

def cross_sectional_area(D, y):
    """
    Calculate the cross-sectional area for partial flow in a circular pipe.

    Parameters:
        D (float): Diameter of the pipe (m).
        y (float): Flow depth (m).

    Returns:
        A (float): Cross-sectional area (m²).
    """
    if y > D:
        raise ValueError("Flow depth (y) cannot be greater than pipe diameter (D).")
    
    theta = np.arccos(1 - (2 * y) / D)
    A = (D**2 / 4) * (theta - np.sin(theta))
    return A

def hydraulic_radius(D, y):
    """
    Calculate the hydraulic radius for partial flow in a circular pipe.

    Parameters:
        D (float): Diameter of the pipe (m).
        y (float): Flow depth (m).

    Returns:
        R (float): Hydraulic radius (m).
    """
    A = cross_sectional_area(D, y)
    P = wetted_perimeter(D, y)
    R = A / P
    return R

def flow_capacity(D, y, n, S):
    """
    Calculate the flow capacity for partial flow in a circular pipe using Manning's equation.

    Parameters:
        D (float): Diameter of the pipe (m).
        y (float): Flow depth (m).
        n (float): Manning's roughness coefficient.
        S (float): Slope of the pipe (m/m).

    Returns:
        Q (float): Flow capacity (m³/s).
    """
    A = cross_sectional_area(D, y)
    R = hydraulic_radius(D, y)
    Q = (1 / n) * A * (R ** (2/3)) * (S ** 0.5)
    return Q

def flow_velocity(D, y, n, S):
    """
    Calculate the flow velocity for partial flow in a circular pipe using Manning's equation.

    Parameters:
        D (float): Diameter of the pipe (m).
        y (float): Flow depth (m).
        n (float): Manning's roughness coefficient.
        S (float): Slope of the pipe (m/m).

    Returns:
        V (float): Flow velocity (m/s).
    """
    Q = flow_capacity(D, y, n, S)
    A = cross_sectional_area(D, y)
    V = Q / A
    return V

def calculate_required_sewer_pipe(input_data: SewerPipeInput) -> SewerPipeResult:
    diameter = input_data.diameter
    p_factor = calculate_peak_factor(input_data.population)
    f_depth = flow_depth(input_data.diameter, input_data.flow_ratio)
    w_perimeter = wetted_perimeter(input_data.diameter, f_depth)
    c_sectional_area = cross_sectional_area(input_data.diameter, f_depth)
    h_radius = hydraulic_radius(input_data.diameter, f_depth)
    demand_ms = calculate_peak_demand(input_data.population, input_data.per_capita_flow)
    demand_ls = demand_ms * 1000
    capacity = flow_capacity(input_data.diameter, f_depth, input_data.n, input_data.slope)
    velocity = flow_velocity(input_data.diameter, f_depth, input_data.n, input_data.slope)

    return SewerPipeResult(
        diameter=diameter,
        peak_factor=p_factor,
        flow_depth=f_depth,
        wetted_perimeter=w_perimeter,
        cross_sectional_area=c_sectional_area,
        hydraulic_radius=h_radius,
        demand_ls=demand_ls,
        demand_ms=demand_ms,
        capacity=capacity,
        velocity=velocity
    )