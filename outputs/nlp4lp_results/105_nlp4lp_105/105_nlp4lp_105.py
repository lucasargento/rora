# Problem Description:
'''Problem description: A pharmacy makes eye cream and foot cream using two different machines, machine 1 and machine 2. Machine 1 can  make 30 ml of eye cream and 60 ml of foot cream per hour. Machine 2 can make 45 ml of eye cream and 30 ml of foot cream per hour. Furthermore, machine 1 requires 20 ml of distilled water per hour while machine 2 requires 15 ml of distilled water per hour. The pharmacy has available 1200 ml of distilled water. If the pharmacy needs to make at least 1300 ml of eye cream and 1500 ml of foot cream, how many hours should each machine be used to minimize the total time needed?

Expected Output Schema:
{
  "variables": {
    "OperatingTime": {
      "0": "float",
      "1": "float"
    }
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Below is one valid formulation using the five-element structured model.

----------------------------------------------------------------
Sets:
- M: set of machines = {1, 2}

Parameters:
- eyeProd[1] = 30      (ml of eye cream produced per hour by machine 1)
- eyeProd[2] = 45      (ml of eye cream produced per hour by machine 2)
- footProd[1] = 60     (ml of foot cream produced per hour by machine 1)
- footProd[2] = 30     (ml of foot cream produced per hour by machine 2)
- waterUse[1] = 20     (ml of water consumed per hour by machine 1)
- waterUse[2] = 15     (ml of water consumed per hour by machine 2)

- minEyeCream = 1300   (minimum required ml of eye cream)
- minFootCream = 1500  (minimum required ml of foot cream)
- availWater = 1200    (total available ml of distilled water)

Comments:
- All production numbers are in milliliters (ml) per hour.
- Operating times are measured in hours.
- The water constraint uses the same unit (ml).

Variables:
- OperatingTime[i] for each machine i in M, where OperatingTime[i] is a continuous variable representing the number of hours machine i is used.
  • OperatingTime[1] ≥ 0
  • OperatingTime[2] ≥ 0

Objective:
- Minimize TotalTime = OperatingTime[1] + OperatingTime[2]
  (This minimizes the total machine operating time in hours.)

Constraints:
1. Eye Cream Production Constraint:
   - eyeProd[1] * OperatingTime[1] + eyeProd[2] * OperatingTime[2] ≥ minEyeCream
   - (30 * OperatingTime[1] + 45 * OperatingTime[2] ≥ 1300)

2. Foot Cream Production Constraint:
   - footProd[1] * OperatingTime[1] + footProd[2] * OperatingTime[2] ≥ minFootCream
   - (60 * OperatingTime[1] + 30 * OperatingTime[2] ≥ 1500)

3. Water Availability Constraint:
   - waterUse[1] * OperatingTime[1] + waterUse[2] * OperatingTime[2] ≤ availWater
   - (20 * OperatingTime[1] + 15 * OperatingTime[2] ≤ 1200)

----------------------------------------------------------------
This complete model clearly defines the decision variables, objective, and constraints using the five-element framework.'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp
from ortools.sat.python import cp_model

def solve_linear():
    """Solve the problem using ortools.linear_solver (GLOP)."""
    # Create the solver with the GLOP backend.
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Linear solver not available.")
        return None

    # Decision variables: OperatingTime for machine 1 and 2.
    # Variables are continuous and > 0.
    t1 = solver.NumVar(0, solver.infinity(), "t1")  # OperatingTime for machine 1.
    t2 = solver.NumVar(0, solver.infinity(), "t2")  # OperatingTime for machine 2.

    # Add constraints.
    # Eye Cream Production: 30*t1 + 45*t2 >= 1300
    solver.Add(30 * t1 + 45 * t2 >= 1300)

    # Foot Cream Production: 60*t1 + 30*t2 >= 1500
    solver.Add(60 * t1 + 30 * t2 >= 1500)

    # Water Availability: 20*t1 + 15*t2 <= 1200
    solver.Add(20 * t1 + 15 * t2 <= 1200)

    # Objective: minimize the total operating time t1 + t2.
    objective = solver.Objective()
    objective.SetMinimization()
    objective.SetCoefficient(t1, 1)
    objective.SetCoefficient(t2, 1)

    # Solve the problem.
    status = solver.Solve()

    if status != pywraplp.Solver.OPTIMAL:
        print("The linear solver did not find an optimal solution.")
        return None

    solution = {
        "OperatingTime": {
            "0": t1.solution_value(),
            "1": t2.solution_value()
        },
        "objective": objective.Value()
    }
    return solution

def solve_cp():
    """Solve the problem using ortools.sat.python.cp_model.
       Because the CP-SAT solver handles only integer variables,
       we scale the continuous operating times by a factor (scale factor)
       to represent fractions (e.g., hundredths of hours)."""
    model = cp_model.CpModel()
    scale = 100  # scale factor so that t_actual = t / scale (i.e., 0.01 hour resolution)

    # Decision variables: t1 and t2 as integer variables.
    # Upper bound is set arbitrarily (e.g., 100 hours -> 100*scale = 10000).
    t1 = model.NewIntVar(0, 10000, "t1")
    t2 = model.NewIntVar(0, 10000, "t2")

    # Add constraints with scaled variables.
    # Eye Cream Production: 30*(t1/scale) + 45*(t2/scale) >= 1300  -->
    #   30*t1 + 45*t2 >= 1300 * scale
    model.Add(30 * t1 + 45 * t2 >= 1300 * scale)

    # Foot Cream Production: 60*(t1/scale) + 30*(t2/scale) >= 1500  -->
    #   60*t1 + 30*t2 >= 1500 * scale
    model.Add(60 * t1 + 30 * t2 >= 1500 * scale)

    # Water Availability: 20*(t1/scale) + 15*(t2/scale) <= 1200  -->
    #   20*t1 + 15*t2 <= 1200 * scale
    model.Add(20 * t1 + 15 * t2 <= 1200 * scale)

    # Objective: minimize total operating time t1+t2 (in scaled units).
    model.Minimize(t1 + t2)

    # Solve the model.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status != cp_model.OPTIMAL and status != cp_model.FEASIBLE:
        print("The CP-SAT solver did not find an optimal solution.")
        return None

    # Retrieve and scale back the solution.
    solution = {
        "OperatingTime": {
            "0": solver.Value(t1) / scale,
            "1": solver.Value(t2) / scale
        },
        "objective": solver.ObjectiveValue() / scale
    }
    return solution

def main():
    # Solve using the linear solver.
    linear_solution = solve_linear()
    # Solve using the CP-SAT model.
    cp_solution = solve_cp()

    # Print both solutions in a structured way.
    print("Results using ortools.linear_solver (GLOP):")
    if linear_solution is not None:
        print(linear_solution)
    else:
        print("No optimal solution found for the linear model.")

    print("\nResults using ortools.sat.python.cp_model (scaled integer formulation):")
    if cp_solution is not None:
        print(cp_solution)
    else:
        print("No optimal solution found for the CP-SAT model.")

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Results using ortools.linear_solver (GLOP):
{'OperatingTime': {'0': 15.833333333333332, '1': 18.333333333333336}, 'objective': 34.16666666666667}

Results using ortools.sat.python.cp_model (scaled integer formulation):
{'OperatingTime': {'0': 15.83, '1': 18.34}, 'objective': 34.17}
'''

'''Expected Output:
Expected solution

: {'variables': {'OperatingTime': {'0': 15.833333333333334, '1': 18.333333333333332}}, 'objective': 34.166666666666664}'''

