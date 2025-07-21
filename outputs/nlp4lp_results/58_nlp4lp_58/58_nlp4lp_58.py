# Problem Description:
'''Problem description: In order to make carbon dioxide, wood is burned using two processes, with a catalyst and without a catalyst. The process with a catalyst requires 10 units of wood and 20 units of oxygen to make 15 units of carbon dioxide. The process without a catalyst requires 15 units of wood and 12 units of oxygen to make 18 units of carbon dioxide. There are 300 units of wood and 300 units of oxygen available. How many of each process should be used to maximize the amount of carbon dioxide produced?

Expected Output Schema:
{
  "variables": {
    "ProcessUsage": {
      "0": "float",
      "1": "float"
    }
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Below is a complete and self-contained mathematical model following the five-element structure.

─────────────────────────────  
Sets:
• P: set of processes = {0, 1}
  – 0 denotes the process with a catalyst.
  – 1 denotes the process without a catalyst.

─────────────────────────────  
Parameters:
• wood_required[p]:
  – For p = 0 (with catalyst): 10 units of wood per process run.
  – For p = 1 (without catalyst): 15 units of wood per process run.
• oxygen_required[p]:
  – For p = 0: 20 units of oxygen per process run.
  – For p = 1: 12 units of oxygen per process run.
• CO2_produced[p]:
  – For p = 0: 15 units of carbon dioxide produced per process run.
  – For p = 1: 18 units of carbon dioxide produced per process run.
• total_wood: total available wood = 300 units.
• total_oxygen: total available oxygen = 300 units.

─────────────────────────────  
Variables:
• Let x[p] represent the number of times process p is used.
  – x[p] must be a nonnegative number. (In many practical cases x[p] would be integer if processes cannot be fractional.)
  For clarity, we denote:
    – x[0] = number of runs using the catalyst.
    – x[1] = number of runs without the catalyst.

─────────────────────────────  
Objective:
• Maximize total carbon dioxide produced.
  This is given by:
    Total_CO2 = CO2_produced[0]*x[0] + CO2_produced[1]*x[1]
             = 15*x[0] + 18*x[1].

─────────────────────────────  
Constraints:
1. Wood Constraint:
   The wood used by both processes cannot exceed the available wood.
     => wood_required[0]*x[0] + wood_required[1]*x[1] ≤ total_wood
     => 10*x[0] + 15*x[1] ≤ 300.
2. Oxygen Constraint:
   The oxygen used by both processes cannot exceed the available oxygen.
     => oxygen_required[0]*x[0] + oxygen_required[1]*x[1] ≤ total_oxygen
     => 20*x[0] + 12*x[1] ≤ 300.

─────────────────────────────  
Below is the model expressed in a JSON format matching the expected output schema:

{
  "variables": {
    "ProcessUsage": {
      "0": "float",
      "1": "float"
    }
  },
  "objective": "float"
}

In an implementation, x[0] and x[1] (or ProcessUsage[0] and ProcessUsage[1]) would be the decision variables, and the objective would be defined as 15*x[0] + 18*x[1] while ensuring that 10*x[0] + 15*x[1] ≤ 300 and 20*x[0] + 12*x[1] ≤ 300.'''

# Generated Code:
#!/usr/bin/env python3
"""
This script implements the optimization problem using Google OR-Tools.
It solves the following problem:
    - Two processes are available to produce carbon dioxide by burning wood.
    - Process 0 (with catalyst): requires 10 wood and 20 oxygen to produce 15 CO2.
    - Process 1 (without catalyst): requires 15 wood and 12 oxygen to produce 18 CO2.
    - Total resources: 300 wood and 300 oxygen.
The goal is to maximize the total CO2 produced.
    
Two versions are implemented:
1. Continuous model: decision variables can be fractional.
2. Integer model: decision variables are required to be integers.
Both models are solved separately using OR-Tools' linear solver.
"""

from ortools.linear_solver import pywraplp

def solve_continuous_model():
    # Create a solver using the GLOP backend for linear programming.
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Could not create solver for continuous model.")
        return None

    # Decision variables: ProcessUsage[0] and ProcessUsage[1] as continuous (nonnegative).
    x0 = solver.NumVar(0.0, solver.infinity(), 'ProcessUsage_0')  # Process with catalyst
    x1 = solver.NumVar(0.0, solver.infinity(), 'ProcessUsage_1')  # Process without catalyst

    # Parameters:
    # Wood requirements and oxygen requirements.
    wood_req = [10, 15]
    oxygen_req = [20, 12]
    CO2_prod = [15, 18]
    total_wood = 300
    total_oxygen = 300

    # Define Constraints.
    # Wood constraint: 10*x0 + 15*x1 <= 300.
    solver.Add(wood_req[0] * x0 + wood_req[1] * x1 <= total_wood)
    # Oxygen constraint: 20*x0 + 12*x1 <= 300.
    solver.Add(oxygen_req[0] * x0 + oxygen_req[1] * x1 <= total_oxygen)

    # Objective: Maximize CO2 production: 15*x0 + 18*x1.
    objective = solver.Objective()
    objective.SetCoefficient(x0, CO2_prod[0])
    objective.SetCoefficient(x1, CO2_prod[1])
    objective.SetMaximization()

    status = solver.Solve()

    solution = {}
    if status == pywraplp.Solver.OPTIMAL:
        solution['ProcessUsage'] = {
            '0': x0.solution_value(),
            '1': x1.solution_value()
        }
        solution['objective'] = objective.Value()
    else:
        print("The continuous model does not have an optimal solution.")
        solution = None

    return solution


def solve_integer_model():
    # Create a solver with CBC_MIXED_INTEGER_PROGRAMMING backend for integer programs.
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Could not create solver for integer model.")
        return None

    # Decision variables: ProcessUsage[0] and ProcessUsage[1] as integers (nonnegative).
    x0 = solver.IntVar(0, solver.infinity(), 'ProcessUsage_0')  # Process with catalyst
    x1 = solver.IntVar(0, solver.infinity(), 'ProcessUsage_1')  # Process without catalyst

    # Parameters:
    wood_req = [10, 15]
    oxygen_req = [20, 12]
    CO2_prod = [15, 18]
    total_wood = 300
    total_oxygen = 300

    # Constraints:
    # Wood constraint: 10*x0 + 15*x1 <= 300.
    solver.Add(wood_req[0] * x0 + wood_req[1] * x1 <= total_wood)
    # Oxygen constraint: 20*x0 + 12*x1 <= 300.
    solver.Add(oxygen_req[0] * x0 + oxygen_req[1] * x1 <= total_oxygen)

    # Objective: Maximize CO2 production: 15*x0 + 18*x1.
    objective = solver.Objective()
    objective.SetCoefficient(x0, CO2_prod[0])
    objective.SetCoefficient(x1, CO2_prod[1])
    objective.SetMaximization()

    status = solver.Solve()

    solution = {}
    if status == pywraplp.Solver.OPTIMAL:
        solution['ProcessUsage'] = {
            '0': x0.solution_value(),
            '1': x1.solution_value()
        }
        solution['objective'] = objective.Value()
    else:
        print("The integer model does not have an optimal solution.")
        solution = None

    return solution


def main():
    print("Solving the continuous model (variables can be fractional):")
    cont_solution = solve_continuous_model()
    if cont_solution:
        print("Continuous Model Solution:")
        print("ProcessUsage[0] (with catalyst) =", cont_solution['ProcessUsage']['0'])
        print("ProcessUsage[1] (without catalyst) =", cont_solution['ProcessUsage']['1'])
        print("Total CO2 produced =", cont_solution['objective'])
    else:
        print("No optimal solution found for continuous model.")

    print("\n------------------------------------\n")
    print("Solving the integer model (variables are integers):")
    int_solution = solve_integer_model()
    if int_solution:
        print("Integer Model Solution:")
        print("ProcessUsage[0] (with catalyst) =", int_solution['ProcessUsage']['0'])
        print("ProcessUsage[1] (without catalyst) =", int_solution['ProcessUsage']['1'])
        print("Total CO2 produced =", int_solution['objective'])
    else:
        print("No optimal solution found for integer model.")


if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Solving the continuous model (variables can be fractional):
Continuous Model Solution:
ProcessUsage[0] (with catalyst) = 5.0000000000000036
ProcessUsage[1] (without catalyst) = 16.666666666666664
Total CO2 produced = 375.0

------------------------------------

Solving the integer model (variables are integers):
Integer Model Solution:
ProcessUsage[0] (with catalyst) = 3.0
ProcessUsage[1] (without catalyst) = 18.0
Total CO2 produced = 369.0
'''

'''Expected Output:
Expected solution

: {'variables': {'ProcessUsage': {'0': 5.0, '1': 16.666666666666668}}, 'objective': 375.0}'''

