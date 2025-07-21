# Problem Description:
'''Problem description: A doctor suggests that his patient eat oranges and grapefruit to meet his vitamin C and vitamin A requirements. One orange contains 5 units of vitamin C, 3 units of vitamin A, and 5 grams of sugar. One grapefruit contains 7 units of vitamin C, 5 units of vitamin A, and 6 grams of sugar. The patient must get at least 80 units of vitamin C and 70 units of vitamin A. Since the patent prefers oranges, he must eat at least 2 times as many oranges as grapefruit. How many of each should he eat to minimize his sugar intake?

Expected Output Schema:
{
  "variables": {
    "NumberOfOranges": "float",
    "NumberOfGrapefruits": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- F: set of fruits = {Orange, Grapefruit}

Parameters:
- vitaminC_f: vitamin C content per unit of fruit f
  - vitaminC_Orange = 5 units per orange
  - vitaminC_Grapefruit = 7 units per grapefruit
- vitaminA_f: vitamin A content per unit of fruit f
  - vitaminA_Orange = 3 units per orange
  - vitaminA_Grapefruit = 5 units per grapefruit
- sugar_f: sugar content per unit of fruit f [grams]
  - sugar_Orange = 5 grams per orange
  - sugar_Grapefruit = 6 grams per grapefruit
- req_vitaminC: required vitamin C intake = 80 units
- req_vitaminA: required vitamin A intake = 70 units
- min_ratio_oranges: minimum ratio of oranges to grapefruits = 2

Variables:
- x_Orange: number of oranges to eat [nonnegative integer, units]
- x_Grapefruit: number of grapefruits to eat [nonnegative integer, units]

Objective:
- Minimize total sugar intake
  TotalSugar = sugar_Orange * x_Orange + sugar_Grapefruit * x_Grapefruit

Constraints:
1. Vitamin C requirement:
   vitaminC_Orange * x_Orange + vitaminC_Grapefruit * x_Grapefruit ≥ req_vitaminC
   i.e., 5 * x_Orange + 7 * x_Grapefruit ≥ 80

2. Vitamin A requirement:
   vitaminA_Orange * x_Orange + vitaminA_Grapefruit * x_Grapefruit ≥ req_vitaminA
   i.e., 3 * x_Orange + 5 * x_Grapefruit ≥ 70

3. Preference for oranges:
   x_Orange ≥ min_ratio_oranges * x_Grapefruit
   i.e., x_Orange ≥ 2 * x_Grapefruit

Note:
- All units are consistent: vitamins in “units” and sugar in “grams.”
- The decision variables (x_Orange and x_Grapefruit) are assumed to be integers since the patient can only eat whole fruits.

Expected Output Schema:
{
  "variables": {
    "NumberOfOranges": "x_Orange",
    "NumberOfGrapefruits": "x_Grapefruit"
  },
  "objective": "TotalSugar"
}'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_with_linear_solver():
    # Create the mip solver with SCIP backend.
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        print("Solver not found.")
        return None

    # Decision variables: x_Orange and x_Grapefruit (nonnegative integers)
    x_Orange = solver.IntVar(0, solver.infinity(), 'x_Orange')
    x_Grapefruit = solver.IntVar(0, solver.infinity(), 'x_Grapefruit')
    
    # Parameters as defined in the problem statement.
    # Vitamins and sugar contents:
    vitaminC_Orange = 5
    vitaminC_Grapefruit = 7
    vitaminA_Orange = 3
    vitaminA_Grapefruit = 5
    sugar_Orange = 5
    sugar_Grapefruit = 6
    req_vitaminC = 80
    req_vitaminA = 70
    min_ratio_oranges = 2

    # Constraints:
    # 1. Vitamin C requirement: 5*x_Orange + 7*x_Grapefruit >= 80
    solver.Add(vitaminC_Orange * x_Orange + vitaminC_Grapefruit * x_Grapefruit >= req_vitaminC)
    
    # 2. Vitamin A requirement: 3*x_Orange + 5*x_Grapefruit >= 70
    solver.Add(vitaminA_Orange * x_Orange + vitaminA_Grapefruit * x_Grapefruit >= req_vitaminA)
    
    # 3. Preference for oranges: x_Orange >= 2*x_Grapefruit
    solver.Add(x_Orange >= min_ratio_oranges * x_Grapefruit)
    
    # Objective: Minimize total sugar intake
    objective = solver.Objective()
    objective.SetCoefficient(x_Orange, sugar_Orange)
    objective.SetCoefficient(x_Grapefruit, sugar_Grapefruit)
    objective.SetMinimization()
    
    status = solver.Solve()
    
    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "variables": {
                "NumberOfOranges": x_Orange.solution_value(),
                "NumberOfGrapefruits": x_Grapefruit.solution_value()
            },
            "objective": objective.Value()
        }
        return result
    else:
        print("The problem does not have an optimal solution.")
        return None

def main():
    print("Solution using OR-Tools Linear Solver:")
    result = solve_with_linear_solver()
    if result is not None:
        print(result)
    else:
        print("No feasible solution found.")

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Solution using OR-Tools Linear Solver:
{'variables': {'NumberOfOranges': 15.0, 'NumberOfGrapefruits': 5.0}, 'objective': 105.0}
'''

'''Expected Output:
Expected solution

: {'variables': {'NumberOfOranges': 15.0, 'NumberOfGrapefruits': 5.0}, 'objective': 105.0}'''

