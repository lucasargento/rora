# Problem Description:
'''Problem description: A vine company sells vine in vintage and regular bottles. A vintage bottle can hold 500 ml of vine while a regular bottle can hold 750 ml of vine. The company has available 100000 ml of vine. Because vintage bottles are mostly bought by collectors, the number of regular bottles must be at least 4 times as much as the number of vintage bottles. However, at least 10 vintage bottles must be made. How many of each should be made to maximize the total number of bottles produced?

Expected Output Schema:
{
  "variables": {
    "NumberVintageBottles": "float",
    "NumberRegularBottles": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- BottleTypes: set of bottle types = {Vintage, Regular}

Parameters:
- capacity_Vintage: vine capacity per vintage bottle (ml) = 500
- capacity_Regular: vine capacity per regular bottle (ml) = 750
- vineAvailable: total available vine (ml) = 100000
- minVintage: minimum number of vintage bottles = 10
- regularMultiplier: minimum ratio of regular to vintage bottles = 4
  (This means the number of Regular bottles must be at least 4 times the number of Vintage bottles.)

Variables:
- NumberVintageBottles: number of vintage bottles produced [float, ≥ 0]
- NumberRegularBottles: number of regular bottles produced [float, ≥ 0]

Objective:
- Maximize total bottles produced = NumberVintageBottles + NumberRegularBottles

Constraints:
1. Vine capacity constraint:
   500 * NumberVintageBottles + 750 * NumberRegularBottles ≤ vineAvailable
   (Ensure the total vine used does not exceed 100000 ml.)
2. Market ratio constraint:
   NumberRegularBottles ≥ regularMultiplier * NumberVintageBottles
   (At least 4 regular bottles are made for every vintage bottle.)
3. Minimum vintage production:
   NumberVintageBottles ≥ minVintage
   (At least 10 vintage bottles must be produced.)

-----------------------------------------------------------
Expected Output Schema:
{
  "variables": {
    "NumberVintageBottles": "float",
    "NumberRegularBottles": "float"
  },
  "objective": "float"
}'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp
from ortools.sat.python import cp_model

def solve_using_linear_solver():
    # Create the linear solver with the GLOP backend.
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        return None, "Linear solver not available."

    # Parameters
    capacity_vintage = 500
    capacity_regular = 750
    vine_available = 100000
    min_vintage = 10
    regular_multiplier = 4

    # Variables (continuous as per formulation)
    NumberVintageBottles = solver.NumVar(0.0, solver.infinity(), 'NumberVintageBottles')
    NumberRegularBottles = solver.NumVar(0.0, solver.infinity(), 'NumberRegularBottles')

    # Constraints:
    # 1. Vine capacity constraint:
    solver.Add(capacity_vintage * NumberVintageBottles + capacity_regular * NumberRegularBottles <= vine_available)
    # 2. Market ratio constraint: Regular bottles >= 4 * Vintage bottles
    solver.Add(NumberRegularBottles >= regular_multiplier * NumberVintageBottles)
    # 3. Minimum vintage production:
    solver.Add(NumberVintageBottles >= min_vintage)

    # Objective: maximize total bottles produced.
    objective = solver.Objective()
    objective.SetCoefficient(NumberVintageBottles, 1)
    objective.SetCoefficient(NumberRegularBottles, 1)
    objective.SetMaximization()

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "NumberVintageBottles": NumberVintageBottles.solution_value(),
            "NumberRegularBottles": NumberRegularBottles.solution_value()
        }
        objective_value = objective.Value()
        return (result, objective_value)
    else:
        return (None, "No optimal solution found (Linear Solver).")

def solve_using_cp_model():
    # Create the CP-SAT model.
    model = cp_model.CpModel()

    # Parameters (using same values).
    capacity_vintage = 500
    capacity_regular = 750
    vine_available = 100000
    min_vintage = 10
    regular_multiplier = 4

    # For cp_model we need integer variables. We set reasonable bounds.
    # Upper bound decisions: maximum vintage bottles if only vintage used.
    max_vintage = vine_available // capacity_vintage  # 200
    # Maximum regular bottles if only regular used.
    max_regular = vine_available // capacity_regular  # 133

    # Variables (integer)
    NumberVintageBottles = model.NewIntVar(min_vintage, max_vintage, 'NumberVintageBottles')
    NumberRegularBottles = model.NewIntVar(0, max_regular, 'NumberRegularBottles')

    # Constraints:
    # 1. Vine capacity constraint:
    model.Add(capacity_vintage * NumberVintageBottles + capacity_regular * NumberRegularBottles <= vine_available)
    # 2. Market ratio constraint:
    model.Add(NumberRegularBottles >= regular_multiplier * NumberVintageBottles)
    # (Minimum vintage production constraint is already set by variable domain)

    # Objective: maximize total bottles produced.
    total_bottles = model.NewIntVar(0, max_vintage + max_regular, 'total_bottles')
    model.Add(total_bottles == NumberVintageBottles + NumberRegularBottles)
    model.Maximize(total_bottles)

    # Solve the model.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    if status in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
        result = {
            "NumberVintageBottles": solver.Value(NumberVintageBottles),
            "NumberRegularBottles": solver.Value(NumberRegularBottles)
        }
        objective_value = solver.Value(total_bottles)
        return (result, objective_value)
    else:
        return (None, "No optimal solution found (CP-SAT Model).")

def main():
    print("Results using OR-Tools Linear Solver:")
    linear_result, linear_objective = solve_using_linear_solver()
    if linear_result is not None:
        print({
            "variables": linear_result,
            "objective": linear_objective
        })
    else:
        print(linear_objective)

    print("\nResults using OR-Tools CP-SAT Model:")
    cp_result, cp_objective = solve_using_cp_model()
    if cp_result is not None:
        print({
            "variables": cp_result,
            "objective": cp_objective
        })
    else:
        print(cp_objective)

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Results using OR-Tools Linear Solver:
{'variables': {'NumberVintageBottles': 28.571428571428573, 'NumberRegularBottles': 114.28571428571429}, 'objective': 142.85714285714286}

Results using OR-Tools CP-SAT Model:
{'variables': {'NumberVintageBottles': 28, 'NumberRegularBottles': 114}, 'objective': 142}
'''

'''Expected Output:
Expected solution

: {'variables': {'NumberVintageBottles': 28.0, 'NumberRegularBottles': 114.0}, 'objective': 142.0}'''

