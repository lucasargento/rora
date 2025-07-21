# Problem Description:
'''Problem description: A doctor recommends that a man eat burgers and pizza in order to put on weight. Each burger contains 10 units of fat and 300 calories. Each slice of pizza contains 8 units of fat and 250 calories. The man must get at least 130 units of fat and 3000 calories. Further, each burger contains 12 units of cholesterol while each slice of pizza contains 10 units of cholesterol. Since burgers are slightly more expensive, the man decides to eat at least twice as many slices of pizza as burgers. How many of each should he eat to minimize his cholesterol intake?

Expected Output Schema:
{
  "variables": {
    "Burgers": "float",
    "PizzaSlices": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Below is the structured mathematical model following the five-element framework. Note that the units for fat, calories, and cholesterol are taken directly from the problem (fat in “units”, calories in “calories”, and cholesterol in “units”), and the decision variables count the number of burgers and pizza slices (assumed to be nonnegative integers). We assume a person can only eat whole burgers and whole slices of pizza.

------------------------------------------------------------
Sets:
• FoodItems = {Burger, PizzaSlice}
  (This set labels the two types of items under consideration.)

------------------------------------------------------------
Parameters:
• BurgerFat = 10           (fat per burger in fat units)
• BurgerCalories = 300     (calories per burger)
• BurgerCholesterol = 12   (cholesterol per burger in cholesterol units)
• PizzaFat = 8             (fat per pizza slice in fat units)
• PizzaCalories = 250      (calories per pizza slice)
• PizzaCholesterol = 10    (cholesterol per pizza slice in cholesterol units)
• MinimumFat = 130         (required fat intake in fat units)
• MinimumCalories = 3000   (required caloric intake)
• PizzaMultiplier = 2      (pizza slices must be at least twice the number of burgers)

------------------------------------------------------------
Variables:
• x_Burger: number of burgers to eat [integer, ≥ 0, units = items]
• x_PizzaSlice: number of pizza slices to eat [integer, ≥ 0, units = items]

------------------------------------------------------------
Objective:
Minimize TotalCholesterol = (BurgerCholesterol * x_Burger) + (PizzaCholesterol * x_PizzaSlice)
   i.e., minimize 12 * x_Burger + 10 * x_PizzaSlice
(This objective minimizes the man's overall cholesterol intake.)

------------------------------------------------------------
Constraints:
1. Fat Constraint: (BurgerFat * x_Burger) + (PizzaFat * x_PizzaSlice) ≥ MinimumFat  
   i.e., 10 * x_Burger + 8 * x_PizzaSlice ≥ 130

2. Calorie Constraint: (BurgerCalories * x_Burger) + (PizzaCalories * x_PizzaSlice) ≥ MinimumCalories  
   i.e., 300 * x_Burger + 250 * x_PizzaSlice ≥ 3000

3. Pizza-to-Burger Ratio Constraint: The number of pizza slices must be at least twice the number of burgers  
   i.e., x_PizzaSlice ≥ PizzaMultiplier * x_Burger  
   (This ensures x_PizzaSlice ≥ 2 * x_Burger)

------------------------------------------------------------
Below is the expected output schema in JSON format:

{
  "variables": {
    "Burgers": "integer (≥0)",
    "PizzaSlices": "integer (≥0)"
  },
  "objective": "Minimize 12 * Burgers + 10 * PizzaSlices"
}

This model is complete, self-contained, and directly mappable to a working implementation in Python or OR-Tools.'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp


def solve_linear_model():
    """Solves the optimization problem using OR-Tools linear solver (CBC_MIXED_INTEGER_PROGRAMMING)."""
    # Create the solver with the CBC backend.
    solver = pywraplp.Solver.CreateSolver('CBC_MIXED_INTEGER_PROGRAMMING')
    if not solver:
        print("Solver not created.")
        return None

    # Decision Variables:
    # Burgers: number of burgers (nonnegative integer)
    # PizzaSlices: number of pizza slices (nonnegative integer)
    burgers = solver.IntVar(0, solver.infinity(), 'Burgers')
    pizza_slices = solver.IntVar(0, solver.infinity(), 'PizzaSlices')

    # Constraints:
    # 1. Fat Constraint: 10 * burgers + 8 * pizza_slices >= 130
    solver.Add(10 * burgers + 8 * pizza_slices >= 130)

    # 2. Calorie Constraint: 300 * burgers + 250 * pizza_slices >= 3000
    solver.Add(300 * burgers + 250 * pizza_slices >= 3000)

    # 3. Pizza-to-Burger Ratio Constraint: pizza_slices >= 2 * burgers
    solver.Add(pizza_slices >= 2 * burgers)

    # Objective:
    # Minimize total cholesterol: 12 * burgers + 10 * pizza_slices
    solver.Minimize(12 * burgers + 10 * pizza_slices)

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        solution = {
            "variables": {
                "Burgers": int(burgers.solution_value()),
                "PizzaSlices": int(pizza_slices.solution_value())
            },
            "objective": solver.Objective().Value()
        }
        return solution
    else:
        return None


def main():
    results = {}
    # Only one formulation is needed as per the provided mathematical model.
    linear_model_result = solve_linear_model()
    results["LinearModel"] = linear_model_result

    # Print the results in a structured way
    if linear_model_result:
        print("Optimal Solution for the Linear Model:")
        print("Burgers =", linear_model_result["variables"]["Burgers"])
        print("PizzaSlices =", linear_model_result["variables"]["PizzaSlices"])
        print("Objective value (Total Cholesterol) =", linear_model_result["objective"])
    else:
        print("The linear model did not find a feasible solution.")


if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Optimal Solution for the Linear Model:
Burgers = 5
PizzaSlices = 10
Objective value (Total Cholesterol) = 160.0
'''

'''Expected Output:
Expected solution

: {'variables': {'Burgers': 5.0, 'PizzaSlices': 10.0}, 'objective': 160.0}'''

