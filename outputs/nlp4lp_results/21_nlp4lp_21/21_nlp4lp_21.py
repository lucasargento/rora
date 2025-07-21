# Problem Description:
'''Problem description: You are designing an office space with two types of desks: long desks and short desks. You can spend at most $2000. Long desks cost $300, take up 10 square feet of space, and seat 6 employees. Short desks cost $100, take up 4 square feet of space, and seat 2 employees. The office can have at most 200 square feet of desks. How many of each desk should you buy in order to maximize the seating availability?

Expected Output Schema:
{
  "variables": {
    "NumDesks": {
      "0": "float",
      "1": "float"
    }
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- D = {LongDesk, ShortDesk} 
  (Interpretation: The two types of desks available for purchase.)

Parameters:
- cost_long = 300 (USD per long desk)
- cost_short = 100 (USD per short desk)
- area_long = 10 (square feet per long desk)
- area_short = 4 (square feet per short desk)
- seats_long = 6 (number of employees seated per long desk)
- seats_short = 2 (number of employees seated per short desk)
- max_budget = 2000 (USD total available cost)
- max_area = 200 (square feet total available desk space)

Variables:
- x_long: number of long desks to buy [nonnegative integer; units: desks]
- x_short: number of short desks to buy [nonnegative integer; units: desks]

Objective:
- Maximize total seating capacity = (seats_long * x_long) + (seats_short * x_short)
  (Interpretation: The goal is to maximize the number of employees that can be seated.)

Constraints:
1. Cost Constraint: (cost_long * x_long) + (cost_short * x_short) <= max_budget
   (Interpretation: Total money spent on desks must not exceed $2000.)
2. Area Constraint: (area_long * x_long) + (area_short * x_short) <= max_area
   (Interpretation: Total desk area used must not exceed 200 square feet.)
3. Nonnegativity Constraint: x_long >= 0 and x_short >= 0
   (Interpretation: Negative quantities of desks are not allowed.)

----------------------------------------------------
Mapping to Expected Output Schema:

{
  "variables": {
    "NumDesks": {
      "0": "float",     // Represents x_long: number of long desks
      "1": "float"      // Represents x_short: number of short desks
    }
  },
  "objective": "float"   // Represents the maximum seating capacity value computed as (6*x_long) + (2*x_short)"
}'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_linear_model():
    # Create the solver using SCIP backend
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        print("Solver not available.")
        return None

    # Variables:
    # x_long: number of long desks (nonnegative integer)
    # x_short: number of short desks (nonnegative integer)
    x_long = solver.IntVar(0, solver.infinity(), 'x_long')
    x_short = solver.IntVar(0, solver.infinity(), 'x_short')

    # Parameters:
    cost_long = 300    # cost (USD) per long desk
    cost_short = 100   # cost (USD) per short desk
    area_long = 10     # square feet per long desk
    area_short = 4     # square feet per short desk
    seats_long = 6     # seats per long desk
    seats_short = 2    # seats per short desk
    max_budget = 2000  # maximum budget (USD)
    max_area = 200     # maximum desk area (square feet)

    # Constraints:
    # 1. Cost Constraint:
    solver.Add(cost_long * x_long + cost_short * x_short <= max_budget)

    # 2. Area Constraint:
    solver.Add(area_long * x_long + area_short * x_short <= max_area)

    # Objective: Maximize total seating capacity = (seats_long * x_long) + (seats_short * x_short)
    solver.Maximize(seats_long * x_long + seats_short * x_short)

    # Solve the problem
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        # Constructing results as dictated by the expected output schema:
        # "NumDesks": { "0": number of long desks, "1": number of short desks }
        result = {
            "variables": {
                "NumDesks": {
                    "0": float(x_long.solution_value()),
                    "1": float(x_short.solution_value())
                }
            },
            "objective": float(solver.Objective().Value())
        }
        return result
    else:
        print("No optimal solution found for the Linear Model.")
        return None

def main():
    # In this case, we have only one formulation based on the provided mathematical model.
    # Call the linear model solver and display its result.
    print("Solving the Office Desk Optimization Problem using OR-Tools Linear Solver\n")
    linear_solution = solve_linear_model()
    
    if linear_solution:
        print("Linear Model Optimal Solution:")
        print("Variables (NumDesks):")
        print("  Long Desks (x_long):", linear_solution["variables"]["NumDesks"]["0"])
        print("  Short Desks (x_short):", linear_solution["variables"]["NumDesks"]["1"])
        print("Objective (Maximum Seating Capacity):", linear_solution["objective"])
    else:
        print("No solution found in the linear model.")

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Solving the Office Desk Optimization Problem using OR-Tools Linear Solver

Linear Model Optimal Solution:
Variables (NumDesks):
  Long Desks (x_long): -0.0
  Short Desks (x_short): 20.0
Objective (Maximum Seating Capacity): 40.0
'''

'''Expected Output:
Expected solution

: {'variables': {'NumDesks': {'0': -0.0, '1': 20.0}}, 'objective': 40.0}'''

