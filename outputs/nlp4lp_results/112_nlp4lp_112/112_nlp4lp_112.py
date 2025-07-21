# Problem Description:
'''Problem description: A competitive eater challenges himself to eat slices of cheesecake and caramel cake. Each slice of cheesecake contains 200 calories and 40 grams of sugar. Each slice of caramel cake contains 250 calories and 50 grams of sugar. He prefers cheesecake and decides to eat at least 3 times as many slices of cheesecake as caramel cake. However, he must also eat at least 3 slices of caramel cake. If he can consume at most 10000 calories in one day, how many slices of each cake should he eat to maximize the total amount of sugar he consumes?

Expected Output Schema:
{
  "variables": {
    "CheesecakeSlices": "float",
    "CaramelCakeSlices": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- C: set of cake types = {Cheesecake, CaramelCake}

Parameters:
- calories_Cheesecake = 200 (calories per slice of cheesecake)
- calories_Caramel = 250 (calories per slice of caramel cake)
- sugar_Cheesecake = 40 (grams of sugar per slice of cheesecake)
- sugar_Caramel = 50 (grams of sugar per slice of caramel cake)
- min_CaramelSlices = 3 (minimum number of caramel cake slices required)
- calorie_limit = 10000 (maximum calories that can be consumed in a day)

Variables:
- CheesecakeSlices: float, number of cheesecake slices eaten (expected to be integer but defined as float per output schema)
- CaramelCakeSlices: float, number of caramel cake slices eaten (expected to be integer but defined as float per output schema)

Objective:
- Maximize total sugar consumption = (sugar_Cheesecake * CheesecakeSlices) + (sugar_Caramel * CaramelCakeSlices)
  (Objective unit: grams of sugar)

Constraints:
1. Calorie constraint: (calories_Cheesecake * CheesecakeSlices) + (calories_Caramel * CaramelCakeSlices) ≤ calorie_limit
2. Preference constraint: CheesecakeSlices ≥ 3 * CaramelCakeSlices (at least three times as many cheesecake slices as caramel cake slices)
3. Minimum caramel cake slices: CaramelCakeSlices ≥ min_CaramelSlices

Output Schema:
{
  "variables": {
    "CheesecakeSlices": "float",
    "CaramelCakeSlices": "float"
  },
  "objective": "float"
}'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_linear_program():
    # Create the linear solver with the GLOP backend for linear programming.
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        return None, None, "Solver not created."

    # PARAMETERS as defined
    calories_cheesecake = 200  # per slice
    calories_caramel = 250     # per slice
    sugar_cheesecake = 40      # grams of sugar per slice
    sugar_caramel = 50         # grams of sugar per slice
    min_caramel_slices = 3
    calorie_limit = 10000

    # VARIABLES: using continuous variables as per output schema definition.
    cheesecake = solver.NumVar(0.0, solver.infinity(), 'CheesecakeSlices')
    caramel = solver.NumVar(0.0, solver.infinity(), 'CaramelCakeSlices')

    # CONSTRAINTS

    # 1. Calorie constraint: 200 * cheesecake + 250 * caramel <= 10000
    solver.Add(calories_cheesecake * cheesecake + calories_caramel * caramel <= calorie_limit)

    # 2. Preference constraint: cheesecake >= 3 * caramel
    solver.Add(cheesecake >= 3 * caramel)

    # 3. Minimum caramel cake slices: caramel >= 3
    solver.Add(caramel >= min_caramel_slices)

    # OBJECTIVE: Maximize total sugar = 40*cheesecake + 50*caramel
    objective = solver.Objective()
    objective.SetCoefficient(cheesecake, sugar_cheesecake)
    objective.SetCoefficient(caramel, sugar_caramel)
    objective.SetMaximization()

    # Solve the model
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        # Format the output results per expected output schema.
        result = {
            "variables": {
                "CheesecakeSlices": cheesecake.solution_value(),
                "CaramelCakeSlices": caramel.solution_value()
            },
            "objective": objective.Value()
        }
        return result, solver, None
    else:
        return None, solver, "The problem does not have an optimal solution."

def main():
    # Since only one formulation was provided, we run a single implementation.
    lp_result, solver_instance, error_msg = solve_linear_program()

    print("Linear Programming Model Result:")
    if error_msg:
        print("Error:", error_msg)
    else:
        print(lp_result)

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Linear Programming Model Result:
{'variables': {'CheesecakeSlices': 46.25, 'CaramelCakeSlices': 3.0}, 'objective': 2000.0}
'''

'''Expected Output:
Expected solution

: {'variables': {'CheesecakeSlices': 45.0, 'CaramelCakeSlices': 4.0}, 'objective': 2000.0}'''

