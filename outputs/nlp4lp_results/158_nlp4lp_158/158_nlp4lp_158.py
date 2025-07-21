# Problem Description:
'''Problem description: A tourist spot in the mountains allows visitors to travel to the top either by hot-air balloon or gondola lift. A hot air balloon can carry 4 visitors while a gondola lift can carry 6 visitors. Each hot air balloon produces 10 units of pollution while each gondola lift produces 15 units of pollution. There can be at most 10 hot-air balloon rides and at least 70 visitors need to be transported. How many of each type of transport method should be taken to minimize the total pollution produced?

Expected Output Schema:
{
  "variables": {
    "BalloonRides": "float",
    "GondolaLifts": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- Method: set of transportation methods = {HotAirBalloon, GondolaLift}

Parameters:
- Capacity_Balloon: number of visitors per hot-air balloon ride = 4 (visitors/ride)
- Capacity_Gondola: number of visitors per gondola lift = 6 (visitors/ride)
- Pollution_Balloon: pollution produced per hot-air balloon ride = 10 (pollution units/ride)
- Pollution_Gondola: pollution produced per gondola lift = 15 (pollution units/ride)
- Max_Balloon_Rides: maximum allowable hot-air balloon rides = 10 (rides)
- Min_Visitors: minimum visitors to transport = 70 (visitors)

Variables:
- BalloonRides: number of hot-air balloon rides taken [integer, ≥ 0] (rides)
- GondolaLifts: number of gondola lifts taken [integer, ≥ 0] (rides)

Objective:
- Minimize total pollution produced = (Pollution_Balloon * BalloonRides) + (Pollution_Gondola * GondolaLifts)

Constraints:
1. Visitor Transportation Constraint:
   - (Capacity_Balloon * BalloonRides) + (Capacity_Gondola * GondolaLifts) ≥ Min_Visitors
   - This ensures that at least 70 visitors are transported.
2. Hot-Air Balloon Ride Limit:
   - BalloonRides ≤ Max_Balloon_Rides
   - This restricts the number of hot-air balloon rides to at most 10.

------------------------------------------------------------
Expected Output Schema:
{
  "variables": {
    "BalloonRides": "integer, ≥ 0",
    "GondolaLifts": "integer, ≥ 0"
  },
  "objective": "Minimize (10 * BalloonRides) + (15 * GondolaLifts)"
}'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_transportation_problem():
    # Create the solver using CBC mixed integer programming.
    solver = pywraplp.Solver.CreateSolver('CBC_MIXED_INTEGER_PROGRAMMING')
    if not solver:
        print("Solver not created.")
        return None

    # Parameters
    capacity_balloon = 4        # visitors per hot-air balloon ride
    capacity_gondola = 6        # visitors per gondola lift ride
    pollution_balloon = 10      # pollution units per hot-air balloon ride
    pollution_gondola = 15      # pollution units per gondola lift ride
    max_balloon_rides = 10      # maximum number of hot-air balloon rides
    min_visitors = 70           # minimum visitors to transport

    # Variables
    balloon_rides = solver.IntVar(0, max_balloon_rides, 'BalloonRides')
    gondola_lifts = solver.IntVar(0, solver.infinity(), 'GondolaLifts')

    # Constraints
    # Visitor Transportation Constraint:
    # (capacity_balloon * balloon_rides) + (capacity_gondola * gondola_lifts) >= min_visitors
    solver.Add(capacity_balloon * balloon_rides + capacity_gondola * gondola_lifts >= min_visitors)

    # Note: The constraint balloon_rides <= max_balloon_rides is already applied through variable bounds
    # Thus, we don't need to add it again.

    # Objective: Minimize total pollution produced = (pollution_balloon * balloon_rides) + (pollution_gondola * gondola_lifts)
    objective = solver.Objective()
    objective.SetCoefficient(balloon_rides, pollution_balloon)
    objective.SetCoefficient(gondola_lifts, pollution_gondola)
    objective.SetMinimization()

    # Solve the problem
    status = solver.Solve()

    # Create a dictionary to store the results
    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result['BalloonRides'] = balloon_rides.solution_value()
        result['GondolaLifts'] = gondola_lifts.solution_value()
        result['objective'] = objective.Value()
    elif status == pywraplp.Solver.INFEASIBLE:
        result['error'] = "The problem is infeasible."
    else:
        result['error'] = "Solver ended with non-optimal solution."

    return result

def main():
    # Since only one formulation was provided, we call the single model implementation.
    result_linear = solve_transportation_problem()

    print("Linear Solver Implementation Result:")
    if 'error' in result_linear:
        print(result_linear['error'])
    else:
        print("Optimal solution:")
        print("  BalloonRides =", result_linear['BalloonRides'])
        print("  GondolaLifts =", result_linear['GondolaLifts'])
        print("  Objective (Total Pollution) =", result_linear['objective'])

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Linear Solver Implementation Result:
Optimal solution:
  BalloonRides = 10.0
  GondolaLifts = 5.0
  Objective (Total Pollution) = 175.0
'''

'''Expected Output:
Expected solution

: {'variables': {'BalloonRides': 1.0, 'GondolaLifts': 11.0}, 'objective': 175.0}'''

