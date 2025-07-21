# Problem Description:
'''Problem description: A sandwich company can open two types of stores, a dine-in place and a food-truck. A dine-in place can make 100 sandwiches per day and requires 8 employees to operate. A food-truck can make 50 sandwiches per day and requires 3 employees to operate. The company must make at least 500 sandwiches per day but they only have available 35 employees. How many of each type of store should the company open to minimize the total number of stores?

Expected Output Schema:
{
  "variables": {
    "NumberStore": {
      "0": "float",
      "1": "float"
    }
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Below is a complete formulation of the problem using the five‐element model framework.

--------------------------------------------------------------------
Sets:
• S = {dine_in, food_truck}
  (Interpretation: the two types of store options available.)

--------------------------------------------------------------------
Parameters:
• Sandwiches per day:
  – sandwich_capacity[dine_in] = 100    (sandiwches per dine‐in store per day)
  – sandwich_capacity[food_truck] = 50  (sandwiches per food-truck per day)
• Employees required per store:
  – employees[dine_in] = 8    (employees needed for one dine‐in store)
  – employees[food_truck] = 3   (employees needed for one food-truck)
• Overall resource limits:
  – min_sandwiches = 500   (minimum number of sandwiches that must be produced per day)
  – max_employees = 35    (maximum number of employees available)

--------------------------------------------------------------------
Variables:
• Let x[dine_in] be the number of dine-in stores to open (integer ≥ 0).
• Let x[food_truck] be the number of food-truck stores to open (integer ≥ 0).

(For clarity in a two-index format, one may denote these as:
  NumberStore[0] = x[dine_in]
  NumberStore[1] = x[food_truck] )

--------------------------------------------------------------------
Objective:
Minimize the total number of stores opened.
Mathematically: Minimize x[dine_in] + x[food_truck].

--------------------------------------------------------------------
Constraints:
1. Sandwich Production Constraint: 
  100 · x[dine_in] + 50 · x[food_truck] ≥ 500.
  This ensures that the daily sandwich production reaches at least the required minimum.

2. Employee Availability Constraint:
  8 · x[dine_in] + 3 · x[food_truck] ≤ 35.
  This ensures that the total number of employees required does not exceed available resources.

--------------------------------------------------------------------
Below is the output schema in JSON format as requested:

{
  "variables": {
    "NumberStore": {
      "0": "integer, number of dine-in stores to open",
      "1": "integer, number of food truck stores to open"
    }
  },
  "objective": "Minimize total stores = NumberStore[0] + NumberStore[1]"
}

This structured model captures all aspects of the original problem.'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_model():
    # Create the solver using CBC backend.
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Solver not created.")
        return None
    
    # Decision Variables
    # x0: number of dine-in stores (integer, >= 0)
    # x1: number of food-truck stores (integer, >= 0)
    x0 = solver.IntVar(0, solver.infinity(), 'NumberStore[0]')  # dine-in
    x1 = solver.IntVar(0, solver.infinity(), 'NumberStore[1]')  # food truck
    
    # Constraints:
    # 1. Sandwich Production Constraint:
    # 100*x0 + 50*x1 >= 500
    solver.Add(100 * x0 + 50 * x1 >= 500)
    
    # 2. Employee Availability Constraint:
    # 8*x0 + 3*x1 <= 35
    solver.Add(8 * x0 + 3 * x1 <= 35)
    
    # Objective: Minimize total number of stores = x0 + x1
    objective = solver.Objective()
    objective.SetCoefficient(x0, 1)
    objective.SetCoefficient(x1, 1)
    objective.SetMinimization()
    
    # Solve the problem
    status = solver.Solve()
    
    # Prepare result dictionary for structured output
    result = {}
    
    if status == pywraplp.Solver.OPTIMAL:
        result['status'] = 'optimal'
        result['objective'] = objective.Value()
        result['variables'] = {
            "NumberStore": {
                "0": x0.solution_value(),  # dine-in
                "1": x1.solution_value()   # food truck
            }
        }
    elif status == pywraplp.Solver.FEASIBLE:
        result['status'] = 'feasible'
        result['objective'] = objective.Value()
        result['variables'] = {
            "NumberStore": {
                "0": x0.solution_value(),  # dine-in
                "1": x1.solution_value()   # food truck
            }
        }
    else:
        result['status'] = 'infeasible'
        result['message'] = 'No solution found.'
    
    return result

def main():
    # Since the problem formulation does not have multiple distinct versions,
    # we only implement one version using the linear solver.
    model_result = solve_model()
    
    # Print the result in a structured way.
    print("=== Model 1: Linear Solver Implementation ===")
    if model_result:
        if model_result.get('status') == 'optimal' or model_result.get('status') == 'feasible':
            print("Optimal solution found:")
            print("Objective value (total stores):", model_result['objective'])
            print("Number of dine-in stores (NumberStore[0]):", model_result['variables']['NumberStore']['0'])
            print("Number of food truck stores (NumberStore[1]):", model_result['variables']['NumberStore']['1'])
        else:
            print("Problem infeasible. No solution found.")
    else:
        print("Solver creation failed.")

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
=== Model 1: Linear Solver Implementation ===
Optimal solution found:
Objective value (total stores): 8.0
Number of dine-in stores (NumberStore[0]): 2.0
Number of food truck stores (NumberStore[1]): 6.0
'''

'''Expected Output:
Expected solution

: {'variables': {'NumberStore': {'0': 2.0, '1': 6.0}}, 'objective': 8.0}'''

