# Problem Description:
'''Problem description: A jam company sends its product out in small and large jars. A small jar can hold 50 ml of jam while a large jar can hold 200 ml of jam. Most store prefer the smaller size and so the number of large jars cannot exceed the number of small jars. If the company wants to ship at least 100000 ml of jam, find the minimum number of jars that can be used.

Expected Output Schema:
{
  "variables": {
    "NumberOfSmallJars": "float",
    "NumberOfLargeJars": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- J: set of jar types = {Small, Large}

Parameters:
- volume_small: volume contained in a small jar = 50 ml per jar
- volume_large: volume contained in a large jar = 200 ml per jar
- minimum_total_volume: minimum jam to be shipped = 100000 ml

Variables:
- NumberOfSmallJars: number of small jars used [nonnegative integer]
- NumberOfLargeJars: number of large jars used [nonnegative integer]
- TotalJars: auxiliary variable representing the total number of jars = NumberOfSmallJars + NumberOfLargeJars [nonnegative integer]

Objective:
- Minimize TotalJars

Constraints:
1. Jam volume requirement: (volume_small * NumberOfSmallJars) + (volume_large * NumberOfLargeJars) ≥ minimum_total_volume  
   (i.e., 50 * NumberOfSmallJars + 200 * NumberOfLargeJars ≥ 100000)
2. Jar type preference: NumberOfLargeJars ≤ NumberOfSmallJars

// Expected output schema:
{
  "variables": {
    "NumberOfSmallJars": "float",
    "NumberOfLargeJars": "float"
  },
  "objective": "float"
}'''

# Generated Code:
#!/usr/bin/env python3
"""
This script implements the jam jar optimization problem using two separate models:
1. A linear/MIP model using ortools.linear_solver.
2. A CP-SAT model using ortools.sat.python.cp_model.

Both models minimize the total number of jars used (small and large) subject to:
  - 50 * NumberOfSmallJars + 200 * NumberOfLargeJars >= 100000
  - NumberOfLargeJars <= NumberOfSmallJars

Each model is implemented independently. The main() function calls both implementations
and prints their optimal solutions in a structured format.
"""

from ortools.linear_solver import pywraplp
from ortools.sat.python import cp_model

def solve_with_linear_solver():
    # Create linear solver with CBC backend.
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Linear solver not available.")
        return None

    # Variables: nonnegative integers.
    small = solver.IntVar(0, solver.infinity(), 'NumberOfSmallJars')
    large = solver.IntVar(0, solver.infinity(), 'NumberOfLargeJars')

    # Constraints:
    # Constraint 1: 50*small + 200*large >= 100000
    solver.Add(50 * small + 200 * large >= 100000)
    # Constraint 2: large <= small
    solver.Add(large <= small)

    # Objective: minimize total jars (small + large)
    solver.Minimize(small + large)

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "variables": {
                "NumberOfSmallJars": small.solution_value(),
                "NumberOfLargeJars": large.solution_value()
            },
            "objective": solver.Objective().Value()
        }
        return result
    else:
        print("No optimal solution found using the linear solver.")
        return None

def solve_with_cp_model():
    model = cp_model.CpModel()

    # We set a reasonable upper bound.
    # Using all small jars: 50 * NumberOfSmallJars >= 100000  -> NumberOfSmallJars >= 2000.
    # So an upper bound of 10000 is generously safe.
    ub = 10000

    # Variables: nonnegative integers.
    small = model.NewIntVar(0, ub, 'NumberOfSmallJars')
    large = model.NewIntVar(0, ub, 'NumberOfLargeJars')

    # Constraints:
    # Constraint 1: 50*small + 200*large >= 100000
    model.Add(50 * small + 200 * large >= 100000)
    # Constraint 2: large <= small
    model.Add(large <= small)

    # Objective: minimize total jars (small + large)
    total_jars = model.NewIntVar(0, 2 * ub, 'TotalJars')
    model.Add(total_jars == small + large)
    model.Minimize(total_jars)

    # Solve model.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
        result = {
            "variables": {
                "NumberOfSmallJars": solver.Value(small),
                "NumberOfLargeJars": solver.Value(large)
            },
            "objective": solver.Value(total_jars)
        }
        return result
    else:
        print("No optimal solution found using the CP-SAT model.")
        return None

def main():
    print("=== Solution using ortools.linear_solver (MIP) ===")
    linear_result = solve_with_linear_solver()
    if linear_result:
        print(linear_result)
    else:
        print("Linear solver did not find an optimal solution.")

    print("\n=== Solution using ortools.sat.python.cp_model (CP-SAT) ===")
    cp_result = solve_with_cp_model()
    if cp_result:
        print(cp_result)
    else:
        print("CP-SAT model did not find an optimal solution.")

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
=== Solution using ortools.linear_solver (MIP) ===
{'variables': {'NumberOfSmallJars': 400.0, 'NumberOfLargeJars': 400.0}, 'objective': 800.0}

=== Solution using ortools.sat.python.cp_model (CP-SAT) ===
{'variables': {'NumberOfSmallJars': 400, 'NumberOfLargeJars': 400}, 'objective': 800}
'''

'''Expected Output:
Expected solution

: {'variables': {'NumberOfSmallJars': 400.0, 'NumberOfLargeJars': 400.0}, 'objective': 800.0}'''

