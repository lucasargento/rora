# Problem Description:
'''Problem description: John has a 300 acre berry farm on which to plant blueberries and raspberries. John has $10000 to spend on watering and 575 days worth of labor available. For each acre of blueberries, 6 days worth of labor and $22 in watering costs is required. For each acre of raspberries, 3 days worth of labor and $25 in watering costs is required. The profit per acre of blueberries is $56 and the profit per acre of raspberries is $75. Formulate an LP problem in order to maximize profit.

Expected Output Schema:
{
  "variables": {
    "Acreage": [
      "float"
    ]
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- B: set of berry types = {Blueberries, Raspberries}

Parameters:
- total_acres: total available farmland [acres] = 300
- total_watering_budget: total available watering funds [USD] = 10000
- total_labor_days: total available labor days [days] = 575
- water_cost[b] for b in B:
  - water_cost[Blueberries] = 22 [USD per acre]
  - water_cost[Raspberries] = 25 [USD per acre]
- labor_requirement[b] for b in B:
  - labor_requirement[Blueberries] = 6 [days per acre]
  - labor_requirement[Raspberries] = 3 [days per acre]
- profit[b] for b in B:
  - profit[Blueberries] = 56 [USD per acre]
  - profit[Raspberries] = 75 [USD per acre]

Variables:
- x[b] for b in B: acres planted with berry type b [continuous, with x[b] ≥ 0] 
  (Interpretation: number of acres allocated to each berry type)

Objective:
- Maximize total profit = profit[Blueberries] * x[Blueberries] + profit[Raspberries] * x[Raspberries]

Constraints:
1. Land constraint:
   - x[Blueberries] + x[Raspberries] ≤ total_acres
2. Watering cost constraint:
   - water_cost[Blueberries] * x[Blueberries] + water_cost[Raspberries] * x[Raspberries] ≤ total_watering_budget
3. Labor days constraint:
   - labor_requirement[Blueberries] * x[Blueberries] + labor_requirement[Raspberries] * x[Raspberries] ≤ total_labor_days

Comments:
- All monetary values are in US dollars.
- Acres can be assumed continuous unless integer acreage is required.
- The model assumes that planting an acre is the smallest decision unit.

Expected Output Schema:
{
  "variables": {
    "Acreage": [
      "float"
    ]
  },
  "objective": "float"
}'''

# Generated Code:
from ortools.linear_solver import pywraplp

def solve_lp_model():
    # Create the linear solver with the GLOP backend for LP.
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Error: Could not create solver.")
        return None

    # Parameters
    total_acres = 300
    total_watering_budget = 10000  # in USD
    total_labor_days = 575         # in days

    # Data for each berry type
    water_cost = {'Blueberries': 22, 'Raspberries': 25}
    labor_requirement = {'Blueberries': 6, 'Raspberries': 3}
    profit = {'Blueberries': 56, 'Raspberries': 75}

    # Decision variables (acreage planted for each berry type)
    acres_blue = solver.NumVar(0, total_acres, 'Blueberries')
    acres_rasp = solver.NumVar(0, total_acres, 'Raspberries')

    # Constraints
    # Land Constraint: acres_blue + acres_rasp <= total_acres
    solver.Add(acres_blue + acres_rasp <= total_acres)

    # Watering Cost Constraint:
    solver.Add(water_cost['Blueberries'] * acres_blue + water_cost['Raspberries'] * acres_rasp <= total_watering_budget)

    # Labor Constraint:
    solver.Add(labor_requirement['Blueberries'] * acres_blue + labor_requirement['Raspberries'] * acres_rasp <= total_labor_days)

    # Objective: maximize total profit.
    solver.Maximize(profit['Blueberries'] * acres_blue + profit['Raspberries'] * acres_rasp)

    # Solve the problem.
    status = solver.Solve()

    solution = {}
    if status == pywraplp.Solver.OPTIMAL:
        solution['Blueberries_acres'] = acres_blue.solution_value()
        solution['Raspberries_acres'] = acres_rasp.solution_value()
        solution['Optimal_profit'] = solver.Objective().Value()
    else:
        solution['message'] = "No optimal solution found."

    return solution

def main():
    results = {}
    # Only one formulation as per given problem description
    results['LP_Model'] = solve_lp_model()

    # Print the results in a structured manner
    print("Optimization Results:")
    for model, result in results.items():
        print(f"\nModel: {model}")
        if 'message' in result:
            print(result['message'])
        else:
            print(f"Acres of Blueberries: {result.get('Blueberries_acres', 'N/A')}")
            print(f"Acres of Raspberries: {result.get('Raspberries_acres', 'N/A')}")
            print(f"Optimal Total Profit: {result.get('Optimal_profit', 'N/A')}")

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Optimization Results:

Model: LP_Model
Acres of Blueberries: 0.0
Acres of Raspberries: 191.66666666666663
Optimal Total Profit: 14374.999999999996
'''

'''Expected Output:
Expected solution

: {'variables': {'Acreage': [0.0, 191.66666666666666]}, 'objective': 14375.0}'''

