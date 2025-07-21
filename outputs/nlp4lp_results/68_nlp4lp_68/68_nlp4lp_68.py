# Problem Description:
'''Problem description: A man fishes in a 250 acre lake and can catch fish either using a net or fishing line. For each acre of the lake, using a net will catch 8 fish and requires 4 units of bait but also causes 2 units of pain for the fisherman. For each acre of the lake, using a fishing line will catch 5 fish and requires 3 units of bait but also causes 1 unit of pain for the fisherman. The fisherman has available 800 units of bait and can tolerate at most 350 units of pain. For how many acres each should he use each fishing method to maximize the amount of fish he can catch?

Expected Output Schema:
{
  "variables": {
    "AcresNet": "float",
    "AcresLine": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- F: set of fishing methods = {Net, Line}

Parameters:
- lake_area: total available lake area [acres] = 250
- fish_net: fish caught per acre using a net [fish/acre] = 8
- fish_line: fish caught per acre using a fishing line [fish/acre] = 5
- bait_net: bait required per acre using a net [units/acre] = 4
- bait_line: bait required per acre using a fishing line [units/acre] = 3
- pain_net: pain incurred per acre using a net [pain units/acre] = 2
- pain_line: pain incurred per acre using a fishing line [pain units/acre] = 1
- bait_available: total available bait [units] = 800
- pain_tolerance: maximum tolerable pain [pain units] = 350

Variables:
- AcresNet: acres of lake fished using the net [continuous, acres, ≥ 0]
- AcresLine: acres of lake fished using the fishing line [continuous, acres, ≥ 0]

Objective:
- Maximize total fish caught = (fish_net * AcresNet) + (fish_line * AcresLine)
  (i.e., Maximize 8 * AcresNet + 5 * AcresLine)

Constraints:
1. Lake area constraint:
   - AcresNet + AcresLine ≤ lake_area
   - (AcresNet + AcresLine ≤ 250 acres)
2. Bait availability constraint:
   - (bait_net * AcresNet) + (bait_line * AcresLine) ≤ bait_available
   - (4 * AcresNet + 3 * AcresLine ≤ 800 units)
3. Pain tolerance constraint:
   - (pain_net * AcresNet) + (pain_line * AcresLine) ≤ pain_tolerance
   - (2 * AcresNet + 1 * AcresLine ≤ 350 units)

Comments:
- All parameters are taken directly from the problem statement and units are consistent (acres for area, fish per acre, units of bait, and pain units).
- The decision variables are continuous since fractional acres can be considered.
- The objective is solely focused on maximizing the fish yield without mixing revenues and costs.

This completes the five-element structured mathematical model for the fishing problem.'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_using_linear_solver():
    # Create the linear solver using the GLOP backend for linear programming.
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Linear solver (GLOP) is not available.")
        return None

    # Decision Variables:
    # AcresNet: acres fished using the net (≥ 0)
    # AcresLine: acres fished using the fishing line (≥ 0)
    AcresNet = solver.NumVar(0.0, solver.infinity(), 'AcresNet')
    AcresLine = solver.NumVar(0.0, solver.infinity(), 'AcresLine')

    # Constraints:
    # 1. Lake area constraint: AcresNet + AcresLine ≤ 250 acres.
    solver.Add(AcresNet + AcresLine <= 250)
    # 2. Bait availability constraint: 4 * AcresNet + 3 * AcresLine ≤ 800 units.
    solver.Add(4 * AcresNet + 3 * AcresLine <= 800)
    # 3. Pain tolerance constraint: 2 * AcresNet + 1 * AcresLine ≤ 350 pain units.
    solver.Add(2 * AcresNet + AcresLine <= 350)

    # Objective:
    # Maximize fish caught = 8 * AcresNet + 5 * AcresLine.
    solver.Maximize(8 * AcresNet + 5 * AcresLine)

    # Solve the model.
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        solution = {
            "AcresNet": AcresNet.solution_value(),
            "AcresLine": AcresLine.solution_value(),
            "objective": solver.Objective().Value()
        }
        return solution
    else:
        print("The linear solver problem does not have an optimal solution.")
        return None

def main():
    # Since the problem formulation is unique and linear,
    # we implement it only once using the linear solver model.
    result_linear = solve_using_linear_solver()

    if result_linear:
        print("Results for Linear Solver Implementation:")
        print("AcresNet:", result_linear["AcresNet"])
        print("AcresLine:", result_linear["AcresLine"])
        print("Total Fish Caught (Objective):", result_linear["objective"])
    else:
        print("No optimal solution found in the linear solver model.")

if __name__ == "__main__":
    main()

'''Execution Results:
SUCCESS:
Results for Linear Solver Implementation:
AcresNet: 124.99999999999991
AcresLine: 100.00000000000014
Total Fish Caught (Objective): 1500.0
'''

'''Expected Output:
Expected solution

: {'variables': {'AcresNet': 50.0, 'AcresLine': 200.0}, 'objective': 1400.0}'''

