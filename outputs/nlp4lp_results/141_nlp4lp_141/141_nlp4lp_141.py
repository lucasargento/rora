# Problem Description:
'''Problem description: A meal service company delivers meals to customers either on electric bikes or scooters. A bike can hold 8 meals and requires 3 units of charge. A scooter can hold 5 meals and requires 2 units of charge. Since the city is more friendly towards scooters, at most 30% of the electric vehicles can be bikes and at least 20 scooters must be used. If the company only has 200 units of charge available, how many of each vehicle should be used to maximize the number of meals that can be delivered?

Expected Output Schema:
{
  "variables": {
    "NumberOfBikes": "float",
    "NumberOfScooters": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Below is the structured five‐element formulation for the problem.

----------------------------------------------------------------
Sets:
- V = {Bike, Scooter} 
  (the set of available electric vehicle types)

----------------------------------------------------------------
Parameters:
- meal_capacity_Bike = 8 meals per Bike  
- meal_capacity_Scooter = 5 meals per Scooter  
- charge_required_Bike = 3 charge units per Bike  
- charge_required_Scooter = 2 charge units per Scooter  
- total_charge = 200 charge units available  
- bike_percentage_limit = 0.30  
  (at most 30% of the total electric vehicles can be Bikes)  
- min_scooters = 20  
  (minimum number of Scooters to be used)

Note: The charge and capacity units for Bikes and Scooters are assumed consistent with the problem description.

----------------------------------------------------------------
Variables:
- x_Bike: number of Bikes to use [integer, ≥ 0]  
- x_Scooter: number of Scooters to use [integer, ≥ 0]

----------------------------------------------------------------
Objective:
Maximize Total Meals Delivered =  
   meal_capacity_Bike * x_Bike + meal_capacity_Scooter * x_Scooter  
which evaluates to:  
   8 * x_Bike + 5 * x_Scooter

----------------------------------------------------------------
Constraints:
1. Charging Constraint:
   charge_required_Bike * x_Bike + charge_required_Scooter * x_Scooter ≤ total_charge  
   That is, 3 * x_Bike + 2 * x_Scooter ≤ 200

2. Fleet Composition Constraint (30% limit on Bikes):
   x_Bike ≤ bike_percentage_limit * (x_Bike + x_Scooter)  
   In other words, the number of Bikes is at most 30% of the total vehicles.

3. Minimum Scooter Constraint:
   x_Scooter ≥ min_scooters  
   That is, x_Scooter ≥ 20

----------------------------------------------------------------

This formulation is fully self-contained and unambiguous.'''

# Generated Code:
#!/usr/bin/env python3
"""
This script implements the optimization problem using Google OR-Tools.
It models the following problem:

    A meal service company delivers meals using electric Bikes and Scooters.
    - A Bike holds 8 meals and requires 3 units of charge.
    - A Scooter holds 5 meals and requires 2 units of charge.
    
    Constraints:
      1. Total charge used must not exceed 200 units.
         (3 * x_Bike + 2 * x_Scooter <= 200)
      2. No more than 30% of the vehicles can be Bikes.
         (x_Bike <= 0.30 * (x_Bike + x_Scooter)) 
         which can be rearranged to: 7*x_Bike <= 3*x_Scooter.
      3. At least 20 Scooters must be used.
         (x_Scooter >= 20)
    
    Objective:
      Maximize the total number of meals delivered:
          8 * x_Bike + 5 * x_Scooter

Since the formulation is a linear mixed-integer program,
we use OR-Tools' linear_solver (pywraplp).

NOTE: This implementation is standalone as only one formulation is provided.
"""

from ortools.linear_solver import pywraplp

def solve_with_linear_solver():
    # Create the linear solver with the CBC backend.
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Solver not found.")
        return None

    # Define decision variables as non-negative integers.
    x_Bike = solver.IntVar(0.0, solver.infinity(), 'x_Bike')
    x_Scooter = solver.IntVar(0.0, solver.infinity(), 'x_Scooter')

    # Parameters:
    meal_capacity_Bike = 8
    meal_capacity_Scooter = 5
    charge_required_Bike = 3
    charge_required_Scooter = 2
    total_charge = 200
    bike_percentage_limit = 0.30  # at most 30%
    min_scooters = 20

    # Constraint 1: Charging Constraint
    # 3*x_Bike + 2*x_Scooter <= 200
    solver.Add(charge_required_Bike * x_Bike + charge_required_Scooter * x_Scooter <= total_charge)

    # Constraint 2: Fleet Composition Constraint (Bikes at most 30% of vehicles)
    # x_Bike <= 0.30 * (x_Bike + x_Scooter)
    # Rearranging: x_Bike <= 0.30*x_Bike + 0.30*x_Scooter  -->  0.70*x_Bike <= 0.30*x_Scooter
    # Multiply both sides by 10 to avoid fractions: 7*x_Bike <= 3*x_Scooter
    solver.Add(7 * x_Bike <= 3 * x_Scooter)

    # Constraint 3: Minimum Scooter Constraint
    # x_Scooter >= 20
    solver.Add(x_Scooter >= min_scooters)

    # Objective: Maximize meals delivered = 8*x_Bike + 5*x_Scooter
    objective = solver.Objective()
    objective.SetCoefficient(x_Bike, meal_capacity_Bike)
    objective.SetCoefficient(x_Scooter, meal_capacity_Scooter)
    objective.SetMaximization()

    # Solve the problem.
    status = solver.Solve()

    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "model": "Linear Solver (CBC)",
            "variables": {
                "NumberOfBikes": x_Bike.solution_value(),
                "NumberOfScooters": x_Scooter.solution_value()
            },
            "objective": objective.Value()
        }
    else:
        result = {
            "model": "Linear Solver (CBC)",
            "message": "The problem does not have an optimal solution."
        }
    return result

def main():
    # Only one formulation is provided; using the OR-Tools linear_solver model.
    results = {}
    results['Linear_Programming_Implementation'] = solve_with_linear_solver()
    
    # Print the results in a structured way.
    import json
    print(json.dumps(results, indent=4))

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
{
    "Linear_Programming_Implementation": {
        "model": "Linear Solver (CBC)",
        "variables": {
            "NumberOfBikes": 26.0,
            "NumberOfScooters": 61.0
        },
        "objective": 513.0
    }
}
'''

'''Expected Output:
Expected solution

: {'variables': {'NumberOfBikes': 26.0, 'NumberOfScooters': 61.0}, 'objective': 513.0}'''

