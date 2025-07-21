# Problem Description:
'''Problem description: A meat shop ships their burger patties using refrigerated trucks and vans. Each truck can take 1000 patties at a cost of $300 per trip. Each van can take 500 patties at a cost of $100 per trip. Because the trucks have difficulty moving around in the city, the number of trucks must not exceed the number of vans. The meat shop has to ship at least 50000 patties and they have a budget of $12500. How should they plan their shipment to minimize the total number of trips?

Expected Output Schema:
{
  "variables": {
    "NumTrips": {
      "0": "float",
      "1": "float"
    },
    "NumVehicles": {
      "0": "float",
      "1": "float"
    }
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- VehicleTypes: the set of available vehicle types = {truck, van}

Parameters:
- cap_truck: capacity of a truck per trip = 1000 patties per trip
- cap_van: capacity of a van per trip = 500 patties per trip
- cost_truck: shipping cost per truck trip = 300 USD per trip
- cost_van: shipping cost per van trip = 100 USD per trip
- demand: the minimum number of patties to ship = 50000 patties
- budget: the maximum allowed shipping cost = 12500 USD

Variables:
- Let NumTrips["0"] be the number of truck trips (integer ≥ 0, measured in trips)
- Let NumTrips["1"] be the number of van trips (integer ≥ 0, measured in trips)
- Let NumVehicles["0"] be the number of trucks used (integer ≥ 0, measured in vehicles)
- Let NumVehicles["1"] be the number of vans used (integer ≥ 0, measured in vehicles)
  (Note: Since each trip uses one vehicle, we have NumVehicles["0"] = NumTrips["0"] and NumVehicles["1"] = NumTrips["1"].)

Objective:
- Minimize total trips = NumTrips["0"] + NumTrips["1"]

Constraints:
1. Shipping capacity constraint (patties shipped must meet or exceed demand):
   1000 * NumTrips["0"] + 500 * NumTrips["1"] ≥ 50000
2. Budget constraint (total shipping cost must not exceed the available budget):
   300 * NumTrips["0"] + 100 * NumTrips["1"] ≤ 12500
3. Vehicle routing constraint (number of truck trips must not exceed number of van trips):
   NumTrips["0"] ≤ NumTrips["1"]

Comments:
- All costs are in USD per trip and capacities in patties per trip.
- The demand and budget constraints use totals over all trips.
- Although the model defines both NumTrips and NumVehicles, they represent the same counts since every trip uses one vehicle.
- Decision variables are integers, as fractional trips are not allowed.'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp
from ortools.sat.python import cp_model

def solve_with_linear_solver():
    # Create the linear solver with the CBC MIP backend.
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Linear solver not found.")
        return None

    # Decision variables:
    # NumTrips["0"] for truck trips, NumTrips["1"] for van trips.
    # As mentioned, NumVehicles equals NumTrips.
    truck_trips = solver.IntVar(0, solver.infinity(), "truck_trips")
    van_trips = solver.IntVar(0, solver.infinity(), "van_trips")

    # Constraints:
    # 1. Shipping capacity constraint: 1000*truck_trips + 500*van_trips >= 50000
    solver.Add(1000 * truck_trips + 500 * van_trips >= 50000)
    
    # 2. Budget constraint: 300*truck_trips + 100*van_trips <= 12500
    solver.Add(300 * truck_trips + 100 * van_trips <= 12500)
    
    # 3. Vehicle routing constraint: truck_trips <= van_trips
    solver.Add(truck_trips <= van_trips)

    # Objective: minimize the total number of trips.
    solver.Minimize(truck_trips + van_trips)

    status = solver.Solve()

    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "model": "LinearSolver",
            "variables": {
                "NumTrips": {
                    "0": truck_trips.solution_value(),
                    "1": van_trips.solution_value()
                },
                "NumVehicles": {
                    "0": truck_trips.solution_value(),
                    "1": van_trips.solution_value()
                }
            },
            "objective": truck_trips.solution_value() + van_trips.solution_value()
        }
    else:
        result = {"model": "LinearSolver", "message": "No optimal solution found."}
    return result

def solve_with_cp_model():
    # Create a CP-SAT model.
    model = cp_model.CpModel()

    # Upper bounds: use some reasonable big number.
    # Since shipping 50000 patties, max truck trips if used only trucks = ceil(50000/1000)=50,
    # max van trips if used only vans = ceil(50000/500)=100.
    # Additionally, budget restricts them, but we can use these as upper bounds.
    truck_trips = model.NewIntVar(0, 50, "truck_trips")
    van_trips = model.NewIntVar(0, 100, "van_trips")

    # Constraint 1: Shipping capacity.
    model.Add(1000 * truck_trips + 500 * van_trips >= 50000)

    # Constraint 2: Budget constraint.
    model.Add(300 * truck_trips + 100 * van_trips <= 12500)

    # Constraint 3: Vehicle routing constraint.
    model.Add(truck_trips <= van_trips)

    # Objective: minimize total trips.
    total_trips = model.NewIntVar(0, 150, "total_trips")
    model.Add(total_trips == truck_trips + van_trips)
    model.Minimize(total_trips)

    # Solve the model.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    result = {}
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        result = {
            "model": "CpModel",
            "variables": {
                "NumTrips": {
                    "0": solver.Value(truck_trips),
                    "1": solver.Value(van_trips)
                },
                "NumVehicles": {
                    "0": solver.Value(truck_trips),
                    "1": solver.Value(van_trips)
                }
            },
            "objective": solver.Value(total_trips)
        }
    else:
        result = {"model": "CpModel", "message": "No optimal solution found."}
    return result

def main():
    # Solve using the linear solver based model.
    linear_result = solve_with_linear_solver()

    # Solve using the cp_model based model.
    cp_result = solve_with_cp_model()

    # Output both models results in a structured way.
    results = {
        "LinearSolverImplementation": linear_result,
        "CpModelImplementation": cp_result
    }
    print(results)

if __name__ == "__main__":
    main()

'''Execution Results:
SUCCESS:
{'LinearSolverImplementation': {'model': 'LinearSolver', 'variables': {'NumTrips': {'0': 25.0, '1': 50.0}, 'NumVehicles': {'0': 25.0, '1': 50.0}}, 'objective': 75.0}, 'CpModelImplementation': {'model': 'CpModel', 'variables': {'NumTrips': {'0': 25, '1': 50}, 'NumVehicles': {'0': 25, '1': 50}}, 'objective': 75}}
'''

'''Expected Output:
Expected solution

: {'variables': {'NumTrips': {'0': 25.0, '1': 50.0}, 'NumVehicles': {'0': 0.0, '1': -0.0}}, 'objective': 75.0}'''

