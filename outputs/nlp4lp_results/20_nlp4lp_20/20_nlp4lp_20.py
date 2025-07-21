# Problem Description:
'''Problem description: A car manufacturer makes two versions of the same car, a regular model and a premium model. They make x1 regular models per day and x2 premium models per day. The profit per regular model is $5000 and the profit per premium model is $8500 (x1 and x2 are unknown values both greater than or equal to 0). The daily demand for these cars is limited to and most 8 regular models and 6 premium models. In addition, the manufacturer can make a maximum of 12 cars of either type per day. How many cars of each model should the manufacturer make in order to maximize profit?

Expected Output Schema:
{
  "variables": {
    "RegularModelsProduced": "float",
    "PremiumModelsProduced": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- M: set of car models = {Regular, Premium}

Parameters:
- profit_Regular: profit per regular model produced [USD per car] = 5000
- profit_Premium: profit per premium model produced [USD per car] = 8500
- max_demand_Regular: maximum daily demand for regular models [cars/day] = 8
- max_demand_Premium: maximum daily demand for premium models [cars/day] = 6
- max_total_production: maximum number of cars that can be produced per day, regardless of model [cars/day] = 12

Variables:
- RegularModelsProduced (x1): number of regular models produced per day [nonnegative integer or float; ideally integer]
- PremiumModelsProduced (x2): number of premium models produced per day [nonnegative integer or float; ideally integer]

Objective:
- Maximize total profit = (profit_Regular * RegularModelsProduced) + (profit_Premium * PremiumModelsProduced)

Constraints:
1. Demand constraint for regular models: RegularModelsProduced ≤ max_demand_Regular  
2. Demand constraint for premium models: PremiumModelsProduced ≤ max_demand_Premium  
3. Total production capacity constraint: RegularModelsProduced + PremiumModelsProduced ≤ max_total_production  
4. Non-negativity constraints: RegularModelsProduced ≥ 0, PremiumModelsProduced ≥ 0

------------------------------------------------------------
The following JSON output uses the expected output schema:

{
  "variables": {
    "RegularModelsProduced": "float",
    "PremiumModelsProduced": "float"
  },
  "objective": "5000 * RegularModelsProduced + 8500 * PremiumModelsProduced"
}'''

# Generated Code:
from ortools.linear_solver import pywraplp
import json

def solve_car_production():
    # Create the linear solver using CBC
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Solver not created.")
        return None

    # Define variables with their natural demand upper bounds:
    # RegularModelsProduced: x1 in [0, 8]
    # PremiumModelsProduced: x2 in [0, 6]
    x1 = solver.NumVar(0, 8, 'RegularModelsProduced')
    x2 = solver.NumVar(0, 6, 'PremiumModelsProduced')

    # Add total production capacity constraint: x1 + x2 <= 12
    solver.Add(x1 + x2 <= 12)

    # Objective: maximize profit => 5000*x1 + 8500*x2
    objective = solver.Objective()
    objective.SetCoefficient(x1, 5000)
    objective.SetCoefficient(x2, 8500)
    objective.SetMaximization()

    # Solve the problem
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        solution = {
            "variables": {
                "RegularModelsProduced": x1.solution_value(),
                "PremiumModelsProduced": x2.solution_value()
            },
            "objective": objective.Value()
        }
        return solution
    else:
        return {"error": "The problem does not have an optimal solution."}

def main():
    # Solve the car production problem using linear programming approach.
    result_lp = solve_car_production()

    # Print the results in a nicely structured JSON format.
    print(json.dumps({"LinearProgrammingSolution": result_lp}, indent=4))

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
{
    "LinearProgrammingSolution": {
        "variables": {
            "RegularModelsProduced": 6.0,
            "PremiumModelsProduced": 6.0
        },
        "objective": 81000.0
    }
}
'''

'''Expected Output:
Expected solution

: {'variables': {'RegularModelsProduced': 6.0, 'PremiumModelsProduced': 6.0}, 'objective': 81000.0}'''

