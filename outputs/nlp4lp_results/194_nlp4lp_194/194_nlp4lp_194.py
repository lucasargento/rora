# Problem Description:
'''Problem description: Zeta Bakery sells two types of cookies. They sell a strawberry cookie and a sugar cookie. Let's say they make x1 strawberry cookies, at a profit of $5.5 each, and x2 sugar cookies, at a profit of $12 each (x1 and x2 are unknowns both greater than or equal to 0). The daily demand for these cookies is at most 100 strawberry cookies and at most 80 sugar cookies. The bakery is short staffed and can make a maximum of 100 cookies of either type per day. How much of each cookie should the bakery make in order to maximize profit?

Expected Output Schema:
{
  "variables": {
    "NumStrawberryCookies": "float",
    "NumSugarCookies": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- CookieTypes: {Strawberry, Sugar}

Parameters:
- profit: dictionary with profit per cookie [USD per cookie]
  • profit[Strawberry] = 5.5
  • profit[Sugar] = 12.0
- maxDemand: dictionary with maximum daily demand [cookies]
  • maxDemand[Strawberry] = 100
  • maxDemand[Sugar] = 80
- maxDailyProduction: maximum total cookies that can be produced per day due to staffing (cookies per day)
  • maxDailyProduction = 100

Variables:
- x[c]: number of cookies of type c to produce [integer ≥ 0 or float ≥ 0, representing cookies]
  • For c in CookieTypes

Objective:
- Maximize total profit = profit[Strawberry] * x[Strawberry] + profit[Sugar] * x[Sugar]

Constraints:
1. Demand constraints:
   • x[Strawberry] ≤ maxDemand[Strawberry]
   • x[Sugar] ≤ maxDemand[Sugar]
2. Production capacity constraint due to staffing:
   • x[Strawberry] + x[Sugar] ≤ maxDailyProduction

Model Comments:
- All parameters are expressed in consistent units: profits in USD per cookie, production and demand in cookies.
- Although cookies are naturally integer units, the formulation allows for continuous variables; if integer solutions are required, x[c] can be specified as integer.
- The overall production constraint reflects the limited staffing capacity rather than a machine or ingredient limit.
- This structured model is directly translatable to Python or OR-Tools code.'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_continuous():
    # Create solver for continuous variables using GLOP linear programming solver.
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Continuous model: Solver not created.")
        return None

    # Decision variables: Continuous variables for number of cookies (>=0)
    x_strawberry = solver.NumVar(0.0, 100.0, 'NumStrawberryCookies')  # also demand constraint upper bound applied later
    x_sugar = solver.NumVar(0.0, 80.0, 'NumSugarCookies')  # demand constraint upper bound applied later

    # Note: Even though we set upper bounds here, we add production constraint separately.

    # Constraint: Production capacity constraint due to staffing: 
    # x_strawberry + x_sugar <= 100
    production_capacity = solver.Constraint(-solver.infinity(), 100.0)
    production_capacity.SetCoefficient(x_strawberry, 1)
    production_capacity.SetCoefficient(x_sugar, 1)

    # The demand constraints are already enforced by variable bounds (x_strawberry ≤100, x_sugar ≤80)

    # Objective: Maximize profit = 5.5*x_strawberry + 12*x_sugar
    objective = solver.Objective()
    objective.SetCoefficient(x_strawberry, 5.5)
    objective.SetCoefficient(x_sugar, 12.0)
    objective.SetMaximization()

    status = solver.Solve()
    
    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "variables": {
                "NumStrawberryCookies": x_strawberry.solution_value(),
                "NumSugarCookies": x_sugar.solution_value()
            },
            "objective": objective.Value()
        }
    else:
        result = None
        print("Continuous model: No optimal solution found.")
    return result

def solve_integer():
    # Create solver for integer variables using CBC MILP solver.
    solver = pywraplp.Solver.CreateSolver('CBC_MIXED_INTEGER_PROGRAMMING')
    if not solver:
        print("Integer model: Solver not created.")
        return None

    # Decision variables: Integer variables for number of cookies (>=0)
    # Considering cookies are naturally integer.
    x_strawberry = solver.IntVar(0, 100, 'NumStrawberryCookies')  # upper bound per demand constraint
    x_sugar = solver.IntVar(0, 80, 'NumSugarCookies')  # upper bound per demand constraint

    # Constraint: Production capacity constraint due to staffing:
    # x_strawberry + x_sugar <= 100
    production_capacity = solver.Constraint(-solver.infinity(), 100)
    production_capacity.SetCoefficient(x_strawberry, 1)
    production_capacity.SetCoefficient(x_sugar, 1)

    # Demand constraints are enforced by variable bounds.

    # Objective: Maximize profit = 5.5*x_strawberry + 12*x_sugar
    objective = solver.Objective()
    objective.SetCoefficient(x_strawberry, 5.5)
    objective.SetCoefficient(x_sugar, 12.0)
    objective.SetMaximization()

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "variables": {
                "NumStrawberryCookies": x_strawberry.solution_value(),
                "NumSugarCookies": x_sugar.solution_value()
            },
            "objective": objective.Value()
        }
    else:
        result = None
        print("Integer model: No optimal solution found.")
    return result

def main():
    continuous_solution = solve_continuous()
    integer_solution = solve_integer()

    print("Continuous Model Solution:")
    if continuous_solution:
        print(continuous_solution)
    else:
        print("No optimal solution found for continuous model.")
    
    print("\nInteger Model Solution:")
    if integer_solution:
        print(integer_solution)
    else:
        print("No optimal solution found for integer model.")

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Continuous Model Solution:
{'variables': {'NumStrawberryCookies': 20.0, 'NumSugarCookies': 80.0}, 'objective': 1070.0}

Integer Model Solution:
{'variables': {'NumStrawberryCookies': 20.0, 'NumSugarCookies': 80.0}, 'objective': 1070.0}
'''

'''Expected Output:
Expected solution

: {'variables': {'NumStrawberryCookies': 20.0, 'NumSugarCookies': 80.0}, 'objective': 1070.0}'''

