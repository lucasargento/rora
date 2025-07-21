# Problem Description:
'''Problem description: A man  only eats vegetable and fruits. A serving of vegetables contains 2 units of vitamins and 3 units of minerals. A serving of fruit contains 4 units of vitamins and 1 unit of minerals. He wants to eat at least 20 units of vitamins and 30 units of minerals. If vegetables cost $3 per serving and fruits cost $5 per serving, how many servings of each should he eat to minimize his cost?

Expected Output Schema:
{
  "variables": {
    "VegetableServings": "float",
    "FruitServings": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- FoodItems = {Vegetables, Fruits}

Parameters:
- vitamins_per_serving:
   - Vegetables: 2 (units of vitamins per serving)
   - Fruits: 4 (units of vitamins per serving)
- minerals_per_serving:
   - Vegetables: 3 (units of minerals per serving)
   - Fruits: 1 (units of minerals per serving)
- cost_per_serving:
   - Vegetables: 3 (USD per serving)
   - Fruits: 5 (USD per serving)
- required_vitamins: 20 (units)
- required_minerals: 30 (units)

Variables:
- VegetableServings: number of servings of vegetables to eat (continuous, ≥ 0)
- FruitServings: number of servings of fruits to eat (continuous, ≥ 0)

Objective:
- Minimize total cost = (3 * VegetableServings) + (5 * FruitServings)

Constraints:
1. Vitamin requirement constraint:
   (2 * VegetableServings) + (4 * FruitServings) ≥ 20
2. Mineral requirement constraint:
   (3 * VegetableServings) + (1 * FruitServings) ≥ 30

--------------------------------------------------

According to the expected output schema, the solution can be summarized as follows:
{
  "variables": {
    "VegetableServings": "float",
    "FruitServings": "float"
  },
  "objective": "float"
}'''

# Generated Code:
from ortools.linear_solver import pywraplp

def solve_linear_program():
    # Create the linear solver with the GLOP backend.
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Error: Could not create solver.")
        return None

    # Define decision variables: VegetableServings and FruitServings (continuous >= 0)
    vegetable_servings = solver.NumVar(0.0, solver.infinity(), 'VegetableServings')
    fruit_servings = solver.NumVar(0.0, solver.infinity(), 'FruitServings')

    # Constraint 1: Vitamin requirement: 2 * VegetableServings + 4 * FruitServings >= 20
    solver.Add(2 * vegetable_servings + 4 * fruit_servings >= 20)

    # Constraint 2: Mineral requirement: 3 * VegetableServings + 1 * FruitServings >= 30
    solver.Add(3 * vegetable_servings + 1 * fruit_servings >= 30)

    # Objective: Minimize total cost = 3 * VegetableServings + 5 * FruitServings
    solver.Minimize(3 * vegetable_servings + 5 * fruit_servings)

    # Solve the problem and check the result.
    status = solver.Solve()
    if status != pywraplp.Solver.OPTIMAL:
        print("The problem does not have an optimal solution!")
        return None

    # Prepare and return the solution following the expected output schema.
    solution = {
        "variables": {
            "VegetableServings": vegetable_servings.solution_value(),
            "FruitServings": fruit_servings.solution_value()
        },
        "objective": solver.Objective().Value()
    }
    return solution

def main():
    # Solve the LP problem using OR-Tools
    lp_solution = solve_linear_program()

    # Print the results in a structured way
    if lp_solution:
        print("Optimal Solution (Linear Programming Model):")
        print(lp_solution)
    else:
        print("No optimal solution found for the LP model.")

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Optimal Solution (Linear Programming Model):
{'variables': {'VegetableServings': 10.0, 'FruitServings': 1.6062967656290216e-15}, 'objective': 30.000000000000007}
'''

'''Expected Output:
Expected solution

: {'variables': {'VegetableServings': 10.0, 'FruitServings': 0.0}, 'objective': 30.0}'''

