# Problem Description:
'''Problem description: A bee farmer transports his honey in small and large bottles. A small bottle can take 5 units of honey while a large bottle can take 20 units of honey. The farmer has available at most 300 small bottles and at most 100 large bottles. In addition, since small bottles are easier to sell, at least twice as many small bottles must be used than large bottles. Finally, he can transport at most 200 bottles total and at least 50 must be large bottles. How many of each bottle should be use to maximize the total amount of honey he can transport?

Expected Output Schema:
{
  "variables": {
    "SmallBottlesUsed": "float",
    "LargeBottlesUsed": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- BottleTypes = {Small, Large}

Parameters:
- capacity_small: honey capacity per small bottle [units] = 5
- capacity_large: honey capacity per large bottle [units] = 20
- max_small: maximum available small bottles [bottles] = 300
- max_large: maximum available large bottles [bottles] = 100
- max_total_bottles: maximum total bottles that can be transported [bottles] = 200
- min_large_used: minimum large bottles to use [bottles] = 50
- small_to_large_ratio: minimum ratio of small bottles to large bottles = 2  (i.e., number of small bottles used must be at least twice the number of large bottles used)

Variables:
- x_small: number of small bottles to use [integer, units = bottles]
- x_large: number of large bottles to use [integer, units = bottles]

Objective:
- Maximize total honey transported = (capacity_small * x_small) + (capacity_large * x_large)

Constraints:
1. Availability constraints:
   - x_small <= max_small
   - x_large <= max_large

2. Total bottle constraint:
   - x_small + x_large <= max_total_bottles

3. Ratio constraint:
   - x_small >= small_to_large_ratio * x_large

4. Minimum large bottle usage constraint:
   - x_large >= min_large_used

Comments:
- All decision variables are assumed to be integer since the number of bottles must be whole numbers.
- The units for capacities are in "units of honey" (e.g., liters, kilograms) as described in the problem but no specific unit was provided.
- This model maximizes the total transported honey subject to the available bottle counts and additional constraints.

Expected Output Schema:
{
  "variables": {
    "SmallBottlesUsed": "float",
    "LargeBottlesUsed": "float"
  },
  "objective": "float"
}'''

# Generated Code:
#!/usr/bin/env python3
"""
This script implements the optimization problem for the bee farmer using two separate formulations:
1. Using ortools.linear_solver (MIP)
2. Using ortools.sat.python.cp_model (CP)
Each model is kept completely separate.
The problem:
    - A small bottle has a capacity of 5 units, a large bottle 20 units.
    - Available: at most 300 small bottles, 100 large bottles.
    - Total bottles used: at most 200.
    - Small bottles used must be at least twice the large bottles used.
    - At least 50 large bottles must be used.
Objective: Maximize the total honey transported.
"""

from ortools.linear_solver import pywraplp
from ortools.sat.python import cp_model

def solve_with_linear_solver():
    """Solves the problem using the MIP solver from ortools.linear_solver."""
    # Create the MIP solver using CBC backend.
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Linear solver not available.")
        return None

    # Data parameters
    capacity_small = 5
    capacity_large = 20
    max_small = 300
    max_large = 100
    max_total_bottles = 200
    min_large_used = 50
    small_to_large_ratio = 2

    # Decision variables: number of bottles used.
    x_small = solver.IntVar(0, max_small, 'SmallBottlesUsed')
    x_large = solver.IntVar(0, max_large, 'LargeBottlesUsed')

    # Constraint 1: Total bottle constraint.
    solver.Add(x_small + x_large <= max_total_bottles)

    # Constraint 2: Ratio constraint.
    solver.Add(x_small >= small_to_large_ratio * x_large)

    # Constraint 3: Minimum large bottle usage.
    solver.Add(x_large >= min_large_used)

    # Objective: Maximize total honey transported.
    objective = solver.Objective()
    objective.SetCoefficient(x_small, capacity_small)
    objective.SetCoefficient(x_large, capacity_large)
    objective.SetMaximization()

    # Solve the problem.
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "variables": {
                "SmallBottlesUsed": x_small.solution_value(),
                "LargeBottlesUsed": x_large.solution_value()
            },
            "objective": objective.Value()
        }
        print("Linear Solver (MIP) Solution:")
        print(result)
        return result
    else:
        print("Linear Solver: No optimal solution found.")
        return None

def solve_with_cp_model():
    """Solves the problem using the CP-SAT solver from ortools.sat.python.cp_model."""
    model = cp_model.CpModel()

    # Data parameters
    capacity_small = 5
    capacity_large = 20
    max_small = 300
    max_large = 100
    max_total_bottles = 200
    min_large_used = 50
    small_to_large_ratio = 2

    # Decision variables: number of bottles used.
    x_small = model.NewIntVar(0, max_small, 'SmallBottlesUsed')
    x_large = model.NewIntVar(0, max_large, 'LargeBottlesUsed')

    # Constraint 1: Total bottle constraint.
    model.Add(x_small + x_large <= max_total_bottles)

    # Constraint 2: Ratio constraint (small >= 2 * large).
    model.Add(x_small >= small_to_large_ratio * x_large)

    # Constraint 3: Minimum large bottle usage.
    model.Add(x_large >= min_large_used)

    # Objective: Maximize total honey transported.
    # Since CP-SAT maximizes integer expressions, we directly add the objective.
    model.Maximize(capacity_small * x_small + capacity_large * x_large)

    # Solve the model.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        result = {
            "variables": {
                "SmallBottlesUsed": solver.Value(x_small),
                "LargeBottlesUsed": solver.Value(x_large)
            },
            "objective": solver.ObjectiveValue()
        }
        print("CP-SAT Solver Solution:")
        print(result)
        return result
    else:
        print("CP-SAT Solver: No optimal solution found.")
        return None

def main():
    print("=== Solving with Linear Solver (MIP) ===")
    linear_result = solve_with_linear_solver()
    
    print("\n=== Solving with CP-SAT Solver ===")
    cp_result = solve_with_cp_model()

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
=== Solving with Linear Solver (MIP) ===
Linear Solver (MIP) Solution:
{'variables': {'SmallBottlesUsed': 134.0, 'LargeBottlesUsed': 66.0}, 'objective': 1990.0}

=== Solving with CP-SAT Solver ===
CP-SAT Solver Solution:
{'variables': {'SmallBottlesUsed': 134, 'LargeBottlesUsed': 66}, 'objective': 1990.0}
'''

'''Expected Output:
Expected solution

: {'variables': {'SmallBottlesUsed': 134.0, 'LargeBottlesUsed': 66.0}, 'objective': 1990.0}'''

