# Problem Description:
'''Problem description: A farmer on an island sends corn to the main land either by ferry or light rail. Each ferry trip can take 20 boxes of corn while each light rail trip can take 15 boxes of corn. Since ferry trips are slow, the number of light rail trip has to be at least 4 times the number of ferry trips. If the farmer wants to send at least 500 boxes of corn, minimize the total number of trips of either type needed.

Expected Output Schema:
{
  "variables": {
    "FerryTrips": "float",
    "LightRailTrips": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- Mode: set of transportation modes = {Ferry, LightRail}

Parameters:
- ferry_capacity = 20 (boxes per ferry trip)
- lightrail_capacity = 15 (boxes per light rail trip)
- min_boxes = 500 (minimum number of corn boxes to be sent)
- ratio_multiplier = 4 (light rail trips must be at least 4 times ferry trips)

Variables:
- FerryTrips: number of ferry trips to use (integer, ≥ 0)
- LightRailTrips: number of light rail trips to use (integer, ≥ 0)

Objective:
- Minimize total trips = FerryTrips + LightRailTrips

Constraints:
1. Shipment capacity constraint:
   - (ferry_capacity * FerryTrips) + (lightrail_capacity * LightRailTrips) ≥ min_boxes
   - That is, 20 * FerryTrips + 15 * LightRailTrips ≥ 500

2. Mode ratio constraint:
   - LightRailTrips ≥ ratio_multiplier * FerryTrips
   - That is, LightRailTrips ≥ 4 * FerryTrips

Notes:
- All units are consistent: box counts for corn and trips.  
- It is assumed that the trips must be integer numbers since fractional trips are not meaningful in this context.'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp
from ortools.sat.python import cp_model

def solve_with_linear_solver():
    # Create the linear solver with CBC backend.
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        return None
    
    # Parameters.
    ferry_capacity = 20
    lightrail_capacity = 15
    min_boxes = 500
    ratio_multiplier = 4
    
    # Variables: Non-negative integer variables.
    FerryTrips = solver.IntVar(0, solver.infinity(), 'FerryTrips')
    LightRailTrips = solver.IntVar(0, solver.infinity(), 'LightRailTrips')
    
    # Objective: minimize total trips.
    solver.Minimize(FerryTrips + LightRailTrips)
    
    # Constraints.
    # 1. Shipment capacity: 20 * FerryTrips + 15 * LightRailTrips >= 500
    solver.Add(ferry_capacity * FerryTrips + lightrail_capacity * LightRailTrips >= min_boxes)
    
    # 2. Mode ratio: LightRailTrips >= 4 * FerryTrips
    solver.Add(LightRailTrips >= ratio_multiplier * FerryTrips)
    
    status = solver.Solve()
    
    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "variables": {
                "FerryTrips": FerryTrips.solution_value(),
                "LightRailTrips": LightRailTrips.solution_value()
            },
            "objective": solver.Objective().Value()
        }
        return result
    else:
        return {"message": "No optimal solution found in the linear solver model."}

def solve_with_cp_model():
    # Create the CP-SAT model.
    model = cp_model.CpModel()
    
    # Parameters.
    ferry_capacity = 20
    lightrail_capacity = 15
    min_boxes = 500
    ratio_multiplier = 4
    
    # Variables.
    # Define an upper bound that is sufficiently high.
    # The worst-case scenario: all trips are light rail (15 boxes per trip)
    max_trips = min_boxes // lightrail_capacity + 10
    FerryTrips = model.NewIntVar(0, max_trips, 'FerryTrips')
    LightRailTrips = model.NewIntVar(0, max_trips * 10, 'LightRailTrips')  # Give a relaxed bound.
    
    # Constraints.
    # 1. Shipment capacity constraint: 20*FerryTrips + 15*LightRailTrips >= 500.
    model.Add(ferry_capacity * FerryTrips + lightrail_capacity * LightRailTrips >= min_boxes)
    
    # 2. Mode ratio constraint: LightRailTrips >= 4 * FerryTrips.
    model.Add(LightRailTrips >= ratio_multiplier * FerryTrips)
    
    # Objective: minimize total trips.
    total_trips = model.NewIntVar(0, max_trips * 10, 'total_trips')
    model.Add(total_trips == FerryTrips + LightRailTrips)
    model.Minimize(total_trips)
    
    # Solve the CP-SAT model.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        result = {
            "variables": {
                "FerryTrips": solver.Value(FerryTrips),
                "LightRailTrips": solver.Value(LightRailTrips)
            },
            "objective": solver.Value(total_trips)
        }
        return result
    else:
        return {"message": "No optimal solution found in the CP-SAT model."}

def main():
    print("Solving using Linear Solver (CBC):")
    linear_result = solve_with_linear_solver()
    print(linear_result)
    
    print("\nSolving using CP-SAT Model:")
    cp_result = solve_with_cp_model()
    print(cp_result)

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Solving using Linear Solver (CBC):
{'variables': {'FerryTrips': 6.0, 'LightRailTrips': 26.0}, 'objective': 32.0}

Solving using CP-SAT Model:
{'variables': {'FerryTrips': 4, 'LightRailTrips': 28}, 'objective': 32}
'''

'''Expected Output:
Expected solution

: {'variables': {'FerryTrips': 6.0, 'LightRailTrips': 26.0}, 'objective': 32.0}'''

