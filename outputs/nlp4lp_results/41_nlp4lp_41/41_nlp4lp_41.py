# Problem Description:
'''Problem description: A woodshop can purchase two types of saws, a miter saw and a circular saw. A miter saw can cut 50 planks of wood and produces 60 units of sawdust per day. A circular saw can cut 70 planks of wood and produces 100 units of sawdust per day. The woodshop must cut at least 1500 planks of wood per day. However, to avoid too much pollution in the woodshop they can produce at most 2000 units of sawdust per day. How many of each type of saw should be purchased to minimize the total number of saws needed?

Expected Output Schema:
{
  "variables": {
    "NumberOfSaws": {
      "0": "float",
      "1": "float"
    }
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- SawTypes: {Miter, Circular}

Parameters:
- cuts_per_day:
  - Miter: 50 planks per saw per day
  - Circular: 70 planks per saw per day
- sawdust_per_day:
  - Miter: 60 units of sawdust per saw per day
  - Circular: 100 units of sawdust per saw per day
- required_planks: 1500 planks per day (minimum)
- max_sawdust: 2000 units of sawdust per day (maximum)

Variables:
- x_Miter: number of miter saws purchased [integer, ≥ 0]
- x_Circular: number of circular saws purchased [integer, ≥ 0]

Objective:
- Minimize total_saws = x_Miter + x_Circular

Constraints:
- Plank Cutting Constraint: (50 * x_Miter) + (70 * x_Circular) ≥ 1500  
  (This ensures the woodshop cuts at least 1500 planks per day.)
- Sawdust Production Constraint: (60 * x_Miter) + (100 * x_Circular) ≤ 2000  
  (This ensures the woodshop produces at most 2000 units of sawdust per day.)

--------------------------------------------------

For reference, the expected output schema in JSON format is structured as follows:

{
  "variables": {
    "NumberOfSaws": {
      "0": "x_Miter as float (or integer)",
      "1": "x_Circular as float (or integer)"
    }
  },
  "objective": "total_saws as float (or integer)"
}'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp
import json

def solve_linear_programming():
    # Create the solver using CBC backend.
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Solver not created.")
        return None

    # Define variables.
    # x_miter: number of miter saws purchased [integer, >= 0].
    # x_circular: number of circular saws purchased [integer, >= 0].
    x_miter = solver.IntVar(0, solver.infinity(), 'x_miter')
    x_circular = solver.IntVar(0, solver.infinity(), 'x_circular')

    # Define constraints.
    # Plank Cutting Constraint: 50*x_miter + 70*x_circular >= 1500.
    solver.Add(50 * x_miter + 70 * x_circular >= 1500)
    # Sawdust Production Constraint: 60*x_miter + 100*x_circular <= 2000.
    solver.Add(60 * x_miter + 100 * x_circular <= 2000)

    # Define objective: Minimize the total number of saws purchased.
    solver.Minimize(x_miter + x_circular)

    # Solve the model.
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        # Build the solution dictionary following the expected JSON schema.
        solution = {
            "variables": {
                "NumberOfSaws": {
                    "0": x_miter.solution_value(),
                    "1": x_circular.solution_value()
                }
            },
            "objective": solver.Objective().Value()
        }
        return solution
    else:
        print("No optimal solution found for the Linear Programming model.")
        return None

def main():
    # Run the Linear Programming version.
    lp_solution = solve_linear_programming()

    # Print results in a structured JSON format.
    print("Linear Programming Model Results:")
    if lp_solution is not None:
        print(json.dumps(lp_solution, indent=2))
    else:
        print("No solution available.")
    
if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Linear Programming Model Results:
{
  "variables": {
    "NumberOfSaws": {
      "0": 15.0,
      "1": 11.0
    }
  },
  "objective": 26.0
}
'''

'''Expected Output:
Expected solution

: {'variables': {'NumberOfSaws': {'0': 15.0, '1': 11.0}}, 'objective': 26.0}'''

