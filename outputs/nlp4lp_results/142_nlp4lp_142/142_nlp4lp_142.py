# Problem Description:
'''Problem description: A car manufacturer ships their cars on large and small planes. A large plane can carry 30 cars while a small plane can carry 10 cars. Since large planes cause more pollution, the number of large planes must be less than the number of small planes. If the manufacturer wants to deliver at least 300 cars, find the minimum number of planes that can be used.

Expected Output Schema:
{
  "variables": {
    "NumLargePlanes": "float",
    "NumSmallPlanes": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- PlaneTypes = {Large, Small}

Parameters:
- capacity_Large = 30 (cars per large plane)
- capacity_Small = 10 (cars per small plane)
- minCars = 300 (minimum cars to deliver)

Variables:
- NumLargePlanes: integer, nonnegative (number of large planes)
- NumSmallPlanes: integer, nonnegative (number of small planes)

Objective:
- Minimize total planes used = NumLargePlanes + NumSmallPlanes

Constraints:
1. Delivery Requirement: (capacity_Large * NumLargePlanes) + (capacity_Small * NumSmallPlanes) ≥ minCars
2. Pollution Constraint: NumLargePlanes < NumSmallPlanes 
   (This can be modeled as: NumLargePlanes ≤ NumSmallPlanes - 1, ensuring that the number of large planes is strictly less than the number of small planes.)'''

# Generated Code:
#!/usr/bin/env python3
"""
This script solves the following optimization problem using Google OR-Tools:

A car manufacturer ships their cars on large and small planes. A large plane can carry 30 cars while a small plane can carry 10 cars. Since large planes cause more pollution, the number of large planes must be less than the number of small planes. The manufacturer wants to deliver at least 300 cars. The objective is to minimize the total number of planes used.

Mathematical Formulation:

Sets:
- PlaneTypes = {Large, Small}

Parameters:
- capacity_Large = 30 (cars per large plane)
- capacity_Small = 10 (cars per small plane)
- minCars = 300 (minimum cars to deliver)

Variables:
- NumLargePlanes: nonnegative integer (number of large planes)
- NumSmallPlanes: nonnegative integer (number of small planes)

Objective:
- Minimize total planes used = NumLargePlanes + NumSmallPlanes

Constraints:
1. Delivery Requirement: 30 * NumLargePlanes + 10 * NumSmallPlanes ≥ 300
2. Pollution Constraint: NumLargePlanes < NumSmallPlanes 
   (modeled as: NumLargePlanes ≤ NumSmallPlanes - 1)
   
Since this is a linear mixed-integer optimization problem, we use ortools.linear_solver.
"""

from ortools.linear_solver import pywraplp

def solve_model():
    # Create the MIP solver using CBC backend.
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Solver not created.")
        return None

    infinity = solver.infinity()
    
    # Define decision variables.
    # NumLargePlanes and NumSmallPlanes must be nonnegative integers.
    NumLargePlanes = solver.IntVar(0, infinity, 'NumLargePlanes')
    NumSmallPlanes = solver.IntVar(0, infinity, 'NumSmallPlanes')

    # Constraint 1: Delivery requirement.
    # 30 * NumLargePlanes + 10 * NumSmallPlanes >= 300
    solver.Add(30 * NumLargePlanes + 10 * NumSmallPlanes >= 300)

    # Constraint 2: Pollution constraint (large planes are fewer than small planes).
    # Using: NumLargePlanes <= NumSmallPlanes - 1
    solver.Add(NumLargePlanes <= NumSmallPlanes - 1)

    # Objective: Minimize the total number of planes used.
    solver.Minimize(NumLargePlanes + NumSmallPlanes)

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "NumLargePlanes": NumLargePlanes.solution_value(),
            "NumSmallPlanes": NumSmallPlanes.solution_value(),
            "objective": solver.Objective().Value()
        }
        return result
    else:
        return None

def main():
    # Since only one formulation is provided in the problem description,
    # we implement one model.
    solution = solve_model()
    
    print("Results:")
    if solution:
        # Print the solution in the expected output schema format.
        print("{")
        print('  "variables": {')
        print('    "NumLargePlanes": {},'.format(solution["NumLargePlanes"]))
        print('    "NumSmallPlanes": {}'.format(solution["NumSmallPlanes"]))
        print("  },")
        print('  "objective": {}'.format(solution["objective"]))
        print("}")
    else:
        print("No optimal solution found.")

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Results:
{
  "variables": {
    "NumLargePlanes": 7.0,
    "NumSmallPlanes": 9.0
  },
  "objective": 16.0
}
'''

'''Expected Output:
Expected solution

: {'variables': {'NumLargePlanes': 7.0, 'NumSmallPlanes': 9.0}, 'objective': 16.0}'''

