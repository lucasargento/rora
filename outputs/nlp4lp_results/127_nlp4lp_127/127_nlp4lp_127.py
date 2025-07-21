# Problem Description:
'''Problem description: An international goods exporter uses ships and planes to transport goods. A ship can take 40 containers worth of goods and uses 500 liters of fuel per trip. A plane can take 20 containers worth of goods and uses 300 liters of fuel per trip. The company needs to transport at least 500 containers worth of goods. In addition, there can be at most 10 plane trips made and a minimum of 50% of the trips made must be by ship. How many of each trip should be made to minimize the total amount of fuel consumed?

Expected Output Schema:
{
  "variables": {
    "ShipTrips": "float",
    "PlaneTrips": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- Modes: set of transportation modes = {Ship, Plane}

Parameters:
- capacity_ship: containers carried per ship trip [40 containers per trip]
- capacity_plane: containers carried per plane trip [20 containers per trip]
- fuel_ship: fuel consumption per ship trip [500 liters per trip]
- fuel_plane: fuel consumption per plane trip [300 liters per trip]
- min_containers: minimum total containers to transport [500 containers]
- max_plane_trips: maximum number of plane trips [10 trips]
- min_ship_fraction: minimum fraction of total trips that must be by ship [0.5 (i.e., 50%)]

Variables:
- ShipTrips: number of ship trips [nonnegative integer or continuous if relaxable; units: trips]
- PlaneTrips: number of plane trips [nonnegative integer or continuous if relaxable; units: trips]

Objective:
- Minimize total fuel consumption, calculated as:
  Total_Fuel = fuel_ship * ShipTrips + fuel_plane * PlaneTrips

Constraints:
1. Container Transport Requirement:
   capacity_ship * ShipTrips + capacity_plane * PlaneTrips >= min_containers
2. Plane Trips Limit:
   PlaneTrips <= max_plane_trips
3. Minimum Ship Trip Proportion:
   ShipTrips >= min_ship_fraction * (ShipTrips + PlaneTrips)
   (This constraint can be simplified to ShipTrips >= PlaneTrips)

Comments:
- All units are consistent as containers, trips, and liters.
- The decision variables are typically integer; if fractional trips are allowed, relax integrality.
- The simplified interpretation of the minimum ship trip proportion is based on ShipTrips/(ShipTrips + PlaneTrips) >= 0.5, which implies ShipTrips >= PlaneTrips.

Expected Output Schema:
{
  "variables": {
    "ShipTrips": "float",
    "PlaneTrips": "float"
  },
  "objective": "float"
}'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_integer_model():
    # Create the MIP solver with CBC backend.
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Integer model: Solver creation failed.")
        return None

    # Parameters
    capacity_ship = 40
    capacity_plane = 20
    fuel_ship = 500
    fuel_plane = 300
    min_containers = 500
    max_plane_trips = 10
    min_ship_fraction = 0.5  # implies ShipTrips/(ShipTrips+PlaneTrips) >=0.5  => ShipTrips >= PlaneTrips

    # Define variables (Integer version)
    ShipTrips = solver.IntVar(0, solver.infinity(), 'ShipTrips')
    PlaneTrips = solver.IntVar(0, solver.infinity(), 'PlaneTrips')

    # Objective: minimize total fuel consumption:
    # Total_Fuel = fuel_ship * ShipTrips + fuel_plane * PlaneTrips
    objective = solver.Objective()
    objective.SetCoefficient(ShipTrips, fuel_ship)
    objective.SetCoefficient(PlaneTrips, fuel_plane)
    objective.SetMinimization()

    # Constraint 1: Transport at least min_containers containers
    solver.Add(capacity_ship * ShipTrips + capacity_plane * PlaneTrips >= min_containers)

    # Constraint 2: At most max_plane_trips plane trips
    solver.Add(PlaneTrips <= max_plane_trips)

    # Constraint 3: Minimum Ship Trip Proportion
    # ShipTrips/(ShipTrips+PlaneTrips) >= 0.5 => ShipTrips >= PlaneTrips
    solver.Add(ShipTrips >= PlaneTrips)

    # Solve and return result
    status = solver.Solve()

    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result["ShipTrips"] = ShipTrips.solution_value()
        result["PlaneTrips"] = PlaneTrips.solution_value()
        result["objective"] = objective.Value()
    else:
        result["error"] = "No optimal solution found in the integer model."
    return result

def solve_continuous_model():
    # Create the LP solver.
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Continuous model: Solver creation failed.")
        return None

    # Parameters
    capacity_ship = 40
    capacity_plane = 20
    fuel_ship = 500
    fuel_plane = 300
    min_containers = 500
    max_plane_trips = 10
    min_ship_fraction = 0.5  # implies ShipTrips/(ShipTrips+PlaneTrips) >=0.5 => ShipTrips >= PlaneTrips

    # Define variables (Continuous version)
    ShipTrips = solver.NumVar(0.0, solver.infinity(), 'ShipTrips')
    PlaneTrips = solver.NumVar(0.0, solver.infinity(), 'PlaneTrips')

    # Objective: minimize total fuel consumption:
    objective = solver.Objective()
    objective.SetCoefficient(ShipTrips, fuel_ship)
    objective.SetCoefficient(PlaneTrips, fuel_plane)
    objective.SetMinimization()

    # Constraint 1: Transport at least min_containers containers
    solver.Add(capacity_ship * ShipTrips + capacity_plane * PlaneTrips >= min_containers)

    # Constraint 2: At most max_plane_trips plane trips
    solver.Add(PlaneTrips <= max_plane_trips)

    # Constraint 3: Minimum Ship Trip Proportion: ShipTrips >= PlaneTrips
    solver.Add(ShipTrips >= PlaneTrips)

    # Solve and return result
    status = solver.Solve()

    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result["ShipTrips"] = ShipTrips.solution_value()
        result["PlaneTrips"] = PlaneTrips.solution_value()
        result["objective"] = objective.Value()
    else:
        result["error"] = "No optimal solution found in the continuous model."
    return result

def main():
    integer_result = solve_integer_model()
    continuous_result = solve_continuous_model()
    
    print("Integer Model Solution:")
    if "error" in integer_result:
        print(integer_result["error"])
    else:
        print(f"ShipTrips: {integer_result['ShipTrips']}")
        print(f"PlaneTrips: {integer_result['PlaneTrips']}")
        print(f"Objective (Total Fuel): {integer_result['objective']} liters")
    
    print("\nContinuous Model Solution:")
    if "error" in continuous_result:
        print(continuous_result["error"])
    else:
        print(f"ShipTrips: {continuous_result['ShipTrips']:.2f}")
        print(f"PlaneTrips: {continuous_result['PlaneTrips']:.2f}")
        print(f"Objective (Total Fuel): {continuous_result['objective']:.2f} liters")

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Integer Model Solution:
ShipTrips: 12.0
PlaneTrips: 1.0
Objective (Total Fuel): 6300.0 liters

Continuous Model Solution:
ShipTrips: 12.50
PlaneTrips: 0.00
Objective (Total Fuel): 6250.00 liters
'''

'''Expected Output:
Expected solution

: {'variables': {'ShipTrips': 12.0, 'PlaneTrips': 1.0}, 'objective': 6300.0}'''

