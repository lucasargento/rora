# Problem Description:
'''Problem description: A summer camps does science experiments in two pre filled beakers, beaker 1 and beaker 2. Beaker 1 uses 4 units of flour and 6 units of special liquid to make 5 units of slime. Beaker 2 uses 6 units of flour and 3 units of special liquid to make 3 units of slime.  However, beaker 1 creates 4 units of waste while beaker 2 creates 2 units of waste. The summer camp has available 150 units of flour and 100 units of special liquid. If at most 30 units of waste can be produced, how many of each beaker should be used to maximize the amount of slime produced?

Expected Output Schema:
{
  "variables": {
    "FlourUsedPerBeaker": {
      "0": "float",
      "1": "float"
    }
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Below is the structured mathematical model for the problem using the five‐element framework.

------------------------------------------------
Sets:
• B = {1, 2}  
  (Beaker types: 1 for beaker 1 and 2 for beaker 2)

------------------------------------------------
Parameters:
• flour_b: units of flour used per experiment with beaker b  
  – flour_1 = 4 units per use (beaker 1)  
  – flour_2 = 6 units per use (beaker 2)

• liquid_b: units of special liquid used per experiment with beaker b  
  – liquid_1 = 6 units per use (beaker 1)  
  – liquid_2 = 3 units per use (beaker 2)

• slime_b: units of slime produced per experiment with beaker b  
  – slime_1 = 5 units per use (beaker 1)  
  – slime_2 = 3 units per use (beaker 2)

• waste_b: units of waste produced per experiment with beaker b  
  – waste_1 = 4 units per use (beaker 1)  
  – waste_2 = 2 units per use (beaker 2)

• resource limits (all units are consistent with the given descriptions):  
  – total_flour = 150 units  
  – total_liquid = 100 units  
  – max_waste = 30 units

------------------------------------------------
Variables:
• x_b for b in B, where:
  – x_1 = number of times beaker 1 is used  
  – x_2 = number of times beaker 2 is used  
 Domain: x_b ∈ {0, 1, 2, …} (nonnegative integers)  
  (Note: we assume each usage represents one complete experiment with the beaker)

------------------------------------------------
Objective:
Maximize total slime production (in units) given by:
 TotalSlime = slime_1 * x_1 + slime_2 * x_2  
In other words, maximize 5 * x_1 + 3 * x_2

------------------------------------------------
Constraints:
1. Flour Constraint:  
  flour_1 * x_1 + flour_2 * x_2 ≤ total_flour  
  i.e., 4 * x_1 + 6 * x_2 ≤ 150

2. Special Liquid Constraint:  
  liquid_1 * x_1 + liquid_2 * x_2 ≤ total_liquid  
  i.e., 6 * x_1 + 3 * x_2 ≤ 100

3. Waste Constraint:  
  waste_1 * x_1 + waste_2 * x_2 ≤ max_waste  
  i.e., 4 * x_1 + 2 * x_2 ≤ 30

------------------------------------------------
Notes and Assumptions:
• All resource usage and production values are in “units” as stated in the problem.  
• The decision variables (x_1 and x_2) are assumed to be integer because you cannot use a beaker a fractional number of times.  
• The formulation is directly based on the real-world description with no data simplification or transformation.  

This model is now complete and ready for implementation in a tool such as OR-Tools.'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp
from ortools.sat.python import cp_model

def solve_with_linear_solver():
    # Create the MIP solver using SCIP backend.
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        print("Linear solver not available.")
        return None

    # Decision variables: integer and non-negative.
    x1 = solver.IntVar(0, solver.infinity(), 'x1')  # number of times beaker 1 is used
    x2 = solver.IntVar(0, solver.infinity(), 'x2')  # number of times beaker 2 is used

    # Parameters definition (resources and outputs)
    # For beaker 1:
    flour_1, liquid_1, slime_1, waste_1 = 4, 6, 5, 4
    # For beaker 2:
    flour_2, liquid_2, slime_2, waste_2 = 6, 3, 3, 2

    # Resource limits:
    total_flour = 150
    total_liquid = 100
    max_waste = 30

    # Constraints
    # 1. Flour: 4*x1 + 6*x2 <= 150
    solver.Add(flour_1 * x1 + flour_2 * x2 <= total_flour)
    # 2. Special Liquid: 6*x1 + 3*x2 <= 100
    solver.Add(liquid_1 * x1 + liquid_2 * x2 <= total_liquid)
    # 3. Waste: 4*x1 + 2*x2 <= 30
    solver.Add(waste_1 * x1 + waste_2 * x2 <= max_waste)

    # Objective: maximize slime production = 5*x1 + 3*x2
    solver.Maximize(slime_1 * x1 + slime_2 * x2)

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "variables": {
                "FlourUsedPerBeaker": {
                    "0": x1.solution_value(),
                    "1": x2.solution_value()
                }
            },
            "objective": solver.Objective().Value()
        }
    else:
        result = {"message": "No optimal solution found using linear solver."}
    return result

def solve_with_cp_model():
    # Create the CP model.
    model = cp_model.CpModel()

    # Decision variables: integer by default in cp_model.
    x1 = model.NewIntVar(0, 1000, 'x1')  # arbitrary high upper bound
    x2 = model.NewIntVar(0, 1000, 'x2')

    # Parameters definition (resources and outputs)
    flour_1, liquid_1, slime_1, waste_1 = 4, 6, 5, 4
    flour_2, liquid_2, slime_2, waste_2 = 6, 3, 3, 2

    total_flour = 150
    total_liquid = 100
    max_waste = 30

    # Constraints
    model.Add(flour_1 * x1 + flour_2 * x2 <= total_flour)
    model.Add(liquid_1 * x1 + liquid_2 * x2 <= total_liquid)
    model.Add(waste_1 * x1 + waste_2 * x2 <= max_waste)

    # Objective: maximize 5*x1 + 3*x2.
    # In CP-SAT, we must define a variable for the objective if we want to maximize.
    objective_var = model.NewIntVar(0, 10000, 'objective')
    model.Add(objective_var == slime_1 * x1 + slime_2 * x2)
    model.Maximize(objective_var)

    # Solve the model using CpSolver.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        result = {
            "variables": {
                "FlourUsedPerBeaker": {
                    "0": solver.Value(x1),
                    "1": solver.Value(x2)
                }
            },
            "objective": solver.Value(objective_var)
        }
    else:
        result = {"message": "No optimal solution found using CP model."}
    return result

def main():
    linear_res = solve_with_linear_solver()
    cp_res = solve_with_cp_model()

    print("Results:")
    print("----------")
    print("Linear Solver Implementation:")
    for key, value in linear_res.items():
        print(f"{key}: {value}")

    print("\nCP-SAT Model Implementation:")
    for key, value in cp_res.items():
        print(f"{key}: {value}")

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Results:
----------
Linear Solver Implementation:
variables: {'FlourUsedPerBeaker': {'0': -0.0, '1': 15.0}}
objective: 45.0

CP-SAT Model Implementation:
variables: {'FlourUsedPerBeaker': {'0': 0, '1': 15}}
objective: 45
'''

'''Expected Output:
Expected solution

: {'variables': {'FlourUsedPerBeaker': {'0': 0.0, '1': 15.0}}, 'objective': 45.0}'''

