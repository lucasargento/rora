# Problem Description:
'''Problem description: A woman eats cashews and almonds to get her calorie and protein intake. A serving of almonds contains 200 calories and 20 grams of protein. A serving of cashews contains 300 calories and 25 grams of protein. The woman decides to eat at least twice as many servings of almonds as cashews. Furthermore, a serving of almonds contains 15 grams of fat while a serving of cashews contains 12 grams of fat. If the woman needs to consume at least 10000 calories and 800 grams of protein this week, how many servings of each should she eat to minimize her fat intake?

Expected Output Schema:
{
  "variables": {
    "NutServings": {
      "0": "float",
      "1": "float"
    }
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- Nuts: set of nut types = {almonds, cashews}

Parameters:
- calories_n: calories per serving for each nut type
  almonds: 200 calories per serving
  cashews: 300 calories per serving
- protein_n: protein per serving (in grams) for each nut type
  almonds: 20 grams per serving
  cashews: 25 grams per serving
- fat_n: fat per serving (in grams) for each nut type
  almonds: 15 grams per serving
  cashews: 12 grams per serving
- min_calories: minimum required total calories per week = 10000 calories
- min_protein: minimum required total protein per week = 800 grams
- min_almonds_ratio: minimum ratio of almonds servings to cashews servings = 2 (i.e., at least twice as many servings of almonds as cashews)

Variables:
- x_n: number of servings of nut type n consumed per week
  For each n in {almonds, cashews}, x_n is a continuous real variable with lower bound 0.
  (In some implementations these could be forced to be integer if servings must be whole numbers.)

Objective:
- Minimize total fat intake per week = (15 * x_almonds) + (12 * x_cashews)
  (Units: total grams of fat per week)

Constraints:
1. Calorie constraint: (200 * x_almonds) + (300 * x_cashews) ≥ 10000
2. Protein constraint: (20 * x_almonds) + (25 * x_cashews) ≥ 800
3. Almond-to-Cashew ratio constraint: x_almonds ≥ 2 * x_cashews

---------------------------------------------
Based on the expected output schema, we provide the following JSON mapping of decision variables and the objective function:

{
  "variables": {
    "NutServings": {
      "0": "float",   // servings of almonds
      "1": "float"    // servings of cashews
    }
  },
  "objective": "float"   // total fat intake = 15 * NutServings[0] + 12 * NutServings[1]"
}'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_continuous():
    # Create the solver with the GLOP backend for continuous variables.
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("GLOP solver unavailable.")
        return None

    # Variables: x0 = servings of almonds, x1 = servings of cashews (continuous)
    x0 = solver.NumVar(0, solver.infinity(), 'almonds')
    x1 = solver.NumVar(0, solver.infinity(), 'cashews')

    # Constraints:
    # 1. Calorie constraint: 200 * almonds + 300 * cashews >= 10000
    solver.Add(200 * x0 + 300 * x1 >= 10000)
    # 2. Protein constraint: 20 * almonds + 25 * cashews >= 800
    solver.Add(20 * x0 + 25 * x1 >= 800)
    # 3. Almond-to-Cashew ratio constraint: almonds >= 2 * cashews
    solver.Add(x0 >= 2 * x1)

    # Objective: minimize total fat intake = 15 * almonds + 12 * cashews
    objective = solver.Objective()
    objective.SetCoefficient(x0, 15)
    objective.SetCoefficient(x1, 12)
    objective.SetMinimization()

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "model": "Continuous",
            "variables": {
                "NutServings": {
                    "0": x0.solution_value(),  # servings of almonds
                    "1": x1.solution_value()   # servings of cashews
                }
            },
            "objective": objective.Value()
        }
        return result
    else:
        return {"model": "Continuous", "message": "No optimal solution found."}


def solve_integer():
    # Create the solver with the CBC backend for integer programming.
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("CBC solver unavailable.")
        return None

    # Variables: x0 = servings of almonds, x1 = servings of cashews (integer version)
    # We assume servings are whole numbers.
    x0 = solver.IntVar(0, solver.infinity(), 'almonds_int')
    x1 = solver.IntVar(0, solver.infinity(), 'cashews_int')

    # Constraints:
    # 1. Calorie constraint: 200 * almonds + 300 * cashews >= 10000
    solver.Add(200 * x0 + 300 * x1 >= 10000)
    # 2. Protein constraint: 20 * almonds + 25 * cashews >= 800
    solver.Add(20 * x0 + 25 * x1 >= 800)
    # 3. Almond-to-Cashew ratio constraint: almonds >= 2 * cashews
    solver.Add(x0 >= 2 * x1)

    # Objective: minimize total fat intake = 15 * almonds + 12 * cashews
    objective = solver.Objective()
    objective.SetCoefficient(x0, 15)
    objective.SetCoefficient(x1, 12)
    objective.SetMinimization()

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "model": "Integer",
            "variables": {
                "NutServings": {
                    "0": x0.solution_value(),  # servings of almonds
                    "1": x1.solution_value()   # servings of cashews
                }
            },
            "objective": objective.Value()
        }
        return result
    else:
        return {"model": "Integer", "message": "No optimal solution found."}


def main():
    # Solve continuous formulation
    continuous_result = solve_continuous()
    # Solve integer formulation
    integer_result = solve_integer()

    # Print the results in a structured manner
    print("Optimization Results:")
    if continuous_result:
        print("\nContinuous Model Output:")
        for key, value in continuous_result.items():
            print(f"{key}: {value}")
    if integer_result:
        print("\nInteger Model Output:")
        for key, value in integer_result.items():
            print(f"{key}: {value}")

if __name__ == "__main__":
    main()

'''Execution Results:
SUCCESS:
Optimization Results:

Continuous Model Output:
model: Continuous
variables: {'NutServings': {'0': 28.57142857142858, '1': 14.28571428571429}}
objective: 600.0000000000002

Integer Model Output:
model: Integer
variables: {'NutServings': {'0': 29.0, '1': 14.0}}
objective: 603.0
'''

'''Expected Output:
Expected solution

: {'variables': {'NutServings': {'0': 28.571428571428573, '1': 14.285714285714286}}, 'objective': 600.0}'''

