# Problem Description:
'''Problem description: A bakery uses a stand-mixer and a slow bake oven to make bread and cookies. Each machine can run for at most 3000 hours per year. To bake a loaf of bread takes 1 hour in the stand mixer and 3 hours in the oven. A batch of cookies requires 0.5 hours in the mixer and 1 hour in the oven. The profit per loaf of bread is $5 and the profit per batch of cookies is $3. How should the bakery operate to maximize total profit?

Expected Output Schema:
{
  "variables": {
    "BreadQuantity": "float",
    "CookiesQuantity": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Below is the structured model using the five-element framework.

--------------------------------------------------
Sets:
- Product: set of products = {Bread, Cookies}

--------------------------------------------------
Parameters:
- profit:
  - profit[Bread] = 5 dollars per loaf of bread
  - profit[Cookies] = 3 dollars per batch of cookies
- mixer_time:
  - mixer_time[Bread] = 1 hour per loaf of bread
  - mixer_time[Cookies] = 0.5 hours per batch of cookies
- oven_time:
  - oven_time[Bread] = 3 hours per loaf of bread
  - oven_time[Cookies] = 1 hour per batch of cookies
- capacity:
  - max_mixer_hours = 3000 hours per year (stand mixer)
  - max_oven_hours = 3000 hours per year (slow bake oven)

--------------------------------------------------
Variables:
- BreadQuantity: number of loaves of bread to produce (nonnegative continuous; note: if production must be an integer count then declare as integer)
- CookiesQuantity: number of batches of cookies to produce (nonnegative continuous; note: if production must be an integer count then declare as integer)

--------------------------------------------------
Objective:
- Maximize total profit defined as:
  Total_Profit = profit[Bread] * BreadQuantity + profit[Cookies] * CookiesQuantity
  That is, maximize (5 * BreadQuantity + 3 * CookiesQuantity)

--------------------------------------------------
Constraints:
1. Mixer capacity constraint:
   mixer_time[Bread] * BreadQuantity + mixer_time[Cookies] * CookiesQuantity ≤ max_mixer_hours
   i.e., (1 * BreadQuantity + 0.5 * CookiesQuantity) ≤ 3000

2. Oven capacity constraint:
   oven_time[Bread] * BreadQuantity + oven_time[Cookies] * CookiesQuantity ≤ max_oven_hours
   i.e., (3 * BreadQuantity + 1 * CookiesQuantity) ≤ 3000

--------------------------------------------------
Below is the expected JSON output schema for variables and the objective:

{
  "variables": {
    "BreadQuantity": "float",
    "CookiesQuantity": "float"
  },
  "objective": "float"
}'''

# Generated Code:
from ortools.linear_solver import pywraplp

def solve_continuous():
    """Solve the bakery optimization problem with continuous decision variables."""
    # Create the solver using the GLOP backend for linear programming.
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Solver not created.")
        return None

    # Variables (continuous)
    BreadQuantity = solver.NumVar(0.0, solver.infinity(), "BreadQuantity")
    CookiesQuantity = solver.NumVar(0.0, solver.infinity(), "CookiesQuantity")

    # Constraints:
    # Mixer capacity: 1 * BreadQuantity + 0.5 * CookiesQuantity <= 3000
    solver.Add(BreadQuantity + 0.5 * CookiesQuantity <= 3000)
    # Oven capacity: 3 * BreadQuantity + 1 * CookiesQuantity <= 3000
    solver.Add(3 * BreadQuantity + CookiesQuantity <= 3000)

    # Objective: Maximize total profit = 5 * BreadQuantity + 3 * CookiesQuantity
    objective = solver.Objective()
    objective.SetCoefficient(BreadQuantity, 5)
    objective.SetCoefficient(CookiesQuantity, 3)
    objective.SetMaximization()

    # Solve
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "variables": {
                "BreadQuantity": BreadQuantity.solution_value(),
                "CookiesQuantity": CookiesQuantity.solution_value()
            },
            "objective": objective.Value()
        }
        return result
    else:
        return {"message": "The continuous model does not have an optimal solution."}

def solve_integer():
    """Solve the bakery optimization problem with integer decision variables."""
    # Create the solver using CBC MIP backend.
    solver = pywraplp.Solver.CreateSolver('CBC_MIXED_INTEGER_PROGRAMMING')
    if not solver:
        print("Integer solver not created.")
        return None

    # Variables (integer)
    BreadQuantity = solver.IntVar(0.0, solver.infinity(), "BreadQuantity")
    CookiesQuantity = solver.IntVar(0.0, solver.infinity(), "CookiesQuantity")

    # Constraints:
    # Mixer capacity: 1 * BreadQuantity + 0.5 * CookiesQuantity <= 3000
    # Note: Because CookiesQuantity is integer, 0.5 * CookiesQuantity is fractional;
    # the constraint remains the same.
    solver.Add(BreadQuantity + 0.5 * CookiesQuantity <= 3000)
    # Oven capacity: 3 * BreadQuantity + 1 * CookiesQuantity <= 3000
    solver.Add(3 * BreadQuantity + CookiesQuantity <= 3000)

    # Objective: Maximize total profit = 5 * BreadQuantity + 3 * CookiesQuantity
    objective = solver.Objective()
    objective.SetCoefficient(BreadQuantity, 5)
    objective.SetCoefficient(CookiesQuantity, 3)
    objective.SetMaximization()

    # Solve
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "variables": {
                "BreadQuantity": BreadQuantity.solution_value(),
                "CookiesQuantity": CookiesQuantity.solution_value()
            },
            "objective": objective.Value()
        }
        return result
    else:
        return {"message": "The integer model does not have an optimal solution."}

def main():
    # Solve the continuous version of the problem.
    continuous_result = solve_continuous()
    # Solve the integer version of the problem.
    integer_result = solve_integer()

    # Print the results in a structured way.
    print("Continuous Model Result:")
    if "message" in continuous_result:
        print(continuous_result["message"])
    else:
        print(continuous_result)

    print("\nInteger Model Result:")
    if "message" in integer_result:
        print(integer_result["message"])
    else:
        print(integer_result)

if __name__ == "__main__":
    main()

'''Execution Results:
SUCCESS:
Continuous Model Result:
{'variables': {'BreadQuantity': 0.0, 'CookiesQuantity': 3000.0}, 'objective': 9000.0}

Integer Model Result:
{'variables': {'BreadQuantity': 0.0, 'CookiesQuantity': 3000.0}, 'objective': 9000.0}
'''

'''Expected Output:
Expected solution

: {'variables': {'BreadQuantity': 0.0, 'CookiesQuantity': 3000.0}, 'objective': 9000.0}'''

