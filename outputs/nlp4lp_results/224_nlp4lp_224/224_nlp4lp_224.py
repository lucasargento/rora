# Problem Description:
'''Problem description: There are two ways to extract a metal from mined ores. The first way is to use process J and the second is process P. Process J can extract 5 units of metal using 8 units of water and produces 3 units of pollution. Process P can extract 9 units of metal using 6 units of water and produces 5 units of pollution. There can be at most 1500 units of water 1350 units of pollution. How many of each type of processes should be performed to maximize the amount of metal extracted?

Expected Output Schema:
{
  "variables": {
    "ProcessUnit": {
      "0": "float",
      "1": "float"
    }
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- P: set of processes = {J, P}

Parameters:
- metal_p: amount of metal extracted per operation of process p [units of metal]
  • metal_J = 5, metal_P = 9
- water_p: water used per operation of process p [units of water]
  • water_J = 8, water_P = 6
- pollution_p: pollution produced per operation of process p [units of pollution]
  • pollution_J = 3, pollution_P = 5
- max_water: maximum available water [units of water] = 1500
- max_pollution: maximum allowed pollution [units of pollution] = 1350

Variables:
- x_p: number of operations to perform for process p [real number ≥ 0]
  • x_J: operations under process J (can be nonnegative float; if process counts must be integer, then restrict accordingly)
  • x_P: operations under process P (can be nonnegative float; if process counts must be integer, then restrict accordingly)
  
(In the expected output schema, these are represented as ProcessUnit { "0": x_J, "1": x_P } with float values.)

Objective:
- Maximize total metal extracted defined as:
  TotalMetal = metal_J * x_J + metal_P * x_P
  (Units: units of metal)

Constraints:
1. Water usage constraint:
   water_J * x_J + water_P * x_P ≤ max_water
   (8 * x_J + 6 * x_P ≤ 1500)

2. Pollution constraint:
   pollution_J * x_J + pollution_P * x_P ≤ max_pollution
   (3 * x_J + 5 * x_P ≤ 1350)

Note: All parameters are in consistent units as described (units of water, metal, and pollution). The model assumes that process counts (x_J and x_P) can be fractional; if only whole process operations are allowed, then x_J and x_P should be declared as integer variables.'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_continuous():
    """Solve the problem with continuous (nonnegative float) variables using OR-Tools linear solver."""
    # Create the solver with the GLOP backend (linear programming)
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Could not create solver for continuous model.")
        return None

    # Parameters
    metal_J = 5
    metal_P = 9
    water_J = 8
    water_P = 6
    pollution_J = 3
    pollution_P = 5
    max_water = 1500
    max_pollution = 1350

    # Decision Variables (continuous)
    x_J = solver.NumVar(0.0, solver.infinity(), 'x_J')
    x_P = solver.NumVar(0.0, solver.infinity(), 'x_P')

    # Objective: Maximize total metal extracted = 5*x_J + 9*x_P
    solver.Maximize(metal_J * x_J + metal_P * x_P)

    # Constraints
    # Water constraint: 8 * x_J + 6 * x_P <= 1500
    solver.Add(water_J * x_J + water_P * x_P <= max_water)
    # Pollution constraint: 3 * x_J + 5 * x_P <= 1350
    solver.Add(pollution_J * x_J + pollution_P * x_P <= max_pollution)

    # Solve the model
    status = solver.Solve()

    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "ProcessUnit": {
                "0": x_J.solution_value(),  # continuous value for process J
                "1": x_P.solution_value()   # continuous value for process P
            },
            "objective": solver.Objective().Value()
        }
    else:
        result = {"error": "The continuous model did not find an optimal solution."}

    return result

def solve_integer():
    """Solve the problem with integer variables using OR-Tools linear solver."""
    # Create the solver with the CBC backend for Mixed Integer Programming.
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Could not create solver for integer model.")
        return None

    # Parameters
    metal_J = 5
    metal_P = 9
    water_J = 8
    water_P = 6
    pollution_J = 3
    pollution_P = 5
    max_water = 1500
    max_pollution = 1350

    # Decision Variables (integer, nonnegative)
    x_J = solver.IntVar(0, solver.infinity(), 'x_J')
    x_P = solver.IntVar(0, solver.infinity(), 'x_P')

    # Objective: Maximize metal extracted = 5*x_J + 9*x_P
    solver.Maximize(metal_J * x_J + metal_P * x_P)

    # Constraints
    solver.Add(water_J * x_J + water_P * x_P <= max_water)       # Water usage constraint
    solver.Add(pollution_J * x_J + pollution_P * x_P <= max_pollution)  # Pollution constraint

    # Solve the model
    status = solver.Solve()

    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "ProcessUnit": {
                "0": float(x_J.solution_value()),  # convert integer solution to float for consistency
                "1": float(x_P.solution_value())
            },
            "objective": solver.Objective().Value()
        }
    else:
        result = {"error": "The integer model did not find an optimal solution."}

    return result

def main():
    continuous_result = solve_continuous()
    integer_result = solve_integer()

    print("Continuous Model Result:")
    print(continuous_result)
    print("\nInteger Model Result:")
    print(integer_result)

if __name__ == "__main__":
    main()

'''Execution Results:
SUCCESS:
Continuous Model Result:
{'ProcessUnit': {'0': 0.0, '1': 249.99999999999994}, 'objective': 2249.9999999999995}

Integer Model Result:
{'ProcessUnit': {'0': 0.0, '1': 250.0}, 'objective': 2250.0}
'''

'''Expected Output:
Expected solution

: {'variables': {'ProcessUnit': {'0': 0.0, '1': 250.0}}, 'objective': 2250.0}'''

