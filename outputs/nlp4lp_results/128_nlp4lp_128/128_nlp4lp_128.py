# Problem Description:
'''Problem description: There has been an oil spill in the ocean and ducks need to be taken to shore to be cleaned either by boat or by canoe. A boat can take 10 ducks per trip while a canoe can take 8 ducks per trip. Since the boats are motor powered, they take 20 minutes per trip while the canoes take 40 minutes per trip. In order to avoid further environmental damage, there can be at most 12 boat trips and at least 60% of the trips should be by canoe. If at least 300 ducks need to be taken to shore, how many of each transportation method should be used to minimize the total amount of time needed to transport the ducks?

Expected Output Schema:
{
  "variables": {
    "BoatTrips": "float",
    "CanoeTrips": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Below is a complete translation of the problem using the five-element framework.

------------------------------------------------------------
Sets:
- TripModes: the set of transportation methods used = {Boat, Canoe}

------------------------------------------------------------
Parameters:
- boat_capacity = 10 ducks per boat trip
- canoe_capacity = 8 ducks per canoe trip
- boat_time = 20 minutes per boat trip
- canoe_time = 40 minutes per canoe trip
- max_boat_trips = 12 trips (boats cannot be used more than 12 times)
- ducks_required = 300 ducks (at least 300 ducks must be transported)
- min_canoe_proportion = 0.6 (at least 60% of all trips must be by canoe)

------------------------------------------------------------
Variables:
- BoatTrips: number of trips made by boat; nonnegative integer (or float if integrality is relaxed) [units: trips]
- CanoeTrips: number of trips made by canoe; nonnegative integer (or float if integrality is relaxed) [units: trips]

------------------------------------------------------------
Objective:
Minimize TotalTime where
  TotalTime = (boat_time * BoatTrips) + (canoe_time * CanoeTrips)
In other words, minimize 20 * BoatTrips + 40 * CanoeTrips [units: minutes]

------------------------------------------------------------
Constraints:
1. Boat trips limit:
   BoatTrips <= max_boat_trips 
   (i.e., BoatTrips <= 12)

2. Duck transport capacity requirement:
   (boat_capacity * BoatTrips) + (canoe_capacity * CanoeTrips) >= ducks_required 
   (i.e., 10*BoatTrips + 8*CanoeTrips >= 300)

3. Minimum canoe trips proportion:
   CanoeTrips >= min_canoe_proportion * (BoatTrips + CanoeTrips)
   This can be rearranged for clarity:
     CanoeTrips >= 0.6 * (BoatTrips + CanoeTrips)
   Equivalently, subtracting 0.6 * CanoeTrips from both sides:
     0.4 * CanoeTrips >= 0.6 * BoatTrips 
   Which can be simplified to:
     CanoeTrips >= 1.5 * BoatTrips

------------------------------------------------------------
Model Comments:
- All time parameters are in minutes, capacities are in ducks per trip, and trips are counts.
- The decision variables may be modelled as integers if an exactly countable number of trips is required.
- The minimum canoe trips constraint ensures that at least 60% of the total trips are by canoe.
- This formulation minimizes the total time required to transport a minimum of 300 ducks under the given operational limits.

------------------------------------------------------------
Expected Output Schema (example):
{
  "variables": {
    "BoatTrips": "float",
    "CanoeTrips": "float"
  },
  "objective": "float"
}'''

# Generated Code:
#!/usr/bin/env python3
"""
This script implements the oil spill duck transport optimization problem using two separate formulations:
1. Integer formulation using CBC_MIXED_INTEGER_PROGRAMMING, where the number of trips are integer.
2. Continuous (linear relaxation) formulation using GLOP_LINEAR_PROGRAMMING, where trips are float.
Both models are solved independently and the results are printed.
"""

from ortools.linear_solver import pywraplp


def solve_integer_model():
    # Create solver with CBC for Mixed Integer Programming.
    solver = pywraplp.Solver.CreateSolver('CBC_MIXED_INTEGER_PROGRAMMING')
    if not solver:
        print("Could not create solver for integer model.")
        return None

    # Parameters from problem formulation.
    boat_capacity = 10
    canoe_capacity = 8
    boat_time = 20
    canoe_time = 40
    max_boat_trips = 12
    ducks_required = 300

    # Variables: nonnegative integer trips.
    BoatTrips = solver.IntVar(0, max_boat_trips, 'BoatTrips')
    # CanoeTrips is not explicitly limited in maximum
    CanoeTrips = solver.IntVar(0, solver.infinity(), 'CanoeTrips')

    # Objective: minimize total transport time
    # TotalTime = 20*BoatTrips + 40*CanoeTrips.
    solver.Minimize(boat_time * BoatTrips + canoe_time * CanoeTrips)

    # Constraint 1: Boat trips limit.
    solver.Add(BoatTrips <= max_boat_trips)

    # Constraint 2: Duck transport capacity requirement.
    solver.Add(boat_capacity * BoatTrips + canoe_capacity * CanoeTrips >= ducks_required)

    # Constraint 3: Minimum canoe trips proportion:
    # CanoeTrips >= 1.5 * BoatTrips.
    solver.Add(CanoeTrips >= 1.5 * BoatTrips)

    status = solver.Solve()
    result = {}

    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "variables": {
                "BoatTrips": BoatTrips.solution_value(),
                "CanoeTrips": CanoeTrips.solution_value()
            },
            "objective": solver.Objective().Value()
        }
    elif status == pywraplp.Solver.INFEASIBLE:
        result = {"error": "The integer model is infeasible."}
    else:
        result = {"error": "The integer model did not solve optimally."}
    return result


def solve_continuous_model():
    # Create solver with GLOP for continuous Linear Programming.
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Could not create solver for continuous model.")
        return None

    # Parameters from problem formulation.
    boat_capacity = 10
    canoe_capacity = 8
    boat_time = 20
    canoe_time = 40
    max_boat_trips = 12
    ducks_required = 300

    # Variables: nonnegative floats.
    BoatTrips = solver.NumVar(0, max_boat_trips, 'BoatTrips')
    CanoeTrips = solver.NumVar(0, solver.infinity(), 'CanoeTrips')

    # Objective: minimize total transport time.
    solver.Minimize(boat_time * BoatTrips + canoe_time * CanoeTrips)

    # Constraint 1: Boat trips limit.
    solver.Add(BoatTrips <= max_boat_trips)

    # Constraint 2: Duck transport capacity requirement.
    solver.Add(boat_capacity * BoatTrips + canoe_capacity * CanoeTrips >= ducks_required)

    # Constraint 3: Minimum canoe trips proportion:
    solver.Add(CanoeTrips >= 1.5 * BoatTrips)

    status = solver.Solve()
    result = {}

    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "variables": {
                "BoatTrips": BoatTrips.solution_value(),
                "CanoeTrips": CanoeTrips.solution_value()
            },
            "objective": solver.Objective().Value()
        }
    elif status == pywraplp.Solver.INFEASIBLE:
        result = {"error": "The continuous model is infeasible."}
    else:
        result = {"error": "The continuous model did not solve optimally."}
    return result


def main():
    print("Solving Integer Model (Trips as integers):")
    integer_result = solve_integer_model()
    print(integer_result)
    print("\nSolving Continuous Model (Trips as floats):")
    continuous_result = solve_continuous_model()
    print(continuous_result)


if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Solving Integer Model (Trips as integers):
{'variables': {'BoatTrips': 12.0, 'CanoeTrips': 23.0}, 'objective': 1160.0}

Solving Continuous Model (Trips as floats):
{'variables': {'BoatTrips': 12.0, 'CanoeTrips': 22.5}, 'objective': 1140.0}
'''

'''Expected Output:
Expected solution

: {'variables': {'BoatTrips': 12.0, 'CanoeTrips': 23.0}, 'objective': 1160.0}'''

