# Problem Description:
'''Problem description: An airport buys two types of vehicles, a 4-wheeler and 3-wheeler, to help move luggage. A 4-wheeler vehicle can move 60 luggage per day and produces 30 units of pollutant per day. A 3-wheeler vehicle can move 40 luggage per day and produces 15 units of pollutant per day. The airport needs to be able to move at least 1000 luggage per day. To avoid over-polluting the airport, they can produce at most 430 units of pollutant per day. How many of each vehicle should the airport buy to minimize the total number of vehicles needed.  

Expected Output Schema:
{
  "variables": {
    "NumberOfVehicles": {
      "0": "float",
      "1": "float"
    }
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- V: set of vehicle types = {4-wheel, 3-wheel}

Parameters:
- luggage_capacity[4-wheel] = 60 (luggage moved per day per 4-wheeler)
- luggage_capacity[3-wheel] = 40 (luggage moved per day per 3-wheeler)
- pollutant[4-wheel] = 30 (pollutant units produced per day per 4-wheeler)
- pollutant[3-wheel] = 15 (pollutant units produced per day per 3-wheeler)
- required_luggage = 1000 (minimum luggage to be moved per day)
- max_pollutant = 430 (maximum pollutant allowed per day)

Variables:
- x[v] for each v in V: number of vehicles of type v to buy [integer, nonnegative]
  (Interpretation: x["4-wheel"] is the number of 4-wheeler vehicles; x["3-wheel"] is the number of 3-wheeler vehicles.)

Objective:
- Minimize the total number of vehicles, expressed as: 
  TotalVehicles = x["4-wheel"] + x["3-wheel"]

Constraints:
1. Luggage movement requirement:
  (luggage_capacity[4-wheel] * x["4-wheel"]) + (luggage_capacity[3-wheel] * x["3-wheel"]) ≥ required_luggage
  (This ensures that at least 1000 luggage items are moved per day.)

2. Pollutant limit requirement:
  (pollutant[4-wheel] * x["4-wheel"]) + (pollutant[3-wheel] * x["3-wheel"]) ≤ max_pollutant
  (This ensures that the total pollutant produced does not exceed 430 units per day.)

--------------------------------------------------
Expected Output Schema:
{
  "variables": {
    "NumberOfVehicles": {
      "0": "float",  // corresponds to number of 4-wheelers (decision variable x['4-wheel'])
      "1": "float"   // corresponds to number of 3-wheelers (decision variable x['3-wheel'])
    }
  },
  "objective": "float"  // total number of vehicles
}'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp
from ortools.sat.python import cp_model
import json

def solve_with_linear_solver():
    # Create the solver using CBC Mixed Integer Programming
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Linear solver not available.")
        return None

    # Parameters
    luggage_capacity_4 = 60
    luggage_capacity_3 = 40
    pollutant_4 = 30
    pollutant_3 = 15
    required_luggage = 1000
    max_pollutant = 430

    # Decision Variables (nonnegative integers)
    x4 = solver.IntVar(0, solver.infinity(), 'x_4wheel')  # Number of 4-wheelers
    x3 = solver.IntVar(0, solver.infinity(), 'x_3wheel')  # Number of 3-wheelers

    # Constraints
    # Luggage movement constraint: 60*x4 + 40*x3 >= 1000
    solver.Add(luggage_capacity_4 * x4 + luggage_capacity_3 * x3 >= required_luggage)

    # Pollutant constraint: 30*x4 + 15*x3 <= 430
    solver.Add(pollutant_4 * x4 + pollutant_3 * x3 <= max_pollutant)

    # Objective: Minimize total number of vehicles: x4 + x3
    objective = solver.Objective()
    objective.SetCoefficient(x4, 1)
    objective.SetCoefficient(x3, 1)
    objective.SetMinimization()

    # Solve the problem
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        solution = {
            "variables": {
                "NumberOfVehicles": {
                    "0": x4.solution_value(),  # Number of 4-wheelers
                    "1": x3.solution_value()   # Number of 3-wheelers
                }
            },
            "objective": objective.Value()  # Total number of vehicles
        }
        return solution
    else:
        print("No feasible solution found using linear solver.")
        return None

def solve_with_cp_model():
    model = cp_model.CpModel()

    # Parameters
    luggage_capacity_4 = 60
    luggage_capacity_3 = 40
    pollutant_4 = 30
    pollutant_3 = 15
    required_luggage = 1000
    max_pollutant = 430

    # Estimate an upper bound, considering worst case: In pollutant constraint, for instance,
    # For 3-wheelers, max vehicles = floor(max_pollutant/15) = 28 might be a safe upper bound,
    # or for 4-wheelers, floor(max_pollutant/30)=14. We'll take a safe upper bound as 50.
    ub = 50

    # Decision Variables (nonnegative integers)
    x4 = model.NewIntVar(0, ub, 'x_4wheel')
    x3 = model.NewIntVar(0, ub, 'x_3wheel')

    # Constraints:
    # Luggage movement constraint: 60*x4 + 40*x3 >= 1000
    model.Add(luggage_capacity_4 * x4 + luggage_capacity_3 * x3 >= required_luggage)

    # Pollutant constraint: 30*x4 + 15*x3 <= 430
    model.Add(pollutant_4 * x4 + pollutant_3 * x3 <= max_pollutant)

    # Objective: Minimize x4 + x3
    model.Minimize(x4 + x3)

    # Solve the model.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        solution = {
            "variables": {
                "NumberOfVehicles": {
                    "0": solver.Value(x4),  # Number of 4-wheelers
                    "1": solver.Value(x3)   # Number of 3-wheelers
                }
            },
            "objective": solver.ObjectiveValue()  # Total number of vehicles
        }
        return solution
    else:
        print("No feasible solution found using CP-SAT model.")
        return None

def main():
    results = {}

    # Solve using linear solver (MIP)
    linear_solution = solve_with_linear_solver()
    if linear_solution:
        results["LinearSolver"] = linear_solution
    else:
        results["LinearSolver"] = "No feasible solution found."

    # Solve using CP-SAT model
    cp_solution = solve_with_cp_model()
    if cp_solution:
        results["CpModel"] = cp_solution
    else:
        results["CpModel"] = "No feasible solution found."

    # Print the results in a structured JSON format
    print(json.dumps(results, indent=2))

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
{
  "LinearSolver": {
    "variables": {
      "NumberOfVehicles": {
        "0": 6.0,
        "1": 16.0
      }
    },
    "objective": 22.0
  },
  "CpModel": {
    "variables": {
      "NumberOfVehicles": {
        "0": 6,
        "1": 16
      }
    },
    "objective": 22.0
  }
}
'''

'''Expected Output:
Expected solution

: {'variables': {'NumberOfVehicles': {'0': 6.0, '1': 16.0}}, 'objective': 22.0}'''

