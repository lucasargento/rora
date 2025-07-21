# Problem Description:
'''Problem description: A parent feeds their baby two flavors of baby food, apple and carrot, in order to meet the babies fat and folate requirements. Each serving of apple flavored baby food contains 2 units of fat and 5 units of folate. Each serving of carrot flavored baby food contains 4 units of fat and 3 units of folate. The baby does not like the carrot flavor, and therefore he must eat three times as many apple flavored baby food as carrot flavored baby food. However, he must eat at least 2 servings of carrot flavored baby food. If the baby can consume at most 100 units of folate, how many servings of each should he eat to maximize his fat intake?

Expected Output Schema:
{
  "variables": {
    "AppleServings": "float",
    "CarrotServings": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Below is a complete five‐element formulation of the baby food serving problem, expressed in a clear and self-contained format.

------------------------------------------------------------
Sets:
- F: set of baby food flavors = {Apple, Carrot}

Parameters:
- fat_Apple = 2       // fat units per serving of apple-flavored baby food (units/serving)
- fat_Carrot = 4      // fat units per serving of carrot-flavored baby food (units/serving)
- folate_Apple = 5    // folate units per serving of apple-flavored baby food (units/serving)
- folate_Carrot = 3   // folate units per serving of carrot-flavored baby food (units/serving)
- folate_max = 100    // maximum allowed folate intake (units)
- ratio = 3           // baby must eat 3 times as many apple servings as carrot servings (unitless ratio)
- min_Carrot = 2      // minimum number of carrot servings (servings)

Variables:
- AppleServings: integer ≥ 0 
     // number of servings of apple-flavored baby food (servings)
- CarrotServings: integer ≥ 0 
     // number of servings of carrot-flavored baby food (servings)

Objective:
- Maximize TotalFat = fat_Apple * AppleServings + fat_Carrot * CarrotServings
     // This total fat intake is measured in fat units

Constraints:
1. Folate Constraint:
   folate_Apple * AppleServings + folate_Carrot * CarrotServings ≤ folate_max
   // Total folate from both foods must not exceed 100 units

2. Serving Ratio Constraint:
   AppleServings = ratio * CarrotServings
   // The baby must have three times as many apple servings as carrot servings

3. Minimum Carrot Servings:
   CarrotServings ≥ min_Carrot
   // The baby must consume at least 2 servings of carrot-flavored baby food

------------------------------------------------------------
Comments:
- All parameters’ units are consistent: servings yield known fat and folate units.
- Decision variables are defined as integers because servings are counted in whole numbers.
- This model maximizes the baby’s fat intake subject to the folate limit and the serving ratio preference.

Below is the answer in the expected JSON schema format (listing only the decision variables and the objective expression for reference):

{
  "variables": {
    "AppleServings": "integer ≥ 0",
    "CarrotServings": "integer ≥ 0"
  },
  "objective": "Maximize TotalFat = 2 * AppleServings + 4 * CarrotServings"
}'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_with_linear_solver():
    # Create the MIP solver with CBC
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Solver not found!")
        return None

    # Parameters
    fat_Apple = 2
    fat_Carrot = 4
    folate_Apple = 5
    folate_Carrot = 3
    folate_max = 100
    ratio = 3
    min_Carrot = 2

    # Variables: use integer variables for servings
    AppleServings = solver.IntVar(0, solver.infinity(), 'AppleServings')
    CarrotServings = solver.IntVar(0, solver.infinity(), 'CarrotServings')

    # Constraint 1: Folate Constraint
    solver.Add(folate_Apple * AppleServings + folate_Carrot * CarrotServings <= folate_max)

    # Constraint 2: Serving Ratio Constraint: AppleServings = 3 * CarrotServings
    solver.Add(AppleServings == ratio * CarrotServings)

    # Constraint 3: Minimum Carrot Servings
    solver.Add(CarrotServings >= min_Carrot)

    # Objective: Maximize TotalFat = 2 * AppleServings + 4 * CarrotServings
    solver.Maximize(fat_Apple * AppleServings + fat_Carrot * CarrotServings)

    status = solver.Solve()

    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result["variables"] = {
            "AppleServings": int(AppleServings.solution_value()),
            "CarrotServings": int(CarrotServings.solution_value())
        }
        result["objective"] = fat_Apple * AppleServings.solution_value() + fat_Carrot * CarrotServings.solution_value()
    elif status == pywraplp.Solver.FEASIBLE:
        print("A suboptimal solution was found.")
        result["variables"] = {
            "AppleServings": int(AppleServings.solution_value()),
            "CarrotServings": int(CarrotServings.solution_value())
        }
        result["objective"] = fat_Apple * AppleServings.solution_value() + fat_Carrot * CarrotServings.solution_value()
    else:
        result = "The problem does not have an optimal solution."
    
    return result

def solve_with_cp_model():
    # Although the problem is linear, we also provide a CP-SAT version implementation as a separate version.
    from ortools.sat.python import cp_model
    model = cp_model.CpModel()

    # Parameters
    fat_Apple = 2
    fat_Carrot = 4
    folate_Apple = 5
    folate_Carrot = 3
    folate_max = 100
    ratio = 3
    min_Carrot = 2

    max_serving = 1000  # a sufficiently large number for servings domain

    # Variables: using integer domain cp_model.NewIntVar
    AppleServings = model.NewIntVar(0, max_serving, 'AppleServings')
    CarrotServings = model.NewIntVar(0, max_serving, 'CarrotServings')

    # Constraint 1: Folate Constraint
    # folate_Apple * AppleServings + folate_Carrot * CarrotServings <= folate_max
    model.Add(folate_Apple * AppleServings + folate_Carrot * CarrotServings <= folate_max)

    # Constraint 2: Serving Ratio Constraint: AppleServings = 3 * CarrotServings
    model.Add(AppleServings == ratio * CarrotServings)

    # Constraint 3: Minimum Carrot Servings
    model.Add(CarrotServings >= min_Carrot)

    # Objective: Maximize total fat
    totalFat = model.NewIntVar(0, max_serving * max(fat_Apple, fat_Carrot), 'totalFat')
    model.Add(totalFat == fat_Apple * AppleServings + fat_Carrot * CarrotServings)
    model.Maximize(totalFat)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    result = {}
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        result["variables"] = {
            "AppleServings": solver.Value(AppleServings),
            "CarrotServings": solver.Value(CarrotServings)
        }
        result["objective"] = solver.Value(totalFat)
    else:
        result = "The problem does not have an optimal solution."
    
    return result

def main():
    # Solve with the linear solver (MIP)
    result_linear = solve_with_linear_solver()
    # Solve with CP-SAT (also linear in this case)
    result_cp = solve_with_cp_model()

    # Print results in a structured way
    print("Results using ortools.linear_solver:")
    print(result_linear)
    print("\nResults using ortools.sat.python.cp_model:")
    print(result_cp)

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Results using ortools.linear_solver:
{'variables': {'AppleServings': 15, 'CarrotServings': 5}, 'objective': 50.0}

Results using ortools.sat.python.cp_model:
{'variables': {'AppleServings': 15, 'CarrotServings': 5}, 'objective': 50}
'''

'''Expected Output:
Expected solution

: {'variables': {'AppleServings': 16.666666666666668, 'CarrotServings': 5.555555555555556}, 'objective': 55.55555555555556}'''

