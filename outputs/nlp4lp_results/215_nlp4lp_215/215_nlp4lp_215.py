# Problem Description:
'''Problem description: A cruise company can either have two types of trips, a large cruise ship or a small cruise ship. A large cruise ship trip can carry 2000 customers and produces 20 units of pollution. A small cruise ship trip can carry 800 customers and produces 15 units of pollution. There can be at most 7 large cruise ship trips and at least 40% of the total trips must be made by small cruise ships. If the cruise company aims to transport at least 20000 customers, how many of each size of cruise ships should the company use to minimize the total amount of pollution produced?

Expected Output Schema:
{
  "variables": {
    "NumberLargeTrips": "float",
    "NumberSmallTrips": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Below is the structured mathematical model following the five-element format.

--------------------------------------------------

Sets:
- ShipType = {Large, Small}

Parameters:
- LargeCapacity = 2000 (number of customers per large cruise trip)
- SmallCapacity = 800 (number of customers per small cruise trip)
- LargePollution = 20 (pollution units produced per large cruise trip)
- SmallPollution = 15 (pollution units produced per small cruise trip)
- MaxLargeTrips = 7 (maximum allowable number of large cruise trips)
- MinTotalCustomers = 20000 (minimum total number of customers to be transported)
- MinSmallFraction = 0.4 (minimum fraction of total trips that must be small cruise trips)
  (Note: The small-ship requirement implies that the number of small trips must be at least 0.4 times the total trips.)

Variables:
- NumberLargeTrips [integer, ≥ 0]: Number of large cruise ship trips to schedule (units: trips)
- NumberSmallTrips [integer, ≥ 0]: Number of small cruise ship trips to schedule (units: trips)

Objective:
- Minimize total pollution produced:
  TotalPollution = LargePollution * NumberLargeTrips + SmallPollution * NumberSmallTrips

Constraints:
1. Customer Requirement Constraint:
   LargeCapacity * NumberLargeTrips + SmallCapacity * NumberSmallTrips ≥ MinTotalCustomers

2. Maximum Large Trips Constraint:
   NumberLargeTrips ≤ MaxLargeTrips

3. Minimum Small Trip Fraction Constraint:
   To ensure at least 40% of all trips are small trips, we enforce:
   NumberSmallTrips ≥ MinSmallFraction * (NumberLargeTrips + NumberSmallTrips)
   (Note: This inequality is equivalent to NumberSmallTrips ≥ (2/3) * NumberLargeTrips.)

4. Non-negativity Constraints:
   NumberLargeTrips ≥ 0  
   NumberSmallTrips ≥ 0

--------------------------------------------------

This complete model can now be implemented in a mathematical optimization framework where the decision variables and parameters are as described.

Expected Output Schema:
{
  "variables": {
    "NumberLargeTrips": "float",
    "NumberSmallTrips": "float"
  },
  "objective": "float"
}'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_model_version1():
    # Create the CBC solver.
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Solver not created.")
        return None

    # Decision variables:
    # NumberLargeTrips: integer, ≥ 0 and ≤ 7.
    NumberLargeTrips = solver.IntVar(0, 7, 'NumberLargeTrips')
    # NumberSmallTrips: integer, ≥ 0 with no explicit upper bound.
    NumberSmallTrips = solver.IntVar(0, solver.infinity(), 'NumberSmallTrips')

    # Constraint 1: Customer Requirement Constraint.
    # 2000 * NumberLargeTrips + 800 * NumberSmallTrips ≥ 20000.
    solver.Add(2000 * NumberLargeTrips + 800 * NumberSmallTrips >= 20000)

    # Constraint 2 is built in variable domain: NumberLargeTrips ≤ 7.

    # Constraint 3: Minimum Small Trip Fraction Constraint.
    # Original formulation: NumberSmallTrips ≥ 0.4 * (NumberLargeTrips + NumberSmallTrips).
    # Rearranging: 0.6*NumberSmallTrips ≥ 0.4*NumberLargeTrips => multiply both sides by 5:
    # 3 * NumberSmallTrips ≥ 2 * NumberLargeTrips.
    solver.Add(3 * NumberSmallTrips >= 2 * NumberLargeTrips)

    # Objective: Minimize total pollution = 20*NumberLargeTrips + 15*NumberSmallTrips.
    objective = solver.Objective()
    objective.SetCoefficient(NumberLargeTrips, 20)
    objective.SetCoefficient(NumberSmallTrips, 15)
    objective.SetMinimization()

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL:
        return {
            "NumberLargeTrips": NumberLargeTrips.solution_value(),
            "NumberSmallTrips": NumberSmallTrips.solution_value(),
            "objective": objective.Value()
        }
    else:
        print("No optimal solution found in Model Version 1.")
        return None

def solve_model_version2():
    # Create the CBC solver.
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Solver not created.")
        return None

    # Decision variables:
    NumberLargeTrips = solver.IntVar(0, 7, 'NumberLargeTrips')
    NumberSmallTrips = solver.IntVar(0, solver.infinity(), 'NumberSmallTrips')

    # Constraint 1: Customer Requirement Constraint.
    solver.Add(2000 * NumberLargeTrips + 800 * NumberSmallTrips >= 20000)
    
    # Constraint 2 is built in via variable domain.

    # Constraint 3: Minimum Small Trip Fraction Constraint.
    # Alternate formulation: NumberSmallTrips ≥ (2/3) * NumberLargeTrips.
    # Multiply both sides by 3 to avoid fractions: 3 * NumberSmallTrips ≥ 2 * NumberLargeTrips.
    solver.Add(3 * NumberSmallTrips >= 2 * NumberLargeTrips)
    
    # Objective: Minimize total pollution = 20*NumberLargeTrips + 15*NumberSmallTrips.
    objective = solver.Objective()
    objective.SetCoefficient(NumberLargeTrips, 20)
    objective.SetCoefficient(NumberSmallTrips, 15)
    objective.SetMinimization()

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL:
        return {
            "NumberLargeTrips": NumberLargeTrips.solution_value(),
            "NumberSmallTrips": NumberSmallTrips.solution_value(),
            "objective": objective.Value()
        }
    else:
        print("No optimal solution found in Model Version 2.")
        return None

def main():
    # Solve both formulations.
    result_v1 = solve_model_version1()
    result_v2 = solve_model_version2()

    # Print results in a structured manner.
    print("Results for Model Version 1 (using the constraint NumberSmallTrips ≥ 0.4*(NumberLargeTrips+NumberSmallTrips)):")
    if result_v1:
        print(result_v1)
    else:
        print("Model Version 1 did not find an optimal solution.")

    print("\nResults for Model Version 2 (using the equivalent constraint NumberSmallTrips ≥ (2/3)*NumberLargeTrips):")
    if result_v2:
        print(result_v2)
    else:
        print("Model Version 2 did not find an optimal solution.")

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Results for Model Version 1 (using the constraint NumberSmallTrips ≥ 0.4*(NumberLargeTrips+NumberSmallTrips)):
{'NumberLargeTrips': 7.0, 'NumberSmallTrips': 8.0, 'objective': 260.0}

Results for Model Version 2 (using the equivalent constraint NumberSmallTrips ≥ (2/3)*NumberLargeTrips):
{'NumberLargeTrips': 7.0, 'NumberSmallTrips': 8.0, 'objective': 260.0}
'''

'''Expected Output:
Expected solution

: {'variables': {'NumberLargeTrips': 7.0, 'NumberSmallTrips': 8.0}, 'objective': 260.0}'''

