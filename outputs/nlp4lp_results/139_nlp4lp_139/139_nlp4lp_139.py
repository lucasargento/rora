# Problem Description:
'''Problem description: A farmer decides to move his cows to a nearby farm using helicopters and trucks. A helicopter can take 3 cows per trip and creates 5 units of pollution. A truck can take 7 cows per trip and creates 10 units of pollution. The farmer needs to transport 80 cows and he only has enough money for at most 8 truck trips. How many of each type of trip should be taken to minimize the total amount of pollution produced?

Expected Output Schema:
{
  "variables": {
    "NumHelicopterTrips": "float",
    "NumTruckTrips": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- M: set of transportation modes = {Helicopter, Truck}

Parameters:
- TotalCows: total number of cows to transport [cows] = 80
- Capacity_H: number of cows per helicopter trip [cows/trip] = 3
- Capacity_T: number of cows per truck trip [cows/trip] = 7
- Pollution_H: pollution generated per helicopter trip [pollution units/trip] = 5
- Pollution_T: pollution generated per truck trip [pollution units/trip] = 10
- MaxTruckTrips: maximum allowed truck trips [trips] = 8
  // Assumption: All units are consistent (cows, trips, pollution units). Trips must be integer,
  // however, we allow continuous variables for a relaxed version per expected output schema.

Variables:
- NumHelicopterTrips: number of helicopter trips to use [continuous, ≥ 0] (in implementation, may be integer)
- NumTruckTrips: number of truck trips to use [continuous, ≥ 0] (in implementation, may be integer)

Objective:
- Minimize TotalPollution = Pollution_H * NumHelicopterTrips + Pollution_T * NumTruckTrips
  // This represents the total pollution produced by all trips.

Constraints:
1. Cows Transported Constraint:
   Capacity_H * NumHelicopterTrips + Capacity_T * NumTruckTrips ≥ TotalCows
   // The total number of cows transported must be at least 80.
2. Truck Trips Limit:
   NumTruckTrips ≤ MaxTruckTrips
   // The number of truck trips cannot exceed 8.

Final Structured Model Output Schema:
{
  "variables": {
    "NumHelicopterTrips": "float (≥ 0)",
    "NumTruckTrips": "float (≥ 0)"
  },
  "objective": "Minimize 5 * NumHelicopterTrips + 10 * NumTruckTrips"
}'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_continuous_model():
    """Solve the continuous relaxation of the cow transportation problem using OR-Tools' linear solver (GLOP)."""
    # Create the linear solver with the GLOP backend (for continuous LPs).
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Failed to create solver instance.")
        return None

    # -----------------------------
    # Parameters
    total_cows = 80
    capacity_h = 3   # cows per helicopter trip
    capacity_t = 7   # cows per truck trip
    pollution_h = 5  # pollution units per helicopter trip
    pollution_t = 10 # pollution units per truck trip
    max_truck_trips = 8

    # -----------------------------
    # Variables
    # Define continuous variables for the number of trips (≥ 0)
    num_helicopter_trips = solver.NumVar(0.0, solver.infinity(), 'NumHelicopterTrips')
    num_truck_trips = solver.NumVar(0.0, solver.infinity(), 'NumTruckTrips')

    # -----------------------------
    # Constraints
    # 1. Cows transported constraint: 3 * NumHelicopterTrips + 7 * NumTruckTrips ≥ 80.
    solver.Add(capacity_h * num_helicopter_trips + capacity_t * num_truck_trips >= total_cows)
    # 2. Truck trips limit: NumTruckTrips ≤ 8.
    solver.Add(num_truck_trips <= max_truck_trips)

    # -----------------------------
    # Objective: Minimize total pollution = 5 * NumHelicopterTrips + 10 * NumTruckTrips.
    objective = solver.Objective()
    objective.SetCoefficient(num_helicopter_trips, pollution_h)
    objective.SetCoefficient(num_truck_trips, pollution_t)
    objective.SetMinimization()

    # -----------------------------
    # Solve the model.
    status = solver.Solve()

    # Prepare results.
    if status == pywraplp.Solver.OPTIMAL:
        solution = {
            "variables": {
                "NumHelicopterTrips": num_helicopter_trips.solution_value(),
                "NumTruckTrips": num_truck_trips.solution_value()
            },
            "objective": objective.Value()
        }
        return solution
    else:
        print("The problem does not have an optimal solution.")
        return None

def main():
    # Since the mathematical formulation suggests a continuous model, we only implement the continuous version.
    continuous_solution = solve_continuous_model()
    
    print("Continuous Model Solution:")
    if continuous_solution:
        print("Optimal number of Helicopter Trips:", continuous_solution["variables"]["NumHelicopterTrips"])
        print("Optimal number of Truck Trips:", continuous_solution["variables"]["NumTruckTrips"])
        print("Minimum Total Pollution:", continuous_solution["objective"])
    else:
        print("No solution found for the continuous model.")

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Continuous Model Solution:
Optimal number of Helicopter Trips: 8.0
Optimal number of Truck Trips: 8.0
Minimum Total Pollution: 120.0
'''

'''Expected Output:
Expected solution

: {'variables': {'NumHelicopterTrips': 8.0, 'NumTruckTrips': 8.0}, 'objective': 120.0}'''

