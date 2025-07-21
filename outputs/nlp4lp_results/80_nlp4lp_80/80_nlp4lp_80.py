# Problem Description:
'''Problem description: A patient in the hospital can take two pills, Pill 1 and Pill 2. Per pill, pill 1 provides 0.2 units of pain medication and 0.3 units of anxiety medication. Per pill, pill 2 provides 0.6 units of pain medication and 0.2 units of anxiety medication. In addition, pill 1 causes 0.3 units of discharge while pill 2 causes 0.1 units of discharge. At most 6 units of pain medication can be provided and at least 3 units of anxiety medication must be provided. How many pills of each should the patient be given to minimize the total amount of discharge?

Expected Output Schema:
{
  "variables": {
    "NumberOfPills": {
      "0": "float",
      "1": "float"
    }
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- Pills: set of pill types = {1, 2}

Parameters:
- pain_per_pill: amount of pain medication provided per pill, with
  - For Pill 1: 0.2 [units/pill]
  - For Pill 2: 0.6 [units/pill]
- anxiety_per_pill: amount of anxiety medication provided per pill, with
  - For Pill 1: 0.3 [units/pill]
  - For Pill 2: 0.2 [units/pill]
- discharge_per_pill: amount of discharge caused per pill, with
  - For Pill 1: 0.3 [units/pill]
  - For Pill 2: 0.1 [units/pill]
- max_total_pain: maximum allowed total pain medication = 6 [units]
- min_total_anxiety: minimum required total anxiety medication = 3 [units]

Variables:
- x[i] for each pill i in Pills:
  - x[1]: number of Pill 1 to administer [continuous, x[1] ≥ 0]
  - x[2]: number of Pill 2 to administer [continuous, x[2] ≥ 0]

Objective:
- Minimize total discharge = (0.3 * x[1]) + (0.1 * x[2])

Constraints:
1. Pain Medication Constraint:
   - (0.2 * x[1]) + (0.6 * x[2]) ≤ 6
2. Anxiety Medication Constraint:
   - (0.3 * x[1]) + (0.2 * x[2]) ≥ 3
3. Non-negativity:
   - x[1] ≥ 0, x[2] ≥ 0

Comments:
- All units are consistent with the problem description (units of medication or discharge per pill).
- Although pills are naturally discrete, the decision variables are modeled as continuous (float) as specified in the expected output schema.'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_model_version1():
    # Create the linear solver using the GLOP backend.
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        return {"message": "Solver unavailable."}
    
    # Define variables:
    # x[1]: number of Pill 1 to administer (continuous, non-negative)
    # x[2]: number of Pill 2 to administer (continuous, non-negative)
    pill1 = solver.NumVar(0.0, solver.infinity(), 'Pill1')
    pill2 = solver.NumVar(0.0, solver.infinity(), 'Pill2')
    
    # Constraint 1: Pain Medication Constraint
    # (0.2 * pill1) + (0.6 * pill2) <= 6
    solver.Add(0.2 * pill1 + 0.6 * pill2 <= 6)
    
    # Constraint 2: Anxiety Medication Constraint
    # (0.3 * pill1) + (0.2 * pill2) >= 3
    solver.Add(0.3 * pill1 + 0.2 * pill2 >= 3)
    
    # Objective: Minimize total discharge = (0.3 * pill1) + (0.1 * pill2)
    solver.Minimize(0.3 * pill1 + 0.1 * pill2)
    
    # Solve the model.
    status = solver.Solve()
    
    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "variables": {
                "NumberOfPills": {
                    "0": pill1.solution_value(),
                    "1": pill2.solution_value()
                }
            },
            "objective": solver.Objective().Value()
        }
    else:
        result = {"message": "No optimal solution found."}
    
    return result

def main():
    # Since only one formulation is provided, we run a single implementation.
    solution_version1 = solve_model_version1()
    
    # Print results in a structured way.
    print("Solution for Model Version 1:")
    print(solution_version1)

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Solution for Model Version 1:
{'variables': {'NumberOfPills': {'0': 4.2857142857142865, '1': 8.57142857142857}}, 'objective': 2.142857142857143}
'''

'''Expected Output:
Expected solution

: {'variables': {'NumberOfPills': {'0': 5.0, '1': 8.0}}, 'objective': 2.3}'''

