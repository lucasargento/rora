# Problem Description:
'''Problem description: A car manufacturing company makes hamburgers and chicken wraps for workers. They need to ensure workers get at least 2200 calories, 50 grams of protein, and 70 grams of carbs. One hamburger costs $6.5 and contains 800 calories, 19 grams of protein, and 20 grams of carbs. One chicken wrap costs $4 and contains 450 calories, 12 grams of protein, and 10 grams of carbs. What is the minimum cost diet that the company can provide for its workers?

Expected Output Schema:
{
  "variables": {
    "Quantity": {
      "0": "float",
      "1": "float"
    }
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Below is the structured mathematical model using the five-element framework.

------------------------------------------------------------
Sets:
- F: set of food items = {Hamburger, ChickenWrap}

------------------------------------------------------------
Parameters:
- min_calories: minimum required calories per worker = 2200 [calories]
- min_protein: minimum required protein per worker = 50 [grams]
- min_carbs: minimum required carbohydrates per worker = 70 [grams]
- cost_Hamburger: cost per hamburger = 6.5 [USD per unit]
- cost_ChickenWrap: cost per chicken wrap = 4 [USD per unit]
- cal_Hamburger: calories per hamburger = 800 [calories per unit]
- cal_ChickenWrap: calories per chicken wrap = 450 [calories per unit]
- protein_Hamburger: protein per hamburger = 19 [grams per unit]
- protein_ChickenWrap: protein per chicken wrap = 12 [grams per unit]
- carbs_Hamburger: carbohydrates per hamburger = 20 [grams per unit]
- carbs_ChickenWrap: carbohydrates per chicken wrap = 10 [grams per unit]

------------------------------------------------------------
Variables:
- quantity_f: number of units of food item f to provide [units, assumed to be non-negative integers]
  where f in F. In particular:
    - x_Hamburger: number of hamburgers (x_Hamburger ≥ 0)
    - x_ChickenWrap: number of chicken wraps (x_ChickenWrap ≥ 0)

------------------------------------------------------------
Objective:
- Minimize total cost = (cost_Hamburger * x_Hamburger) + (cost_ChickenWrap * x_ChickenWrap)
  [USD]

------------------------------------------------------------
Constraints:
1. Calorie requirement: (cal_Hamburger * x_Hamburger) + (cal_ChickenWrap * x_ChickenWrap) ≥ min_calories
2. Protein requirement: (protein_Hamburger * x_Hamburger) + (protein_ChickenWrap * x_ChickenWrap) ≥ min_protein
3. Carbohydrate requirement: (carbs_Hamburger * x_Hamburger) + (carbs_ChickenWrap * x_ChickenWrap) ≥ min_carbs

------------------------------------------------------------
Additional Comments:
- Units are consistent: costs in USD per unit, nutritional values in calories or grams per unit.
- Although in practice counts of food items are integer, the decision variables are defined as non-negative integers; if a relaxation (continuous values) is needed, then integrality can be enforced later.
- This model aims at finding the minimum-cost combination of hamburgers and chicken wraps that meets the nutritional requirements for the workers.

------------------------------------------------------------

Below is a representation of the key decision variables and the objective in the expected output schema:

{
  "variables": {
    "Quantity": {
      "Hamburger": "integer (≥ 0)",
      "ChickenWrap": "integer (≥ 0)"
    }
  },
  "objective": "Minimize (6.5 * x_Hamburger) + (4 * x_ChickenWrap)"
}'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_mip():
    # Create the MIP solver with CBC backend.
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Solver not created for MIP model.")
        return None

    # Data parameters.
    min_calories = 2200
    min_protein = 50
    min_carbs = 70

    cost_Hamburger = 6.5
    cost_ChickenWrap = 4

    cal_Hamburger = 800
    cal_ChickenWrap = 450

    protein_Hamburger = 19
    protein_ChickenWrap = 12

    carbs_Hamburger = 20
    carbs_ChickenWrap = 10

    # Decision variables (non-negative integers)
    x_Hamburger = solver.IntVar(0, solver.infinity(), 'x_Hamburger')
    x_ChickenWrap = solver.IntVar(0, solver.infinity(), 'x_ChickenWrap')

    # Objective: Minimize cost
    solver.Minimize(cost_Hamburger * x_Hamburger + cost_ChickenWrap * x_ChickenWrap)

    # Constraints:
    # 1. Calorie constraint
    solver.Add(cal_Hamburger * x_Hamburger + cal_ChickenWrap * x_ChickenWrap >= min_calories)
    # 2. Protein constraint
    solver.Add(protein_Hamburger * x_Hamburger + protein_ChickenWrap * x_ChickenWrap >= min_protein)
    # 3. Carbohydrates constraint
    solver.Add(carbs_Hamburger * x_Hamburger + carbs_ChickenWrap * x_ChickenWrap >= min_carbs)

    status = solver.Solve()

    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result['x_Hamburger'] = x_Hamburger.solution_value()
        result['x_ChickenWrap'] = x_ChickenWrap.solution_value()
        result['objective'] = solver.Objective().Value()
    else:
        result['message'] = "No optimal solution found for the MIP model."
    return result

def solve_lp():
    # Create the LP solver with GLOP (continuous optimization).
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Solver not created for LP model.")
        return None

    # Data parameters.
    min_calories = 2200
    min_protein = 50
    min_carbs = 70

    cost_Hamburger = 6.5
    cost_ChickenWrap = 4

    cal_Hamburger = 800
    cal_ChickenWrap = 450

    protein_Hamburger = 19
    protein_ChickenWrap = 12

    carbs_Hamburger = 20
    carbs_ChickenWrap = 10

    # Decision variables (continuous non-negative values)
    x_Hamburger = solver.NumVar(0, solver.infinity(), 'x_Hamburger')
    x_ChickenWrap = solver.NumVar(0, solver.infinity(), 'x_ChickenWrap')

    # Objective: Minimize cost
    solver.Minimize(cost_Hamburger * x_Hamburger + cost_ChickenWrap * x_ChickenWrap)

    # Constraints:
    # 1. Calorie constraint
    solver.Add(cal_Hamburger * x_Hamburger + cal_ChickenWrap * x_ChickenWrap >= min_calories)
    # 2. Protein constraint
    solver.Add(protein_Hamburger * x_Hamburger + protein_ChickenWrap * x_ChickenWrap >= min_protein)
    # 3. Carbohydrates constraint
    solver.Add(carbs_Hamburger * x_Hamburger + carbs_ChickenWrap * x_ChickenWrap >= min_carbs)

    status = solver.Solve()

    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result['x_Hamburger'] = x_Hamburger.solution_value()
        result['x_ChickenWrap'] = x_ChickenWrap.solution_value()
        result['objective'] = solver.Objective().Value()
    else:
        result['message'] = "No optimal solution found for the LP model."
    return result

def main():
    print("----- MIP Model (Integer Variables) Solution -----")
    mip_result = solve_mip()
    if mip_result is None or 'message' in mip_result:
        print(mip_result.get('message', "Error solving MIP model."))
    else:
        print("Number of Hamburgers: ", mip_result['x_Hamburger'])
        print("Number of Chicken Wraps: ", mip_result['x_ChickenWrap'])
        print("Total Cost: ", mip_result['objective'])

    print("\n----- LP Relaxation Model (Continuous Variables) Solution -----")
    lp_result = solve_lp()
    if lp_result is None or 'message' in lp_result:
        print(lp_result.get('message', "Error solving LP model."))
    else:
        print("Number of Hamburgers: ", lp_result['x_Hamburger'])
        print("Number of Chicken Wraps: ", lp_result['x_ChickenWrap'])
        print("Total Cost: ", lp_result['objective'])

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
----- MIP Model (Integer Variables) Solution -----
Number of Hamburgers:  3.0
Number of Chicken Wraps:  1.0
Total Cost:  23.5

----- LP Relaxation Model (Continuous Variables) Solution -----
Number of Hamburgers:  3.5
Number of Chicken Wraps:  0.0
Total Cost:  22.75
'''

'''Expected Output:
Expected solution

: {'variables': {'Quantity': {'0': 3.5, '1': 0.0}}, 'objective': 22.75}'''

