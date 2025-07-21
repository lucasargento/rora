# Problem Description:
'''Problem description: A cell phone company is building rural and urban factories. A rural factory can make 100 phones per day and requires 8 managers. An urban factory can make 200 phones per day and requires 20 managers. The company has available 260 managers and must make at least 3000 phones per day. How many of each factory type should be built to minimize the total number of factories?

Expected Output Schema:
{
  "variables": {
    "FactoriesBuilt": {
      "0": "float",
      "1": "float"
    }
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Below is the mathematical model using the five-element framework.

------------------------------------------------------------
Sets:
- F: set of factory types = {Rural, Urban}

------------------------------------------------------------
Parameters:
- production_Rural: number of phones produced per rural factory per day (100 phones/day)
- production_Urban: number of phones produced per urban factory per day (200 phones/day)
- managers_Rural: number of managers required per rural factory (8 managers)
- managers_Urban: number of managers required per urban factory (20 managers)
- available_managers: total number of managers available (260 managers)
- required_phones: minimum number of phones to be produced per day (3000 phones)

------------------------------------------------------------
Variables:
- x_Rural: number of rural factories to build (integer ≥ 0)
- x_Urban: number of urban factories to build (integer ≥ 0)

------------------------------------------------------------
Objective:
Minimize total factories built = x_Rural + x_Urban

------------------------------------------------------------
Constraints:
1. Production Constraint (phone requirement):
   production_Rural * x_Rural + production_Urban * x_Urban ≥ required_phones
   i.e., 100 * x_Rural + 200 * x_Urban ≥ 3000

2. Manager Constraint:
   managers_Rural * x_Rural + managers_Urban * x_Urban ≤ available_managers
   i.e., 8 * x_Rural + 20 * x_Urban ≤ 260

------------------------------------------------------------
Notes:
- All units are consistent (phones/day, managers, and factory counts).
- The decision variables are assumed to be integers since you cannot build a fractional factory.
- The objective is to minimize the number of factories while meeting production and manager constraints.'''

# Generated Code:
from ortools.linear_solver import pywraplp
import json

def solve_mip_model():
    # Create the MILP solver using SCIP.
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        print("SCIP solver unavailable.")
        return

    # Parameters
    production_rural = 100      # phones per rural factory/day
    production_urban = 200      # phones per urban factory/day
    managers_rural = 8          # managers per rural factory
    managers_urban = 20         # managers per urban factory
    available_managers = 260    # total managers available
    required_phones = 3000      # minimum phones to produce per day

    # Decision Variables: number of factories to build. Must be non-negative integers.
    x_rural = solver.IntVar(0, solver.infinity(), 'x_Rural')
    x_urban = solver.IntVar(0, solver.infinity(), 'x_Urban')

    # Constraint 1: Production Constraint
    # 100*x_rural + 200*x_urban >= 3000
    solver.Add(production_rural * x_rural + production_urban * x_urban >= required_phones)

    # Constraint 2: Manager Constraint
    # 8*x_rural + 20*x_urban <= 260
    solver.Add(managers_rural * x_rural + managers_urban * x_urban <= available_managers)

    # Objective: Minimize total number of factories built: x_rural + x_urban
    solver.Minimize(x_rural + x_urban)

    # Solve the model.
    status = solver.Solve()

    # Process and print the results.
    if status == pywraplp.Solver.OPTIMAL:
        solution = {
            "variables": {
                "FactoriesBuilt": {
                    "0": float(x_rural.solution_value()),
                    "1": float(x_urban.solution_value())
                }
            },
            "objective": float(solver.Objective().Value())
        }
        print("MILP Model (using ortools.linear_solver) Optimal Solution:")
        print("  Rural factories:", int(x_rural.solution_value()))
        print("  Urban factories:", int(x_urban.solution_value()))
        print("  Objective (total factories):", solver.Objective().Value())
        print("\nOutput Schema:")
        print(json.dumps(solution, indent=4))
    else:
        print("The problem does not have an optimal solution.")

def main():
    # There is only one formulation provided.
    solve_mip_model()

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
MILP Model (using ortools.linear_solver) Optimal Solution:
  Rural factories: 20
  Urban factories: 5
  Objective (total factories): 25.0

Output Schema:
{
    "variables": {
        "FactoriesBuilt": {
            "0": 20.0,
            "1": 5.0
        }
    },
    "objective": 25.0
}
'''

'''Expected Output:
Expected solution

: {'variables': {'FactoriesBuilt': {'0': 20.0, '1': 5.0}}, 'objective': 25.0}'''

