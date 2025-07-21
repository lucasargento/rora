# Problem Description:
'''Problem description: A university research lab can make two types of diabetes medicine, medicine A and medicine B. Per dose, medicine A takes 30 units of imported material and 50 units of mRNA to make. Per dose, medicine B takes 40 units of imported material and 30 units of mRNA to take. The lab has available at most 300 units of imported material and 400 units of mRNA. The lab can make at most 5 doses of medicine A and the number of doses of medicine B must be larger than the number of dosed of medicine A. If one dose of medicine A can treat 12 people and one dose of medicine B can treat 8 people, how many doses of each should be made to maximize the number of people that can be treated?

Expected Output Schema:
{
  "variables": {
    "DosesA": "float",
    "DosesB": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- M: set of medicines = {A, B}

Parameters:
- imported_A: imported material required per dose of medicine A = 30 [units per dose]
- imported_B: imported material required per dose of medicine B = 40 [units per dose]
- mRNA_A: mRNA required per dose of medicine A = 50 [units per dose]
- mRNA_B: mRNA required per dose of medicine B = 30 [units per dose]
- treat_A: number of people treated per dose of medicine A = 12 [people per dose]
- treat_B: number of people treated per dose of medicine B = 8 [people per dose]
- max_imported: available imported material = 300 [units]
- max_mRNA: available mRNA = 400 [units]
- max_doses_A: maximum doses of medicine A that can be produced = 5 [doses]
- epsilon: a small positive number to enforce that doses of medicine B are strictly greater than doses of medicine A (e.g., 0.001)

Variables:
- DosesA: number of doses of medicine A produced [continuous; expected to be integer in practice; units: doses]
- DosesB: number of doses of medicine B produced [continuous; expected to be integer in practice; units: doses]

Objective:
- Maximize total number of people treated = (treat_A * DosesA) + (treat_B * DosesB)

Constraints:
1. Imported material constraint:
   (imported_A * DosesA) + (imported_B * DosesB) <= max_imported
2. mRNA constraint:
   (mRNA_A * DosesA) + (mRNA_B * DosesB) <= max_mRNA
3. Production limit for medicine A:
   DosesA <= max_doses_A
4. Relative production constraint:
   DosesB >= DosesA + epsilon
   (Note: The epsilon parameter ensures that the number of doses of medicine B is strictly larger than the number of doses of medicine A. If a nonstrict inequality (i.e., DosesB >= DosesA) is acceptable, then epsilon may be set to 0.)

---

Expected Output Schema:
{
  "variables": {
    "DosesA": "float",
    "DosesB": "float"
  },
  "objective": "float"
}'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_model_strict():
    """
    Model 1: Using strict inequality for the relative production constraint.
    i.e., DosesB >= DosesA + epsilon, with epsilon set effectively to 1 for integer variables.
    """
    # Create the solver using CBC mixed integer programming.
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Solver not found.")
        return None

    # Parameters
    imported_A = 30
    imported_B = 40
    mRNA_A = 50
    mRNA_B = 30
    treat_A = 12
    treat_B = 8
    max_imported = 300
    max_mRNA = 400
    max_doses_A = 5
    # For strict inequality in integer context, using epsilon = 1 ensures DosesB > DosesA.
    epsilon_int = 1

    # Variables: using integer variables since doses are discrete.
    DosesA = solver.IntVar(0, max_doses_A, 'DosesA')
    # Upper bound for DosesB can be derived from resource constraints; we use a safe upper bound.
    DosesB = solver.IntVar(0, solver.infinity(), 'DosesB')

    # Constraints:
    # 1. Imported material constraint: 30*DosesA + 40*DosesB <= 300.
    solver.Add(imported_A * DosesA + imported_B * DosesB <= max_imported)

    # 2. mRNA constraint: 50*DosesA + 30*DosesB <= 400.
    solver.Add(mRNA_A * DosesA + mRNA_B * DosesB <= max_mRNA)

    # 3. Production limit for medicine A is already enforced by variable upper bound.
    # (DosesA <= max_doses_A) is implicitly satisfied.

    # 4. Relative production constraint: DosesB >= DosesA + epsilon.
    solver.Add(DosesB >= DosesA + epsilon_int)

    # Objective: Maximize total people treated = 12*DosesA + 8*DosesB.
    objective = solver.Objective()
    objective.SetCoefficient(DosesA, treat_A)
    objective.SetCoefficient(DosesB, treat_B)
    objective.SetMaximization()

    status = solver.Solve()

    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "variables": {
                "DosesA": DosesA.solution_value(),
                "DosesB": DosesB.solution_value()
            },
            "objective": objective.Value()
        }
    else:
        result = {"message": "The strict model did not find an optimal solution."}
    return result

def solve_model_nonstrict():
    """
    Model 2: Using non-strict inequality for the relative production constraint.
    i.e., DosesB >= DosesA (epsilon = 0 case).
    """
    # Create the solver using CBC mixed integer programming.
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Solver not found.")
        return None

    # Parameters
    imported_A = 30
    imported_B = 40
    mRNA_A = 50
    mRNA_B = 30
    treat_A = 12
    treat_B = 8
    max_imported = 300
    max_mRNA = 400
    max_doses_A = 5
    epsilon_int = 0  # no strict inequality

    # Variables: using integer variables.
    DosesA = solver.IntVar(0, max_doses_A, 'DosesA')
    DosesB = solver.IntVar(0, solver.infinity(), 'DosesB')

    # Constraints:
    solver.Add(imported_A * DosesA + imported_B * DosesB <= max_imported)
    solver.Add(mRNA_A * DosesA + mRNA_B * DosesB <= max_mRNA)
    # Production limit for medicine A is implicitly defined by variable bound.
    solver.Add(DosesB >= DosesA + epsilon_int)

    # Objective: Maximize total people treated = 12*DosesA + 8*DosesB.
    objective = solver.Objective()
    objective.SetCoefficient(DosesA, treat_A)
    objective.SetCoefficient(DosesB, treat_B)
    objective.SetMaximization()

    status = solver.Solve()

    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "variables": {
                "DosesA": DosesA.solution_value(),
                "DosesB": DosesB.solution_value()
            },
            "objective": objective.Value()
        }
    else:
        result = {"message": "The non-strict model did not find an optimal solution."}
    return result

def main():
    # Solve both model versions.
    result_strict = solve_model_strict()
    result_nonstrict = solve_model_nonstrict()

    # Print results in a structured way.
    print("Results for Model with Strict Inequality (DosesB >= DosesA + epsilon with epsilon=1):")
    print(result_strict)
    print("\nResults for Model with Non-Strict Inequality (DosesB >= DosesA):")
    print(result_nonstrict)

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Results for Model with Strict Inequality (DosesB >= DosesA + epsilon with epsilon=1):
{'variables': {'DosesA': 3.0, 'DosesB': 5.0}, 'objective': 76.0}

Results for Model with Non-Strict Inequality (DosesB >= DosesA):
{'variables': {'DosesA': 4.0, 'DosesB': 4.0}, 'objective': 80.0}
'''

'''Expected Output:
Expected solution

: {'variables': {'DosesA': 3.7142857142857144, 'DosesB': 4.714285714285714}, 'objective': 82.28571428571428}'''

