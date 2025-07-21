# Problem Description:
'''Problem description: There is 1000 mg of gold available that is needed to make long and short cables. Long cables require 10 mg of gold while short cables require 7 mg of gold. Because of their compact size, at least 5 times the number of short cables are needed than the long cables. In addition, there needs to be at least 10 long cables made. If each long cable sold results in a $12 profit and each short cable sold results in a $5 profit, how many of each type of cable should be made to maximize profit?

Expected Output Schema:
{
  "variables": {
    "NumberLongCables": "float",
    "NumberShortCables": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- Cables: {Long, Short}

Parameters:
- TotalGold (mg): 1000            // Total available gold in milligrams.
- GoldPerLong (mg): 10            // Gold required per long cable.
- GoldPerShort (mg): 7            // Gold required per short cable.
- ProfitLong (USD): 12            // Profit per long cable produced.
- ProfitShort (USD): 5            // Profit per short cable produced.
- MinLongCables (units): 10       // Minimum required number of long cables.
- ShortToLongRatio: 5             // At least 5 short cables per each long cable.

Variables:
- NumberLongCables: integer, ≥ 0  // Number of long cables produced.
- NumberShortCables: integer, ≥ 0 // Number of short cables produced.

Objective:
- Maximize TotalProfit defined as:
  TotalProfit = ProfitLong * NumberLongCables + ProfitShort * NumberShortCables
  // That is, maximize (12 * NumberLongCables + 5 * NumberShortCables).

Constraints:
1. Gold Constraint:
   GoldPerLong * NumberLongCables + GoldPerShort * NumberShortCables ≤ TotalGold
   => 10 * NumberLongCables + 7 * NumberShortCables ≤ 1000

2. Minimum Long Cables Constraint:
   NumberLongCables ≥ MinLongCables
   => NumberLongCables ≥ 10

3. Short-to-Long Ratio Constraint:
   NumberShortCables ≥ ShortToLongRatio * NumberLongCables
   => NumberShortCables ≥ 5 * NumberLongCables

Comments:
- All quantities are assumed to be integers since the cables can only be produced in whole units.
- The units for gold are in milligrams (mg) and profits are in US dollars (USD).
- This model is self-contained, using a simple linear formulation suitable for implementation in Python or OR-Tools.'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp
from ortools.sat.python import cp_model

def solve_with_linear_solver():
    # Create the mip solver with the CBC backend.
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Linear solver not available.")
        return None

    # Define variables.
    # Variables are non-negative integers.
    # Upper bounds are set based on resource limits.
    NumberLongCables = solver.IntVar(0, 1000 // 10, "NumberLongCables")
    NumberShortCables = solver.IntVar(0, 1000 // 7, "NumberShortCables")

    # Add constraints.
    # 1. Gold constraint: 10 * NumberLongCables + 7 * NumberShortCables <= 1000
    solver.Add(10 * NumberLongCables + 7 * NumberShortCables <= 1000)
    # 2. Minimum long cables: NumberLongCables >= 10
    solver.Add(NumberLongCables >= 10)
    # 3. Short-to-long ratio: NumberShortCables >= 5 * NumberLongCables
    solver.Add(NumberShortCables >= 5 * NumberLongCables)

    # Objective: maximize profit = 12*NumberLongCables + 5*NumberShortCables
    objective = solver.Objective()
    objective.SetCoefficient(NumberLongCables, 12)
    objective.SetCoefficient(NumberShortCables, 5)
    objective.SetMaximization()

    status = solver.Solve()
    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "variables": {
                "NumberLongCables": NumberLongCables.solution_value(),
                "NumberShortCables": NumberShortCables.solution_value()
            },
            "objective": objective.Value()
        }
    else:
        print("No optimal solution found with linear solver!")
        result = None

    return result

def solve_with_cp_sat():
    model = cp_model.CpModel()

    # Define variables.
    # We set an upper bound for NumberLongCables and NumberShortCables
    max_long = 1000 // 10  # Max long cables if all gold used solely for long cables.
    max_short = 1000 // 7  # Max short cables if all gold used solely for short cables.
    NumberLongCables = model.NewIntVar(0, max_long, "NumberLongCables")
    NumberShortCables = model.NewIntVar(0, max_short, "NumberShortCables")

    # Add constraints.
    # Gold constraint: 10 * NumberLongCables + 7 * NumberShortCables <= 1000
    model.Add(10 * NumberLongCables + 7 * NumberShortCables <= 1000)
    # Minimum long cables: NumberLongCables >= 10
    model.Add(NumberLongCables >= 10)
    # Short-to-long ratio: NumberShortCables >= 5 * NumberLongCables
    model.Add(NumberShortCables >= 5 * NumberLongCables)

    # Define objective: maximize 12 * NumberLongCables + 5 * NumberShortCables
    objective_var = model.NewIntVar(0, 10000, "objective")
    model.Add(objective_var == 12 * NumberLongCables + 5 * NumberShortCables)
    model.Maximize(objective_var)

    # Solve the model.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    result = {}

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        result = {
            "variables": {
                "NumberLongCables": solver.Value(NumberLongCables),
                "NumberShortCables": solver.Value(NumberShortCables)
            },
            "objective": solver.Value(objective_var)
        }
    else:
        print("No optimal solution found with CP-SAT!")
        result = None

    return result

def main():
    print("Solving using OR-Tools Linear Solver (MIP)...")
    linear_result = solve_with_linear_solver()
    if linear_result:
        print("Linear Solver Result:")
        print(linear_result)
    else:
        print("Linear Solver did not find an optimal solution.")

    print("\nSolving using OR-Tools CP-SAT Solver...")
    cp_sat_result = solve_with_cp_sat()
    if cp_sat_result:
        print("CP-SAT Solver Result:")
        print(cp_sat_result)
    else:
        print("CP-SAT Solver did not find an optimal solution.")

if __name__ == "__main__":
    main()

'''Execution Results:
SUCCESS:
Solving using OR-Tools Linear Solver (MIP)...
Linear Solver Result:
{'variables': {'NumberLongCables': 22.0, 'NumberShortCables': 111.0}, 'objective': 819.0}

Solving using OR-Tools CP-SAT Solver...
CP-SAT Solver Result:
{'variables': {'NumberLongCables': 22, 'NumberShortCables': 111}, 'objective': 819}
'''

'''Expected Output:
Expected solution

: {'variables': {'NumberLongCables': 22.0, 'NumberShortCables': 111.0}, 'objective': 819.0}'''

