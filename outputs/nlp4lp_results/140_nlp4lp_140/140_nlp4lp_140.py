# Problem Description:
'''Problem description: A sand company delivers sand for playgrounds in small and large containers. A small container requires 1 person to unload and can hold 20 units of sand. A large container requires 3 people to unload and can hold 50 units of sand. Since most playgrounds are small, the number of small containers used must be thrice the number of large containers used. In addition, there must be at least 5 small containers and 3 large containers used. If the company has 100 people available, maximize the amount of sand that they can deliver.

Expected Output Schema:
{
  "variables": {
    "SmallContainers": "float",
    "LargeContainers": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- C: set of container types = {Small, Large}

Parameters:
- unload_req_Small: persons required to unload one small container = 1 (person/container)
- unload_req_Large: persons required to unload one large container = 3 (persons/container)
- capacity_Small: sand capacity of one small container = 20 (units/container)
- capacity_Large: sand capacity of one large container = 50 (units/container)
- available_persons: total number of available people = 100 (persons)
- min_Small: minimum number of small containers to use = 5 (containers)
- min_Large: minimum number of large containers to use = 3 (containers)
- ratio_Small_to_Large: required ratio of small to large containers = 3 (i.e., SmallContainers must equal 3 * LargeContainers)

Variables:
- SmallContainers: number of small containers used (continuous or integer; if containers must be whole, then integer) [units: containers]
- LargeContainers: number of large containers used (continuous or integer; if containers must be whole, then integer) [units: containers]

Objective:
- Maximize total sand delivered, defined as 
  TotalSand = capacity_Small * SmallContainers + capacity_Large * LargeContainers 
  (units: sand units)

Constraints:
1. Personnel constraint: 
   unload_req_Small * SmallContainers + unload_req_Large * LargeContainers <= available_persons
   (i.e., 1 * SmallContainers + 3 * LargeContainers <= 100)

2. Ratio constraint for container usage:
   SmallContainers = ratio_Small_to_Large * LargeContainers
   (i.e., SmallContainers = 3 * LargeContainers)

3. Minimum containers constraints:
   - SmallContainers >= min_Small 
   - LargeContainers >= min_Large

Comments:
- It is assumed that containers are indivisible; hence, the decision variables can be modeled as integers in an actual implementation.
- This formulation uses consistent units: persons for unloading constraints and container capacity in sand units.
- The objective is to maximize the total delivered sand given the available unloading capacity and container requirements.'''

# Generated Code:
#!/usr/bin/env python3
"""
This script implements the optimization problem in two separate ways:
1. Using the OR-Tools Linear Solver module (MIP formulation).
2. Using the OR-Tools CP-SAT module (CP formulation).

Both models maximize the total delivered sand subject to the constraints:
- 1*SmallContainers + 3*LargeContainers <= 100 (personnel constraint)
- SmallContainers == 3 * LargeContainers (ratio constraint)
- SmallContainers >= 5 and LargeContainers >= 3 (minimum container constraints)
"""

from ortools.linear_solver import pywraplp
from ortools.sat.python import cp_model

def solve_linear():
    # Create the mip solver with the CBC backend.
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Linear solver not available.")
        return None

    # PARAMETERS
    unload_req_small = 1
    unload_req_large = 3
    capacity_small = 20
    capacity_large = 50
    available_persons = 100
    min_small = 5
    min_large = 3
    ratio_small_to_large = 3

    # VARIABLES: Since containers are considered indivisible, use integers.
    small = solver.IntVar(min_small, solver.infinity(), 'SmallContainers')
    large = solver.IntVar(min_large, solver.infinity(), 'LargeContainers')

    # CONSTRAINTS

    # Personnel constraint: 1 * small + 3 * large <= 100.
    solver.Add(unload_req_small * small + unload_req_large * large <= available_persons)

    # Ratio constraint: small == 3 * large.
    solver.Add(small == ratio_small_to_large * large)

    # Note: minimum constraints are already set in variable lower bounds.

    # OBJECTIVE: Maximize total sand delivered.
    objective = solver.Objective()
    objective.SetCoefficient(small, capacity_small)
    objective.SetCoefficient(large, capacity_large)
    objective.SetMaximization()

    # Solve.
    status = solver.Solve()
    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "model": "LinearSolver",
            "variables": {
                "SmallContainers": small.solution_value(),
                "LargeContainers": large.solution_value()
            },
            "objective": objective.Value()
        }
    else:
        result = {
            "model": "LinearSolver",
            "message": "No optimal solution found."
        }
    return result


def solve_cp():
    # Create the CP-SAT model.
    model = cp_model.CpModel()

    # PARAMETERS
    unload_req_small = 1
    unload_req_large = 3
    capacity_small = 20
    capacity_large = 50
    available_persons = 100
    min_small = 5
    min_large = 3
    ratio_small_to_large = 3

    # VARIABLE DOMAINS:
    # Estimate an upper bound for large containers:
    # From personnel: small + 3*large <= 100 and small = 3*large -> 3*large + 3*large <= 100 -> 6*large <= 100 -> large <= 16
    large = model.NewIntVar(min_large, 16, 'LargeContainers')
    # Since small = 3 * large, small's domain is derived from large.
    small = model.NewIntVar(min_small, ratio_small_to_large * 16, 'SmallContainers')

    # CONSTRAINTS

    # Ratio constraint: small == 3 * large.
    model.Add(small == ratio_small_to_large * large)

    # Personnel constraint: 1 * small + 3 * large <= 100.
    model.Add(unload_req_small * small + unload_req_large * large <= available_persons)

    # OBJECTIVE: Maximize total sand delivered.
    # CP-SAT does not support floats directly, so we work with integers.
    total_sand = model.NewIntVar(0, 10000, 'TotalSand')
    model.Add(total_sand == capacity_small * small + capacity_large * large)
    model.Maximize(total_sand)

    # Solve the model.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    result = {}
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        result = {
            "model": "CPSat",
            "variables": {
                "SmallContainers": solver.Value(small),
                "LargeContainers": solver.Value(large)
            },
            "objective": solver.Value(total_sand)
        }
    else:
        result = {
            "model": "CPSat",
            "message": "No optimal solution found."
        }
    return result

def main():
    # Solve with the Linear Solver implementation.
    linear_result = solve_linear()
    # Solve with the CP-SAT implementation.
    cp_result = solve_cp()

    # Print results for both implementations in a structured way.
    print("Results:")
    print("---------")
    print("Linear Solver Result:")
    print(linear_result)
    print("---------")
    print("CP-SAT Result:")
    print(cp_result)

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Results:
---------
Linear Solver Result:
{'model': 'LinearSolver', 'variables': {'SmallContainers': 48.0, 'LargeContainers': 16.0}, 'objective': 1760.0}
---------
CP-SAT Result:
{'model': 'CPSat', 'variables': {'SmallContainers': 48, 'LargeContainers': 16}, 'objective': 1760}
'''

'''Expected Output:
Expected solution

: {'variables': {'SmallContainers': 48.0, 'LargeContainers': 16.0}, 'objective': 1760.0}'''

