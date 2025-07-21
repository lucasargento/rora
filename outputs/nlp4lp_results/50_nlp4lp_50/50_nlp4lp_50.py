# Problem Description:
'''Problem description: There are two specialized containers, a small and large one, that are used to make a pharmaceutical paste. The small container requires 10 units of water and 15 units of the powdered pill to make 20 units of the paste. The large container requires 20 units of water and 20 units of the powdered pill to make 30 units of the paste. The pharmacy has available 500 units of water and 700 units of the powdered pill. How many of each container should be used to maximize the amount of paste that can be made?

Expected Output Schema:
{
  "variables": {
    "NumUsedContainers": [
      "float"
    ]
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Below is the structured mathematical model following the five-element format.

------------------------------------------------------------
Sets:
- C: set of container types = {small, large}

------------------------------------------------------------
Parameters (all units are in “units”; note that water and powdered pill input quantities are provided per container, and the output is measured in paste “units”):
- water_req[c]: water required per container c
    • water_req[small] = 10 (units of water per small container)
    • water_req[large] = 20 (units of water per large container)
- pill_req[c]: powdered pill required per container c
    • pill_req[small] = 15 (units of powdered pill per small container)
    • pill_req[large] = 20 (units of powdered pill per large container)
- paste_out[c]: paste output per container c
    • paste_out[small] = 20 (units of paste per small container)
    • paste_out[large] = 30 (units of paste per large container)
- total_water: total available water = 500 (units)
- total_pill: total available powdered pill = 700 (units)

------------------------------------------------------------
Variables:
- x[c]: number of containers of type c to use
  • For each c in C, x[c] is a decision variable (assumed continuous for modeling, but naturally expected to be integer and nonnegative)
  • Domain: x[c] ≥ 0 (units may be “container uses”)

------------------------------------------------------------
Objective:
Maximize total paste output produced by the containers.
- Total_Paste = sum over c in C of (paste_out[c] * x[c])
In other words, maximize: 20*x[small] + 30*x[large]

------------------------------------------------------------
Constraints:
1. Water availability constraint:
   - For water: sum over c in C of (water_req[c] * x[c]) ≤ total_water
   - That is: 10*x[small] + 20*x[large] ≤ 500

2. Powdered pill availability constraint:
   - For pills: sum over c in C of (pill_req[c] * x[c]) ≤ total_pill
   - That is: 15*x[small] + 20*x[large] ≤ 700

------------------------------------------------------------
Notes:
- The units for water and pills are assumed to be consistent throughout the model.
- Although the decision variables x[small] and x[large] are defined here as continuous (floats) per the expected output schema, the context implies that they should be nonnegative integers for a practical implementation.
- If needed, one could include integrality constraints in an implementation.
- This formulation directly maps to typical Python or OR-Tools code using the variables, constraints, and objective defined above.

------------------------------------------------------------
Alternative Version (if fractional container use is not allowed):
- One might explicitly enforce that:
   • x[c] ∈ Z (nonnegative integers)
This additional condition would be added to the “Variables” section if an integer program is required.'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_continuous_model():
    # Create solver for continuous LP (using GLOP)
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Continuous solver not available.")
        return None

    # Parameters
    total_water = 500
    total_pill = 700
    water_req_small = 10
    water_req_large = 20
    pill_req_small = 15
    pill_req_large = 20
    paste_out_small = 20
    paste_out_large = 30

    # Variables: continuous nonnegative decision variables.
    x_small = solver.NumVar(0.0, solver.infinity(), 'x_small')
    x_large = solver.NumVar(0.0, solver.infinity(), 'x_large')

    # Constraints
    # Water constraint: 10*x_small + 20*x_large <= 500
    solver.Add(water_req_small * x_small + water_req_large * x_large <= total_water)
    # Pill constraint: 15*x_small + 20*x_large <= 700
    solver.Add(pill_req_small * x_small + pill_req_large * x_large <= total_pill)

    # Objective: maximize paste production: 20*x_small + 30*x_large
    objective = solver.Objective()
    objective.SetCoefficient(x_small, paste_out_small)
    objective.SetCoefficient(x_large, paste_out_large)
    objective.SetMaximization()

    # Solve the problem
    status = solver.Solve()

    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result['x_small'] = x_small.solution_value()
        result['x_large'] = x_large.solution_value()
        result['objective'] = objective.Value()
    else:
        result['error'] = 'No optimal solution found for continuous model.'

    return result

def solve_integer_model():
    # Create solver for Mixed Integer Programming (using CBC_MIXED_INTEGER_PROGRAMMING)
    solver = pywraplp.Solver.CreateSolver('CBC_MIXED_INTEGER_PROGRAMMING')
    if not solver:
        print("Integer solver not available.")
        return None

    # Parameters
    total_water = 500
    total_pill = 700
    water_req_small = 10
    water_req_large = 20
    pill_req_small = 15
    pill_req_large = 20
    paste_out_small = 20
    paste_out_large = 30

    # Variables: use integer decision variables.
    x_small = solver.IntVar(0, solver.infinity(), 'x_small')
    x_large = solver.IntVar(0, solver.infinity(), 'x_large')

    # Constraints
    # Water constraint: 10*x_small + 20*x_large <= 500
    solver.Add(water_req_small * x_small + water_req_large * x_large <= total_water)
    # Pill constraint: 15*x_small + 20*x_large <= 700
    solver.Add(pill_req_small * x_small + pill_req_large * x_large <= total_pill)

    # Objective: maximize paste production: 20*x_small + 30*x_large
    objective = solver.Objective()
    objective.SetCoefficient(x_small, paste_out_small)
    objective.SetCoefficient(x_large, paste_out_large)
    objective.SetMaximization()

    # Solve the problem
    status = solver.Solve()

    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result['x_small'] = x_small.solution_value()
        result['x_large'] = x_large.solution_value()
        result['objective'] = objective.Value()
    else:
        result['error'] = 'No optimal solution found for integer model.'

    return result

def main():
    print("=== Continuous Model (Fractional Container Use Allowed) ===")
    continuous_result = solve_continuous_model()
    if continuous_result is not None:
        if 'error' in continuous_result:
            print(continuous_result['error'])
        else:
            print("Optimal number of small containers (x_small):", continuous_result['x_small'])
            print("Optimal number of large containers (x_large):", continuous_result['x_large'])
            print("Maximum paste produced:", continuous_result['objective'])
    print("\n=== Integer Model (Discrete Container Use) ===")
    integer_result = solve_integer_model()
    if integer_result is not None:
        if 'error' in integer_result:
            print(integer_result['error'])
        else:
            print("Optimal number of small containers (x_small):", int(integer_result['x_small']))
            print("Optimal number of large containers (x_large):", int(integer_result['x_large']))
            print("Maximum paste produced:", integer_result['objective'])

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
=== Continuous Model (Fractional Container Use Allowed) ===
Optimal number of small containers (x_small): 39.999999999999986
Optimal number of large containers (x_large): 5.000000000000007
Maximum paste produced: 950.0

=== Integer Model (Discrete Container Use) ===
Optimal number of small containers (x_small): 40
Optimal number of large containers (x_large): 5
Maximum paste produced: 950.0
'''

'''Expected Output:
Expected solution

: {'variables': {'NumUsedContainers': [40.0, 5.0]}, 'objective': 950.0}'''

