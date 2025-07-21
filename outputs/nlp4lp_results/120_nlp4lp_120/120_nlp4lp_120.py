# Problem Description:
'''Problem description: A lab has 1000 units of medicinal ingredients to make two pills, a large pill and a small pill. A large pill requires 3 units of medicinal ingredients and 2 units of filler. A small pill requires 2 units of medicinal ingredients and 1 unit of filler. The lab has to make at least 100 large pills. However, since small pills are more popular at least 60% of the total number of pills must be small. How many of each should be made to minimize the total number of filler material needed?

Expected Output Schema:
{
  "variables": {
    "PillsProduced": {
      "0": "float",
      "1": "float"
    }
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- PILL_TYPE: set of pill types = {Large, Small}

Parameters:
- medicinal_available: total available medicinal ingredients = 1000 (units)
- req_med_large: medicinal ingredients required per large pill = 3 (units per pill)
- req_med_small: medicinal ingredients required per small pill = 2 (units per pill)
- req_fill_large: filler material required per large pill = 2 (units per pill)
- req_fill_small: filler material required per small pill = 1 (unit per pill)
- min_large: minimum number of large pills to produce = 100 (pills)
- small_fraction: minimum fraction of small pills among total pills = 0.60  
  (Note: This requirement is equivalent to enforcing small_pills ≥ 1.5 × large_pills)

Variables:
- PillsProduced[p] for p in PILL_TYPE, where:
  • PillsProduced[Large]: number of large pills to produce [integer ≥ 0]
  • PillsProduced[Small]: number of small pills to produce [integer ≥ 0]

Objective:
- Minimize total filler consumption = (req_fill_large × PillsProduced[Large]) + (req_fill_small × PillsProduced[Small])
  That is, minimize (2 × PillsProduced[Large] + 1 × PillsProduced[Small])

Constraints:
1. Medicinal ingredient availability:
   (req_med_large × PillsProduced[Large]) + (req_med_small × PillsProduced[Small]) ≤ medicinal_available
   i.e., 3 × PillsProduced[Large] + 2 × PillsProduced[Small] ≤ 1000

2. Minimum large pills production:
   PillsProduced[Large] ≥ min_large
   i.e., PillsProduced[Large] ≥ 100

3. Popularity requirement (at least 60% of pills must be small):
   This can be written as:
   PillsProduced[Small] ≥ small_fraction × (PillsProduced[Large] + PillsProduced[Small])
   Rearranging gives: PillsProduced[Small] ≥ 1.5 × PillsProduced[Large]

4. Non-negativity and integrality:
   PillsProduced[Large] and PillsProduced[Small] are integers and ≥ 0

----------------------
Mapping to the Expected Output Schema:

{
  "variables": {
    "PillsProduced": {
      "0": "float",   // corresponds to PillsProduced[Large]
      "1": "float"    // corresponds to PillsProduced[Small]
    }
  },
  "objective": "float"  // represents the total filler consumption: 2*PillsProduced[Large] + 1*PillsProduced[Small]"
}

Notes:
- Even though the expected JSON schema lists the decision variables as floats, the context (number of pills) implies ideally integer decisions. This can be adapted in implementation.
- All parameter units (ingredients per pill, overall available ingredients) are assumed to be consistent.'''

# Generated Code:
#!/usr/bin/env python3
"""
This script implements the optimization problem with two separate implementations:
1. Using the Google OR-Tools Linear Solver (mixed-integer programming).
2. Using the Google OR-Tools CP-SAT Solver (constraint programming).

Both models are kept separate and are called from the main() function.
"""

from ortools.linear_solver import pywraplp
from ortools.sat.python import cp_model

def solve_with_linear_solver():
    # Create the MIP solver with the CBC backend.
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Linear solver not available.")
        return None

    # Parameters
    medicinal_available = 1000
    req_med_large = 3
    req_med_small = 2
    req_fill_large = 2
    req_fill_small = 1
    min_large = 100

    # Decision variables:
    # PillsProduced[Large] and PillsProduced[Small]
    # Using integer variables since number of pills should be integer.
    large = solver.IntVar(0, solver.infinity(), 'Large')
    small = solver.IntVar(0, solver.infinity(), 'Small')

    # Constraints:
    # 1. Medicinal ingredient availability: 3*large + 2*small <= 1000
    solver.Add(req_med_large * large + req_med_small * small <= medicinal_available)

    # 2. Minimum large pills production: large >= 100
    solver.Add(large >= min_large)

    # 3. Popularity requirement: small >= 1.5 * large; to avoid fractional coefficient, multiply both sides by 2: 2 * small >= 3 * large
    solver.Add(2 * small >= 3 * large)

    # Objective: minimize filler consumption = 2*large + 1*small
    objective = solver.Objective()
    objective.SetCoefficient(large, req_fill_large)
    objective.SetCoefficient(small, req_fill_small)
    objective.SetMinimization()

    # Solve model
    status = solver.Solve()

    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "model": "Linear Solver (MIP)",
            "variables": {
                "PillsProduced": {
                    "0": large.solution_value(),  # Large pills produced
                    "1": small.solution_value()     # Small pills produced
                }
            },
            "objective": objective.Value()
        }
    else:
        result = {
            "model": "Linear Solver (MIP)",
            "message": "No optimal solution found."
        }
    return result

def solve_with_cp_model():
    # Create the CP model.
    model = cp_model.CpModel()

    # Parameters
    medicinal_available = 1000
    req_med_large = 3
    req_med_small = 2
    req_fill_large = 2
    req_fill_small = 1
    min_large = 100

    # Decision variables: using integer variables.
    # We set an upper bound for the decision variables. 
    # For large pills, maximum possible if only large pills were produced: floor(1000/3)
    # For small pills, maximum possible if only small pills were produced: floor(1000/2)
    max_large = 1000 // req_med_large
    max_small = 1000 // req_med_small
    
    large = model.NewIntVar(0, max_large, 'Large')
    small = model.NewIntVar(0, max_small, 'Small')

    # Constraints:
    # 1. Medicinal ingredient availability: 3*large + 2*small <= 1000
    model.Add(req_med_large * large + req_med_small * small <= medicinal_available)

    # 2. Minimum large pills production: large >= 100
    model.Add(large >= min_large)

    # 3. Popularity requirement: small >= 1.5 * large. Multiply by 2 to avoid fractional coefficient: 2 * small >= 3 * large
    model.Add(2 * small >= 3 * large)

    # Objective: minimize filler consumption = 2*large + 1*small
    # In CP-SAT, objective coefficients must be integer.
    objective_var = model.NewIntVar(0, 10000, 'objective')
    model.Add(objective_var == req_fill_large * large + req_fill_small * small)
    model.Minimize(objective_var)

    # Create a solver and solve.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    result = {}
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        result = {
            "model": "CP-SAT Solver",
            "variables": {
                "PillsProduced": {
                    "0": solver.Value(large),  # Large pills produced
                    "1": solver.Value(small)     # Small pills produced
                }
            },
            "objective": solver.Value(objective_var)
        }
    else:
        result = {
            "model": "CP-SAT Solver",
            "message": "No optimal solution found."
        }
    return result

def main():
    results = {}
    linear_result = solve_with_linear_solver()
    cp_result = solve_with_cp_model()

    results["LinearSolver"] = linear_result
    results["CPSAT"] = cp_result

    # Print the structured results.
    print(results)

if __name__ == "__main__":
    main()

'''Execution Results:
SUCCESS:
{'LinearSolver': {'model': 'Linear Solver (MIP)', 'variables': {'PillsProduced': {'0': 100.0, '1': 150.0}}, 'objective': 350.0}, 'CPSAT': {'model': 'CP-SAT Solver', 'variables': {'PillsProduced': {'0': 100, '1': 150}}, 'objective': 350}}
'''

'''Expected Output:
Expected solution

: {'variables': {'PillsProduced': {'0': 100.0, '1': 150.0}}, 'objective': 350.0}'''

