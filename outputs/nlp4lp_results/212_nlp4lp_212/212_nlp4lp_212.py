# Problem Description:
'''Problem description: A macro-counting fitness guru only eats salmon and eggs. Each bowl of salmon contains 300 calories, 15 grams of protein, and 80 mg of sodium. Each bowl of eggs contains 200 calories, 8 grams of protein, and 20 mg of sodium. Since the fitness guru has a limit to how many eggs he would like to eat, at most 40% of his meals can be eggs. The fitness guru needs to eat at least 2000 calories and 90 grams of protein. How many of each type of meal should he eat to minimize his sodium intake?

Expected Output Schema:
{
  "variables": {
    "NumMealsPerFoodType": {
      "0": "float",
      "1": "float"
    }
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- F: set of food types = {salmon, eggs}

Parameters:
- calories[f]: calories per bowl of food f
   • salmon: 300 calories per bowl
   • eggs: 200 calories per bowl
- protein[f]: protein (grams) per bowl of food f
   • salmon: 15 grams per bowl
   • eggs: 8 grams per bowl
- sodium[f]: sodium (mg) per bowl of food f
   • salmon: 80 mg per bowl
   • eggs: 20 mg per bowl
- min_calories: minimum required calories per day = 2000 calories
- min_protein: minimum required protein per day = 90 grams
- max_eggs_ratio: maximum fraction of meals that can be eggs = 0.4  
  (Note: This means eggs can be at most 40% of total meals)
  
Variables:
- x[f]: number of bowls of food f to consume [continuous, x[f] ≥ 0]
  • x[salmon]: number of salmon bowls
  • x[eggs]: number of eggs bowls

Objective:
- Minimize total sodium intake = (80 * x[salmon]) + (20 * x[eggs])  
  (Units: mg)

Constraints:
1. Calorie constraint: (300 * x[salmon]) + (200 * x[eggs]) ≥ 2000
2. Protein constraint: (15 * x[salmon]) + (8 * x[eggs]) ≥ 90
3. Egg meal ratio constraint:
   Since at most 40% of the meals can be eggs, we have 
   x[eggs] ≤ 0.4 * (x[salmon] + x[eggs])
   This can be rearranged to: x[eggs] ≤ (2/3) * x[salmon]
4. Non-negativity: x[salmon] ≥ 0 and x[eggs] ≥ 0

Comments:
- The egg ratio constraint was algebraically rearranged from 
  x[eggs] ≤ 0.4 * (x[salmon] + x[eggs]) to avoid nonlinearity.
- While bowls are countable, we model the decision variables as continuous (floats) per the expected output schema.

This complete five-element model faithfully translates the given real-world optimization problem.'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_model():
    # Create the linear solver with the GLOP backend (for linear programming)
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Error: GLOP solver unavailable.")
        return None

    # Declare decision variables
    # x_salmon: number of salmon bowls, x_eggs: number of eggs bowls.
    x_salmon = solver.NumVar(0.0, solver.infinity(), 'x_salmon')
    x_eggs = solver.NumVar(0.0, solver.infinity(), 'x_eggs')

    # Parameters
    min_calories = 2000
    min_protein = 90
    # Nutritional values per bowl
    calories_salmon = 300
    calories_eggs = 200
    protein_salmon = 15
    protein_eggs = 8
    sodium_salmon = 80
    sodium_eggs = 20

    # Constraints

    # Calorie constraint: (300 * x_salmon) + (200 * x_eggs) >= 2000
    solver.Add(calories_salmon * x_salmon + calories_eggs * x_eggs >= min_calories)

    # Protein constraint: (15 * x_salmon) + (8 * x_eggs) >= 90
    solver.Add(protein_salmon * x_salmon + protein_eggs * x_eggs >= min_protein)
    
    # Egg meal ratio constraint: x_eggs <= (2/3)* x_salmon.
    # Derived from x[eggs] ≤ 0.4*(x[salmon]+x[eggs])
    solver.Add(x_eggs <= (2.0 / 3.0) * x_salmon)

    # Objective: Minimize total sodium intake = (80 * x_salmon) + (20 * x_eggs)
    objective = solver.Minimize(sodium_salmon * x_salmon + sodium_eggs * x_eggs)

    # Solve the problem
    status = solver.Solve()

    # Parse solution
    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result['status'] = "OPTIMAL"
        result['values'] = {
            "NumMealsPerFoodType": {
                "0": x_salmon.solution_value(),  # Salmon bowls
                "1": x_eggs.solution_value()       # Eggs bowls
            }
        }
        result['objective'] = solver.Objective().Value()
    elif status == pywraplp.Solver.FEASIBLE:
        result['status'] = "FEASIBLE (suboptimal)"
        result['values'] = {
            "NumMealsPerFoodType": {
                "0": x_salmon.solution_value(),
                "1": x_eggs.solution_value()
            }
        }
        result['objective'] = solver.Objective().Value()
    else:
        result['status'] = "No feasible solution found"
        result['values'] = None
        result['objective'] = None

    return result

def main():
    # Since the mathematical formulation provided leads us to a single model,
    # we implement one version using OR-Tools Linear Solver.
    results = {}
    
    # Implementation 1: Using Linear Programming as modeled above.
    results['Implementation1'] = solve_model()
    
    # Display results in structured format.
    print("Results Summary:")
    for impl, res in results.items():
        print("-------------------------------------------------")
        print(f"{impl}:")
        if res['status'] in ["OPTIMAL", "FEASIBLE (suboptimal)"]:
            print(f"Status    : {res['status']}")
            print("Variables:")
            num_meals = res['values']["NumMealsPerFoodType"]
            # index 0: Salmon, index 1: Eggs.
            print(f"  Salmon bowls (index 0): {num_meals['0']}")
            print(f"  Eggs bowls   (index 1): {num_meals['1']}")
            print(f"Objective : {res['objective']} (minimum total sodium intake in mg)")
        else:
            print("No feasible solution found.")
    print("-------------------------------------------------")

if __name__ == "__main__":
    main()

'''Execution Results:
SUCCESS:
Results Summary:
-------------------------------------------------
Implementation1:
Status    : OPTIMAL
Variables:
  Salmon bowls (index 0): 4.615384615384616
  Eggs bowls   (index 1): 3.076923076923077
Objective : 430.76923076923083 (minimum total sodium intake in mg)
-------------------------------------------------
'''

'''Expected Output:
Expected solution

: {'variables': {'NumMealsPerFoodType': {'0': 0.0, '1': 12.0}}, 'objective': 240.0}'''

