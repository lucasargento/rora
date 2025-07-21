# Problem Description:
'''Problem description: A coffee shop sells mochas and regular coffees. Each mocha requires 3 units of coffee powder and 6 units of milk. Each regular coffee requires 6 units of coffee powder and 2 units of milk. The shop has available 400 units of coffee powder and 500 units of milk. Making a mocha takes 5 minutes and making a regular coffee takes 3 minutes. Since mochas are more popular among people, the shop must make at least 3 times as many mochas as regular coffees. How many of each should they make to minimize the total production time?

Expected Output Schema:
{
  "variables": {
    "NumMocha": "float",
    "NumRegularCoffee": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- Drinks: a set of coffee drink types = {Mocha, RegularCoffee}

Parameters:
- coffeePowderPerMocha = 3 (units of coffee powder required per mocha)
- coffeePowderPerRegular = 6 (units of coffee powder required per regular coffee)
- milkPerMocha = 6 (units of milk required per mocha)
- milkPerRegular = 2 (units of milk required per regular coffee)
- availableCoffeePowder = 400 (total available units of coffee powder)
- availableMilk = 500 (total available units of milk)
- productionTimeMocha = 5 (minutes required to make one mocha)
- productionTimeRegular = 3 (minutes required to make one regular coffee)
- minMochaToRegularRatio = 3 (mochas must be at least 3 times the number of regular coffees)

Variables:
- NumMocha: number of mochas to produce (float, ≥ 0) [units]
- NumRegularCoffee: number of regular coffees to produce (float, ≥ 0) [units]

Objective:
- Minimize total production time in minutes = productionTimeMocha * NumMocha + productionTimeRegular * NumRegularCoffee
  That is, minimize (5 * NumMocha + 3 * NumRegularCoffee)

Constraints:
1. Coffee powder constraint:
   3 * NumMocha + 6 * NumRegularCoffee ≤ 400
2. Milk constraint:
   6 * NumMocha + 2 * NumRegularCoffee ≤ 500
3. Demand ratio constraint:
   NumMocha ≥ 3 * NumRegularCoffee

Comments:
- All unit quantities are assumed to be consistent (e.g., production time in minutes, material usage in units).
- Although production quantities are typically integers, the expected output schema specifies float variables for NumMocha and NumRegularCoffee.
- This model minimizes the total production time subject to resource and ratio constraints, and is ready to be implemented using Python or OR-Tools code.

Expected Output Schema:
{
  "variables": {
    "NumMocha": "float",
    "NumRegularCoffee": "float"
  },
  "objective": "float"
}'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_with_linear_solver():
    # Create a solver using the GLOP linear programming solver (suitable for continuous LP)
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Solver not created.")
        return None

    # Variables: number of mochas and regular coffees (>= 0, continuous)
    NumMocha = solver.NumVar(0.0, solver.infinity(), 'NumMocha')
    NumRegularCoffee = solver.NumVar(0.0, solver.infinity(), 'NumRegularCoffee')

    # Parameters
    coffeePowderPerMocha = 3
    coffeePowderPerRegular = 6
    milkPerMocha = 6
    milkPerRegular = 2
    availableCoffeePowder = 400
    availableMilk = 500
    productionTimeMocha = 5
    productionTimeRegular = 3
    minMochaToRegularRatio = 3

    # Constraints:
    # 1. Coffee powder constraint: 3*NumMocha + 6*NumRegularCoffee <= 400
    solver.Add(coffeePowderPerMocha * NumMocha + coffeePowderPerRegular * NumRegularCoffee <= availableCoffeePowder)

    # 2. Milk constraint: 6*NumMocha + 2*NumRegularCoffee <= 500
    solver.Add(milkPerMocha * NumMocha + milkPerRegular * NumRegularCoffee <= availableMilk)

    # 3. Demand ratio constraint: NumMocha >= 3 * NumRegularCoffee
    solver.Add(NumMocha >= minMochaToRegularRatio * NumRegularCoffee)

    # Objective: Minimize total production time (5*NumMocha + 3*NumRegularCoffee)
    objective = solver.Objective()
    objective.SetCoefficient(NumMocha, productionTimeMocha)
    objective.SetCoefficient(NumRegularCoffee, productionTimeRegular)
    objective.SetMinimization()

    status = solver.Solve()

    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result["variables"] = {
            "NumMocha": NumMocha.solution_value(),
            "NumRegularCoffee": NumRegularCoffee.solution_value()
        }
        result["objective"] = objective.Value()
    elif status == pywraplp.Solver.FEASIBLE:
        result["message"] = "A feasible solution was found, but it might not be optimal."
    else:
        result["message"] = "The problem does not have an optimal solution."

    return result

def main():
    # Solve the problem using the linear solver implementation
    print("Solution using ortools.linear_solver:")
    linear_solution = solve_with_linear_solver()
    print(linear_solution)

if __name__ == "__main__":
    main()

'''Execution Results:
SUCCESS:
Solution using ortools.linear_solver:
{'variables': {'NumMocha': 0.0, 'NumRegularCoffee': 0.0}, 'objective': 0.0}
'''

'''Expected Output:
Expected solution

: {'variables': {'NumMocha': -0.0, 'NumRegularCoffee': -0.0}, 'objective': 0.0}'''

