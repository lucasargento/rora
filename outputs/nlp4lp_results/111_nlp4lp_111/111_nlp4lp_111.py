# Problem Description:
'''Problem description: In a science club, there are two tables that can be set up to make slime. At table 1, 3 units of powder and 5 units of glue are used to make 4 units of slime. At table 2, 8 units of powder and 6 units of glue are used to make 5 units of slime. However, table 1 produces 2 units of mess while table 2 produces 4 units of mess. The science club has available 100 units of powder and 90 units of glue.  If at most 30 units of mess can be made, how many of each table should be set up to maximize the amount of slime produced?

Expected Output Schema:
{
  "variables": {
    "Production": {
      "0": "float",
      "1": "float"
    }
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- T: set of tables = {1, 2}

Parameters:
- powder_usage[t]: units of powder used at table t. Values: powder_usage[1] = 3 (units per setup), powder_usage[2] = 8 (units per setup)
- glue_usage[t]: units of glue used at table t. Values: glue_usage[1] = 5 (units per setup), glue_usage[2] = 6 (units per setup)
- slime_production[t]: units of slime produced at table t. Values: slime_production[1] = 4 (units per setup), slime_production[2] = 5 (units per setup)
- mess_production[t]: units of mess produced at table t. Values: mess_production[1] = 2 (units per setup), mess_production[2] = 4 (units per setup)
- available_powder: total available powder = 100 (units)
- available_glue: total available glue = 90 (units)
- max_mess: maximum allowable mess = 30 (units)

Variables:
- x[t]: number of setups at table t, where t ∈ T. 
  -- Decision variables are nonnegative integers (or continuous if fractional setups are allowed, but usually setups are integer). Assume integer ≥ 0.

Objective:
- Maximize total slime produced = sum over t in T of (slime_production[t] * x[t])
  (Units: units of slime)

Constraints:
1. Powder constraint: sum over t in T of (powder_usage[t] * x[t]) ≤ available_powder  
   (Interpretation: total powder used should not exceed 100 units)
2. Glue constraint: sum over t in T of (glue_usage[t] * x[t]) ≤ available_glue  
   (Interpretation: total glue used should not exceed 90 units)
3. Mess constraint: sum over t in T of (mess_production[t] * x[t]) ≤ max_mess  
   (Interpretation: total mess produced should not exceed 30 units)

Notes:
- All units are assumed to be consistent: "units" represents the same measurement across powder, glue, slime, and mess.
- Decision variables (x[1], x[2]) represent how many setups (or batches) of slime production to run at each corresponding table.
- This formulation is self-contained and directly translatable into Python or OR-Tools code.'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_with_linear_solver():
    # Create the linear solver with the CBC backend.
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("CBC solver unavailable.")
        return None

    # Decision variables: number of table setups for table 1 and table 2 (nonnegative integers)
    x0 = solver.IntVar(0, solver.infinity(), 'x0')  # Table 1 setups
    x1 = solver.IntVar(0, solver.infinity(), 'x1')  # Table 2 setups

    # Parameters based on problem description:
    # For table 1:
    powder_usage_0 = 3
    glue_usage_0 = 5
    slime_production_0 = 4
    mess_production_0 = 2
    # For table 2:
    powder_usage_1 = 8
    glue_usage_1 = 6
    slime_production_1 = 5
    mess_production_1 = 4

    available_powder = 100
    available_glue = 90
    max_mess = 30

    # Constraints:
    # 1. Powder constraint: 3*x0 + 8*x1 <= 100
    solver.Add(powder_usage_0 * x0 + powder_usage_1 * x1 <= available_powder)

    # 2. Glue constraint: 5*x0 + 6*x1 <= 90
    solver.Add(glue_usage_0 * x0 + glue_usage_1 * x1 <= available_glue)

    # 3. Mess constraint: 2*x0 + 4*x1 <= 30
    solver.Add(mess_production_0 * x0 + mess_production_1 * x1 <= max_mess)

    # Objective: maximize total slime produced: 4*x0 + 5*x1
    objective = solver.Objective()
    objective.SetCoefficient(x0, slime_production_0)
    objective.SetCoefficient(x1, slime_production_1)
    objective.SetMaximization()

    status = solver.Solve()

    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result["variables"] = {
            "Production": {
                "0": x0.solution_value(),
                "1": x1.solution_value()
            }
        }
        result["objective"] = objective.Value()
    else:
        result["error"] = "No optimal solution found."

    return result

def main():
    # As only one formulation is provided, we only call one implementation.
    result_linear = solve_with_linear_solver()

    # Printing the results in a structured way.
    print("Solution from Linear Solver Implementation:")
    if result_linear is not None:
        print(result_linear)
    else:
        print("No solution found.")

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Solution from Linear Solver Implementation:
{'variables': {'Production': {'0': 15.0, '1': 0.0}}, 'objective': 60.0}
'''

'''Expected Output:
Expected solution

: {'variables': {'Production': {'0': 15.0, '1': 0.0}}, 'objective': 60.0}'''

