# Problem Description:
'''Problem description: A patient is undergoing radiation treatment involving two beams, Beam 1 and Beam 2. Beam 1 delivers a dose of 0.3 units of medicine per minute to the benign area of the pancreas and 0.2 units of medicine per minute to the benign area of the skin. Beam 2 delivers 0.2 units of medicine per minute to the benign area of the pancreas and 0.1 units of medicine per minute to the benign area of the skin.  In addition, beam 1 delivers 0.6 units of medicine per minute to the tumor and beam 2 delivers 0.4 units of medicine per minute to the tumor. At most 4 units of medicine should be received by the skin and at least 3 units of medicine should be delivered to the tumor.  How many minutes of each beam should be used to minimize the total radiation received by the pancreas?

Expected Output Schema:
{
  "variables": {
    "MinutesBeam1": "float",
    "MinutesBeam2": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- B: set of beams = {Beam1, Beam2}

Parameters:
- pancreas_rate: dose delivered to the pancreas per minute
  - For Beam1: 0.3 [units/minute]
  - For Beam2: 0.2 [units/minute]
- skin_rate: dose delivered to the skin per minute
  - For Beam1: 0.2 [units/minute]
  - For Beam2: 0.1 [units/minute]
- tumor_rate: dose delivered to the tumor per minute
  - For Beam1: 0.6 [units/minute]
  - For Beam2: 0.4 [units/minute]
- max_skin_dose: maximum dose allowed for the skin = 4 [units]
- min_tumor_dose: minimum dose required for the tumor = 3 [units]

Variables:
- MinutesBeam1: continuous variable representing the number of minutes to use Beam1 [minutes, ≥ 0]
- MinutesBeam2: continuous variable representing the number of minutes to use Beam2 [minutes, ≥ 0]

Objective:
- Minimize total dose to the pancreas = 0.3 * MinutesBeam1 + 0.2 * MinutesBeam2

Constraints:
1. Skin dose constraint:
   - 0.2 * MinutesBeam1 + 0.1 * MinutesBeam2 ≤ max_skin_dose
2. Tumor dose constraint:
   - 0.6 * MinutesBeam1 + 0.4 * MinutesBeam2 ≥ min_tumor_dose

Notes:
- All units are assumed to be consistent (dose units per minute and minutes for time).
- The decision variables (MinutesBeam1 and MinutesBeam2) are continuous, non-negative values.
- The model aims to minimize the harm to the pancreas by reducing its radiation exposure while satisfying the treatment requirements for the skin and tumor.

Expected Output Schema:
{
  "variables": {
    "MinutesBeam1": "float",
    "MinutesBeam2": "float"
  },
  "objective": "float"
}'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_with_linear_solver():
    # Create the solver using GLOP as the linear programming solver.
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        return None, "Linear solver not created."

    # Variables: MinutesBeam1 and MinutesBeam2 (continuous and non-negative)
    minutes_beam1 = solver.NumVar(0.0, solver.infinity(), 'MinutesBeam1')
    minutes_beam2 = solver.NumVar(0.0, solver.infinity(), 'MinutesBeam2')

    # Parameters:
    # Rates for pancreas, skin, and tumor per minute for each beam.
    # Beam1: pancreas_rate = 0.3, skin_rate = 0.2, tumor_rate = 0.6
    # Beam2: pancreas_rate = 0.2, skin_rate = 0.1, tumor_rate = 0.4
    max_skin_dose = 4.0
    min_tumor_dose = 3.0

    # Constraints:
    # 1. Skin dose constraint: 0.2 * MinutesBeam1 + 0.1 * MinutesBeam2 ≤ 4
    skin_constraint = solver.Add(0.2 * minutes_beam1 + 0.1 * minutes_beam2 <= max_skin_dose)

    # 2. Tumor dose constraint: 0.6 * MinutesBeam1 + 0.4 * MinutesBeam2 ≥ 3
    tumor_constraint = solver.Add(0.6 * minutes_beam1 + 0.4 * minutes_beam2 >= min_tumor_dose)

    # Objective:
    # Minimize total dose to the pancreas = 0.3 * MinutesBeam1 + 0.2 * MinutesBeam2
    objective = solver.Objective()
    objective.SetCoefficient(minutes_beam1, 0.3)
    objective.SetCoefficient(minutes_beam2, 0.2)
    objective.SetMinimization()

    # Solve the model
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        solution = {
            "MinutesBeam1": minutes_beam1.solution_value(),
            "MinutesBeam2": minutes_beam2.solution_value(),
            "objective": objective.Value()
        }
        return solution, None
    else:
        return None, "The problem does not have an optimal solution."

def main():
    results = {}

    # Model using the linear solver approach.
    solution_linear, error_linear = solve_with_linear_solver()
    if solution_linear:
        results["LinearSolverModel"] = solution_linear
    else:
        results["LinearSolverModel"] = {"error": error_linear}

    # Since the problem is linear, only one formulation (linear programming) is implemented.
    # Print results in a structured way.
    print("Results:")
    for model_name, result in results.items():
        print(f"{model_name}:")
        for key, value in result.items():
            print(f"  {key}: {value}")
        print("")

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Results:
LinearSolverModel:
  MinutesBeam1: 0.0
  MinutesBeam2: 7.499999999999999
  objective: 1.5

'''

'''Expected Output:
Expected solution

: {'variables': {'MinutesBeam1': 0.0, 'MinutesBeam2': 7.5}, 'objective': 1.5}'''

