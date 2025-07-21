# Problem Description:
'''Problem description: A post office is buying stamping machines and they can buy a dual or single model stamping machine. A dual model stamping machine can stamp 50 letters per minute while a single model stamping machine can stamp 30 letters per minute. The dual model stamping machine requires 20 units of glue per minute while the single model stamping machine requires 15 units of glue per minute. Since the single model stamping machine is quieter, the number of single model stamping machines must be more than the number of dual model stamping machines. Further, the post office wants to make sure they can stamp at least 300 letters per minute and use at most 135 units of glue per minute. How many of each stamping machine should they purchase to minimize the total number of stamping machines?

Expected Output Schema:
{
  "variables": {
    "SingleStampMachines": "float",
    "DualStampMachines": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- M: set of machine types = {Dual, Single}

Parameters:
- letters_per_minute[Dual] = 50 (letters stamped per minute per Dual machine)
- letters_per_minute[Single] = 30 (letters stamped per minute per Single machine)
- glue_usage[Dual] = 20 (units of glue used per minute per Dual machine)
- glue_usage[Single] = 15 (units of glue used per minute per Single machine)
- min_letters = 300 (minimum letters to be stamped per minute)
- max_glue = 135 (maximum glue units available per minute)
- quiet_gap = 1 (at least one more Single machine than Dual machines; i.e., Single - Dual >= 1)

Variables:
- DualStampMachines: integer, number of Dual stamping machines purchased (>= 0)
- SingleStampMachines: integer, number of Single stamping machines purchased (>= 0)

Objective:
- Minimize TotalMachines = SingleStampMachines + DualStampMachines

Constraints:
1. Letters production constraint:
   (letters_per_minute[Dual] * DualStampMachines) + (letters_per_minute[Single] * SingleStampMachines) >= min_letters
   i.e., 50 * DualStampMachines + 30 * SingleStampMachines >= 300

2. Glue usage constraint:
   (glue_usage[Dual] * DualStampMachines) + (glue_usage[Single] * SingleStampMachines) <= max_glue
   i.e., 20 * DualStampMachines + 15 * SingleStampMachines <= 135

3. Quiet operation constraint (Single machines must outnumber Dual machines):
   SingleStampMachines - DualStampMachines >= quiet_gap
   i.e., SingleStampMachines - DualStampMachines >= 1

4. Non-negativity and integrality constraints:
   DualStampMachines ∈ {0, 1, 2, ...}
   SingleStampMachines ∈ {0, 1, 2, ...}

Notes:
- All units are expressed per minute.
- The model minimizes the total number of machines while satisfying the performance and resource usage constraints.'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_linear_model():
    # Create the MIP solver with the CBC backend.
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Solver not created.")
        return None

    # Variables:
    # DualStampMachines: integer >= 0
    dual = solver.IntVar(0, solver.infinity(), 'DualStampMachines')
    # SingleStampMachines: integer >= 0
    single = solver.IntVar(0, solver.infinity(), 'SingleStampMachines')

    # Objective: Minimize total machines: single + dual
    solver.Minimize(single + dual)

    # Constraints:
    # 1. Letters production constraint: 50*dual + 30*single >= 300
    solver.Add(50 * dual + 30 * single >= 300)

    # 2. Glue usage constraint: 20*dual + 15*single <= 135
    solver.Add(20 * dual + 15 * single <= 135)

    # 3. Quiet operation constraint: single - dual >= 1
    solver.Add(single - dual >= 1)

    status = solver.Solve()

    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "model": "Linear Model",
            "variables": {
                "SingleStampMachines": single.solution_value(),
                "DualStampMachines": dual.solution_value()
            },
            "objective": solver.Objective().Value()
        }
    elif status == pywraplp.Solver.FEASIBLE:
        result = {"model": "Linear Model", "message": "A feasible solution was found, but it may not be optimal."}
    else:
        result = {"model": "Linear Model", "message": "The problem does not have an optimal solution."}
    return result

def main():
    # Since the mathematical formulation provided only one formulation,
    # we only implement one version using the linear solver.
    linear_result = solve_linear_model()

    # Print results in a structured way:
    print("Optimization Results:")
    if "variables" in linear_result:
        print("Model: {}".format(linear_result["model"]))
        print("Optimal Number of SingleStampMachines: {}".format(linear_result["variables"]["SingleStampMachines"]))
        print("Optimal Number of DualStampMachines: {}".format(linear_result["variables"]["DualStampMachines"]))
        print("Objective (Total Machines): {}".format(linear_result["objective"]))
    else:
        print(linear_result.get("message", "No result available."))

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Optimization Results:
Model: Linear Model
Optimal Number of SingleStampMachines: 5.0
Optimal Number of DualStampMachines: 3.0
Objective (Total Machines): 8.0
'''

'''Expected Output:
Expected solution

: {'variables': {'SingleStampMachines': 5.0, 'DualStampMachines': 3.0}, 'objective': 8.0}'''

