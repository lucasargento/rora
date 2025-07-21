# Problem Description:
'''Problem description: A souvenir shop makes wooden elephants and tigers with plastic ornaments. Each elephant requires 50 grams of wood and 20 grams of plastic. Each tiger requires 40 grams of wood and 30 grams of plastic. In a week, 5000 grams of wood and 4000 grams of plastic are available. The profit per elephant sold is $5 and the profit per tiger sold is $4. How many of each should be made in order to maximize profit?

Expected Output Schema:
{
  "variables": {
    "Production": {
      "0": "float",
      "1": "float"
    }
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- A: set of products = {Elephant, Tiger}

Parameters:
- profit_Animal: profit per unit of each animal produced [USD per unit]
  • profit_Animal[Elephant] = 5
  • profit_Animal[Tiger] = 4
- wood_req_Animal: grams of wood required per unit [grams per unit]
  • wood_req_Animal[Elephant] = 50
  • wood_req_Animal[Tiger] = 40
- plastic_req_Animal: grams of plastic required per unit [grams per unit]
  • plastic_req_Animal[Elephant] = 20
  • plastic_req_Animal[Tiger] = 30
- available_wood: total available wood per week [grams] = 5000
- available_plastic: total available plastic per week [grams] = 4000

Variables:
- x_Animal: number of units of animal to produce [integer ≥ 0]
  • x_Animal[Elephant] represents the number of elephants produced.
  • x_Animal[Tiger] represents the number of tigers produced.

Objective:
- Maximize total profit = profit_Animal[Elephant] * x_Animal[Elephant] + profit_Animal[Tiger] * x_Animal[Tiger]

Constraints:
1. Wood constraint: wood_req_Animal[Elephant] * x_Animal[Elephant] + wood_req_Animal[Tiger] * x_Animal[Tiger] ≤ available_wood
2. Plastic constraint: plastic_req_Animal[Elephant] * x_Animal[Elephant] + plastic_req_Animal[Tiger] * x_Animal[Tiger] ≤ available_plastic

-------------------------------------------------------
Mapping to Expected Output Schema:

{
  "variables": {
    "Production": {
      "0": "Number of elephants produced (x_Animal[Elephant], integer, units)",
      "1": "Number of tigers produced (x_Animal[Tiger], integer, units)"
    }
  },
  "objective": "Maximize profit = 5 * (number of elephants) + 4 * (number of tigers)"
}'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_with_linear_solver():
    # Create the solver using CBC backend
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Solver not created.")
        return None

    # Data
    available_wood = 5000  # grams
    available_plastic = 4000  # grams

    profit_elephant = 5
    profit_tiger = 4

    wood_req_elephant = 50  # grams per unit
    wood_req_tiger = 40  # grams per unit

    plastic_req_elephant = 20  # grams per unit
    plastic_req_tiger = 30  # grams per unit

    # Variables: integers representing number of elephants and tigers produced
    elephants = solver.IntVar(0, solver.infinity(), 'elephants')  # x_Animal[Elephant]
    tigers = solver.IntVar(0, solver.infinity(), 'tigers')        # x_Animal[Tiger]

    # Constraints
    # Wood constraint: 50 * elephants + 40 * tigers <= 5000
    solver.Add(wood_req_elephant * elephants + wood_req_tiger * tigers <= available_wood)

    # Plastic constraint: 20 * elephants + 30 * tigers <= 4000
    solver.Add(plastic_req_elephant * elephants + plastic_req_tiger * tigers <= available_plastic)

    # Objective: Maximize profit = 5 * elephants + 4 * tigers
    solver.Maximize(profit_elephant * elephants + profit_tiger * tigers)

    # Solve the problem
    status = solver.Solve()

    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result['elephants'] = elephants.solution_value()
        result['tigers'] = tigers.solution_value()
        result['objective'] = solver.Objective().Value()
    else:
        result['status'] = 'The problem does not have an optimal solution.'

    return result

def main():
    results = {}

    # Implementation using ortools.linear_solver for the production problem
    ls_result = solve_with_linear_solver()
    results['LinearSolver'] = {
        "variables": {
            "Production": {
                "0": "Number of elephants produced (x_Animal[Elephant], integer, units) = {}".format(ls_result.get('elephants', 'N/A')),
                "1": "Number of tigers produced (x_Animal[Tiger], integer, units) = {}".format(ls_result.get('tigers', 'N/A'))
            }
        },
        "objective": ls_result.get('objective', 'No optimal solution')
    }

    # Print the results in a structured way
    print("Optimization Results:")
    for model_name, data in results.items():
        print("Model: {}".format(model_name))
        print("Variables:")
        for var_group, details in data["variables"].items():
            print("  {}:".format(var_group))
            for key, desc in details.items():
                print("    {}: {}".format(key, desc))
        print("Objective Value: {}".format(data["objective"]))
        print("-" * 40)

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Optimization Results:
Model: LinearSolver
Variables:
  Production:
    0: Number of elephants produced (x_Animal[Elephant], integer, units) = 0.0
    1: Number of tigers produced (x_Animal[Tiger], integer, units) = 125.0
Objective Value: 500.0
----------------------------------------
'''

'''Expected Output:
Expected solution

: {'variables': {'Production': {'0': 100.0, '1': 0.0}}, 'objective': 500.0}'''

