# Problem Description:
'''Problem description: A bank can build small and large branches to serve their customers. A small branch can serve 50 customers per day and requires 10 bank tellers. A large branch can serve 100 customers per day and requires 15 bank tellers. The bank has available 200 bank tellers and needs to be able to serve at least 1200 customers per day. How many of each branch size should they build to minimize the total number of branches needed?

Expected Output Schema:
{
  "variables": {
    "SmallBranches": "float",
    "LargeBranches": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- BranchTypes = {Small, Large}

Parameters:
- customers_Small: number of customers served by a small branch per day = 50 (customers/branch/day)
- customers_Large: number of customers served by a large branch per day = 100 (customers/branch/day)
- tellers_Small: number of bank tellers required per small branch = 10 (tellers/branch)
- tellers_Large: number of bank tellers required per large branch = 15 (tellers/branch)
- available_Tellers: total available bank tellers = 200 (tellers)
- min_Customers: minimum customers to be served per day = 1200 (customers/day)

Variables:
- SmallBranches: number of small branches to build [integer, ≥ 0]
- LargeBranches: number of large branches to build [integer, ≥ 0]

Objective:
- Minimize total branches built = SmallBranches + LargeBranches

Constraints:
1. Teller Constraint: tellers_Small * SmallBranches + tellers_Large * LargeBranches ≤ available_Tellers  
   (i.e., 10 * SmallBranches + 15 * LargeBranches ≤ 200)
2. Customer Service Constraint: customers_Small * SmallBranches + customers_Large * LargeBranches ≥ min_Customers  
   (i.e., 50 * SmallBranches + 100 * LargeBranches ≥ 1200)

------------------------------------------------------------
Expected Output Schema:
{
  "variables": {
    "SmallBranches": "float",
    "LargeBranches": "float"
  },
  "objective": "float"
}'''

# Generated Code:
#!/usr/bin/env python3
"""
This script solves the bank branch construction optimization problem using Google OR-Tools.
It uses the linear solver approach since the problem is a linear mixed-integer programming problem.
The problem:
    - A small branch serves 50 customers/day and requires 10 bank tellers.
    - A large branch serves 100 customers/day and requires 15 bank tellers.
    - Total available bank tellers = 200.
    - The bank must serve at least 1200 customers/day.
    - The objective is to minimize the total number of branches built.
"""

from ortools.linear_solver import pywraplp

def solve_with_linear_solver():
    # Create the solver with the CBC backend.
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Linear solver not available.")
        return None
    
    # Define variables.
    # Note: using integer variables for branch counts.
    small_branches = solver.IntVar(0.0, solver.infinity(), 'SmallBranches')
    large_branches = solver.IntVar(0.0, solver.infinity(), 'LargeBranches')
    
    # Parameters
    customers_small = 50
    customers_large = 100
    tellers_small = 10
    tellers_large = 15
    available_tellers = 200
    min_customers = 1200
    
    # Constraints:
    # 1. Teller Constraint: 10 * SmallBranches + 15 * LargeBranches <= 200
    solver.Add(tellers_small * small_branches + tellers_large * large_branches <= available_tellers)
    
    # 2. Customer Service Constraint: 50 * SmallBranches + 100 * LargeBranches >= 1200
    solver.Add(customers_small * small_branches + customers_large * large_branches >= min_customers)
    
    # Objective: Minimize total branches built.
    solver.Minimize(small_branches + large_branches)
    
    # Solve the problem.
    status = solver.Solve()
    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "variables": {
                "SmallBranches": small_branches.solution_value(),
                "LargeBranches": large_branches.solution_value()
            },
            "objective": solver.Objective().Value()
        }
    else:
        result = {"message": "The problem does not have an optimal solution."}
    
    return result

def main():
    # Since the mathematical formulation only provides one version, we call only one implementation.
    linear_result = solve_with_linear_solver()
    
    # Display the results in a structured way.
    print("Linear Solver (MIP) Implementation Result:")
    print(linear_result)

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Linear Solver (MIP) Implementation Result:
{'variables': {'SmallBranches': 0.0, 'LargeBranches': 12.0}, 'objective': 12.0}
'''

'''Expected Output:
Expected solution

: {'variables': {'SmallBranches': -0.0, 'LargeBranches': 12.0}, 'objective': 12.0}'''

