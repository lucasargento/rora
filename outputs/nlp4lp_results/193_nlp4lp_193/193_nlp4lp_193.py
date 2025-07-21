# Problem Description:
'''Problem description: Platinum Database sells two types of subscription software packages: a personal license and a commercial license which will cost $550 and $2000 to generate respectively. The marketing department estimates that they can sell at most 300 licenses for both versions combined a month. The profit per personal license is $450 and the profit per commercial version is $1200. If the company does not want to spend more than $400000, how many of each software package should they produce to maximize the profits.

Expected Output Schema:
{
  "variables": {
    "NumberOfPersonalLicenses": "float",
    "NumberOfCommercialLicenses": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- L: set of license types = {Personal, Commercial}

Parameters:
- cost_Personal = 550 (USD per personal license produced)
- cost_Commercial = 2000 (USD per commercial license produced)
- profit_Personal = 450 (USD profit per personal license)
- profit_Commercial = 1200 (USD profit per commercial license)
- max_total_licenses = 300 (maximum licenses that can be sold per month)
- max_production_budget = 400000 (USD available for production cost)

Variables:
- NumberOfPersonalLicenses: number of personal licenses to produce (integer ≥ 0)
- NumberOfCommercialLicenses: number of commercial licenses to produce (integer ≥ 0)

Objective:
- Maximize total profit = (profit_Personal * NumberOfPersonalLicenses) + (profit_Commercial * NumberOfCommercialLicenses)
  (Note: The profit here is the margin per license after subtracting production costs from revenue or directly given as profit per package.)

Constraints:
1. Sales Constraint: NumberOfPersonalLicenses + NumberOfCommercialLicenses ≤ max_total_licenses
   (This limits the total number of licenses sold per month.)
2. Production Budget Constraint: (cost_Personal * NumberOfPersonalLicenses) + (cost_Commercial * NumberOfCommercialLicenses) ≤ max_production_budget
   (This ensures that the total production cost does not exceed the available USD 400,000 budget.)'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_linear_program():
    # Create the solver with the CBC backend.
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Solver not created.")
        return None

    # Parameters.
    cost_personal = 550
    cost_commercial = 2000
    profit_personal = 450
    profit_commercial = 1200
    max_total_licenses = 300
    max_production_budget = 400000

    # Variables.
    # Even though the output schema lists type float, the problem description indicates integer values.
    # We create integer variables (non-negative).
    x = solver.IntVar(0, max_total_licenses, 'NumberOfPersonalLicenses')
    y = solver.IntVar(0, max_total_licenses, 'NumberOfCommercialLicenses')

    # Constraints.
    # 1. Sales Constraint: x + y <= max_total_licenses.
    solver.Add(x + y <= max_total_licenses)

    # 2. Production Budget Constraint: cost_personal * x + cost_commercial * y <= max_production_budget.
    solver.Add(cost_personal * x + cost_commercial * y <= max_production_budget)

    # Objective: Maximize total profit.
    solver.Maximize(profit_personal * x + profit_commercial * y)

    # Solve the problem.
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "variables": {
                "NumberOfPersonalLicenses": x.solution_value(),
                "NumberOfCommercialLicenses": y.solution_value()
            },
            "objective": solver.Objective().Value()
        }
        return result
    else:
        return None

def main():
    # We have one formulation implementation for this optimization problem.
    result_lp = solve_linear_program()

    if result_lp:
        print("Solution from Linear Programming Model:")
        print("------------------------------------------------")
        print("NumberOfPersonalLicenses:", result_lp["variables"]["NumberOfPersonalLicenses"])
        print("NumberOfCommercialLicenses:", result_lp["variables"]["NumberOfCommercialLicenses"])
        print("Maximum Profit:", result_lp["objective"])
    else:
        print("The problem is infeasible or no optimal solution exists.")

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Solution from Linear Programming Model:
------------------------------------------------
NumberOfPersonalLicenses: 138.0
NumberOfCommercialLicenses: 162.0
Maximum Profit: 256500.0
'''

'''Expected Output:
Expected solution

: {'variables': {'NumberOfPersonalLicenses': 138.0, 'NumberOfCommercialLicenses': 162.0}, 'objective': 256500.0}'''

