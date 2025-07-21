# Problem Description:
'''Problem description: An aquarium does shows using otters and dolphins. An otter will do 3 tricks at a time and requires 3 treats to do so. A dolphin will do 1 trick at a time and requires 5 treats to do so. Since dolphins are more popular, at least 10 dolphins must be used and at most 30% of the performers can be otters. If the aquarium only has 200 treats available, maximize the total number of tricks that can be preformed.

Expected Output Schema:
{
  "variables": {
    "NumberOfDolphins": "float",
    "NumberOfOtters": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- S: set of performer types = {Otter, Dolphin}

Parameters:
- tricks_per_otter = 3       [tricks per performance]
- treats_per_otter = 3       [total treats per otter performance]
- tricks_per_dolphin = 1      [tricks per performance]
- treats_per_dolphin = 5      [total treats per dolphin performance]
- min_dolphins = 10         [minimum number of dolphins required]
- treats_available = 200     [total available treats]
- max_otter_fraction = 0.30     [maximum fraction of performers that can be otters]

Variables:
- NumberOfOtters: number of otters to include in the show [continuous, nonnegative, ideally integer]
- NumberOfDolphins: number of dolphins to include in the show [continuous, nonnegative, ideally integer]

Objective:
- Maximize total_tricks = tricks_per_otter * NumberOfOtters + tricks_per_dolphin * NumberOfDolphins

Constraints:
1. Treats constraint: treats_per_otter * NumberOfOtters + treats_per_dolphin * NumberOfDolphins ≤ treats_available
2. Minimum dolphins constraint: NumberOfDolphins ≥ min_dolphins
3. Otter fraction constraint: NumberOfOtters ≤ max_otter_fraction * (NumberOfOtters + NumberOfDolphins)

Note:
- All treat and trick units are consistent with the problem statement.
- Although the variables are naturally integer values, they are modeled as continuous in this formulation. In an implementation, integrality restrictions might be added if needed.

Expected Output Schema:
{
  "variables": {
    "NumberOfDolphins": "float",
    "NumberOfOtters": "float"
  },
  "objective": "float"
}'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_continuous():
    # Create the linear solver with the CBC backend.
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Continuous solver not created.")
        return None

    # Variables: continuous nonnegative variables
    NumberOfOtters = solver.NumVar(0.0, solver.infinity(), 'NumberOfOtters')
    NumberOfDolphins = solver.NumVar(0.0, solver.infinity(), 'NumberOfDolphins')

    # Parameters
    tricks_per_otter = 3
    treats_per_otter = 3
    tricks_per_dolphin = 1
    treats_per_dolphin = 5
    min_dolphins = 10
    treats_available = 200
    max_otter_fraction = 0.30

    # Objective: Maximize total tricks
    # total_tricks = 3 * NumberOfOtters + 1 * NumberOfDolphins
    objective = solver.Objective()
    objective.SetCoefficient(NumberOfOtters, tricks_per_otter)
    objective.SetCoefficient(NumberOfDolphins, tricks_per_dolphin)
    objective.SetMaximization()

    # Constraints
    # 1. Treats constraint: 3 * NumberOfOtters + 5 * NumberOfDolphins <= 200
    solver.Add(treats_per_otter * NumberOfOtters + treats_per_dolphin * NumberOfDolphins <= treats_available)

    # 2. Minimum dolphins constraint: NumberOfDolphins >= 10
    solver.Add(NumberOfDolphins >= min_dolphins)

    # 3. Otter fraction constraint: NumberOfOtters <= 0.30 * (NumberOfOtters + NumberOfDolphins)
    # Rearrangement: NumberOfOtters <= 0.30*NumberOfOtters + 0.30*NumberOfDolphins
    # ==> 0.70 * NumberOfOtters <= 0.30 * NumberOfDolphins
    # ==> NumberOfOtters <= (0.30/0.70) * NumberOfDolphins = (3/7)*NumberOfDolphins
    solver.Add(NumberOfOtters <= (3/7) * NumberOfDolphins)

    status = solver.Solve()
    results = {}
    if status == pywraplp.Solver.OPTIMAL:
        results = {
            "NumberOfOtters": NumberOfOtters.solution_value(),
            "NumberOfDolphins": NumberOfDolphins.solution_value(),
            "objective": objective.Value()
        }
    else:
        results = {"error": "No optimal solution found (continuous model)."}
    return results

def solve_integer():
    # Create the linear solver with CBC MIP backend.
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Integer solver not created.")
        return None

    # Variables: integer nonnegative variables (ideally integers)
    NumberOfOtters = solver.IntVar(0, solver.infinity(), 'NumberOfOtters')
    NumberOfDolphins = solver.IntVar(0, solver.infinity(), 'NumberOfDolphins')

    # Parameters
    tricks_per_otter = 3
    treats_per_otter = 3
    tricks_per_dolphin = 1
    treats_per_dolphin = 5
    min_dolphins = 10
    treats_available = 200
    max_otter_fraction = 0.30

    # Objective: Maximize total tricks
    objective = solver.Objective()
    objective.SetCoefficient(NumberOfOtters, tricks_per_otter)
    objective.SetCoefficient(NumberOfDolphins, tricks_per_dolphin)
    objective.SetMaximization()

    # Constraints
    # 1. Treats constraint: 3 * NumberOfOtters + 5 * NumberOfDolphins <= 200
    solver.Add(treats_per_otter * NumberOfOtters + treats_per_dolphin * NumberOfDolphins <= treats_available)

    # 2. Minimum dolphins constraint: NumberOfDolphins >= 10
    solver.Add(NumberOfDolphins >= min_dolphins)

    # 3. Otter fraction constraint:
    # Enforcing: NumberOfOtters <= 0.30*(NumberOfOtters + NumberOfDolphins)
    # which is equivalent to NumberOfOtters <= (3/7)*NumberOfDolphins.
    # Use this linear reformulation in the integer model.
    solver.Add(NumberOfOtters <= (3/7) * NumberOfDolphins)

    status = solver.Solve()
    results = {}
    if status == pywraplp.Solver.OPTIMAL:
        results = {
            "NumberOfOtters": NumberOfOtters.solution_value(),
            "NumberOfDolphins": NumberOfDolphins.solution_value(),
            "objective": objective.Value()
        }
    else:
        results = {"error": "No optimal solution found (integer model)."}
    return results

def main():
    print("Solving Continuous Model:")
    continuous_results = solve_continuous()
    if continuous_results is not None:
        print(continuous_results)
    else:
        print("Continuous model did not return results.")

    print("\nSolving Integer Model:")
    integer_results = solve_integer()
    if integer_results is not None:
        print(integer_results)
    else:
        print("Integer model did not return results.")

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Solving Continuous Model:
{'NumberOfOtters': 13.636363636363638, 'NumberOfDolphins': 31.81818181818182, 'objective': 72.72727272727273}

Solving Integer Model:
{'NumberOfOtters': 13.0, 'NumberOfDolphins': 32.0, 'objective': 71.0}
'''

'''Expected Output:
Expected solution

: {'variables': {'NumberOfDolphins': 32.0, 'NumberOfOtters': 13.0}, 'objective': 71.0}'''

