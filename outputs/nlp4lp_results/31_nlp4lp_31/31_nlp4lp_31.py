# Problem Description:
'''Problem description: A company sells custom scooters and bikes for customers. The profit per scooter is $200 and the profit per bike is $300. Each product requires time with the design team and engineering team. Each scooter needs 2 hours with the design team and 3 hours with the engineering team. Each bike needs 4 hours with the design team and 5 hours with the engineering team. Per month, there are 5000 hours available on the design team and 6000 hours available on the engineering team. How many of each should the company make per month to maximize profit?

Expected Output Schema:
{
  "variables": {
    "NumberOfScooters": "float",
    "NumberOfBikes": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- Products: {Scooter, Bike}

Parameters:
- profit: profit per unit, with profit[Scooter] = 200 (USD per scooter) and profit[Bike] = 300 (USD per bike)
- design_hours: design team hours required per unit, with design_hours[Scooter] = 2 (hours per scooter) and design_hours[Bike] = 4 (hours per bike)
- engineering_hours: engineering team hours required per unit, with engineering_hours[Scooter] = 3 (hours per scooter) and engineering_hours[Bike] = 5 (hours per bike)
- available_design_time: total available design team hours per month = 5000 (hours)
- available_engineering_time: total available engineering team hours per month = 6000 (hours)

Variables:
- x[product]: number of units produced of product (Scooter and Bike). These are non-negative decision variables. (They can be modeled as continuous or integer as required by implementation. Typically, production quantities are integer.)

Objective:
- Maximize total profit = profit[Scooter] * x[Scooter] + profit[Bike] * x[Bike]

Constraints:
1. Design time constraint: design_hours[Scooter] * x[Scooter] + design_hours[Bike] * x[Bike] ≤ available_design_time  
   (i.e., 2 * x[Scooter] + 4 * x[Bike] ≤ 5000)
2. Engineering time constraint: engineering_hours[Scooter] * x[Scooter] + engineering_hours[Bike] * x[Bike] ≤ available_engineering_time  
   (i.e., 3 * x[Scooter] + 5 * x[Bike] ≤ 6000)

Notes:
- All units are in hours for time-related parameters and in USD for profit.
- The decision variables represent monthly production quantities.'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_linear_program():
    # Create the solver using the CBC Mixed Integer Programming solver.
    solver = pywraplp.Solver.CreateSolver('CBC_MIXED_INTEGER_PROGRAMMING')
    if not solver:
        return {"error": "Solver not created."}

    # Define decision variables:
    # Production quantities must be non-negative integers.
    NumberOfScooters = solver.IntVar(0, solver.infinity(), 'NumberOfScooters')
    NumberOfBikes = solver.IntVar(0, solver.infinity(), 'NumberOfBikes')

    # Define the objective function:
    # Maximize total profit = 200 * NumberOfScooters + 300 * NumberOfBikes
    solver.Maximize(200 * NumberOfScooters + 300 * NumberOfBikes)

    # Add constraints:
    # 1. Design time constraint: 2 * NumberOfScooters + 4 * NumberOfBikes <= 5000
    solver.Add(2 * NumberOfScooters + 4 * NumberOfBikes <= 5000)

    # 2. Engineering time constraint: 3 * NumberOfScooters + 5 * NumberOfBikes <= 6000
    solver.Add(3 * NumberOfScooters + 5 * NumberOfBikes <= 6000)

    # Solve the model.
    status = solver.Solve()

    # Prepare the result in expected output schema.
    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result["variables"] = {
            "NumberOfScooters": NumberOfScooters.solution_value(),
            "NumberOfBikes": NumberOfBikes.solution_value()
        }
        result["objective"] = solver.Objective().Value()
    else:
        result["error"] = "No optimal solution found. Problem might be infeasible."

    return result

def main():
    # For this particular problem, there is only one valid formulation.
    # Thus, we run one model implementation.
    lp_result = solve_linear_program()

    # Print results for the Linear Programming model in a structured way.
    print("Results for the Linear Programming model:")
    print(lp_result)

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Results for the Linear Programming model:
{'variables': {'NumberOfScooters': 2000.0, 'NumberOfBikes': 0.0}, 'objective': 400000.0}
'''

'''Expected Output:
Expected solution

: {'variables': {'NumberOfScooters': 2000.0, 'NumberOfBikes': 0.0}, 'objective': 400000.0}'''

