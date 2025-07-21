# Problem Description:
'''Problem description: A body builder buys pre prepared meals, a turkey dinner and a tuna salad sandwich. The turkey dinner contains 20 grams of protein, 30 grams of carbs, and 12 grams of fat. The tuna salad sandwich contains 18 grams of protein, 25 grams of carbs, and 8 grams of fat. The bodybuilder wants to get at least 150 grams of protein and 200 grams of carbs. In addition because the turkey dinner is expensive, at most 40% of the meals should be turkey dinner. How many of each meal should he eat if he wants to minimize his fat intake?

Expected Output Schema:
{
  "variables": {
    "QuantityTurkey": "float",
    "QuantityTuna": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Below is the structured model using the five-element framework.

------------------------------------------------------------
Sets:
- M: set of meal types = {TurkeyDinner, TunaSaladSandwich}

Parameters:
- protein[m]: grams of protein per meal m
  • protein[TurkeyDinner] = 20 (grams per meal)
  • protein[TunaSaladSandwich] = 18 (grams per meal)
- carbs[m]: grams of carbohydrates per meal m
  • carbs[TurkeyDinner] = 30 (grams per meal)
  • carbs[TunaSaladSandwich] = 25 (grams per meal)
- fat[m]: grams of fat per meal m
  • fat[TurkeyDinner] = 12 (grams per meal)
  • fat[TunaSaladSandwich] = 8 (grams per meal)
- min_protein: minimum total protein required = 150 (grams)
- min_carbs: minimum total carbohydrates required = 200 (grams)
- max_turkey_ratio: maximum fraction of turkey dinner = 0.4

Variables:
- QuantityTurkey: number of turkey dinners to buy [continuous, ≥ 0] [meals]
- QuantityTuna: number of tuna salad sandwiches to buy [continuous, ≥ 0] [meals]

Objective:
- Minimize total fat intake = (12 * QuantityTurkey) + (8 * QuantityTuna)
  (Units: grams of fat)

Constraints:
1. Protein requirement:
  20 * QuantityTurkey + 18 * QuantityTuna ≥ min_protein
2. Carbohydrate requirement:
  30 * QuantityTurkey + 25 * QuantityTuna ≥ min_carbs
3. Turkey meal limitation (ensuring turkey dinners are at most 40% of total meals):
  QuantityTurkey ≤ max_turkey_ratio * (QuantityTurkey + QuantityTuna)

------------------------------------------------------------
This structured model fully represents the original problem with clear sets, parameters, decision variables, objective, and constraints.'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_linear_model():
    # Create the solver using GLOP, suitable for linear programming.
    solver = pywraplp.Solver('MealOptimization_LP', pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)

    # Decision Variables:
    # QuantityTurkey: number of turkey dinners to buy (continuous, non-negative)
    # QuantityTuna: number of tuna salad sandwiches to buy (continuous, non-negative)
    QuantityTurkey = solver.NumVar(0.0, solver.infinity(), 'QuantityTurkey')
    QuantityTuna   = solver.NumVar(0.0, solver.infinity(), 'QuantityTuna')

    # Parameters:
    # Nutritional content per meal
    protein_turkey = 20  # grams protein in turkey dinner
    protein_tuna   = 18  # grams protein in tuna salad sandwich
    carbs_turkey   = 30  # grams carbs in turkey dinner
    carbs_tuna     = 25  # grams carbs in tuna salad sandwich
    fat_turkey     = 12  # grams fat in turkey dinner
    fat_tuna       = 8   # grams fat in tuna salad sandwich

    # Minimum nutritional requirements
    min_protein = 150  # grams
    min_carbs   = 200  # grams

    # Maximum ratio for turkey dinners (at most 40% of total meals)
    max_turkey_ratio = 0.4

    # Constraints:
    # 1. Protein requirement: 20 * QuantityTurkey + 18 * QuantityTuna >= 150
    solver.Add(protein_turkey * QuantityTurkey + protein_tuna * QuantityTuna >= min_protein)

    # 2. Carbohydrate requirement: 30 * QuantityTurkey + 25 * QuantityTuna >= 200
    solver.Add(carbs_turkey * QuantityTurkey + carbs_tuna * QuantityTuna >= min_carbs)

    # 3. Turkey meal limitation:
    #    QuantityTurkey <= max_turkey_ratio * (QuantityTurkey + QuantityTuna)
    # This is a linear constraint since the right side expands to 0.4 * QuantityTurkey + 0.4 * QuantityTuna.
    solver.Add(QuantityTurkey <= max_turkey_ratio * (QuantityTurkey + QuantityTuna))

    # Objective:
    # Minimize total fat intake = (12 * QuantityTurkey) + (8 * QuantityTuna)
    objective = solver.Objective()
    objective.SetCoefficient(QuantityTurkey, fat_turkey)
    objective.SetCoefficient(QuantityTuna, fat_tuna)
    objective.SetMinimization()

    # Solve the model
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        solution = {
            "QuantityTurkey": QuantityTurkey.solution_value(),
            "QuantityTuna": QuantityTuna.solution_value()
        }
        objective_value = solver.Objective().Value()
        return solution, objective_value
    else:
        return None, None

def main():
    # Only one formulation is provided so we have a single implementation
    solution_lp, objective_lp = solve_linear_model()
    
    print("---- Linear Solver Model ----")
    if solution_lp is None:
        print("No optimal solution found for the linear model.")
    else:
        print("Optimal Solution:")
        print("QuantityTurkey =", solution_lp["QuantityTurkey"])
        print("QuantityTuna   =", solution_lp["QuantityTuna"])
        print("Objective Value (Total Fat) =", objective_lp)

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
---- Linear Solver Model ----
Optimal Solution:
QuantityTurkey = 0.0
QuantityTuna   = 8.333333333333334
Objective Value (Total Fat) = 66.66666666666667
'''

'''Expected Output:
Expected solution

: {'variables': {'QuantityTurkey': 0.0, 'QuantityTuna': 8.333333333333334}, 'objective': 66.66666666666667}'''

