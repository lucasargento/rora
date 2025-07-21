# Problem Description:
'''Problem description: A travelling salesman only eats ramen and fries. Each pack of ramen contains 400 calories, 20 grams of protein, and 100 mg of sodium. Each pack of fries contains 300 calories, 10 grams of protein, and 75 mg of sodium. Since fries are easier to eat while driving, at most 30% of his meals can be ramen. The salesman wants to ensure he eats at least 3000 calories and 80 grams of protein. How many of each should he eat to minimize his sodium intake?

Expected Output Schema:
{
  "variables": {
    "NumRamenPacks": "float",
    "NumFriesPacks": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- F: set of food types = {Ramen, Fries}

Parameters:
- calorie_ramen = 400 (calories per ramen pack)
- protein_ramen = 20 (grams per ramen pack)
- sodium_ramen = 100 (mg sodium per ramen pack)
- calorie_fries = 300 (calories per fries pack)
- protein_fries = 10 (grams per fries pack)
- sodium_fries = 75 (mg sodium per fries pack)
- cal_requirement = 3000 (minimum total calories required)
- protein_requirement = 80 (minimum total grams of protein required)
- max_fraction_ramen = 0.3 (maximum fraction of meals that can be ramen packs)

Variables:
- NumRamenPacks: the number of ramen packs consumed (float, ≥ 0)
- NumFriesPacks: the number of fries packs consumed (float, ≥ 0)

Objective:
- Minimize total sodium intake = (sodium_ramen * NumRamenPacks) + (sodium_fries * NumFriesPacks)

Constraints:
1. Calorie constraint: (calorie_ramen * NumRamenPacks) + (calorie_fries * NumFriesPacks) ≥ cal_requirement
2. Protein constraint: (protein_ramen * NumRamenPacks) + (protein_fries * NumFriesPacks) ≥ protein_requirement
3. Ramen fraction constraint: NumRamenPacks ≤ max_fraction_ramen * (NumRamenPacks + NumFriesPacks)
   - This can be equivalently rearranged as: 7 * NumRamenPacks ≤ 3 * NumFriesPacks
4. Nonnegativity: NumRamenPacks, NumFriesPacks ≥ 0

Expected Output Schema:
{
  "variables": {
    "NumRamenPacks": "float",
    "NumFriesPacks": "float"
  },
  "objective": "float"
}'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_linear_program():
    # Create the linear solver with the GLOP backend.
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Solver not available.")
        return None

    # Parameters
    calorie_ramen = 400
    protein_ramen = 20
    sodium_ramen = 100

    calorie_fries = 300
    protein_fries = 10
    sodium_fries = 75

    cal_requirement = 3000
    protein_requirement = 80

    # Variables: Non-negative continuous variables.
    NumRamenPacks = solver.NumVar(0.0, solver.infinity(), 'NumRamenPacks')
    NumFriesPacks = solver.NumVar(0.0, solver.infinity(), 'NumFriesPacks')

    # Constraint 1: Calorie constraint
    solver.Add(calorie_ramen * NumRamenPacks + calorie_fries * NumFriesPacks >= cal_requirement)

    # Constraint 2: Protein constraint
    solver.Add(protein_ramen * NumRamenPacks + protein_fries * NumFriesPacks >= protein_requirement)

    # Constraint 3: Ramen fraction constraint (NumRamenPacks <= 0.3*(NumRamenPacks + NumFriesPacks))
    # Equivalently: 7 * NumRamenPacks <= 3 * NumFriesPacks
    solver.Add(7 * NumRamenPacks <= 3 * NumFriesPacks)

    # Objective: Minimize total sodium intake.
    objective = solver.Objective()
    objective.SetCoefficient(NumRamenPacks, sodium_ramen)
    objective.SetCoefficient(NumFriesPacks, sodium_fries)
    objective.SetMinimization()

    # Solve the linear program.
    status = solver.Solve()

    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result['variables'] = {
            "NumRamenPacks": NumRamenPacks.solution_value(),
            "NumFriesPacks": NumFriesPacks.solution_value()
        }
        result['objective'] = objective.Value()
        print("Linear Programming Model (Google OR-Tools - Linear Solver) Results:")
        print(result)
    else:
        print("The problem does not have an optimal solution.")

    return result

def main():
    # We only have one formulation to implement, so call the linear programming model.
    print("Running optimization model:")
    solve_linear_program()

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Running optimization model:
Linear Programming Model (Google OR-Tools - Linear Solver) Results:
{'variables': {'NumRamenPacks': 2.7272727272727275, 'NumFriesPacks': 6.363636363636364}, 'objective': 750.0}
'''

'''Expected Output:
Expected solution

: {'variables': {'NumRamenPacks': 0.0, 'NumFriesPacks': 10.0}, 'objective': 750.0}'''

