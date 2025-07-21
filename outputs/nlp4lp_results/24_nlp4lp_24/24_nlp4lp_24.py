# Problem Description:
'''Problem description: A car manufacturer makes two types of car oils: Oil Max and Oil Max Pro. A container of Oil Max contains 46 grams of substance A, 43 grams of substance B and 56 grams of substance C. A container of Oil Max Pro contains 13 grams of substance A, 4 grams of substance B and 45 grams of substance C. The car manufacturer has 1345 grams of substance A, 346 grams of substance B, 1643 grams of substance C. In addition, the profit per container of Oil Max is $10 and the profit per container of Oil Max Pro is $15. How many containers of each of oil should the car manufacturer make to maximize profit?

Expected Output Schema:
{
  "variables": {
    "xOilType": [
      "float"
    ]
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- OILS: set of oil types = {Oil_Max, Oil_Max_Pro}

Parameters:
- substance_A[o] = grams of substance A per container, where:
  - substance_A[Oil_Max] = 46
  - substance_A[Oil_Max_Pro] = 13
- substance_B[o] = grams of substance B per container, where:
  - substance_B[Oil_Max] = 43
  - substance_B[Oil_Max_Pro] = 4
- substance_C[o] = grams of substance C per container, where:
  - substance_C[Oil_Max] = 56
  - substance_C[Oil_Max_Pro] = 45
- profit[o] = profit per container in USD, where:
  - profit[Oil_Max] = 10
  - profit[Oil_Max_Pro] = 15
- available_A: total grams of substance A available = 1345
- available_B: total grams of substance B available = 346
- available_C: total grams of substance C available = 1643

Variables:
- x[o] for each oil type in OILS: number of containers produced of oil type o
  - Type: integer
  - Domain: x[o] ≥ 0
  - Unit: containers

Objective:
- Maximize total profit = sum over o in OILS of (profit[o] * x[o])
  - Interpretation: Total profit in USD from producing containers of oil.

Constraints:
- Constraint for Substance A: substance_A[Oil_Max] * x[Oil_Max] + substance_A[Oil_Max_Pro] * x[Oil_Max_Pro] ≤ available_A
- Constraint for Substance B: substance_B[Oil_Max] * x[Oil_Max] + substance_B[Oil_Max_Pro] * x[Oil_Max_Pro] ≤ available_B
- Constraint for Substance C: substance_C[Oil_Max] * x[Oil_Max] + substance_C[Oil_Max_Pro] * x[Oil_Max_Pro] ≤ available_C

--------------------------------------------------
Expected Output Schema:
{
  "variables": {
    "xOilType": [
      "integer"
    ]
  },
  "objective": "float"
}'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_oil_production_version1():
    # Create the solver instance using the CBC backend.
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Solver not found.")
        return

    # Variables:
    # xOil_Max: number of containers of Oil Max produced (integer, >= 0)
    # xOil_Max_Pro: number of containers of Oil Max Pro produced (integer, >= 0)
    xOil_Max = solver.IntVar(0, solver.infinity(), 'xOil_Max')
    xOil_Max_Pro = solver.IntVar(0, solver.infinity(), 'xOil_Max_Pro')

    # Data
    # Substance requirements per container
    substance_A = {'Oil_Max': 46, 'Oil_Max_Pro': 13}
    substance_B = {'Oil_Max': 43, 'Oil_Max_Pro': 4}
    substance_C = {'Oil_Max': 56, 'Oil_Max_Pro': 45}
    # Available quantities
    available_A = 1345
    available_B = 346
    available_C = 1643
    # Profit per container
    profit = {'Oil_Max': 10, 'Oil_Max_Pro': 15}

    # Constraints:
    # Substance A constraint:
    solver.Add(substance_A['Oil_Max'] * xOil_Max + substance_A['Oil_Max_Pro'] * xOil_Max_Pro <= available_A)
    # Substance B constraint:
    solver.Add(substance_B['Oil_Max'] * xOil_Max + substance_B['Oil_Max_Pro'] * xOil_Max_Pro <= available_B)
    # Substance C constraint:
    solver.Add(substance_C['Oil_Max'] * xOil_Max + substance_C['Oil_Max_Pro'] * xOil_Max_Pro <= available_C)

    # Objective: maximize profit
    objective = solver.Objective()
    objective.SetCoefficient(xOil_Max, profit['Oil_Max'])
    objective.SetCoefficient(xOil_Max_Pro, profit['Oil_Max_Pro'])
    objective.SetMaximization()

    # Solve the problem.
    status = solver.Solve()

    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result['model'] = "Version 1: Linear Programming using ortools.linear_solver"
        result['xOil_Max'] = int(xOil_Max.solution_value())
        result['xOil_Max_Pro'] = int(xOil_Max_Pro.solution_value())
        result['objective'] = objective.Value()
    else:
        result['model'] = "Version 1"
        result['message'] = "The problem does not have an optimal solution."

    return result

def main():
    results = {}
    # Only one formulation provided, so we solve one model.
    results['Version 1'] = solve_oil_production_version1()

    # Print the results in a structured way.
    for version, result in results.items():
        print("==========", version, "==========")
        if 'message' in result:
            print(result['message'])
        else:
            print("Containers of Oil Max: ", result['xOil_Max'])
            print("Containers of Oil Max Pro: ", result['xOil_Max_Pro'])
            print("Optimal Profit: $", result['objective'])
        print()

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
========== Version 1 ==========
Containers of Oil Max:  0
Containers of Oil Max Pro:  36
Optimal Profit: $ 540.0

'''

'''Expected Output:
Expected solution

: {'variables': {'xOilType': [0.0, 36.51111111111111]}, 'objective': 547.6666666666667}'''

