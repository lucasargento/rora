# Problem Description:
'''Problem description: The government is reworking the pipes to transport water to houses in the area. The water can be transported through wide pipes or narrow pipes. Wide pipes can transport 25 units of water per minute and narrow pipes can transport 15 units of water per minute. Due to logistics, the number of wide pipes can be at most a third the number of narrow pipes. If there needs to be at least 900 units of water transported every minute, and at least 5 wide pipes must be used, minimize the total number of pipes required.

Expected Output Schema:
{
  "variables": {
    "WidePipes": "float",
    "NarrowPipes": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Below is a five-element structured formulation of the problem. Note that pipes are assumed to be counted in whole numbers (integers). For simplicity, we assume all capacities and flows are stated in water units per minute.

--------------------------------------------------

Sets:
• (None required for this two-variable problem)

Parameters:
• WidePipeFlow = 25 (water units per minute delivered by one wide pipe)
• NarrowPipeFlow = 15 (water units per minute delivered by one narrow pipe)
• MinWaterFlow = 900 (minimum water flow required in water units per minute)
• MaxWidePipesRatio = 1/3 (the number of wide pipes can be at most one third of the number of narrow pipes)
• MinWidePipes = 5 (minimum number of wide pipes must be used)

Variables:
• WidePipes: an integer representing the number of wide pipes used (integer ≥ MinWidePipes)
• NarrowPipes: an integer representing the number of narrow pipes used (integer ≥ 0)

Objective:
• Minimize total number of pipes = WidePipes + NarrowPipes

Constraints:
1. Water Flow Constraint:
   • 25 * WidePipes + 15 * NarrowPipes ≥ 900
     (ensures that the total water delivered per minute meets the minimum requirement)

2. Pipe Ratio Constraint:
   • WidePipes ≤ (1/3) * NarrowPipes
     (ensures that the number of wide pipes is at most one third of the number of narrow pipes)

3. Minimum Wide Pipe Constraint:
   • WidePipes ≥ 5

--------------------------------------------------

This formulation fully captures the original problem. One can map these elements directly to a Python or OR-Tools implementation. 

For the expected output schema as a JSON object, here is a concise version:

{
  "variables": {
    "WidePipes": "integer, number of wide pipes (>= 5)",
    "NarrowPipes": "integer, number of narrow pipes (>= 0)"
  },
  "objective": "Minimize: WidePipes + NarrowPipes"
}

All parameters and units have been explicitly stated to ensure clarity and consistency with the problem data.'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp
from ortools.sat.python import cp_model

def solve_with_linear_solver():
    # Create the MIP solver using SCIP.
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        return None, None, "Linear Solver not found."

    # PARAMETERS
    WidePipeFlow = 25
    NarrowPipeFlow = 15
    MinWaterFlow = 900
    # Instead of fraction constraint, we use 3*WidePipes <= NarrowPipes equivalent
    MinWidePipes = 5

    # DECISION VARIABLES: integer variables.
    wide_pipes = solver.IntVar(MinWidePipes, solver.infinity(), 'WidePipes')
    narrow_pipes = solver.IntVar(0.0, solver.infinity(), 'NarrowPipes')

    # CONSTRAINTS

    # Water Flow Constraint: 25 * WidePipes + 15 * NarrowPipes >= 900
    solver.Add(WidePipeFlow * wide_pipes + NarrowPipeFlow * narrow_pipes >= MinWaterFlow)

    # Pipe Ratio Constraint: wide_pipes <= (1/3)*narrow_pipes;
    # Multiply both sides by 3 to avoid fractions: 3 * wide_pipes <= narrow_pipes.
    solver.Add(3 * wide_pipes <= narrow_pipes)

    # OBJECTIVE: Minimize total number of pipes = wide_pipes + narrow_pipes.
    solver.Minimize(wide_pipes + narrow_pipes)

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL:
        opt_wide = int(wide_pipes.solution_value())
        opt_narrow = int(narrow_pipes.solution_value())
        opt_obj = opt_wide + opt_narrow
        result = {
            "variables": {
                "WidePipes": opt_wide,
                "NarrowPipes": opt_narrow
            },
            "objective": opt_obj
        }
        return result, "Optimal", None
    else:
        return None, "NotOptimal", "No optimal solution found by linear solver."

def solve_with_cp_model():
    model = cp_model.CpModel()
    # PARAMETERS
    WidePipeFlow = 25
    NarrowPipeFlow = 15
    MinWaterFlow = 900
    MinWidePipes = 5

    # We need to decide reasonable bounds for the number of pipes.
    # For narrow pipes, an upper bound can be derived from water flow.
    # If all water were carried by narrow pipes: NarrowPipes >= 900/15 = 60.
    # But the ratio constraint forces NarrowPipes to be at least 3*WidePipes.
    # We'll assume an upper bound, e.g., 1000 for safety.
    max_pipes = 1000

    # VARIABLES
    wide_pipes = model.NewIntVar(MinWidePipes, max_pipes, 'WidePipes')
    narrow_pipes = model.NewIntVar(0, max_pipes, 'NarrowPipes')

    # CONSTRAINTS

    # Water Flow Constraint: 25 * wide_pipes + 15 * narrow_pipes >= 900
    model.Add(WidePipeFlow * wide_pipes + NarrowPipeFlow * narrow_pipes >= MinWaterFlow)

    # Pipe Ratio Constraint: wide_pipes <= (1/3)*narrow_pipes
    # To avoid fractions, we use: 3*wide_pipes <= narrow_pipes.
    model.Add(3 * wide_pipes <= narrow_pipes)

    # OBJECTIVE: Minimize wide_pipes + narrow_pipes
    obj_var = model.NewIntVar(0, 2 * max_pipes, 'totalPipes')
    model.Add(obj_var == wide_pipes + narrow_pipes)
    model.Minimize(obj_var)

    # Solve model
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        opt_wide = solver.Value(wide_pipes)
        opt_narrow = solver.Value(narrow_pipes)
        opt_obj = solver.Value(obj_var)
        result = {
            "variables": {
                "WidePipes": opt_wide,
                "NarrowPipes": opt_narrow
            },
            "objective": opt_obj
        }
        return result, "Optimal", None
    else:
        return None, "NotOptimal", "No optimal solution found by CP-SAT solver."

def main():
    results = {}

    # Solve using Linear Solver
    lin_result, lin_status, lin_message = solve_with_linear_solver()
    if lin_result:
        results["LinearSolver"] = {
            "status": lin_status,
            "result": lin_result
        }
    else:
        results["LinearSolver"] = {
            "status": lin_status,
            "message": lin_message
        }

    # Solve using CP-SAT model
    cp_result, cp_status, cp_message = solve_with_cp_model()
    if cp_result:
        results["CPSolver"] = {
            "status": cp_status,
            "result": cp_result
        }
    else:
        results["CPSolver"] = {
            "status": cp_status,
            "message": cp_message
        }

    # Print structured results.
    import json
    print(json.dumps(results, indent=2))

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
{
  "LinearSolver": {
    "status": "Optimal",
    "result": {
      "variables": {
        "WidePipes": 13,
        "NarrowPipes": 39
      },
      "objective": 52
    }
  },
  "CPSolver": {
    "status": "Optimal",
    "result": {
      "variables": {
        "WidePipes": 12,
        "NarrowPipes": 40
      },
      "objective": 52
    }
  }
}
'''

'''Expected Output:
Expected solution

: {'variables': {'WidePipes': 12.0, 'NarrowPipes': 40.0}, 'objective': 52.0}'''

