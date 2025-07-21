# Problem Description:
'''Problem description: A toy company can build two factory types, a medium sized factory and a small factory. A medium sized factory can make 50 toys per day and requires 3 operators. A small factory can make 35 toys per day and requires 2 operators. The company must make at least 250 toys per day but they only have available 16 operators. How many of each factory should the company build to minimize the total number of factories?

Expected Output Schema:
{
  "variables": {
    "NumberOfFactories": {
      "0": "float",
      "1": "float"
    }
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- F: set of factory types = {Medium, Small}

Parameters:
- production_per_factory:
    - Medium: 50 (toys produced per day)
    - Small: 35 (toys produced per day)
- operators_required:
    - Medium: 3 (operators needed per factory)
    - Small: 2 (operators needed per factory)
- min_toys: 250 (minimum number of toys required per day)
- available_operators: 16 (total operators available)

Variables:
- x, where:
    - x[Medium] is the number of medium factories (integer ≥ 0)
    - x[Small] is the number of small factories (integer ≥ 0)

Objective:
- Minimize the total number of factories, i.e., minimize x[Medium] + x[Small]

Constraints:
1. Production constraint:
   - 50 * x[Medium] + 35 * x[Small] ≥ 250 
     (ensuring the total toy production meets or exceeds the daily requirement)
2. Operator constraint:
   - 3 * x[Medium] + 2 * x[Small] ≤ 16 
     (ensuring the total number of operators required does not exceed availability)

--------------------------------------------------

Based on the expected output schema:

{
  "variables": {
    "NumberOfFactories": {
      "0": "float",   // corresponds to x[Medium]
      "1": "float"    // corresponds to x[Small]
    }
  },
  "objective": "float"   // represents x[Medium] + x[Small]
}

Notes:
- In practical implementation, the decision variables should be constrained to integer values.
- All units (toys/day for production, number of operators for staffing) are assumed consistent as specified in the problem description.'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_linear_model_version():
    # Create the solver using CBC backend
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        return None, None, "Solver not created."

    # Decision Variables:
    # x[Medium]: number of medium factories
    # x[Small]: number of small factories
    x_medium = solver.IntVar(0, solver.infinity(), 'x_Medium')
    x_small = solver.IntVar(0, solver.infinity(), 'x_Small')
    
    # Constraints:
    # Production constraint: 50*x_medium + 35*x_small >= 250
    production_constraint = solver.Add(50 * x_medium + 35 * x_small >= 250)
    
    # Operator constraint: 3*x_medium + 2*x_small <= 16
    operator_constraint = solver.Add(3 * x_medium + 2 * x_small <= 16)
    
    # Objective: Minimize the total number of factories: x_medium + x_small
    solver.Minimize(x_medium + x_small)
    
    # Solve the problem
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        solution = {
            "NumberOfFactories": {
                "0": x_medium.solution_value(),
                "1": x_small.solution_value()
            },
            "objective": x_medium.solution_value() + x_small.solution_value()
        }
        return solution, solver.Objective().Value(), None
    elif status == pywraplp.Solver.FEASIBLE:
        return None, None, "A feasible solution was found, but it is not proven optimal."
    else:
        return None, None, "The problem does not have an optimal solution."

def main():
    results = {}
    
    # Implementation 1: Linear MIP model using ortools.linear_solver (CBC)
    sol1, obj1, error1 = solve_linear_model_version()
    if error1 is None:
        results["Implementation_1"] = {
            "Status": "Optimal",
            "Solution": sol1,
            "ObjectiveValue": obj1
        }
    else:
        results["Implementation_1"] = {
            "Status": "Error",
            "Message": error1
        }
    
    # Print results in a structured format:
    print("Results:")
    for impl, res in results.items():
        print(f"\n{impl}:")
        for key, value in res.items():
            print(f"  {key}: {value}")

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Results:

Implementation_1:
  Status: Optimal
  Solution: {'NumberOfFactories': {'0': 5.0, '1': 0.0}, 'objective': 5.0}
  ObjectiveValue: 5.0
'''

'''Expected Output:
Expected solution

: {'variables': {'NumberOfFactories': {'0': 5.0, '1': -0.0}}, 'objective': 5.0}'''

