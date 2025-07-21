# Problem Description:
'''Problem description: An appliance company sells and installs refrigerators and stoves. Each refrigerator takes 60 minutes of mover time and 20 minutes of setup time. Each stove takes 45 minutes of mover time and 25 minutes of setup time. The company has available 20000 minutes of mover time and 13000 minutes of setup time. If the profit per refrigerator is $400 and the profit per stove is $260, how many of each should they sell in order to maximize profit?

Expected Output Schema:
{
  "variables": {
    "QuantityOfProduct": {
      "0": "float",
      "1": "float"
    }
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- P: set of products = {Refrigerator, Stove}

Parameters:
- profit_p: profit per unit of product p [USD per unit]
   - profit_Refrigerator = 400
   - profit_Stove = 260
- mover_time_p: mover time required per unit of product p [minutes per unit]
   - mover_time_Refrigerator = 60
   - mover_time_Stove = 45
- setup_time_p: setup time required per unit of product p [minutes per unit]
   - setup_time_Refrigerator = 20
   - setup_time_Stove = 25
- total_mover_time: total available mover time [minutes] = 20000
- total_setup_time: total available setup time [minutes] = 13000

Variables:
- x_p: number of units of product p to sell and install [integer, ≥ 0]
   - x_Refrigerator: number of refrigerators sold and installed
   - x_Stove: number of stoves sold and installed

Objective:
- Maximize total profit = profit_Refrigerator * x_Refrigerator + profit_Stove * x_Stove

Constraints:
- Mover time constraint: mover_time_Refrigerator * x_Refrigerator + mover_time_Stove * x_Stove ≤ total_mover_time
- Setup time constraint: setup_time_Refrigerator * x_Refrigerator + setup_time_Stove * x_Stove ≤ total_setup_time

Note:
- All time units are in minutes.
- Decision variables x_Refrigerator and x_Stove are assumed to be integer values because fractional appliances do not make sense in this context.'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp
from ortools.sat.python import cp_model

def solve_with_linear_solver():
    # Create solver instance using CBC backend (supports integer variables)
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Linear solver not available.")
        return None

    # Decision variables: x0 = number of refrigerators, x1 = number of stoves
    x0 = solver.IntVar(0, solver.infinity(), 'x_Refrigerator')
    x1 = solver.IntVar(0, solver.infinity(), 'x_Stove')

    # Parameters
    profit_r = 400
    profit_s = 260

    mover_time_r = 60
    mover_time_s = 45
    total_mover_time = 20000

    setup_time_r = 20
    setup_time_s = 25
    total_setup_time = 13000

    # Constraints:
    # Mover time: 60*x0 + 45*x1 <= 20000
    solver.Add(mover_time_r * x0 + mover_time_s * x1 <= total_mover_time)
    # Setup time: 20*x0 + 25*x1 <= 13000
    solver.Add(setup_time_r * x0 + setup_time_s * x1 <= total_setup_time)

    # Objective: maximize profit = 400*x0 + 260*x1
    objective = solver.Maximize(profit_r * x0 + profit_s * x1)

    status = solver.Solve()

    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result['variables'] = {
            "QuantityOfProduct": {
                "0": x0.solution_value(),
                "1": x1.solution_value()
            }
        }
        result['objective'] = solver.Objective().Value()
    else:
        result['error'] = "No optimal solution found in linear solver."
    return result

def solve_with_cp_model():
    model = cp_model.CpModel()

    # Decision variables: x0 = number of refrigerators, x1 = number of stoves
    # Since appliances are integers and realistic counts, use non-negative integers.
    x0 = model.NewIntVar(0, 100000, 'x_Refrigerator')  # Upper bound arbitrarily high.
    x1 = model.NewIntVar(0, 100000, 'x_Stove')

    # Parameters
    profit_r = 400
    profit_s = 260

    mover_time_r = 60
    mover_time_s = 45
    total_mover_time = 20000

    setup_time_r = 20
    setup_time_s = 25
    total_setup_time = 13000

    # Constraints:
    # Mover time: 60*x0 + 45*x1 <= 20000
    model.Add(mover_time_r * x0 + mover_time_s * x1 <= total_mover_time)
    # Setup time: 20*x0 + 25*x1 <= 13000
    model.Add(setup_time_r * x0 + setup_time_s * x1 <= total_setup_time)

    # Objective: maximize profit = 400*x0 + 260*x1
    model.Maximize(profit_r * x0 + profit_s * x1)

    # Create solver and solve
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    result = {}
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        result['variables'] = {
            "QuantityOfProduct": {
                "0": solver.Value(x0),
                "1": solver.Value(x1)
            }
        }
        result['objective'] = solver.ObjectiveValue()
    else:
        result['error'] = "No optimal solution found in CP model."
    return result

def main():
    print("----- Solution using ortools.linear_solver (CBC) -----")
    linear_result = solve_with_linear_solver()
    if 'error' in linear_result:
        print(linear_result['error'])
    else:
        print("Optimal decision variables:", linear_result['variables'])
        print("Optimal objective value:", linear_result['objective'])
    
    print("\n----- Solution using ortools.sat.python.cp_model -----")
    cp_result = solve_with_cp_model()
    if 'error' in cp_result:
        print(cp_result['error'])
    else:
        print("Optimal decision variables:", cp_result['variables'])
        print("Optimal objective value:", cp_result['objective'])

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
----- Solution using ortools.linear_solver (CBC) -----
Optimal decision variables: {'QuantityOfProduct': {'0': 333.0, '1': 0.0}}
Optimal objective value: 133200.0

----- Solution using ortools.sat.python.cp_model -----
Optimal decision variables: {'QuantityOfProduct': {'0': 333, '1': 0}}
Optimal objective value: 133200.0
'''

'''Expected Output:
Expected solution

: {'variables': {'QuantityOfProduct': {'0': 333.3333333333333, '1': 0.0}}, 'objective': 133333.3333333333}'''

