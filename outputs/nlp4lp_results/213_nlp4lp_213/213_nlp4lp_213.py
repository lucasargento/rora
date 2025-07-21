# Problem Description:
'''Problem description: A restaurant has two combos available to their customers, an original and an experimental meal. The original meal typically generates 20 units of food waste and 45 units of wrapping waste and takes 10 minutes to cook. In comparison, the experimental meal generates 25 units of food waste and 35 units of wrapping waste and takes 15 minutes to cook. The restaurant can have at most 900 units of wrapping waste and can have at most 800 units of food waste as regulated by the government. How many of each combo should be pushed for by the waiting staff to minimize the cooking time?

Expected Output Schema:
{
  "variables": {
    "OriginalMeals": "float",
    "ExperimentalMeals": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- Combos = {Original, Experimental}

Parameters:
- foodWaste_Original = 20  // food waste units per original meal [units/meal]
- foodWaste_Experimental = 25  // food waste units per experimental meal [units/meal]
- wrappingWaste_Original = 45  // wrapping waste units per original meal [units/meal]
- wrappingWaste_Experimental = 35  // wrapping waste units per experimental meal [units/meal]
- cookTime_Original = 10  // cooking time per original meal [minutes/meal]
- cookTime_Experimental = 15  // cooking time per experimental meal [minutes/meal]
- maxFoodWaste = 800  // maximum allowed food waste [units]
- maxWrappingWaste = 900  // maximum allowed wrapping waste [units]

Variables:
- OriginalMeals: number of original meals to be offered (continuous, nonnegative) [meals]
- ExperimentalMeals: number of experimental meals to be offered (continuous, nonnegative) [meals]

Objective:
- Minimize total cooking time, represented as 
  cookTime_Original * OriginalMeals + cookTime_Experimental * ExperimentalMeals
  [minutes]

Constraints:
1. Food waste constraint:
   foodWaste_Original * OriginalMeals + foodWaste_Experimental * ExperimentalMeals ≤ maxFoodWaste
2. Wrapping waste constraint:
   wrappingWaste_Original * OriginalMeals + wrappingWaste_Experimental * ExperimentalMeals ≤ maxWrappingWaste

Notes:
- All parameters are given in consistent units (waste in units, cooking time in minutes, meals in count).
- The decision variables are continuous as specified, though in a practical scenario they may be integer values.'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_linear_model():
    # Create the linear solver with GLOP backend.
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Could not create solver GLOP")
        return None

    # Parameters
    foodWaste_Original = 20    # units per original meal
    foodWaste_Experimental = 25  # units per experimental meal
    wrappingWaste_Original = 45   # units per original meal
    wrappingWaste_Experimental = 35  # units per experimental meal
    cookTime_Original = 10     # minutes per original meal
    cookTime_Experimental = 15   # minutes per experimental meal
    maxFoodWaste = 800         # units
    maxWrappingWaste = 900     # units

    # Decision Variables: continuous and nonnegative
    OriginalMeals = solver.NumVar(0.0, solver.infinity(), 'OriginalMeals')
    ExperimentalMeals = solver.NumVar(0.0, solver.infinity(), 'ExperimentalMeals')

    # Constraints:
    # Food waste constraint: 20*OriginalMeals + 25*ExperimentalMeals <= 800
    solver.Add(foodWaste_Original * OriginalMeals + foodWaste_Experimental * ExperimentalMeals <= maxFoodWaste)
    
    # Wrapping waste constraint: 45*OriginalMeals + 35*ExperimentalMeals <= 900
    solver.Add(wrappingWaste_Original * OriginalMeals + wrappingWaste_Experimental * ExperimentalMeals <= maxWrappingWaste)
    
    # Objective: minimize cooking time, i.e., 10*OriginalMeals + 15*ExperimentalMeals
    objective = solver.Objective()
    objective.SetCoefficient(OriginalMeals, cookTime_Original)
    objective.SetCoefficient(ExperimentalMeals, cookTime_Experimental)
    objective.SetMinimization()
    
    # Solve the problem and check the result.
    status = solver.Solve()
    
    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "variables": {
                "OriginalMeals": OriginalMeals.solution_value(),
                "ExperimentalMeals": ExperimentalMeals.solution_value()
            },
            "objective": objective.Value()
        }
        return result
    else:
        return "The problem does not have an optimal solution."

def main():
    print("Model 1: Linear Programming Formulation using GLOP")
    solution = solve_linear_model()
    print("Optimal solution:")
    print(solution)

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Model 1: Linear Programming Formulation using GLOP
Optimal solution:
{'variables': {'OriginalMeals': 0.0, 'ExperimentalMeals': 0.0}, 'objective': 0.0}
'''

'''Expected Output:
Expected solution

: {'variables': {'OriginalMeals': -0.0, 'ExperimentalMeals': -0.0}, 'objective': 0.0}'''

