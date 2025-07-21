# Problem Description:
'''Problem description: A new fast food place makes wraps and platters. Each wrap requires 5 units of meat and 3 units of rice. Each platter requires 7 units of meant and 5 units of rice. While each wrap takes 10 minutes to make, each platter takes 8 minutes to make. The fast food place must use at least 3000 units of meat and 2500 units of rice. Since wraps are easier to eat on the go, at least 3 times as many wraps need to be made as platter. How many of each should the fast food place make to minimize the total production time?

Expected Output Schema:
{
  "variables": {
    "NumberOfWraps": "float",
    "NumberOfPlatters": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- Items: the set of food items produced = {Wrap, Platter}

Parameters:
- meat_per_wrap: units of meat required to make one Wrap = 5 (units)
- meat_per_platter: units of meat required to make one Platter = 7 (units)
- rice_per_wrap: units of rice required to make one Wrap = 3 (units)
- rice_per_platter: units of rice required to make one Platter = 5 (units)
- time_per_wrap: production time to make one Wrap = 10 (minutes)
- time_per_platter: production time to make one Platter = 8 (minutes)
- min_meat_usage: minimum required total meat consumption = 3000 (units)
- min_rice_usage: minimum required total rice consumption = 2500 (units)
- wrap_ratio: minimum ratio of Wraps to Platters, meaning Wraps must be at least 3 times the number of Platters

Variables:
- NumberOfWraps: number of Wraps to produce [continuous or integer, ≥ 0] [units]
- NumberOfPlatters: number of Platters to produce [continuous or integer, ≥ 0] [units]

Objective:
Minimize total production time (in minutes) = (time_per_wrap * NumberOfWraps) + (time_per_platter * NumberOfPlatters)

Constraints:
1. Meat usage constraint:
   (meat_per_wrap * NumberOfWraps) + (meat_per_platter * NumberOfPlatters) ≥ min_meat_usage
   i.e., 5 * NumberOfWraps + 7 * NumberOfPlatters ≥ 3000

2. Rice usage constraint:
   (rice_per_wrap * NumberOfWraps) + (rice_per_platter * NumberOfPlatters) ≥ min_rice_usage
   i.e., 3 * NumberOfWraps + 5 * NumberOfPlatters ≥ 2500

3. Wrap-to-Platter ratio constraint:
   NumberOfWraps ≥ wrap_ratio * NumberOfPlatters
   i.e., NumberOfWraps ≥ 3 * NumberOfPlatters

---

Note: All units (meat units, rice units, minutes) are assumed to be consistent as given in the problem description.'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_continuous():
    # Create the linear solver with the GLOP backend for continuous variables.
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Continuous solver not created.")
        return None

    # Variables: continuous variables >= 0.
    NumberOfWraps = solver.NumVar(0.0, solver.infinity(), 'NumberOfWraps')
    NumberOfPlatters = solver.NumVar(0.0, solver.infinity(), 'NumberOfPlatters')

    # Parameters.
    meat_per_wrap = 5.0
    meat_per_platter = 7.0
    rice_per_wrap = 3.0
    rice_per_platter = 5.0
    time_per_wrap = 10.0
    time_per_platter = 8.0
    min_meat_usage = 3000.0
    min_rice_usage = 2500.0
    wrap_ratio = 3.0

    # Constraints.
    # 1. Meat constraint: 5 * NumberOfWraps + 7 * NumberOfPlatters >= 3000
    solver.Add(meat_per_wrap * NumberOfWraps + meat_per_platter * NumberOfPlatters >= min_meat_usage)
    # 2. Rice constraint: 3 * NumberOfWraps + 5 * NumberOfPlatters >= 2500
    solver.Add(rice_per_wrap * NumberOfWraps + rice_per_platter * NumberOfPlatters >= min_rice_usage)
    # 3. Wrap-to-Platter ratio constraint: NumberOfWraps >= 3 * NumberOfPlatters
    solver.Add(NumberOfWraps >= wrap_ratio * NumberOfPlatters)

    # Objective: minimize total production time.
    solver.Minimize(time_per_wrap * NumberOfWraps + time_per_platter * NumberOfPlatters)

    status = solver.Solve()

    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result['NumberOfWraps'] = NumberOfWraps.solution_value()
        result['NumberOfPlatters'] = NumberOfPlatters.solution_value()
        result['objective'] = solver.Objective().Value()
    else:
        result['error'] = "No optimal solution found in continuous formulation."
    return result

def solve_integer():
    # Create the MIP solver with SCIP backend for integer variables.
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        print("Integer solver not created.")
        return None

    # Variables: integer variables >= 0.
    NumberOfWraps = solver.IntVar(0, solver.infinity(), 'NumberOfWraps')
    NumberOfPlatters = solver.IntVar(0, solver.infinity(), 'NumberOfPlatters')

    # Parameters.
    meat_per_wrap = 5
    meat_per_platter = 7
    rice_per_wrap = 3
    rice_per_platter = 5
    time_per_wrap = 10
    time_per_platter = 8
    min_meat_usage = 3000
    min_rice_usage = 2500
    wrap_ratio = 3

    # Constraints.
    # 1. Meat usage: 5 * NumberOfWraps + 7 * NumberOfPlatters >= 3000
    solver.Add(meat_per_wrap * NumberOfWraps + meat_per_platter * NumberOfPlatters >= min_meat_usage)
    # 2. Rice usage: 3 * NumberOfWraps + 5 * NumberOfPlatters >= 2500
    solver.Add(rice_per_wrap * NumberOfWraps + rice_per_platter * NumberOfPlatters >= min_rice_usage)
    # 3. Wrap-to-Platter ratio constraint: NumberOfWraps >= 3 * NumberOfPlatters
    solver.Add(NumberOfWraps >= wrap_ratio * NumberOfPlatters)

    # Objective: minimize total production time.
    solver.Minimize(time_per_wrap * NumberOfWraps + time_per_platter * NumberOfPlatters)

    status = solver.Solve()

    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result['NumberOfWraps'] = NumberOfWraps.solution_value()
        result['NumberOfPlatters'] = NumberOfPlatters.solution_value()
        result['objective'] = solver.Objective().Value()
    else:
        result['error'] = "No optimal solution found in integer formulation."
    return result

def main():
    continuous_result = solve_continuous()
    integer_result = solve_integer()

    results = {
        "Continuous Model": continuous_result,
        "Integer Model": integer_result
    }

    print(results)

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
{'Continuous Model': {'NumberOfWraps': 535.7142857142856, 'NumberOfPlatters': 178.57142857142853, 'objective': 6785.7142857142835}, 'Integer Model': {'NumberOfWraps': 537.0, 'NumberOfPlatters': 178.0, 'objective': 6794.0}}
'''

'''Expected Output:
Expected solution

: {'variables': {'NumberOfWraps': 535.7142857142857, 'NumberOfPlatters': 178.57142857142856}, 'objective': 6785.714285714285}'''

