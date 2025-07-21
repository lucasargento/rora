# Problem Description:
'''Problem description: A milk tea shop owner would like to sell two different milk teas: black milk tea and matcha milk tea. Each contains both milk and honey. A bottle of black milk tea contains 600 grams of milk and 10 grams of honey, whereas a bottle of matcha milk tea contains 525 grams of milk and 5 grams of honey. The profit from each bottle of black milk tea sold is $7.5 and the profit from each bottle of matcha milk tea sold is $5. If his total production must not exceed his available stock of 30000 grams of milk and 500 grams of honey, how many bottles of each type of milk tea should be made to maximize profits?

Expected Output Schema:
{
  "variables": {
    "Produce": {
      "0": "float",
      "1": "float"
    }
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- TeaTypes: set of milk tea types = {black, matcha}

Parameters:
- profit_black: profit per bottle of black milk tea [USD per bottle] = 7.5
- profit_matcha: profit per bottle of matcha milk tea [USD per bottle] = 5
- milk_black: milk required per bottle of black milk tea [grams per bottle] = 600
- milk_matcha: milk required per bottle of matcha milk tea [grams per bottle] = 525
- honey_black: honey required per bottle of black milk tea [grams per bottle] = 10
- honey_matcha: honey required per bottle of matcha milk tea [grams per bottle] = 5
- total_milk: total available milk [grams] = 30000
- total_honey: total available honey [grams] = 500

Variables:
- x_black: number of bottles of black milk tea to produce [nonnegative continuous variable, representing bottles]
- x_matcha: number of bottles of matcha milk tea to produce [nonnegative continuous variable, representing bottles]
  (Note: Even though bottles are discrete, the problem formulation uses floats. In a practical implementation, you might require integer variables.)

Objective:
- Maximize total profit:
  Maximize Profit = (profit_black * x_black) + (profit_matcha * x_matcha)
  which numerically is: Maximize Profit = 7.5*x_black + 5*x_matcha

Constraints:
1. Milk availability constraint:
   milk_black*x_black + milk_matcha*x_matcha ≤ total_milk
   That is: 600*x_black + 525*x_matcha ≤ 30000

2. Honey availability constraint:
   honey_black*x_black + honey_matcha*x_matcha ≤ total_honey
   That is: 10*x_black + 5*x_matcha ≤ 500

# Model Comments:
- All resource units are expressed in grams for milk and honey.
- The decision variables represent the number of bottles produced; while bottles are discrete, the variable type is indicated as float per the expected output schema.
- The objective focuses solely on profit maximization with no additional cost elements.

This structured mathematical model is complete and faithfully represents the original milk tea optimization problem using the five-element framework.'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp
from ortools.sat.python import cp_model

def solve_linear():
    """Solve the milk tea problem using the linear solver (floats)."""
    # Create the solver using GLOP for linear programming.
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Linear Solver not available.")
        return None

    # Define decision variables (floats as per formulation).
    # x_black: bottles of black milk tea, x_matcha: bottles of matcha milk tea.
    x_black = solver.NumVar(0.0, solver.infinity(), 'x_black')
    x_matcha = solver.NumVar(0.0, solver.infinity(), 'x_matcha')

    # Parameters.
    profit_black = 7.5
    profit_matcha = 5.0
    milk_black = 600.0
    milk_matcha = 525.0
    honey_black = 10.0
    honey_matcha = 5.0
    total_milk = 30000.0
    total_honey = 500.0

    # Constraints.
    # Milk constraint: 600*x_black + 525*x_matcha <= 30000
    solver.Add(milk_black * x_black + milk_matcha * x_matcha <= total_milk)
    # Honey constraint: 10*x_black + 5*x_matcha <= 500
    solver.Add(honey_black * x_black + honey_matcha * x_matcha <= total_honey)

    # Objective: maximize profit = 7.5*x_black + 5*x_matcha.
    objective = solver.Objective()
    objective.SetCoefficient(x_black, profit_black)
    objective.SetCoefficient(x_matcha, profit_matcha)
    objective.SetMaximization()

    status = solver.Solve()
    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result['model'] = 'LinearSolver'
        result['variables'] = {
            "Produce": {
                "black": x_black.solution_value(),
                "matcha": x_matcha.solution_value()
            }
        }
        result['objective'] = objective.Value()
    else:
        result['model'] = 'LinearSolver'
        result['message'] = "No optimal solution found."
    return result

def solve_cp():
    """Solve the milk tea problem using the CP-SAT solver (integer formulation)."""
    model = cp_model.CpModel()
    # In CP-SAT, we define integer variables.
    # Upper bounds are derived from constraints.
    # For black tea, maximum by honey constraint is 500/10 = 50.
    # For matcha tea, maximum by honey constraint is 500/5 = 100.
    x_black = model.NewIntVar(0, 50, 'x_black')
    x_matcha = model.NewIntVar(0, 100, 'x_matcha')

    # Parameters (all integers or scaled integers as needed).
    milk_black = 600
    milk_matcha = 525
    total_milk = 30000
    honey_black = 10
    honey_matcha = 5
    total_honey = 500

    # Constraints.
    # Milk constraint: 600*x_black + 525*x_matcha <= 30000
    model.Add(milk_black * x_black + milk_matcha * x_matcha <= total_milk)
    # Honey constraint: 10*x_black + 5*x_matcha <= 500
    model.Add(honey_black * x_black + honey_matcha * x_matcha <= total_honey)

    # Objective:
    # Original profit coefficients are 7.5 and 5. To avoid fractions, multiply by 2:
    # i.e., maximize 15*x_black + 10*x_matcha. We will scale back later.
    profit_black_scaled = 15
    profit_matcha_scaled = 10
    model.Maximize(profit_black_scaled * x_black + profit_matcha_scaled * x_matcha)

    # Solve the model.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    result = {}
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        # Compute original profit value by dividing objective value by 2.
        objective_val = solver.ObjectiveValue() / 2.0
        result['model'] = 'CPSAT'
        result['variables'] = {
            "Produce": {
                "black": solver.Value(x_black),
                "matcha": solver.Value(x_matcha)
            }
        }
        result['objective'] = objective_val
    else:
        result['model'] = 'CPSAT'
        result['message'] = "No optimal solution found."
    return result

def main():
    # Solve using both formulations.
    print("---- Linear Solver (Continuous Variables) ----")
    linear_result = solve_linear()
    if linear_result:
        if 'message' in linear_result:
            print(linear_result['message'])
        else:
            print("Optimal Production Plan:")
            for tea, val in linear_result['variables']['Produce'].items():
                print(f"  {tea}: {val:.2f} bottles")
            print(f"Maximum Profit: ${linear_result['objective']:.2f}")
    print("\n---- CP-SAT Solver (Integer Variables) ----")
    cp_result = solve_cp()
    if cp_result:
        if 'message' in cp_result:
            print(cp_result['message'])
        else:
            print("Optimal Production Plan:")
            for tea, val in cp_result['variables']['Produce'].items():
                print(f"  {tea}: {val} bottles")
            print(f"Maximum Profit: ${cp_result['objective']:.2f}")

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
---- Linear Solver (Continuous Variables) ----
Optimal Production Plan:
  black: 50.00 bottles
  matcha: 0.00 bottles
Maximum Profit: $375.00

---- CP-SAT Solver (Integer Variables) ----
Optimal Production Plan:
  black: 50 bottles
  matcha: 0 bottles
Maximum Profit: $375.00
'''

'''Expected Output:
Expected solution

: {'variables': {'Produce': {'0': 50.0, '1': 0.0}}, 'objective': 375.0}'''

