# Problem Description:
'''Problem description: A drop-in clinic is performing a test either through the ear or blood. A blood test takes 30 minutes to perform while an ear test takes 5 minutes to perform. Since the blood test is more accurate, at least three times as many blood tests should be performed as ear tests. However, at least 12 ear tests must be administered. If the drop-in clinic operates for 7525 minutes, maximize the number of tests that can be performed.

Expected Output Schema:
{
  "variables": {
    "NumberOfBloodTests": "float",
    "NumberOfEarTests": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- T: set of test types = {Blood, Ear}

Parameters:
- time_blood = 30 (minutes per blood test)
- time_ear = 5 (minutes per ear test)
- total_operating_time = 7525 (minutes available)
- ratio_blood_to_ear = 3 (for every ear test, at least 3 blood tests must be conducted)
- min_ear_tests = 12 (minimum number of ear tests)

Variables:
- NumberOfBloodTests: integer ≥ 0 (number of blood tests to perform)
- NumberOfEarTests: integer ≥ 0 (number of ear tests to perform)

Objective:
Maximize the total number of tests performed, i.e.
  TotalTests = NumberOfBloodTests + NumberOfEarTests

Constraints:
1. Time Constraint: 30 * NumberOfBloodTests + 5 * NumberOfEarTests ≤ 7525  
  (The combined test durations cannot exceed the clinic’s available time.)
2. Accuracy (Ratio) Constraint: NumberOfBloodTests ≥ 3 * NumberOfEarTests  
  (Blood tests must be at least three times the ear tests.)
3. Minimum Ear Tests Constraint: NumberOfEarTests ≥ 12  
  (At least 12 ear tests must be administered.)

---------------------------------------------------------------------
Based on the Expected Output Schema, here is the corresponding JSON output:

{
  "variables": {
    "NumberOfBloodTests": "integer >= 0",
    "NumberOfEarTests": "integer >= 0"
  },
  "objective": "Maximize NumberOfBloodTests + NumberOfEarTests under the constraints: 30*NumberOfBloodTests + 5*NumberOfEarTests <= 7525, NumberOfBloodTests >= 3*NumberOfEarTests, and NumberOfEarTests >= 12."
}'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_linear_program():
    # Create a MIP solver with the CBC backend.
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Solver not created.")
        return None

    # Define parameters.
    time_blood = 30    # minutes per blood test
    time_ear = 5       # minutes per ear test
    total_operating_time = 7525  # total available minutes
    ratio_blood_to_ear = 3       # blood tests must be at least 3 times ear tests
    min_ear_tests = 12           # minimum ear tests

    # Define variables: integers >= 0.
    blood = solver.IntVar(0, solver.infinity(), 'NumberOfBloodTests')
    ear = solver.IntVar(0, solver.infinity(), 'NumberOfEarTests')

    # Add constraints.
    # 1. Time constraint: 30 * blood + 5 * ear <= 7525.
    solver.Add(time_blood * blood + time_ear * ear <= total_operating_time)
    
    # 2. Ratio constraint: blood >= 3 * ear.
    solver.Add(blood >= ratio_blood_to_ear * ear)
    
    # 3. Minimum ear tests: ear >= 12.
    solver.Add(ear >= min_ear_tests)

    # Objective: maximize total number of tests (blood + ear).
    objective = solver.Objective()
    objective.SetCoefficient(blood, 1)
    objective.SetCoefficient(ear, 1)
    objective.SetMaximization()

    # Solve the problem.
    status = solver.Solve()

    # Format and return results.
    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result['status'] = 'OPTIMAL'
        result['NumberOfBloodTests'] = blood.solution_value()
        result['NumberOfEarTests'] = ear.solution_value()
        result['objective'] = objective.Value()
    elif status == pywraplp.Solver.FEASIBLE:
        result['status'] = 'FEASIBLE'
        result['NumberOfBloodTests'] = blood.solution_value()
        result['NumberOfEarTests'] = ear.solution_value()
        result['objective'] = objective.Value()
    else:
        result['status'] = 'NO SOLUTION FOUND'
    return result

def main():
    # As only one mathematical formulation is provided, we only run one implementation.
    results = {}
    results['LinearProgram'] = solve_linear_program()
    
    # Structured printout.
    if results['LinearProgram'] is None or results['LinearProgram'].get('status') not in ['OPTIMAL', 'FEASIBLE']:
        print("The problem is infeasible or no solution was found in the Linear Program model.")
    else:
        print("Results for the Linear Program Model:")
        print("Status             :", results['LinearProgram']['status'])
        print("NumberOfBloodTests :", results['LinearProgram']['NumberOfBloodTests'])
        print("NumberOfEarTests   :", results['LinearProgram']['NumberOfEarTests'])
        print("Objective value    :", results['LinearProgram']['objective'])

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Results for the Linear Program Model:
Status             : OPTIMAL
NumberOfBloodTests : 237.0
NumberOfEarTests   : 79.0
Objective value    : 316.0
'''

'''Expected Output:
Expected solution

: {'variables': {'NumberOfBloodTests': 237.0, 'NumberOfEarTests': 79.0}, 'objective': 316.0}'''

