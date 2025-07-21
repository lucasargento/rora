# Problem Description:
'''Problem description: A taco stand sells regular tacos and deluxe tacos with extra meat. The stand makes x1 regular tacos at a profit of $2.50 each and x2 deluxe tacos at a profit of $3.55 each (x1 and x2 are unknown variables both greater than or equal to 0). There is a demand for at most 50 regular tacos and at most 40 deluxe tacos. The stand only has enough supplies to sell at most 70 tacos of either type. How many of each taco should the stand make to maximize profit?

Expected Output Schema:
{
  "variables": {
    "RegularTacosProduced": "float",
    "DeluxeTacosProduced": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- Tacos: set of taco types = {Regular, Deluxe}

Parameters:
- profit_regular: profit per regular taco produced (USD per taco) = 2.50
- profit_deluxe: profit per deluxe taco produced (USD per taco) = 3.55
- max_regular: maximum demand for regular tacos (tacos) = 50
- max_deluxe: maximum demand for deluxe tacos (tacos) = 40
- total_supply: maximum total taco production (tacos) = 70

Variables:
- x_regular: number of regular tacos produced, continuous, x_regular ≥ 0
- x_deluxe: number of deluxe tacos produced, continuous, x_deluxe ≥ 0

Objective:
- Maximize total_profit = profit_regular * x_regular + profit_deluxe * x_deluxe

Constraints:
1. Regular taco demand constraint: x_regular ≤ max_regular
2. Deluxe taco demand constraint: x_deluxe ≤ max_deluxe
3. Total production constraint: x_regular + x_deluxe ≤ total_supply

-------------------------------------------------
Expected Output Schema:
{
  "variables": {
    "RegularTacosProduced": "float",   // corresponds to x_regular
    "DeluxeTacosProduced": "float"       // corresponds to x_deluxe
  },
  "objective": "float"                   // total_profit = 2.50 * RegularTacosProduced + 3.55 * DeluxeTacosProduced
}'''

# Generated Code:
from ortools.linear_solver import pywraplp

def solve_lp_model():
    # Create the linear solver using the GLOP backend.
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Solver not created.")
        return None

    # Parameters
    profit_regular = 2.50
    profit_deluxe = 3.55
    max_regular = 50
    max_deluxe = 40
    total_supply = 70

    # Decision Variables:
    # x_regular: number of regular tacos produced (continuous, >= 0)
    # x_deluxe: number of deluxe tacos produced (continuous, >= 0)
    x_regular = solver.NumVar(0.0, max_regular, 'RegularTacosProduced')
    x_deluxe = solver.NumVar(0.0, max_deluxe, 'DeluxeTacosProduced')

    # Constraint: Total production constraint: x_regular + x_deluxe <= total_supply
    solver.Add(x_regular + x_deluxe <= total_supply)

    # Objective: maximize total profit = 2.50*x_regular + 3.55*x_deluxe
    solver.Maximize(profit_regular * x_regular + profit_deluxe * x_deluxe)

    # Solve the model.
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "variables": {
                "RegularTacosProduced": x_regular.solution_value(),
                "DeluxeTacosProduced": x_deluxe.solution_value()
            },
            "objective": solver.Objective().Value()
        }
        return result
    else:
        print("The problem does not have an optimal solution.")
        return None

def main():
    results = {}

    # Run LP model implementation.
    lp_result = solve_lp_model()
    results["LP_Model"] = lp_result

    # Print results in a structured way.
    print("Optimization Results:")
    for model, result in results.items():
        print(f"\nModel: {model}")
        if result is not None:
            print("Optimal decision variables:")
            for var, value in result["variables"].items():
                print(f"  {var}: {value}")
            print(f"Optimal objective value: {result['objective']}")
        else:
            print("No optimal solution found.")

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Optimization Results:

Model: LP_Model
Optimal decision variables:
  RegularTacosProduced: 30.0
  DeluxeTacosProduced: 40.0
Optimal objective value: 217.0
'''

'''Expected Output:
Expected solution

: {'variables': {'RegularTacosProduced': 30.0, 'DeluxeTacosProduced': 40.0}, 'objective': 217.0}'''

