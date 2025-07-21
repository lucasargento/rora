# Problem Description:
'''Problem description: A soda company sends bottles of their soda to stores around the city in old and new vans. An old van can take 100 soda bottles while a new van can take 80 soda bottles. An old van produces 50 units of pollution while a new van only produces 30 units of pollution. The company needs to send at least 5000 bottles. In addition, at most 30 new vans can be used. How many of each van should be used to minimize the total amount of pollution produced?

Expected Output Schema:
{
  "variables": {
    "NumberOfOldVans": "float",
    "NumberOfNewVans": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- VANS: set of van types = {OldVan, NewVan}

Parameters:
- capacity_OldVan: number of soda bottles that an old van can carry [100 bottles per van]
- capacity_NewVan: number of soda bottles that a new van can carry [80 bottles per van]
- pollution_OldVan: pollution units produced per old van [50 units per van]
- pollution_NewVan: pollution units produced per new van [30 units per van]
- required_bottles: minimum number of soda bottles that must be delivered [5000 bottles]
- max_NewVans: maximum number of new vans available to use [30 vans]

Variables:
- NumberOfOldVans: number of old vans used (integer, nonnegative) [units: vans]
- NumberOfNewVans: number of new vans used (integer, nonnegative) [units: vans]

Objective:
- Minimize total pollution produced, expressed as:
  Total Pollution = (pollution_OldVan * NumberOfOldVans) + (pollution_NewVan * NumberOfNewVans)

Constraints:
1. Bottle delivery requirement:
   (capacity_OldVan * NumberOfOldVans) + (capacity_NewVan * NumberOfNewVans) ≥ required_bottles
2. New van availability constraint:
   NumberOfNewVans ≤ max_NewVans

--------------------------------------------------
Expected Output Schema:
{
  "variables": {
    "NumberOfOldVans": "float",
    "NumberOfNewVans": "float"
  },
  "objective": "float"
}'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_with_linear_solver():
    # Create a mixed integer linear programming solver using CBC.
    solver = pywraplp.Solver.CreateSolver('CBC_MIXED_INTEGER_PROGRAMMING')
    if not solver:
        print("Solver not created.")
        return None

    # Parameters
    capacity_OldVan = 100
    capacity_NewVan = 80
    pollution_OldVan = 50
    pollution_NewVan = 30
    required_bottles = 5000
    max_NewVans = 30

    # Variables: number of old vans and new vans (non-negative integers)
    NumberOfOldVans = solver.IntVar(0, solver.infinity(), 'NumberOfOldVans')
    NumberOfNewVans = solver.IntVar(0, max_NewVans, 'NumberOfNewVans')  # also upper bounded by max_NewVans

    # Constraint 1: Bottle delivery requirement
    # capacity_OldVan * NumberOfOldVans + capacity_NewVan * NumberOfNewVans >= required_bottles
    solver.Add(capacity_OldVan * NumberOfOldVans + capacity_NewVan * NumberOfNewVans >= required_bottles)

    # Constraint 2: New van availability constraint is inherently set by variable upper bound,
    # but we add it explicitly too.
    solver.Add(NumberOfNewVans <= max_NewVans)

    # Objective: Minimize total pollution
    # Total Pollution = pollution_OldVan * NumberOfOldVans + pollution_NewVan * NumberOfNewVans
    objective = solver.Objective()
    objective.SetCoefficient(NumberOfOldVans, pollution_OldVan)
    objective.SetCoefficient(NumberOfNewVans, pollution_NewVan)
    objective.SetMinimization()

    # Solve the model.
    status = solver.Solve()

    # Prepare result in the given output schema.
    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result["variables"] = {
            "NumberOfOldVans": NumberOfOldVans.solution_value(),
            "NumberOfNewVans": NumberOfNewVans.solution_value()
        }
        result["objective"] = objective.Value()
    else:
        result["message"] = "The problem does not have an optimal solution."

    return result

def main():
    # Currently, only one valid formulation exists, implemented with OR-Tools linear solver.
    result_linear = solve_with_linear_solver()

    # Print results in a structured manner.
    print("Results from Linear Solver Implementation:")
    if "message" in result_linear:
        print(result_linear["message"])
    else:
        print("Optimal Number of Old Vans:", result_linear["variables"]["NumberOfOldVans"])
        print("Optimal Number of New Vans:", result_linear["variables"]["NumberOfNewVans"])
        print("Minimum Total Pollution:", result_linear["objective"])

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Results from Linear Solver Implementation:
Optimal Number of Old Vans: 26.0
Optimal Number of New Vans: 30.0
Minimum Total Pollution: 2200.0
'''

'''Expected Output:
Expected solution

: {'variables': {'NumberOfOldVans': 26.0, 'NumberOfNewVans': 30.0}, 'objective': 2200.0}'''

