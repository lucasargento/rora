# Problem Description:
'''Problem description: Jordan is a chef. He wants to design a diet consisting of Kebabs and Rice.  Assume that each serving of Rice costs $3 and contains 300 calories and 4.5 grams of protein. Assume that each serving of Kebab costs $2 and contains 200 calories and 4 grams of protein. He's interested in spending as little money as possible but he wants to ensure that his meals have at least 2200 calories and at least 30 grams of protein per day. Formulate a linear programming problem that will help minimize the cost of the diet.

Expected Output Schema:
{
  "variables": {
    "ServingsRice": "float",
    "ServingsKebab": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- F: set of food items = {Rice, Kebab}

Parameters:
- cost[Rice] = 3 (USD per serving)
- cost[Kebab] = 2 (USD per serving)
- calories[Rice] = 300 (calories per serving)
- calories[Kebab] = 200 (calories per serving)
- protein[Rice] = 4.5 (grams per serving)
- protein[Kebab] = 4 (grams per serving)
- min_calories = 2200 (calories required per day)
- min_protein = 30 (grams required per day)

Variables:
- ServingsRice: number of rice servings (continuous, servings ≥ 0)
- ServingsKebab: number of kebab servings (continuous, servings ≥ 0)

Objective:
- Minimize total cost = (cost[Rice] * ServingsRice) + (cost[Kebab] * ServingsKebab)

Constraints:
1. Calorie constraint: (calories[Rice] * ServingsRice) + (calories[Kebab] * ServingsKebab) ≥ min_calories
2. Protein constraint: (protein[Rice] * ServingsRice) + (protein[Kebab] * ServingsKebab) ≥ min_protein

Note:
- All serving quantities are assumed continuous (allowing fractional servings) unless integer requirements are specified.
- Units across parameters are consistent: cost in USD per serving, energy in calories per serving, protein in grams per serving.

Expected Output Schema:
{
  "variables": {
    "ServingsRice": "float",
    "ServingsKebab": "float"
  },
  "objective": "float"
}'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def model_diet():
    # Create the linear solver using the GLOP backend, which is suitable for linear programming.
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Solver not created.")
        return None

    # Variables:
    # ServingsRice: number of rice servings (continuous, >= 0)
    # ServingsKebab: number of kebab servings (continuous, >= 0)
    servings_rice = solver.NumVar(0.0, solver.infinity(), 'ServingsRice')
    servings_kebab = solver.NumVar(0.0, solver.infinity(), 'ServingsKebab')
    
    # Parameters:
    # cost: Rice = 3 USD per serving, Kebab = 2 USD per serving
    # calories: Rice = 300 cals per serving, Kebab = 200 cals per serving
    # protein: Rice = 4.5 grams per serving, Kebab = 4 grams per serving
    # Minimum thresholds: 2200 calories and 30 grams protein
    cost_rice = 3.0
    cost_kebab = 2.0
    calories_rice = 300.0
    calories_kebab = 200.0
    protein_rice = 4.5
    protein_kebab = 4.0
    min_calories = 2200.0
    min_protein = 30.0

    # Constraints:
    # Calorie constraint: (300 * ServingsRice) + (200 * ServingsKebab) >= 2200
    solver.Add(calories_rice * servings_rice + calories_kebab * servings_kebab >= min_calories)

    # Protein constraint: (4.5 * ServingsRice) + (4 * ServingsKebab) >= 30
    solver.Add(protein_rice * servings_rice + protein_kebab * servings_kebab >= min_protein)

    # Objective:
    # Minimize total cost = (3 * ServingsRice) + (2 * ServingsKebab)
    solver.Minimize(cost_rice * servings_rice + cost_kebab * servings_kebab)

    # Solve the model.
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        # Construct and return the result as a dictionary matching the expected output schema.
        result = {
            "variables": {
                "ServingsRice": servings_rice.solution_value(),
                "ServingsKebab": servings_kebab.solution_value()
            },
            "objective": solver.Objective().Value()
        }
        return result
    else:
        return {"message": "No optimal solution found."}

def main():
    # Only one formulation is provided by the problem, so we implement a single optimization model.
    result_diet = model_diet()
    print("Diet Optimization Results:")
    print(result_diet)

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Diet Optimization Results:
{'variables': {'ServingsRice': 7.333333333333335, 'ServingsKebab': 0.0}, 'objective': 22.000000000000004}
'''

'''Expected Output:
Expected solution

: {'variables': {'ServingsRice': 0.0, 'ServingsKebab': 11.0}, 'objective': 22.0}'''

