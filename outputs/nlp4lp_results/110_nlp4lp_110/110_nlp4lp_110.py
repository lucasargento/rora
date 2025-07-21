# Problem Description:
'''Problem description: A zookeeper feeds a gorilla with bananas and mangoes. Each banana contains 80 calories, 20 grams of potassium, and 10 grams of sugar. Each mango contains 100 calories, 15 grams of potassium, and 8 grams of sugar.  The gorilla must consume at least 4000 calories and 150 grams of potassium. Since the gorilla prefers bananas, at most 33% of the fruits he eats can be mangoes. If excess sugar makes the gorilla aggressive, how many of each fruit should he consume to minimize his sugar intake?

Expected Output Schema:
{
  "variables": {
    "XBanana": "float",
    "XMango": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- F: set of fruits = {Banana, Mango}

Parameters:
- banana_cal: calories per banana [80 calories/banana]
- banana_potassium: potassium per banana [20 grams/banana]
- banana_sugar: sugar per banana [10 grams/banana]
- mango_cal: calories per mango [100 calories/mango]
- mango_potassium: potassium per mango [15 grams/mango]
- mango_sugar: sugar per mango [8 grams/mango]
- min_calories: minimum total calories required [4000 calories]
- min_potassium: minimum total potassium required [150 grams]
- max_frac_mango: maximum fraction of mangoes in total fruits [0.33]

Variables:
- XBanana: number of bananas to feed the gorilla [continuous, nonnegative, units: bananas]
- XMango: number of mangoes to feed the gorilla [continuous, nonnegative, units: mangoes]

Objective:
- Minimize total sugar intake = banana_sugar * XBanana + mango_sugar * XMango  
  (i.e., minimize 10 * XBanana + 8 * XMango)

Constraints:
1. Calorie Constraint:
   - banana_cal * XBanana + mango_cal * XMango >= min_calories  
   (i.e., 80 * XBanana + 100 * XMango >= 4000)

2. Potassium Constraint:
   - banana_potassium * XBanana + mango_potassium * XMango >= min_potassium  
   (i.e., 20 * XBanana + 15 * XMango >= 150)

3. Fruit Preference (Mango Limit) Constraint:
   - XMango <= max_frac_mango * (XBanana + XMango)  
   (i.e., XMango <= 0.33 * (XBanana + XMango))
   
Notes:
- All parameter units are consistent with the description.
- The decision variables are modeled as continuous; if discrete fruit counts are required, the variables can be forced to integer.
- The constraint XMango <= 0.33*(XBanana+XMango) ensures that the number of mangoes does not exceed 33% of the total fruits.

Output Schema (as required):
{
  "variables": {
    "XBanana": "float",
    "XMango": "float"
  },
  "objective": "float"
}'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_linear_program():
    # Create the linear solver with the GLOP backend.
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Linear solver not available.")
        return None

    # Define decision variables: continuous and >= 0.
    XBanana = solver.NumVar(0.0, solver.infinity(), 'XBanana')
    XMango = solver.NumVar(0.0, solver.infinity(), 'XMango')

    # Parameters
    banana_cal = 80
    banana_potassium = 20
    banana_sugar = 10

    mango_cal = 100
    mango_potassium = 15
    mango_sugar = 8

    min_calories = 4000
    min_potassium = 150
    max_frac_mango = 0.33

    # Constraint 1: Calorie constraint
    solver.Add(banana_cal * XBanana + mango_cal * XMango >= min_calories)

    # Constraint 2: Potassium constraint
    solver.Add(banana_potassium * XBanana + mango_potassium * XMango >= min_potassium)

    # Constraint 3: Fruit Preference (Mango Limit)
    # Original formulation: XMango <= max_frac_mango * (XBanana + XMango)
    # Rearranged: XMango - max_frac_mango*XBanana - max_frac_mango*XMango <= 0 -> (1-max_frac_mango)*XMango <= max_frac_mango * XBanana
    # That is equivalent to: 0.67*XMango - 0.33*XBanana <= 0
    solver.Add((1 - max_frac_mango) * XMango - max_frac_mango * XBanana <= 0)

    # Objective: Minimize total sugar intake = 10*XBanana + 8*XMango.
    objective = solver.Objective()
    objective.SetCoefficient(XBanana, banana_sugar)
    objective.SetCoefficient(XMango, mango_sugar)
    objective.SetMinimization()

    status = solver.Solve()

    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "XBanana": XBanana.solution_value(),
            "XMango": XMango.solution_value(),
            "objective": objective.Value()
        }
    else:
        print("The problem does not have an optimal solution.")

    return result

def main():
    # Since only one formulation is provided, we create one model.
    lp_result = solve_linear_program()

    if lp_result:
        print("Optimization Results (Linear Formulation):")
        print("XBanana =", lp_result["XBanana"])
        print("XMango =", lp_result["XMango"])
        print("Objective (Minimized Sugar) =", lp_result["objective"])
    else:
        print("No solution found for the linear formulation.")

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Optimization Results (Linear Formulation):
XBanana = 30.946882217090067
XMango = 15.242494226327947
Objective (Minimized Sugar) = 431.4087759815243
'''

'''Expected Output:
Expected solution

: {'variables': {'XBanana': 32.0, 'XMango': 15.0}, 'objective': 440.0}'''

