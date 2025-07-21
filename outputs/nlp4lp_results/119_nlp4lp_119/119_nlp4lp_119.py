# Problem Description:
'''Problem description: A chemistry teacher teaches her students two experiments, experiment 1 and experiment 2. In experiment 1, 3 units of the red liquid and 4 units of the blue liquid mix to create 5 units of green gas. In experiment 2, 5 units of the red liquid and 3 units of the blue liquid mix to create 6 units of the green gas. In addition, experiment 1 produces 1 units of smelly gas while experiment 2 produces 2 units of smelly gas.  The lab has available 80 units of red liquid and 70 units of blue liquid. If at most 10 units of smelly gas can be produced, how many experiments of each should be done to maximize the total amount of green gas produced?

Expected Output Schema:
{
  "variables": {
    "ExperimentPerformed": [
      "float"
    ]
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- E: set of experiments = {1, 2}

Parameters:
- red_consumption[e]: units of red liquid consumed per experiment e
   • red_consumption[1] = 3 (units per run of experiment 1)
   • red_consumption[2] = 5 (units per run of experiment 2)
- blue_consumption[e]: units of blue liquid consumed per experiment e
   • blue_consumption[1] = 4 (units per run of experiment 1)
   • blue_consumption[2] = 3 (units per run of experiment 2)
- green_production[e]: units of green gas produced per experiment e
   • green_production[1] = 5 (units per run of experiment 1)
   • green_production[2] = 6 (units per run of experiment 2)
- smelly_production[e]: units of smelly gas produced per experiment e
   • smelly_production[1] = 1 (unit per run of experiment 1)
   • smelly_production[2] = 2 (units per run of experiment 2)
- available_red: total available red liquid = 80 units
- available_blue: total available blue liquid = 70 units
- max_smelly: maximum allowed total smelly gas = 10 units

Variables:
- x[e]: number of times experiment e is performed [integer, x[e] ≥ 0 for all e in E]
  (x[1] corresponds to experiment 1; x[2] corresponds to experiment 2)

Objective:
- Maximize TotalGreen = sum over e in E of (green_production[e] * x[e])
  That is: Maximize (5*x[1] + 6*x[2])

Constraints:
1. Red Liquid Constraint:
   - sum over e in E of (red_consumption[e] * x[e]) ≤ available_red
   - 3*x[1] + 5*x[2] ≤ 80

2. Blue Liquid Constraint:
   - sum over e in E of (blue_consumption[e] * x[e]) ≤ available_blue
   - 4*x[1] + 3*x[2] ≤ 70

3. Smelly Gas Constraint:
   - sum over e in E of (smelly_production[e] * x[e]) ≤ max_smelly
   - 1*x[1] + 2*x[2] ≤ 10

Comments:
- The decision variables x[e] are assumed to be integer since experiments are discrete activities.
- Units are consistent: Liquid units for red and blue, gas units for green and smelly.
- The objective is to maximize the total units of green gas produced while not exceeding materials or environmental constraints.

Expected Output Schema:
{
  "variables": {
    "ExperimentPerformed": [
      "float"
    ]
  },
  "objective": "float"
}'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

# Implementation of the optimization problem using OR-Tools Linear Solver
def solve_linear_model():
    # Create the solver using CBC_MIXED_INTEGER_PROGRAMMING
    solver = pywraplp.Solver.CreateSolver('CBC_MIXED_INTEGER_PROGRAMMING')
    if not solver:
        print("Solver not created.")
        return None

    # Sets: Experiments 1 and 2.
    experiments = [1, 2]

    # Parameters for each experiment
    red_consumption = {1: 3, 2: 5}      # Red liquid consumption per experiment
    blue_consumption = {1: 4, 2: 3}     # Blue liquid consumption per experiment
    green_production = {1: 5, 2: 6}     # Green gas produced per experiment
    smelly_production = {1: 1, 2: 2}    # Smelly gas produced per experiment

    # Available resources and bounds
    available_red = 80      # total available red liquid
    available_blue = 70     # total available blue liquid
    max_smelly = 10         # maximum allowed smelly gas

    # Decision Variables: number of times each experiment is performed (integer variables, >= 0)
    x = {}
    for e in experiments:
        # Using integer decision variables
        x[e] = solver.IntVar(0, solver.infinity(), f'x_{e}')

    # Constraints
    # 1. Red Liquid Constraint: 3*x[1] + 5*x[2] <= 80
    solver.Add(red_consumption[1] * x[1] + red_consumption[2] * x[2] <= available_red)

    # 2. Blue Liquid Constraint: 4*x[1] + 3*x[2] <= 70
    solver.Add(blue_consumption[1] * x[1] + blue_consumption[2] * x[2] <= available_blue)

    # 3. Smelly Gas Constraint: 1*x[1] + 2*x[2] <= 10
    solver.Add(smelly_production[1] * x[1] + smelly_production[2] * x[2] <= max_smelly)

    # Objective: Maximize total green gas production = 5*x[1] + 6*x[2]
    objective = solver.Objective()
    objective.SetCoefficient(x[1], green_production[1])
    objective.SetCoefficient(x[2], green_production[2])
    objective.SetMaximization()

    # Solve the model and return the results
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        solution = {
            "variables": {"ExperimentPerformed": [x[1].solution_value(), x[2].solution_value()]},
            "objective": objective.Value()
        }
        return solution
    else:
        print("The problem does not have an optimal solution.")
        return None

def main():
    # Since the problem has only one formulation, we call the linear model solver
    result_linear = solve_linear_model()

    # Structuring the results nicely for display:
    if result_linear is not None:
        print("Linear Solver Model Result:")
        print(result_linear)
    else:
        print("Linear Solver Model: No feasible solution found.")

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Linear Solver Model Result:
{'variables': {'ExperimentPerformed': [10.0, 0.0]}, 'objective': 50.0}
'''

'''Expected Output:
Expected solution

: {'variables': {'ExperimentPerformed': [1.0, 1.0]}, 'objective': 11.0}'''

