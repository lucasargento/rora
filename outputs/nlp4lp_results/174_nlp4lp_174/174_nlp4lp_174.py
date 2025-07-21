# Problem Description:
'''Problem description: An office company makes desks and drawers. Each desk requires 40 minutes of assembly and 20 minutes of sanding. Each drawer requires 30 minutes of assembly and 10 minutes of sanding. The company has available 4000 minutes for assembly and 3500 minutes for sanding. If the profit per desk is $100 and the profit per drawer is $90, how many of each should the company make to maximize profit?

Expected Output Schema:
{
  "variables": {
    "NumberOfDesks": "float",
    "NumberOfDrawers": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- Product: set of office products = {Desk, Drawer}

Parameters:
- profit_desk: profit per desk (USD/unit) = 100
- profit_drawer: profit per drawer (USD/unit) = 90
- assembly_time_desk: assembly time required per desk (minutes/unit) = 40
- assembly_time_drawer: assembly time required per drawer (minutes/unit) = 30
- sanding_time_desk: sanding time required per desk (minutes/unit) = 20
- sanding_time_drawer: sanding time required per drawer (minutes/unit) = 10
- max_assembly_time: total available assembly time (minutes) = 4000
- max_sanding_time: total available sanding time (minutes) = 3500

Variables:
- x_desk: number of desks to produce (float ≥ 0) [units]
- x_drawer: number of drawers to produce (float ≥ 0) [units]

Objective:
- Maximize total profit = (profit_desk * x_desk) + (profit_drawer * x_drawer)
  (This equals 100 * x_desk + 90 * x_drawer)

Constraints:
1. Assembly time constraint: (assembly_time_desk * x_desk) + (assembly_time_drawer * x_drawer) ≤ max_assembly_time  
   (i.e., 40 * x_desk + 30 * x_drawer ≤ 4000)
2. Sanding time constraint: (sanding_time_desk * x_desk) + (sanding_time_drawer * x_drawer) ≤ max_sanding_time  
   (i.e., 20 * x_desk + 10 * x_drawer ≤ 3500)
3. Non-negativity constraints: x_desk ≥ 0 and x_drawer ≥ 0

Additional Comments:
- All time parameters are expressed in minutes, and capacity constraints are given in minutes.
- Profits are in USD per unit produced.
- Although production counts are typically integer, the expected output schema declares the decision variables as float.
  
This completes the structured mathematical model using the five-element framework.'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_continuous():
    # Create solver with GLOP for linear programming (continuous variables)
    solver = pywraplp.Solver.CreateSolver("GLOP")
    if not solver:
        print("Could not create GLOP solver for continuous model.")
        return {"message": "Solver creation failed for continuous model."}

    # Decision variables: continuous (float) variables for desks and drawers
    x_desk = solver.NumVar(0.0, solver.infinity(), "x_desk")
    x_drawer = solver.NumVar(0.0, solver.infinity(), "x_drawer")

    # Constraint 1: Assembly time constraint: 40*x_desk + 30*x_drawer <= 4000
    solver.Add(40 * x_desk + 30 * x_drawer <= 4000)

    # Constraint 2: Sanding time constraint: 20*x_desk + 10*x_drawer <= 3500
    solver.Add(20 * x_desk + 10 * x_drawer <= 3500)

    # Objective: maximize profit = 100*x_desk + 90*x_drawer
    objective = solver.Objective()
    objective.SetCoefficient(x_desk, 100)
    objective.SetCoefficient(x_drawer, 90)
    objective.SetMaximization()

    # Solve the problem
    result_status = solver.Solve()
    solution = {}
    if result_status == pywraplp.Solver.OPTIMAL:
        solution["NumberOfDesks"] = x_desk.solution_value()
        solution["NumberOfDrawers"] = x_drawer.solution_value()
        solution["objective"] = objective.Value()
    else:
        solution["message"] = "No optimal solution found (Continuous Model)."
    return solution

def solve_integer():
    # Create solver with CBC for Mixed Integer Programming (integer variables)
    solver = pywraplp.Solver.CreateSolver("CBC")
    if not solver:
        print("Could not create CBC solver for integer model.")
        return {"message": "Solver creation failed for integer model."}

    # Decision variables: integer variables for desks and drawers.
    # Although the expected output schema uses float, production counts are typically integer.
    x_desk = solver.IntVar(0, solver.infinity(), "x_desk")
    x_drawer = solver.IntVar(0, solver.infinity(), "x_drawer")

    # Constraint 1: Assembly time constraint: 40*x_desk + 30*x_drawer <= 4000
    solver.Add(40 * x_desk + 30 * x_drawer <= 4000)

    # Constraint 2: Sanding time constraint: 20*x_desk + 10*x_drawer <= 3500
    solver.Add(20 * x_desk + 10 * x_drawer <= 3500)

    # Objective: maximize profit = 100*x_desk + 90*x_drawer
    objective = solver.Objective()
    objective.SetCoefficient(x_desk, 100)
    objective.SetCoefficient(x_drawer, 90)
    objective.SetMaximization()

    # Solve the problem
    result_status = solver.Solve()
    solution = {}
    if result_status == pywraplp.Solver.OPTIMAL:
        solution["NumberOfDesks"] = x_desk.solution_value()
        solution["NumberOfDrawers"] = x_drawer.solution_value()
        solution["objective"] = objective.Value()
    else:
        solution["message"] = "No optimal solution found (Integer Model)."
    return solution

def main():
    # Solve using the continuous variables formulation
    continuous_solution = solve_continuous()
    # Solve using the integer variables formulation
    integer_solution = solve_integer()

    # Print solutions in a structured way for both implementations
    print("Continuous Model Solution:")
    for key, value in continuous_solution.items():
        print(f"{key}: {value}")

    print("\nInteger Model Solution:")
    for key, value in integer_solution.items():
        print(f"{key}: {value}")

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Continuous Model Solution:
NumberOfDesks: 0.0
NumberOfDrawers: 133.33333333333331
objective: 11999.999999999998

Integer Model Solution:
NumberOfDesks: 1.0
NumberOfDrawers: 132.0
objective: 11980.0
'''

'''Expected Output:
Expected solution

: {'variables': {'NumberOfDesks': 0.0, 'NumberOfDrawers': 133.33333333333334}, 'objective': 12000.0}'''

