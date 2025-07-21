# Problem Description:
'''Problem description: An international shipping company uses large and small ships to transport containers around the world. A large ship can carry 500 containers while a small ship can carry 200 containers. Because most ports are small, the number of large ships cannot exceed the number of small ships. If the company is under contract needs to transport at least 3000 containers, find the minimum number of ships that can be used.

Expected Output Schema:
{
  "variables": {
    "NumberLargeShips": "float",
    "NumberSmallShips": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Below is the complete mathematical model using the five‐element framework. In this model, all ship counts are assumed to be nonnegative integers, container capacities are in “containers per ship,” and the contract requirement is in “containers.” Note that the port limitation is modeled by requiring that the number of large ships does not exceed the number of small ships.

───────────────────────────── 
Sets:
- S = {Large, Small} 
  (A set that distinguishes the two types of ships)

───────────────────────────── 
Parameters:
- capacity_Large = 500   [containers per large ship]
- capacity_Small = 200   [containers per small ship]
- minRequiredContainers = 3000   [containers]
- Note: The “port constraint” is given by the condition that the number of large ships cannot exceed the number of small ships.

───────────────────────────── 
Variables:
- NumberLargeShips: number of large ships to use (integer, ≥ 0)
- NumberSmallShips: number of small ships to use (integer, ≥ 0)

───────────────────────────── 
Objective:
- Minimize TotalShips  where TotalShips = NumberLargeShips + NumberSmallShips
  (This minimizes the overall number of ships used.)

───────────────────────────── 
Constraints:
1. Container Transport Capability:
  500 * NumberLargeShips + 200 * NumberSmallShips ≥ 3000
  (This constraint ensures that at least 3000 containers can be transported.)

2. Port Size Constraint:
  NumberLargeShips ≤ NumberSmallShips
  (This reflects that “most ports are small” and limits the use of large ships.)

───────────────────────────── 

Below is the final output following the expected output schema:

{
  "variables": {
    "NumberLargeShips": "integer >= 0 (number of large ships)",
    "NumberSmallShips": "integer >= 0 (number of small ships)"
  },
  "objective": "minimize NumberLargeShips + NumberSmallShips"
}'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_model():
    # Create the solver using CBC backend.
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Solver not created.")
        return None

    # Decision Variables:
    # NumberLargeShips: number of large ships (integer, >= 0)
    # NumberSmallShips: number of small ships (integer, >= 0)
    NumberLargeShips = solver.IntVar(0, solver.infinity(), 'NumberLargeShips')
    NumberSmallShips = solver.IntVar(0, solver.infinity(), 'NumberSmallShips')

    # Parameters:
    capacity_Large = 500
    capacity_Small = 200
    minRequiredContainers = 3000

    # Constraints:
    # 1. Container Transport Capability
    # 500 * NumberLargeShips + 200 * NumberSmallShips >= 3000
    solver.Add(capacity_Large * NumberLargeShips + capacity_Small * NumberSmallShips >= minRequiredContainers)

    # 2. Port Size Constraint: NumberLargeShips <= NumberSmallShips
    solver.Add(NumberLargeShips <= NumberSmallShips)

    # Objective:
    # Minimize TotalShips = NumberLargeShips + NumberSmallShips
    objective = solver.Objective()
    objective.SetCoefficient(NumberLargeShips, 1)
    objective.SetCoefficient(NumberSmallShips, 1)
    objective.SetMinimization()

    # Solve the problem.
    status = solver.Solve()
    
    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result["NumberLargeShips"] = NumberLargeShips.solution_value()
        result["NumberSmallShips"] = NumberSmallShips.solution_value()
        result["TotalShips"] = objective.Value()
    else:
        result["message"] = "The problem does not have an optimal solution."

    return result

def main():
    # In this problem formulation, we have a single version to implement.
    # If in the future multiple formulations are provided,
    # separate model implementations can be added and their results combined.
    
    result_model1 = solve_model()

    # Print the result in a structured way.
    print("Model Implementation 1:")
    if "message" in result_model1:
        print(result_model1["message"])
    else:
        print("Optimal Number of Large Ships: {}".format(result_model1["NumberLargeShips"]))
        print("Optimal Number of Small Ships: {}".format(result_model1["NumberSmallShips"]))
        print("Minimum Total Ships: {}".format(result_model1["TotalShips"]))
    
if __name__ == "__main__":
    main()

'''Execution Results:
SUCCESS:
Model Implementation 1:
Optimal Number of Large Ships: 4.0
Optimal Number of Small Ships: 5.0
Minimum Total Ships: 9.0
'''

'''Expected Output:
Expected solution

: {'variables': {'NumberLargeShips': 4.0, 'NumberSmallShips': 5.0}, 'objective': 9.0}'''

