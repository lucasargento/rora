# Problem Description:
'''Problem description: A water company sells water in glass and plastic bottles. A glass bottle can hole 500 ml of water while a plastic bottle can hold 750 ml of water. Because most customer prefer plastic bottles, the number of plastic bottles must be at least 3 times the number of glass bottles. However, there must be at least 20 glass bottles. If the company has available 250000 ml of water, how many of each bottle should be made to maximize the total number of bottles?

Expected Output Schema:
{
  "variables": {
    "PlasticBottles": "float",
    "GlassBottles": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Below is one valid formulation of the problem using the five‐element framework.

-----------------------------------------------------
Sets:
- BottleTypes = {Glass, Plastic}

-----------------------------------------------------
Parameters:
- glass_capacity = 500       // capacity of a glass bottle in ml
- plastic_capacity = 750     // capacity of a plastic bottle in ml
- total_water = 250000       // total available water in ml
- min_glass = 20             // minimum number of glass bottles required
- plastic_factor = 3         // plastic bottles must be at least 3 times the number of glass bottles

-----------------------------------------------------
Variables:
- GlassBottles: integer, number of glass bottles produced (units), GlassBottles ≥ 0
- PlasticBottles: integer, number of plastic bottles produced (units), PlasticBottles ≥ 0

-----------------------------------------------------
Objective:
- Maximize TotalBottles = GlassBottles + PlasticBottles
  (the goal is to maximize the total count of bottles produced)

-----------------------------------------------------
Constraints:
1. Water Constraint:
   500 * GlassBottles + 750 * PlasticBottles ≤ 250000
   (the total water used by the bottles cannot exceed the available 250000 ml)

2. Preference for Plastic Bottles:
   PlasticBottles ≥ 3 * GlassBottles
   (ensures that the number of plastic bottles is at least three times that of glass bottles)

3. Minimum Glass Bottles Constraint:
   GlassBottles ≥ 20
   (at least 20 glass bottles must be produced)
   
-----------------------------------------------------
Expected Output Schema (as JSON):
{
  "variables": {
    "PlasticBottles": "float",
    "GlassBottles": "float"
  },
  "objective": "float"
}

Notes:
- Although the output schema labels the decision variables as float, in a real implementation the bottle counts should be modeled as integers because they represent discrete units.
- All water volumes are in ml, and the capacities are consistent with the available water amount.
- This model assumes that bottles are produced using all available water if possible, while respecting the customer preference and minimum production requirements.
'''

# Generated Code:
#!/usr/bin/env python3
"""
This script solves the water bottle production optimization problem using Google OR-Tools.
The objective is to maximize the total number of bottles produced subject to:
  - Limited total water available (250000 ml)
  - A glass bottle holds 500 ml, a plastic bottle holds 750 ml
  - At least 20 glass bottles must be produced
  - The number of plastic bottles must be at least 3 times the number of glass bottles

We use the ortools.linear_solver module to model and solve the linear integer optimization problem.
"""

from ortools.linear_solver import pywraplp

def solve_with_linear_solver():
    # Create the solver using the SCIP backend (or you can choose CBC)
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        print("Solver not created.")
        return None

    # Define parameters
    glass_capacity = 500       # ml per glass bottle
    plastic_capacity = 750     # ml per plastic bottle
    total_water = 250000       # total available water in ml
    min_glass = 20             # minimum number of glass bottles required

    # Define decision variables
    # GlassBottles: integer variable with lower bound 20 (min_glass) and no upper bound.
    glass_bottles = solver.IntVar(min_glass, solver.infinity(), "GlassBottles")
    # PlasticBottles: integer variable with non-negative domain.
    plastic_bottles = solver.IntVar(0, solver.infinity(), "PlasticBottles")

    # Constraint 1: Water usage must not exceed total water available.
    # 500 * GlassBottles + 750 * PlasticBottles <= 250000
    solver.Add(glass_capacity * glass_bottles + plastic_capacity * plastic_bottles <= total_water)

    # Constraint 2: The number of plastic bottles must be at least 3 times the number of glass bottles.
    solver.Add(plastic_bottles >= 3 * glass_bottles)

    # Objective: maximize the total number of bottles produced.
    # TotalBottles = GlassBottles + PlasticBottles
    objective = solver.Objective()
    objective.SetCoefficient(glass_bottles, 1)
    objective.SetCoefficient(plastic_bottles, 1)
    objective.SetMaximization()

    # Solve the problem
    status = solver.Solve()

    # Check the result status. If an optimal solution is found, build the result output.
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        result = {
            "PlasticBottles": plastic_bottles.solution_value(),
            "GlassBottles": glass_bottles.solution_value(),
            "objective": objective.Value()
        }
        return result
    else:
        print("No feasible solution found.")
        return None

def main():
    # Solve the problem using the linear solver implementation.
    linear_result = solve_with_linear_solver()
    
    # Structured output of the results.
    if linear_result:
        print("Solution from OR-Tools Linear Solver Model:")
        print(linear_result)
    else:
        print("No solution found using the OR-Tools Linear Solver Model.")

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Solution from OR-Tools Linear Solver Model:
{'PlasticBottles': 273.0, 'GlassBottles': 90.0, 'objective': 363.0}
'''

'''Expected Output:
Expected solution

: {'variables': {'PlasticBottles': 274.0, 'GlassBottles': 89.0}, 'objective': 363.0}'''

