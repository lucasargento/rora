# Problem Description:
'''Problem description: An artisan makes two types of terracotta jars: a thin jar and a stubby jar. Each thin jar requires 50 minutes of shaping time and 90 minutes of baking time. Each stubby jar requires 30 minutes of shaping time and 150 minutes of baking time. Per week, there are 3000 minutes available for shaping and 4000 minutes available for baking. The profit per thin jar is $5 and the profit per stubby jar is $9. How many jars of each type should the artisan make to maximize profit?

Expected Output Schema:
{
  "variables": {
    "NumJars": {
      "0": "float",
      "1": "float"
    }
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- Jars: set of jar types = {Thin, Stubby}

Parameters:
- shaping_time_thin: shaping time per thin jar (minutes per jar) = 50
- baking_time_thin: baking time per thin jar (minutes per jar) = 90
- shaping_time_stubby: shaping time per stubby jar (minutes per jar) = 30
- baking_time_stubby: baking time per stubby jar (minutes per jar) = 150
- available_shaping_time: total available shaping time per week (minutes) = 3000
- available_baking_time: total available baking time per week (minutes) = 4000
- profit_thin: profit per thin jar (USD per jar) = 5
- profit_stubby: profit per stubby jar (USD per jar) = 9

Variables:
- x_thin: number of thin jars to produce [integer, ≥ 0] [units]
- x_stubby: number of stubby jars to produce [integer, ≥ 0] [units]

Objective:
- Maximize total profit = (profit_thin * x_thin) + (profit_stubby * x_stubby)
  That is, maximize 5 * x_thin + 9 * x_stubby

Constraints:
1. Shaping time constraint:
   - (shaping_time_thin * x_thin) + (shaping_time_stubby * x_stubby) ≤ available_shaping_time
   - That is, 50 * x_thin + 30 * x_stubby ≤ 3000

2. Baking time constraint:
   - (baking_time_thin * x_thin) + (baking_time_stubby * x_stubby) ≤ available_baking_time
   - That is, 90 * x_thin + 150 * x_stubby ≤ 4000

--------------------------------------------------

Expected Output Schema:
{
  "variables": {
    "NumJars": {
      "0": "x_thin (number of thin jars, integer ≥ 0)",
      "1": "x_stubby (number of stubby jars, integer ≥ 0)"
    }
  },
  "objective": "5*x_thin + 9*x_stubby"
}'''

# Generated Code:
from ortools.linear_solver import pywraplp

def solve_with_linear_solver():
    # Create the MIP solver with the SCIP backend.
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        return {"error": "Solver not created."}

    # Define variables: x_thin and x_stubby, integer nonnegative.
    x_thin = solver.IntVar(0, solver.infinity(), 'x_thin')
    x_stubby = solver.IntVar(0, solver.infinity(), 'x_stubby')

    # Add constraints:
    # Constraint 1: Shaping time constraint: 50*x_thin + 30*x_stubby <= 3000.
    solver.Add(50 * x_thin + 30 * x_stubby <= 3000)

    # Constraint 2: Baking time constraint: 90*x_thin + 150*x_stubby <= 4000.
    solver.Add(90 * x_thin + 150 * x_stubby <= 4000)

    # Define the objective: Maximize 5 * x_thin + 9 * x_stubby.
    solver.Maximize(5 * x_thin + 9 * x_stubby)

    # Solve the problem and check the result.
    status = solver.Solve()

    results = {}
    if status == pywraplp.Solver.OPTIMAL:
        results["variables"] = {
            "NumJars": {
                "0": f"x_thin (number of thin jars, integer ≥ 0) = {int(x_thin.solution_value())}",
                "1": f"x_stubby (number of stubby jars, integer ≥ 0) = {int(x_stubby.solution_value())}"
            }
        }
        results["objective"] = solver.Objective().Value()
    else:
        results["error"] = "The problem does not have an optimal solution."

    return results

def main():
    # Since there is only one mathematical formulation provided,
    # we implement it using the linear_solver module from OR-Tools.
    linear_solver_results = solve_with_linear_solver()

    # Print the results in a structured way.
    print("Results from Linear/MIP formulation using ortools.linear_solver:")
    if "error" in linear_solver_results:
        print(linear_solver_results["error"])
    else:
        print("Optimal Solution:")
        for key, value in linear_solver_results["variables"]["NumJars"].items():
            print(value)
        print(f"Maximum Profit: {linear_solver_results['objective']}")

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Results from Linear/MIP formulation using ortools.linear_solver:
Optimal Solution:
x_thin (number of thin jars, integer ≥ 0) = 1
x_stubby (number of stubby jars, integer ≥ 0) = 26
Maximum Profit: 239.0
'''

'''Expected Output:
Expected solution

: {'variables': {'NumJars': {'0': 0.0, '1': 26.666666666666668}}, 'objective': 240.0}'''

