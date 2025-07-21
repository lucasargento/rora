# Problem Description:
'''Problem description: An extremely large ski resort is looking into purchasing two types of ski lifts, a densely-seated one and a loosely-seated one. The densely-seated ski lift is able to bring 45 guests up the slopes every minute whereas the loosely-seated ski lift can transport 20 guests every minute.  The densely-seated ski lift uses 30 units of electricity and the loosely-seated lift uses 22 units of electricity. There must be at least five loosely-seated ski lifts because they move slower and are friendlier for beginners. The ski resort needs at least 1000 guests every minute to make a profit and has available 940 units of electricity. How many of each type of ski lifts should they plan to install to minimize the total number of ski lifts needed?

Expected Output Schema:
{
  "variables": {
    "LooselySeatedLift": "float",
    "DenselySeatedLift": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- LiftTypes = {LooselySeated, DenselySeated}
  (Note: The two types of ski lifts in the problem)

Parameters:
- capacity_per_minute:
  - For LooselySeated: 20 guests per minute
  - For DenselySeated: 45 guests per minute
- electricity_per_lift:
  - For LooselySeated: 22 electricity units per minute (assumed per lift)
  - For DenselySeated: 30 electricity units per minute (assumed per lift)
- required_guests: 1000 guests per minute (minimum capacity to be profitable)
- electricity_limit: 940 electricity units available per minute
- min_loosely_seated: 5 lifts (guaranteeing sufficient service for beginners)

Variables:
- LooselySeatedLift: integer >= 5
  (Number of loosely-seated ski lifts to install)
- DenselySeatedLift: integer >= 0
  (Number of densely-seated ski lifts to install)

Objective:
- Minimize total_lifts = LooselySeatedLift + DenselySeatedLift
  (The objective is to minimize the total number of lifts installed)

Constraints:
1. Guest Capacity Constraint:
   - 20 * LooselySeatedLift + 45 * DenselySeatedLift >= 1000
   (Ensures that at least 1000 guests are transported per minute)
2. Electricity Usage Constraint:
   - 22 * LooselySeatedLift + 30 * DenselySeatedLift <= 940
   (Ensures that the total electricity consumption does not exceed 940 units)
3. Minimum Loosely-Seated Lifts Constraint:
   - LooselySeatedLift >= 5
   (At least five loosely-seated lifts must be installed)

Expected Output Schema:
{
  "variables": {
    "LooselySeatedLift": "integer (>= 5)",
    "DenselySeatedLift": "integer (>= 0)"
  },
  "objective": "Minimize (LooselySeatedLift + DenselySeatedLift)"
}'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_ski_lift_problem():
    # Create the mip solver with the CBC backend.
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Solver not created.")
        return None

    # Variables
    # LooselySeatedLift: integer >= 5
    # DenselySeatedLift: integer >= 0
    loosely = solver.IntVar(5.0, solver.infinity(), 'LooselySeatedLift')
    densely = solver.IntVar(0.0, solver.infinity(), 'DenselySeatedLift')

    # Constraints:
    # 1. Guest capacity constraint: 20 * loosely + 45 * densely >= 1000
    solver.Add(20 * loosely + 45 * densely >= 1000)

    # 2. Electricity usage constraint: 22 * loosely + 30 * densely <= 940
    solver.Add(22 * loosely + 30 * densely <= 940)

    # Objective: minimize total number of lifts = loosely + densely
    solver.Minimize(loosely + densely)

    # Solve the problem and check the status.
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "variables": {
                "LooselySeatedLift": int(loosely.solution_value()),
                "DenselySeatedLift": int(densely.solution_value())
            },
            "objective": solver.Objective().Value()
        }
        return result
    elif status == pywraplp.Solver.FEASIBLE:
        print("A suboptimal solution was found.")
        return None
    else:
        print("No solution found.")
        return None

def main():
    # Since the problem formulation is unique, we only have one model implementation.
    print("Solution for the Ski Lift Problem (Minimize Total Lifts):")
    result = solve_ski_lift_problem()
    if result is not None:
        print(result)
    else:
        print("The problem is infeasible or no optimal solution exists.")

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Solution for the Ski Lift Problem (Minimize Total Lifts):
{'variables': {'LooselySeatedLift': 5, 'DenselySeatedLift': 20}, 'objective': 25.0}
'''

'''Expected Output:
Expected solution

: {'variables': {'LooselySeatedLift': 5.0, 'DenselySeatedLift': 20.0}, 'objective': 25.0}'''

