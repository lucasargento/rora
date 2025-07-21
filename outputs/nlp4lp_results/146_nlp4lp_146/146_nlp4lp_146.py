# Problem Description:
'''Problem description: A snack exporter sends snacks to his customer in small and large suitcases. A small suitcase can hold 50 snacks while a large suitcase can hold 80 snacks. Most customer prefer small suitcases, and so at least twice as many small suitcases must be used as large suitcases. The exporter has available at most 70 small suitcases and 50 large suitcases. If he must send at least 15 large suitcases and can send  at most 70 suitcases in total, how many of each should he send to maximize the total number of snacks that can be delivered?

Expected Output Schema:
{
  "variables": {
    "SmallSuitcasesUsed": "float",
    "LargeSuitcasesUsed": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- SuitcaseTypes: {Small, Large}

Parameters:
- snackCapacitySmall: number of snacks a small suitcase holds = 50 snacks per suitcase
- snackCapacityLarge: number of snacks a large suitcase holds = 80 snacks per suitcase
- minSmallToLargeRatio: minimum ratio of small to large suitcases = 2 (i.e., number of small suitcases must be at least twice the number of large suitcases)
- maxSmallAvailable: maximum available small suitcases = 70 suitcases
- maxLargeAvailable: maximum available large suitcases = 50 suitcases
- minLargeRequired: minimum number of large suitcases required = 15 suitcases
- maxTotalSuitcases: maximum total suitcases that can be sent = 70 suitcases

Variables:
- SmallSuitcasesUsed: integer variable representing the number of small suitcases used (units: suitcases), where 0 ≤ SmallSuitcasesUsed ≤ maxSmallAvailable
- LargeSuitcasesUsed: integer variable representing the number of large suitcases used (units: suitcases), where minLargeRequired ≤ LargeSuitcasesUsed ≤ maxLargeAvailable

Objective:
- Maximize TotalSnacksDelivered = snackCapacitySmall * SmallSuitcasesUsed + snackCapacityLarge * LargeSuitcasesUsed
  (Units: snacks delivered)

Constraints:
1. Suitcase Ratio Constraint: SmallSuitcasesUsed ≥ minSmallToLargeRatio * LargeSuitcasesUsed
2. Small Suitcase Availability: SmallSuitcasesUsed ≤ maxSmallAvailable
3. Large Suitcase Availability: LargeSuitcasesUsed ≤ maxLargeAvailable
4. Total Suitcase Limit: SmallSuitcasesUsed + LargeSuitcasesUsed ≤ maxTotalSuitcases
5. Minimum Large Suitcases: LargeSuitcasesUsed ≥ minLargeRequired

--------------------------------------------------
Following the Expected Output Schema, here is the digest:

{
  "variables": {
    "SmallSuitcasesUsed": "integer ≥ 0 and ≤ 70",
    "LargeSuitcasesUsed": "integer between 15 and 50, with additional ratio and total constraints"
  },
  "objective": "Maximize total snacks: 50 * SmallSuitcasesUsed + 80 * LargeSuitcasesUsed"
}'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp
from ortools.sat.python import cp_model

def solve_with_linear_solver():
    # Create the MIP solver with CBC backend
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        return None, "Linear solver not created successfully."

    # Parameters
    snackCapacitySmall = 50
    snackCapacityLarge = 80
    minSmallToLargeRatio = 2
    maxSmallAvailable = 70
    maxLargeAvailable = 50
    minLargeRequired = 15
    maxTotalSuitcases = 70

    # Variables: They are integers.
    small = solver.IntVar(0, maxSmallAvailable, 'SmallSuitcasesUsed')
    large = solver.IntVar(minLargeRequired, maxLargeAvailable, 'LargeSuitcasesUsed')

    # Constraints
    # 1. Suitcase Ratio Constraint: small >= 2 * large
    solver.Add(small >= minSmallToLargeRatio * large)
    # 2. Total Suitcase Limit: small + large <= maxTotalSuitcases
    solver.Add(small + large <= maxTotalSuitcases)

    # Objective: maximize total snacks delivered
    # 50 * small + 80 * large
    objective = solver.Objective()
    objective.SetCoefficient(small, snackCapacitySmall)
    objective.SetCoefficient(large, snackCapacityLarge)
    objective.SetMaximization()

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "SmallSuitcasesUsed": small.solution_value(),
            "LargeSuitcasesUsed": large.solution_value()
        }
        optimal_value = objective.Value()
        return (result, optimal_value)
    elif status == pywraplp.Solver.FEASIBLE:
        return None, "A feasible solution was found, but it may not be optimal."
    else:
        return None, "No feasible solution exists for the linear model."

def solve_with_cp_model():
    # Create the CP-SAT model
    model = cp_model.CpModel()

    # Parameters
    snackCapacitySmall = 50
    snackCapacityLarge = 80
    minSmallToLargeRatio = 2
    maxSmallAvailable = 70
    maxLargeAvailable = 50
    minLargeRequired = 15
    maxTotalSuitcases = 70

    # Variables: They are integer variables.
    small = model.NewIntVar(0, maxSmallAvailable, 'SmallSuitcasesUsed')
    large = model.NewIntVar(minLargeRequired, maxLargeAvailable, 'LargeSuitcasesUsed')

    # Constraints
    # 1. Suitcase Ratio Constraint: small >= 2 * large
    model.Add(small >= minSmallToLargeRatio * large)
    # 2. Total Suitcase Limit: small + large <= maxTotalSuitcases
    model.Add(small + large <= maxTotalSuitcases)

    # Since CP-SAT does not natively support maximization of a linear function with multiplication
    # we define an objective variable for total snacks delivered.
    total_snacks = model.NewIntVar(0, snackCapacitySmall * maxSmallAvailable + snackCapacityLarge * maxLargeAvailable, 'TotalSnacksDelivered')
    # Linking constraint: total_snacks == 50*small + 80*large
    model.Add(total_snacks == snackCapacitySmall * small + snackCapacityLarge * large)

    # Objective: maximize total snacks delivered
    model.Maximize(total_snacks)

    # Create the solver and solve.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        result = {
            "SmallSuitcasesUsed": solver.Value(small),
            "LargeSuitcasesUsed": solver.Value(large)
        }
        optimal_value = solver.Value(total_snacks)
        return (result, optimal_value)
    else:
        return None, "No feasible solution exists for the CP model."

def main():
    results = {}

    # Solve using Linear Solver (MIP)
    linear_result, linear_obj = solve_with_linear_solver()
    if linear_result is not None:
        results['LinearSolver'] = {
            "Solution": linear_result,
            "TotalSnacksDelivered": linear_obj
        }
    else:
        results['LinearSolver'] = {"Error": linear_obj}

    # Solve using CP-SAT Solver
    cp_result, cp_obj = solve_with_cp_model()
    if cp_result is not None:
        results['CPSolver'] = {
            "Solution": cp_result,
            "TotalSnacksDelivered": cp_obj
        }
    else:
        results['CPSolver'] = {"Error": cp_obj}

    # Print structured results
    print("Optimization Results:")
    for method, outcome in results.items():
        print(f"\nMethod: {method}")
        for key, value in outcome.items():
            print(f"  {key}: {value}")

if __name__ == "__main__":
    main()

'''Execution Results:
SUCCESS:
Optimization Results:

Method: LinearSolver
  Solution: {'SmallSuitcasesUsed': 47.0, 'LargeSuitcasesUsed': 23.0}
  TotalSnacksDelivered: 4190.0

Method: CPSolver
  Solution: {'SmallSuitcasesUsed': 47, 'LargeSuitcasesUsed': 23}
  TotalSnacksDelivered: 4190
'''

'''Expected Output:
Expected solution

: {'variables': {'SmallSuitcasesUsed': 47.0, 'LargeSuitcasesUsed': 23.0}, 'objective': 4190.0}'''

