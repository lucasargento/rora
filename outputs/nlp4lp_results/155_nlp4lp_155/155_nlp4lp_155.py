# Problem Description:
'''Problem description: An industrial tire company delivers large tires for equipment to remote engineering sites either by cargo planes or ultrawide trucks. Each cargo plane can transport 10 tires per trip and costs $1000. Each ultrawide truck can transport 6 tires per trip and costs $700. The company needs to transport at least 200 tires and has available $22000. Because most remote sites don't have proper airports, the number of plane trips cannot exceed the number of ultrawide truck trips. How many trips of each should be done to minimize the total number of trips?

Expected Output Schema:
{
  "variables": {
    "PlaneTrips": "float",
    "TruckTrips": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- TransportModes: the set of delivery methods available = {Plane, Truck}

Parameters:
- plane_capacity: tires delivered per plane trip = 10 tires/trip
- truck_capacity: tires delivered per truck trip = 6 tires/trip
- plane_cost: cost per plane trip = 1000 dollars/trip
- truck_cost: cost per truck trip = 700 dollars/trip
- tire_requirement: minimum number of tires to transport = 200 tires
- available_budget: maximum spending available = 22000 dollars
- Note: All monetary units are in US dollars, capacities in number of tires, and trips are counted by number of trips.

Variables:
- PlaneTrips: number of cargo plane trips (continuous variable, but representable as integer in practice, measured in trips; units: trips)
- TruckTrips: number of ultrawide truck trips (continuous variable, but representable as integer in practice, measured in trips; units: trips)

Objective:
- Minimize total trips: TotalTrips = PlaneTrips + TruckTrips

Constraints:
1. Tire delivery requirement:
   - 10 * PlaneTrips + 6 * TruckTrips >= 200
   (The total number of tires delivered must be at least 200.)

2. Budget constraint:
   - 1000 * PlaneTrips + 700 * TruckTrips <= 22000
   (Total transportation cost cannot exceed 22000 dollars.)

3. Mode balance constraint:
   - PlaneTrips <= TruckTrips
   (Since many remote sites do not have proper airports, the number of plane trips is not allowed to exceed the number of truck trips.)

Expected Output Schema:
{
  "variables": {
    "PlaneTrips": "float",
    "TruckTrips": "float"
  },
  "objective": "float"
}'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_model():
    # Create the linear solver with SCIP backend.
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        return None, None

    # Variables: number of trips for planes and trucks.
    # Although the formulation mentions continuous variables, in practice these must be integers.
    PlaneTrips = solver.IntVar(0, solver.infinity(), 'PlaneTrips')
    TruckTrips = solver.IntVar(0, solver.infinity(), 'TruckTrips')

    # Constraint 1: Tire delivery requirement
    # 10 * PlaneTrips + 6 * TruckTrips >= 200
    solver.Add(10 * PlaneTrips + 6 * TruckTrips >= 200)

    # Constraint 2: Budget constraint
    # 1000 * PlaneTrips + 700 * TruckTrips <= 22000
    solver.Add(1000 * PlaneTrips + 700 * TruckTrips <= 22000)

    # Constraint 3: Mode balance constraint
    # PlaneTrips <= TruckTrips
    solver.Add(PlaneTrips <= TruckTrips)

    # Objective: Minimize total trips = PlaneTrips + TruckTrips
    solver.Minimize(PlaneTrips + TruckTrips)

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        # Build result dictionary according to expected output schema.
        result = {
            "PlaneTrips": PlaneTrips.solution_value(),
            "TruckTrips": TruckTrips.solution_value()
        }
        objective_value = solver.Objective().Value()
        return result, objective_value
    else:
        return None, None

def main():
    # Since only one formulation is provided, we implement a single model.
    result, obj = solve_model()

    if result is None:
        print("The problem does not have an optimal solution!")
    else:
        # Print the result in the expected output schema.
        print("{")
        print('  "variables": {')
        print(f'    "PlaneTrips": {result["PlaneTrips"]},')
        print(f'    "TruckTrips": {result["TruckTrips"]}')
        print("  },")
        print(f'  "objective": {obj}')
        print("}")

if __name__ == "__main__":
    main()

'''Execution Results:
SUCCESS:
{
  "variables": {
    "PlaneTrips": 11.0,
    "TruckTrips": 15.0
  },
  "objective": 26.0
}
'''

'''Expected Output:
Expected solution

: {'variables': {'PlaneTrips': 12.0, 'TruckTrips': 14.0}, 'objective': 26.0}'''

