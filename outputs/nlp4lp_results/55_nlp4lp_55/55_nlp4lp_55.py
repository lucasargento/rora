# Problem Description:
'''Problem description: A laundromat can buy two types of washing machines, a top-loading model and a front-loading model. The top-loading model can wash 50 items per day while the front-loading model can wash 75 items per day. The top-loading model consumes 85 kWh per day while the front-loading model consumes 100 kWh per day. The laundromat must be able to wash at least 5000 items per day and has available 7000 kWh per day. Since the top-loading machine are harder to use, at most 40% of the machines can be top-loading. Further, at least 10 machines should be front-loading. How many of each machine should the laundromat buy to minimize the total number of washing machines?

Expected Output Schema:
{
  "variables": {
    "NumTopLoading": "float",
    "NumFrontLoading": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- M: set of washing machine types = {TopLoading, FrontLoading}

Parameters:
- WashItems_T: number of items washed per day by a top-loading machine = 50 [items/day]
- WashItems_F: number of items washed per day by a front-loading machine = 75 [items/day]
- Power_T: power consumption per day of a top-loading machine = 85 [kWh/day]
- Power_F: power consumption per day of a front-loading machine = 100 [kWh/day]
- MinItems: minimum items to wash per day = 5000 [items]
- AvailablePower: available power per day = 7000 [kWh]
- MaxTopFraction: maximum fraction of machines that may be top-loading = 0.40 [fraction]
- MinFront: minimum number of front-loading machines required = 10 [machines]

Variables:
- NumTopLoading: number of top-loading machines to buy [integer ≥ 0]
- NumFrontLoading: number of front-loading machines to buy [integer ≥ 0]

Objective:
- Minimize TotalMachines = NumTopLoading + NumFrontLoading

Constraints:
1. Washing capacity constraint:
   (WashItems_T * NumTopLoading) + (WashItems_F * NumFrontLoading) ≥ MinItems

2. Power consumption constraint:
   (Power_T * NumTopLoading) + (Power_F * NumFrontLoading) ≤ AvailablePower

3. Top-loading machine fraction constraint:
   NumTopLoading ≤ MaxTopFraction * (NumTopLoading + NumFrontLoading)

4. Minimum front-loading machines constraint:
   NumFrontLoading ≥ MinFront

Comments:
- All machines are counted as whole units.
- The model assumes that daily performance attributes (items washed, kWh used per day) are additive across machines.
- The top-loading fraction constraint ensures that no more than 40% of the total machines are top-loading, which addresses usability concerns.
- The objective is to minimize the total number of machines purchased while satisfying operational constraints.

This structured model provides a clear formulation that can be directly translated into Python or an optimization solver using OR-Tools.'''

# Generated Code:
#!/usr/bin/env python3
"""
This script implements the laundromat washing machines optimization problem using two separate formulations:
1. A linear/integer programming model using ortools.linear_solver.
2. A CP-SAT model using ortools.sat.python.cp_model.
Each model is implemented separately and their results are printed in a structured way.
"""

from ortools.linear_solver import pywraplp
from ortools.sat.python import cp_model

def solve_with_linear_solver():
    # Create solver (using CBC as MILP solver)
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("CBC solver unavailable.")
        return None

    # Parameters
    WashItems_T = 50
    WashItems_F = 75
    Power_T = 85
    Power_F = 100
    MinItems = 5000
    AvailablePower = 7000
    # For the top-loading fraction constraint, we'll derive an equivalent inequality: 
    # original constraint: x <= 0.40*(x+y)
    # => x - 0.40x <= 0.40 y
    # => 0.60x <= 0.40 y
    # Multiply both sides by 5: 3 x <= 2 y.
    # Thus constraint: 3*x - 2*y <= 0.
    MinFront = 10

    # Decision Variables
    # NumTopLoading (x) and NumFrontLoading (y)
    x = solver.IntVar(0, solver.infinity(), 'NumTopLoading')
    y = solver.IntVar(0, solver.infinity(), 'NumFrontLoading')

    # Constraints
    # Washing capacity constraint: 50*x + 75*y >= 5000
    solver.Add(WashItems_T * x + WashItems_F * y >= MinItems)

    # Power consumption constraint: 85*x + 100*y <= 7000
    solver.Add(Power_T * x + Power_F * y <= AvailablePower)

    # Top-loading fraction constraint: 3*x - 2*y <= 0   <=>   x <= 2/3 y
    solver.Add(3 * x - 2 * y <= 0)

    # Minimum front-loading machines
    solver.Add(y >= MinFront)

    # Objective: minimize total machines
    objective = solver.Objective()
    objective.SetCoefficient(x, 1)
    objective.SetCoefficient(y, 1)
    objective.SetMinimization()

    # Solve model
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "NumTopLoading": x.solution_value(),
            "NumFrontLoading": y.solution_value(),
            "objective": objective.Value()
        }
        return result
    else:
        return "No optimal solution found with linear_solver."

def solve_with_cp_model():
    model = cp_model.CpModel()

    # Parameters
    WashItems_T = 50
    WashItems_F = 75
    Power_T = 85
    Power_F = 100
    MinItems = 5000
    AvailablePower = 7000
    MinFront = 10
    # For the fraction constraint: 3*x - 2*y <= 0
    # We'll use that inequality in the CP model as well.

    # We need to choose an upper bound for decision variables; 
    # we choose a safe large bound that covers potential solutions.
    max_machines = 200  # arbitrary upper bound for each variable

    # Decision Variables
    x = model.NewIntVar(0, max_machines, 'NumTopLoading')
    y = model.NewIntVar(0, max_machines, 'NumFrontLoading')

    # Constraints
    # Washing capacity: 50*x + 75*y >= 5000
    model.Add(WashItems_T * x + WashItems_F * y >= MinItems)

    # Power consumption: 85*x + 100*y <= 7000
    model.Add(Power_T * x + Power_F * y <= AvailablePower)

    # Top-loading fraction: 3*x - 2*y <= 0
    model.Add(3 * x - 2 * y <= 0)

    # Minimum front-loading machines: y >= 10
    model.Add(y >= MinFront)

    # Objective: minimize total machines x + y
    total_machines = model.NewIntVar(0, 2 * max_machines, 'TotalMachines')
    model.Add(total_machines == x + y)
    model.Minimize(total_machines)

    # Solve model
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        result = {
            "NumTopLoading": solver.Value(x),
            "NumFrontLoading": solver.Value(y),
            "objective": solver.Value(total_machines)
        }
        return result
    else:
        return "No optimal solution found with cp_model."

def main():
    # Solve with linear_solver
    linear_result = solve_with_linear_solver()

    # Solve with CP-SAT model
    cp_result = solve_with_cp_model()

    # Print structured results:
    print("Results from ortools.linear_solver:")
    if isinstance(linear_result, dict):
        print({
            "variables": {
                "NumTopLoading": linear_result["NumTopLoading"],
                "NumFrontLoading": linear_result["NumFrontLoading"]
            },
            "objective": linear_result["objective"]
        })
    else:
        print(linear_result)

    print("\nResults from ortools.sat.python.cp_model:")
    if isinstance(cp_result, dict):
        print({
            "variables": {
                "NumTopLoading": cp_result["NumTopLoading"],
                "NumFrontLoading": cp_result["NumFrontLoading"]
            },
            "objective": cp_result["objective"]
        })
    else:
        print(cp_result)

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Results from ortools.linear_solver:
{'variables': {'NumTopLoading': 0.0, 'NumFrontLoading': 67.0}, 'objective': 67.0}

Results from ortools.sat.python.cp_model:
{'variables': {'NumTopLoading': 0, 'NumFrontLoading': 67}, 'objective': 67}
'''

'''Expected Output:
Expected solution

: {'variables': {'NumTopLoading': -0.0, 'NumFrontLoading': 67.0}, 'objective': 67.0}'''

