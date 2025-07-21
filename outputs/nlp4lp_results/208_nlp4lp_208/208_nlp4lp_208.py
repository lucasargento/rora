# Problem Description:
'''Problem description: A neighbourhood pizza restaurant has opened and sells pizzas in two sizes; large pizza and medium pizza. Large pizzas require 12 units of dough, and 5 units of toppings. Medium pizzas require 8 units of dough, and 4 units of toppings. While large pizzas take 12 minutes to bake, medium pizzas require 8 minutes to bake. The neighbourhood pizza restaurant must use at least 10000 units of dough and 4400 units of toppings. Medium pizzas are popular due to a promotion, therefore, at least 200 medium pizzas must be made. There are regulars that prefer large pizzas and at least two times as many large pizzas should be made than medium pizzas. How many of each size of pizzas should the neighbourhood pizza restaurant make to reduce time spent baking?

Expected Output Schema:
{
  "variables": {
    "NumberLargePizzas": "float",
    "NumberMediumPizzas": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- SIZES: set of pizza sizes = {Large, Medium}

Parameters:
- DoughUsage: units of dough required per pizza by size. Specifically, DoughUsage[Large] = 12 (units per large pizza), DoughUsage[Medium] = 8 (units per medium pizza)
- ToppingUsage: units of toppings required per pizza by size. Specifically, ToppingUsage[Large] = 5 (units per large pizza), ToppingUsage[Medium] = 4 (units per medium pizza)
- BakeTime: baking time required per pizza by size. Specifically, BakeTime[Large] = 12 (minutes per large pizza), BakeTime[Medium] = 8 (minutes per medium pizza)
- MinTotalDough: minimum total dough required = 10000 (units)
- MinTotalToppings: minimum total toppings required = 4400 (units)
- MinMediumPizzas: minimum medium pizzas to produce = 200 (pizzas)
- RatioLargeToMedium: minimum ratio of large to medium pizzas = 2

Variables:
- NumberLargePizzas: number of large pizzas to produce (integer >= 0)
- NumberMediumPizzas: number of medium pizzas to produce (integer >= 0)

Objective:
- Minimize total baking time = (BakeTime[Large] * NumberLargePizzas) + (BakeTime[Medium] * NumberMediumPizzas)
  Note: The objective is expressed in minutes.

Constraints:
1. Dough constraint: (DoughUsage[Large] * NumberLargePizzas) + (DoughUsage[Medium] * NumberMediumPizzas) >= MinTotalDough
2. Toppings constraint: (ToppingUsage[Large] * NumberLargePizzas) + (ToppingUsage[Medium] * NumberMediumPizzas) >= MinTotalToppings
3. Medium pizza minimum: NumberMediumPizzas >= MinMediumPizzas
4. Large-to-medium ratio: NumberLargePizzas >= RatioLargeToMedium * NumberMediumPizzas

This structured model completely represents the neighborhood pizza restaurant problem while ensuring all units are consistent, and it is directly translatable to a Python or OR-Tools implementation.'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def run_linear_solver_model():
    # Create the linear solver with the CBC backend.
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Solver 'CBC' not found.")
        return None

    # Parameters
    dough_usage_large = 12
    dough_usage_medium = 8
    topping_usage_large = 5
    topping_usage_medium = 4
    bake_time_large = 12
    bake_time_medium = 8
    min_total_dough = 10000
    min_total_toppings = 4400
    min_medium_pizzas = 200
    ratio_large_to_medium = 2

    # Variables: number of pizzas (integer variables)
    NumberLargePizzas = solver.IntVar(0, solver.infinity(), 'NumberLargePizzas')
    NumberMediumPizzas = solver.IntVar(0, solver.infinity(), 'NumberMediumPizzas')

    # Constraints
    # 1. Dough constraint: 12 * NumberLargePizzas + 8 * NumberMediumPizzas >= 10000
    solver.Add(dough_usage_large * NumberLargePizzas + dough_usage_medium * NumberMediumPizzas >= min_total_dough)

    # 2. Toppings constraint: 5 * NumberLargePizzas + 4 * NumberMediumPizzas >= 4400
    solver.Add(topping_usage_large * NumberLargePizzas + topping_usage_medium * NumberMediumPizzas >= min_total_toppings)

    # 3. Medium pizzas minimum: NumberMediumPizzas >= 200
    solver.Add(NumberMediumPizzas >= min_medium_pizzas)

    # 4. Large-to-medium ratio: NumberLargePizzas >= 2 * NumberMediumPizzas
    solver.Add(NumberLargePizzas >= ratio_large_to_medium * NumberMediumPizzas)

    # Objective: minimize total baking time in minutes
    # Total baking time = 12 * NumberLargePizzas + 8 * NumberMediumPizzas
    objective = solver.Objective()
    objective.SetCoefficient(NumberLargePizzas, bake_time_large)
    objective.SetCoefficient(NumberMediumPizzas, bake_time_medium)
    objective.SetMinimization()

    # Solve the model.
    status = solver.Solve()

    # Prepare result dictionary in the expected output schema.
    result = {
        "variables": {
            "NumberLargePizzas": None,
            "NumberMediumPizzas": None,
        },
        "objective": None
    }

    if status == pywraplp.Solver.OPTIMAL:
        result["variables"]["NumberLargePizzas"] = NumberLargePizzas.solution_value()
        result["variables"]["NumberMediumPizzas"] = NumberMediumPizzas.solution_value()
        result["objective"] = objective.Value()
    else:
        print("The problem does not have an optimal solution!")
        return None

    return result

def main():
    # We have one formulation for this linear optimization problem.
    # In case more formulations are proposed, each model should be separate.
    results = {}

    # Run the linear solver model version.
    linear_result = run_linear_solver_model()
    if linear_result is not None:
        results["Linear_Solver_Model"] = linear_result
    else:
        results["Linear_Solver_Model"] = "No optimal solution found."

    # Printing results in a structured way.
    print("Optimization Results:")
    for model_name, res in results.items():
        print(f"\nModel: {model_name}")
        if isinstance(res, dict):
            print("Variables:")
            for var, val in res["variables"].items():
                print(f"  {var}: {val}")
            print(f"Objective Value: {res['objective']}")
        else:
            print(res)

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Optimization Results:

Model: Linear_Solver_Model
Variables:
  NumberLargePizzas: 629.0
  NumberMediumPizzas: 314.0
Objective Value: 10060.0
'''

'''Expected Output:
Expected solution

: {'variables': {'NumberLargePizzas': 629.0, 'NumberMediumPizzas': 314.0}, 'objective': 10060.0}'''

