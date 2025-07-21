# Problem Description:
'''Problem description: A grocery store wants to liquidate its stock of 10 apples, 20 bananas, and 80 grapes. Given past experience, the store knows that they can propose a banana-haters package with 6 apples and 30 grapes and that this package will bring a profit of six euros. Similarly, they can prepare a combo package with 5 apples, 6 bananas, and 20 grapes, yielding a profit of seven euros. They know they can sell any quantity of these two packages within the availability of its stock. What quantity of each package, banana-haters packages and combo packages, should the store prepare to maximize net profit?

Expected Output Schema:
{
  "variables": {
    "PackageCount": {
      "0": "float",
      "1": "float"
    }
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- Packages: P = {BH, Combo}, where BH represents the banana-haters package and Combo represents the combo package.

Parameters:
- stock_apples = 10 (units available)
- stock_bananas = 20 (units available)
- stock_grapes = 80 (units available)
- apples_BH = 6 (apples required per banana-haters package)
- grapes_BH = 30 (grapes required per banana-haters package)
- apples_Combo = 5 (apples required per combo package)
- bananas_Combo = 6 (bananas required per combo package)
- grapes_Combo = 20 (grapes required per combo package)
- profit_BH = 6 (euros profit per banana-haters package)
- profit_Combo = 7 (euros profit per combo package)

Variables:
- x_BH: number of banana-haters packages to prepare (continuous or integer ≥ 0)
- x_Combo: number of combo packages to prepare (continuous or integer ≥ 0)

Objective:
- Maximize total profit = (profit_BH * x_BH) + (profit_Combo * x_Combo)

Constraints:
1. Apple stock constraint:
   - (apples_BH * x_BH) + (apples_Combo * x_Combo) ≤ stock_apples
   - That is: 6*x_BH + 5*x_Combo ≤ 10

2. Banana stock constraint:
   - (bananas_Combo * x_Combo) ≤ stock_bananas
   - That is: 6*x_Combo ≤ 20
   - (Note: The banana-haters package does not use bananas.)

3. Grape stock constraint:
   - (grapes_BH * x_BH) + (grapes_Combo * x_Combo) ≤ stock_grapes
   - That is: 30*x_BH + 20*x_Combo ≤ 80

This structured model fully represents the original problem using the five-element framework.'''

# Generated Code:
#!/usr/bin/env python3
"""
This script implements the grocery store package optimization problem using the
Google OR-Tools linear solver module. It sets up a linear program to maximize profit 
for the two types of packages subject to stock constraints.
"""

from ortools.linear_solver import pywraplp

def solve_linear_model():
    # Create the linear solver using GLOP (linear programming solver)
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Solver not created.")
        return None

    # Variables:
    # x_BH: number of banana-haters packages to prepare
    # x_Combo: number of combo packages to prepare
    x_BH = solver.NumVar(0.0, solver.infinity(), 'x_BH')
    x_Combo = solver.NumVar(0.0, solver.infinity(), 'x_Combo')

    # Parameters:
    # Stocks and recipe requirements
    stock_apples = 10
    stock_bananas = 20
    stock_grapes = 80

    apples_BH = 6
    grapes_BH = 30

    apples_Combo = 5
    bananas_Combo = 6
    grapes_Combo = 20

    profit_BH = 6
    profit_Combo = 7

    # Objective: maximize total profit = 6*x_BH + 7*x_Combo
    objective = solver.Objective()
    objective.SetCoefficient(x_BH, profit_BH)
    objective.SetCoefficient(x_Combo, profit_Combo)
    objective.SetMaximization()

    # Constraints:
    # 1. Apple stock: 6*x_BH + 5*x_Combo <= 10
    ct_apples = solver.Constraint(-solver.infinity(), stock_apples)
    ct_apples.SetCoefficient(x_BH, apples_BH)
    ct_apples.SetCoefficient(x_Combo, apples_Combo)

    # 2. Banana stock: 6*x_Combo <= 20
    ct_bananas = solver.Constraint(-solver.infinity(), stock_bananas)
    ct_bananas.SetCoefficient(x_Combo, bananas_Combo)

    # 3. Grape stock: 30*x_BH + 20*x_Combo <= 80
    ct_grapes = solver.Constraint(-solver.infinity(), stock_grapes)
    ct_grapes.SetCoefficient(x_BH, grapes_BH)
    ct_grapes.SetCoefficient(x_Combo, grapes_Combo)

    # Solve the model
    status = solver.Solve()

    # Prepare a dictionary for the solution according to the expected output schema
    solution = {}
    if status == pywraplp.Solver.OPTIMAL:
        solution = {
            "variables": {
                "PackageCount": {
                    "0": x_BH.solution_value(),   # banana-haters package count
                    "1": x_Combo.solution_value(), # combo package count
                }
            },
            "objective": objective.Value()
        }
        print("Solution for Pure Linear Model:")
        print("Banana-haters package count (x_BH):", x_BH.solution_value())
        print("Combo package count (x_Combo):", x_Combo.solution_value())
        print("Maximum Profit:", objective.Value())
    else:
        print("The problem does not have an optimal solution.")

    return solution

def main():
    # Only one formulation model is provided, so we run that one implementation.
    sol_linear = solve_linear_model()
    
    # Print a structured view of the solution if available.
    if sol_linear:
        print("\nStructured Solution Output:")
        print(sol_linear)

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Solution for Pure Linear Model:
Banana-haters package count (x_BH): 0.0
Combo package count (x_Combo): 2.0
Maximum Profit: 14.0

Structured Solution Output:
{'variables': {'PackageCount': {'0': 0.0, '1': 2.0}}, 'objective': 14.0}
'''

'''Expected Output:
Expected solution

: {'variables': {'PackageCount': {'0': -0.0, '1': 2.0}}, 'objective': 14.0}'''

