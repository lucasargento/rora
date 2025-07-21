# Problem Description:
'''Problem description: A pharmaceutical company makes skin cream in batches, a regular batch and premium batch, to sell to hospitals. The regular batch requires 50 units of medicinal ingredients and 40 units of rehydration product. A premium batch requires 40 units of medicinal ingredients and 60 units of rehydration product. The company has available 3000 units of medicinal ingredients and 3500 units of rehydration product. Since the premium batch sells better, the number of regular batches must be less than the number of premium batches. In addition, the company must make at least 10 regular batches. If a regular batch can treat 50 people and a premium batch can treat 30 people, how many of each batch should be made to maximize the number of people that can be treated?

Expected Output Schema:
{
  "variables": {
    "RegularBatches": "float",
    "PremiumBatches": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- Batches: a set with two elements {Regular, Premium} representing the two types of skin cream batches.

Parameters:
- medicinal_req_regular: 50 (units of medicinal ingredients needed per regular batch)
- medicinal_req_premium: 40 (units of medicinal ingredients needed per premium batch)
- rehydration_req_regular: 40 (units of rehydration product needed per regular batch)
- rehydration_req_premium: 60 (units of rehydration product needed per premium batch)
- medicinal_avail: 3000 (total available units of medicinal ingredients)
- rehydration_avail: 3500 (total available units of rehydration product)
- treats_regular: 50 (number of people treated by one regular batch)
- treats_premium: 30 (number of people treated by one premium batch)
- min_regular_batches: 10 (minimum number of regular batches that must be produced)
- note: All units are assumed consistent (ingredients and treated people per batch).

Variables:
- x_regular: number of regular batches produced [integer ≥ 0]
- x_premium: number of premium batches produced [integer ≥ 0]

Objective:
Maximize total people treated:
   maximize_total_people = treats_regular * x_regular + treats_premium * x_premium
   i.e., maximize 50 * x_regular + 30 * x_premium

Constraints:
1. Medicinal ingredient constraint:
   medicinal_req_regular * x_regular + medicinal_req_premium * x_premium ≤ medicinal_avail
   i.e., 50 * x_regular + 40 * x_premium ≤ 3000

2. Rehydration product constraint:
   rehydration_req_regular * x_regular + rehydration_req_premium * x_premium ≤ rehydration_avail
   i.e., 40 * x_regular + 60 * x_premium ≤ 3500

3. Batch comparison constraint (regular batches must be less than premium batches):
   x_regular < x_premium

4. Minimum production requirement for regular batches:
   x_regular ≥ min_regular_batches
   i.e., x_regular ≥ 10

5. Domain of decision variables:
   x_regular and x_premium are non-negative integers.

This complete model provides a clear mapping from the problem description into the five-element mathematical optimization formulation.'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp
from ortools.sat.python import cp_model

def solve_linear_solver_model():
    # Create the MIP solver with SCIP backend.
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        return "Solver not available."

    # Define variables:
    # x_regular: number of regular batches (integer ≥ 10)
    # x_premium: number of premium batches (integer ≥ 0)
    # Upper bounds can be set based on resource limits. We'll choose a conservative upper bound.
    x_regular = solver.IntVar(10, 1000, 'RegularBatches')
    x_premium = solver.IntVar(0, 1000, 'PremiumBatches')

    # Add constraints:

    # Constraint 1: Medicinal ingredient constraint: 50*x_regular + 40*x_premium <= 3000
    solver.Add(50 * x_regular + 40 * x_premium <= 3000)

    # Constraint 2: Rehydration product constraint: 40*x_regular + 60*x_premium <= 3500
    solver.Add(40 * x_regular + 60 * x_premium <= 3500)

    # Constraint 3: Batch comparison constraint: x_regular < x_premium.
    # As x_regular and x_premium are integers, x_regular < x_premium is equivalent to:
    solver.Add(x_regular <= x_premium - 1)

    # Objective: Maximize total people treated: 50*x_regular + 30*x_premium
    solver.Maximize(50 * x_regular + 30 * x_premium)

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "variables": {
                "RegularBatches": x_regular.solution_value(),
                "PremiumBatches": x_premium.solution_value()
            },
            "objective": solver.Objective().Value()
        }
    elif status == pywraplp.Solver.FEASIBLE:
        result = "A feasible solution was found, but it may not be optimal."
    else:
        result = "The problem does not have an optimal solution."

    return result


def solve_cp_model():
    model = cp_model.CpModel()

    # Define variables:
    # For CP-SAT, we choose broad upper bounds; resources consider the constraints below.
    x_regular = model.NewIntVar(10, 1000, 'RegularBatches')
    x_premium = model.NewIntVar(0, 1000, 'PremiumBatches')

    # Add constraints:

    # Constraint 1: Medicinal ingredient constraint: 50*x_regular + 40*x_premium <= 3000
    model.Add(50 * x_regular + 40 * x_premium <= 3000)

    # Constraint 2: Rehydration product constraint: 40*x_regular + 60*x_premium <= 3500
    model.Add(40 * x_regular + 60 * x_premium <= 3500)

    # Constraint 3: Batch comparison constraint: x_regular < x_premium.
    # For integer variables, we can write: x_regular <= x_premium - 1
    model.Add(x_regular <= x_premium - 1)

    # Define objective: Maximize total people treated: 50*x_regular + 30*x_premium
    model.Maximize(50 * x_regular + 30 * x_premium)

    # Solve the model using CpSolver.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        result = {
            "variables": {
                "RegularBatches": solver.Value(x_regular),
                "PremiumBatches": solver.Value(x_premium)
            },
            "objective": solver.ObjectiveValue()
        }
    else:
        result = "No solution found."

    return result


def main():
    # Solve using the Linear Solver model (Version 1)
    linear_result = solve_linear_solver_model()

    # Solve using the CP-SAT Model (Version 2)
    cp_result = solve_cp_model()

    # Print structured results
    print("Results:")
    print("-----------")
    print("Model 1: Linear Solver")
    print(linear_result)
    print("-----------")
    print("Model 2: CP-SAT")
    print(cp_result)


if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Results:
-----------
Model 1: Linear Solver
{'variables': {'RegularBatches': 32.0, 'PremiumBatches': 35.0}, 'objective': 2649.9999999999995}
-----------
Model 2: CP-SAT
{'variables': {'RegularBatches': 32, 'PremiumBatches': 35}, 'objective': 2650.0}
'''

'''Expected Output:
Expected solution

: {'variables': {'RegularBatches': 32.0, 'PremiumBatches': 35.0}, 'objective': 2650.0}'''

