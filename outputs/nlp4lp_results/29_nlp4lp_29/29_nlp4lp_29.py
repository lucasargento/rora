# Problem Description:
'''Problem description: A berry farmer has two farms, an old and new farm, where he grows raspberries, blueberries, and strawberries. He has a contract to provide a local store with 10 kg of raspberries, 9 kg of blueberries, and 15 kg of strawberries. At his old farm, it cost $300 to operate per day and he can harvest and deliver 2 kg of raspberries, 2 kg of blueberries, and 4 kg of strawberries in a day. At his new farm, it costs $200 to operate per day and he can harvest and deliver 4 kg of raspberries, 1 kg of blueberries, and 2 kg of strawberries in a day. Formulate a LP to meet his contract while minimizing his cost.

Expected Output Schema:
{
  "variables": {
    "DaysOperated": [
      "float"
    ]
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
• Farms: {Old, New}
• Crops: {Raspberries, Blueberries, Strawberries}

Parameters:
• cost_f: Daily operating cost for each farm f:
  – cost_Old = 300 dollars per day
  – cost_New = 200 dollars per day
• prod_f_c: Daily production (in kg) of crop c at farm f:
  – For Old: prod_Old_Raspberries = 2, prod_Old_Blueberries = 2, prod_Old_Strawberries = 4
  – For New: prod_New_Raspberries = 4, prod_New_Blueberries = 1, prod_New_Strawberries = 2
• req_c: Contract requirement (in kg) for each crop c:
  – req_Raspberries = 10
  – req_Blueberries = 9
  – req_Strawberries = 15

Variables:
• days_f: Number of days to operate farm f (continuous, nonnegative), where f ∈ {Old, New}
  – For example, days_Old and days_New represent the days of operation at the Old and New farms respectively.

Objective:
• Minimize total operating cost:
  Minimize: total_cost = cost_Old * days_Old + cost_New * days_New
  That is, minimize 300 * days_Old + 200 * days_New

Constraints:
• Meeting the raspberries contract:
  2 * days_Old + 4 * days_New >= 10
• Meeting the blueberries contract:
  2 * days_Old + 1 * days_New >= 9
• Meeting the strawberries contract:
  4 * days_Old + 2 * days_New >= 15
• Nonnegativity:
  days_Old >= 0, days_New >= 0

Notes:
• All units are in dollars for costs and kilograms for production and requirements.
• It is assumed that operating a farm for a fractional number of days is acceptable. If days must be integer, then the variable type should be changed accordingly.

This structured model is complete and ready to be translated into a working LP implementation.'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_continuous():
    """Solve the LP with continuous decision variables."""
    # Create the solver with the GLOP backend.
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("GLOP solver unavailable.")
        return None

    # Variables: days_old and days_new (continuous, nonnegative)
    days_old = solver.NumVar(0.0, solver.infinity(), 'days_old')
    days_new = solver.NumVar(0.0, solver.infinity(), 'days_new')

    # Parameters
    cost_old = 300
    cost_new = 200

    # Production rates (kg/day)
    prod_old = {'Raspberries': 2, 'Blueberries': 2, 'Strawberries': 4}
    prod_new = {'Raspberries': 4, 'Blueberries': 1, 'Strawberries': 2}

    # Contract requirements (kg)
    req = {'Raspberries': 10, 'Blueberries': 9, 'Strawberries': 15}

    # Objective: Minimize total cost = 300 * days_old + 200 * days_new
    objective = solver.Objective()
    objective.SetCoefficient(days_old, cost_old)
    objective.SetCoefficient(days_new, cost_new)
    objective.SetMinimization()

    # Constraints:
    # Raspberries: 2*days_old + 4*days_new >= 10
    solver.Add(prod_old['Raspberries'] * days_old + prod_new['Raspberries'] * days_new >= req['Raspberries'])
    # Blueberries: 2*days_old + 1*days_new >= 9
    solver.Add(prod_old['Blueberries'] * days_old + prod_new['Blueberries'] * days_new >= req['Blueberries'])
    # Strawberries: 4*days_old + 2*days_new >= 15
    solver.Add(prod_old['Strawberries'] * days_old + prod_new['Strawberries'] * days_new >= req['Strawberries'])

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        result = {
            'days_old': days_old.solution_value(),
            'days_new': days_new.solution_value(),
            'total_cost': objective.Value()
        }
        return result
    else:
        print("The continuous model did not find an optimal solution.")
        return None

def solve_integer():
    """Solve the model with integer decision variables (if whole number days are required)."""
    # Create the solver with the CBC backend (for integer programming).
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("CBC solver unavailable.")
        return None

    # Variables: days_old and days_new (integer, nonnegative)
    days_old = solver.IntVar(0, solver.infinity(), 'days_old')
    days_new = solver.IntVar(0, solver.infinity(), 'days_new')

    # Parameters
    cost_old = 300
    cost_new = 200

    # Production rates (kg/day)
    prod_old = {'Raspberries': 2, 'Blueberries': 2, 'Strawberries': 4}
    prod_new = {'Raspberries': 4, 'Blueberries': 1, 'Strawberries': 2}

    # Contract requirements (kg)
    req = {'Raspberries': 10, 'Blueberries': 9, 'Strawberries': 15}

    # Objective: Minimize total cost = 300 * days_old + 200 * days_new
    objective = solver.Objective()
    objective.SetCoefficient(days_old, cost_old)
    objective.SetCoefficient(days_new, cost_new)
    objective.SetMinimization()

    # Constraints:
    # Raspberries: 2*days_old + 4*days_new >= 10
    solver.Add(prod_old['Raspberries'] * days_old + prod_new['Raspberries'] * days_new >= req['Raspberries'])
    # Blueberries: 2*days_old + 1*days_new >= 9
    solver.Add(prod_old['Blueberries'] * days_old + prod_new['Blueberries'] * days_new >= req['Blueberries'])
    # Strawberries: 4*days_old + 2*days_new >= 15
    solver.Add(prod_old['Strawberries'] * days_old + prod_new['Strawberries'] * days_new >= req['Strawberries'])

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        result = {
            'days_old': days_old.solution_value(),
            'days_new': days_new.solution_value(),
            'total_cost': objective.Value()
        }
        return result
    else:
        print("The integer model did not find an optimal solution.")
        return None

def main():
    print("----- Continuous LP Model -----")
    continuous_result = solve_continuous()
    if continuous_result:
        print("Optimal days operated at old farm:", continuous_result['days_old'])
        print("Optimal days operated at new farm:", continuous_result['days_new'])
        print("Total operating cost: $", continuous_result['total_cost'])
    else:
        print("No optimal solution found for the continuous model.")

    print("\n----- Integer LP Model -----")
    integer_result = solve_integer()
    if integer_result:
        print("Optimal days operated at old farm:", integer_result['days_old'])
        print("Optimal days operated at new farm:", integer_result['days_new'])
        print("Total operating cost: $", integer_result['total_cost'])
    else:
        print("No optimal solution found for the integer model.")

if __name__ == "__main__":
    main()

'''Execution Results:
SUCCESS:
----- Continuous LP Model -----
Optimal days operated at old farm: 4.333333333333333
Optimal days operated at new farm: 0.33333333333333326
Total operating cost: $ 1366.6666666666667

----- Integer LP Model -----
Optimal days operated at old farm: 4.0
Optimal days operated at new farm: 1.0
Total operating cost: $ 1400.0
'''

'''Expected Output:
Expected solution

: {'variables': {'DaysOperated': [4.333333333333333, 0.3333333333333335]}, 'objective': 1366.6666666666667}'''

