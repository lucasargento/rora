# Problem Description:
'''Problem description: A meat processing plant uses two machines, a meat slicer and a meat packer, to make their hams and pork ribs. To produce one batch of hams requires 4 hours on the meat slicer and 2.5 hours on the meat packer. To produce one batch of pork ribs requires 2 hours on the meat slicer and 3.5 hours on the meat packer. Each machine runs for at most 4000 hours per year. If the profit per batch of hams is $150 and the profit per batch of pork ribs is $300, how many batches of each should be made to maximize profit?

Expected Output Schema:
{
  "variables": {
    "BatchesProduced": {
      "0": "float",
      "1": "float"
    }
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- Products = {Hams, PorkRibs}

Parameters:
- profit: profit per batch in USD.
  • profit[Hams] = 150  (USD per batch of hams)
  • profit[PorkRibs] = 300  (USD per batch of pork ribs)
- slicerTime: meat slicer usage per batch in hours.
  • slicerTime[Hams] = 4  (hours per batch of hams)
  • slicerTime[PorkRibs] = 2  (hours per batch of pork ribs)
- packerTime: meat packer usage per batch in hours.
  • packerTime[Hams] = 2.5  (hours per batch of hams)
  • packerTime[PorkRibs] = 3.5  (hours per batch of pork ribs)
- maxSlicerHours = 4000  (total available hours per year for the meat slicer)
- maxPackerHours = 4000  (total available hours per year for the meat packer)

Variables:
- BatchesProduced[p] for each product p in Products.
  • BatchesProduced[Hams] ∈ float, with BatchesProduced[Hams] ≥ 0  (number of batches of hams produced)
  • BatchesProduced[PorkRibs] ∈ float, with BatchesProduced[PorkRibs] ≥ 0  (number of batches of pork ribs produced)
  (Note: Although batches are typically integer, the expected schema uses float.)

Objective:
- Maximize total profit:
  Total profit = profit[Hams] * BatchesProduced[Hams] + profit[PorkRibs] * BatchesProduced[PorkRibs]

Constraints:
1. Meat slicer capacity:
   slicerTime[Hams] * BatchesProduced[Hams] + slicerTime[PorkRibs] * BatchesProduced[PorkRibs] ≤ maxSlicerHours
   That is, 4 * BatchesProduced[Hams] + 2 * BatchesProduced[PorkRibs] ≤ 4000

2. Meat packer capacity:
   packerTime[Hams] * BatchesProduced[Hams] + packerTime[PorkRibs] * BatchesProduced[PorkRibs] ≤ maxPackerHours
   That is, 2.5 * BatchesProduced[Hams] + 3.5 * BatchesProduced[PorkRibs] ≤ 4000

This structured model is complete and faithful to the problem description and can be directly translated to code in Python or an OR-Tools implementation.'''

# Generated Code:
#!/usr/bin/env python3
"""
This script solves the meat processing plant optimization problem using Google OR-Tools.
It uses the linear solver (ortools.linear_solver) for a linear programming formulation.
The problem:
  - Produce batches of Hams and PorkRibs subject to available machine hours.
  - Hams require 4 hours on the meat slicer and 2.5 hours on the meat packer per batch.
  - PorkRibs require 2 hours on the meat slicer and 3.5 hours on the meat packer per batch.
  - Total available hours for each machine are 4000 per year.
  - Profit: $150 per batch of Hams, $300 per batch of PorkRibs.
The goal is to maximize the total profit.
Expected result output schema:
{
  "variables": {
    "BatchesProduced": {
      "0": "float",
      "1": "float"
    }
  },
  "objective": "float"
}
"""

from ortools.linear_solver import pywraplp

def solve_with_linear_solver():
    # Create the linear solver with the GLOP backend.
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Linear solver not available.")
        return "Solver error", None

    # Decision Variables:
    # BatchesProduced[Hams] and BatchesProduced[PorkRibs] as continuous nonnegative variables.
    hams = solver.NumVar(0.0, solver.infinity(), 'Batches_Hams')
    pork_ribs = solver.NumVar(0.0, solver.infinity(), 'Batches_PorkRibs')

    # Constraints:
    # 1. Meat slicer capacity: 4 * Hams + 2 * PorkRibs <= 4000
    solver.Add(4 * hams + 2 * pork_ribs <= 4000)

    # 2. Meat packer capacity: 2.5 * Hams + 3.5 * PorkRibs <= 4000
    solver.Add(2.5 * hams + 3.5 * pork_ribs <= 4000)

    # Objective: Maximize profit = 150 * Hams + 300 * PorkRibs
    solver.Maximize(150 * hams + 300 * pork_ribs)

    status = solver.Solve()

    result_data = {}
    solution_str = ""

    if status == pywraplp.Solver.OPTIMAL:
        solution_str += "Optimal solution found:\n"
        solution_str += f"  Batches of Hams    : {hams.solution_value():.2f}\n"
        solution_str += f"  Batches of PorkRibs: {pork_ribs.solution_value():.2f}\n"
        solution_str += f"  Objective (Profit) : {solver.Objective().Value():.2f}\n"
        result_data = {
            "variables": {
                "BatchesProduced": {
                    "0": hams.solution_value(),
                    "1": pork_ribs.solution_value()
                }
            },
            "objective": solver.Objective().Value()
        }
    else:
        solution_str = "The problem does not have an optimal solution."

    return solution_str, result_data

def main():
    # In this instance we have only one formulation implementation using ortools.linear_solver.
    linear_solution_str, linear_result = solve_with_linear_solver()

    print("=== Linear Solver Model Output ===")
    print(linear_solution_str)
    if linear_result is not None:
        print("Structured Output:")
        print(linear_result)

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
=== Linear Solver Model Output ===
Optimal solution found:
  Batches of Hams    : 0.00
  Batches of PorkRibs: 1142.86
  Objective (Profit) : 342857.14

Structured Output:
{'variables': {'BatchesProduced': {'0': 0.0, '1': 1142.857142857143}}, 'objective': 342857.14285714284}
'''

'''Expected Output:
Expected solution

: {'variables': {'BatchesProduced': {'0': 0.0, '1': 1142.857142857143}}, 'objective': 342857.14285714284}'''

