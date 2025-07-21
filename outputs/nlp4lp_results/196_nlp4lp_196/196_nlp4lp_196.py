# Problem Description:
'''Problem description: A disease testing station is conducting a temperature check and/or a blood test on each patient. 
A temperature check takes 2 minutes while a blood test takes 10 minutes. The disease testing station must conduct at least 45 blood tests. 
Since the temperature check is recommended to be performed on most people, the testing station requires that the temperature check is performed at 
least 5 times as many as the blood test. If the disease testing station only has a total of 22000 staff minutes, 
how many of each test or check should be done to maximize the number of patients seen?

Expected Output Schema:
{
  "variables": {
    "TemperatureChecks": "float",
    "BloodTests": "float",
    "PatientsSeen": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- TESTS: Set of test types = {Temperature Check, Blood Test}

Parameters:
- time_TC: time required for one temperature check [minutes] = 2
- time_BT: time required for one blood test [minutes] = 10
- total_staff_minutes: total available staff minutes [minutes] = 22000
- min_BT: minimum number of blood tests required [tests] = 45
- TC_to_BT_ratio: minimum ratio of temperature checks to blood tests (Temperature Checks must be at least 5 times the Blood Tests) = 5

Variables:
- TemperatureChecks: number of temperature checks to perform [integer, ≥ 0, unit: tests]
- BloodTests: number of blood tests to perform [integer, ≥ 0, unit: tests]
(Note: In this formulation, each patient receives exactly one test. The objective counts each test as one patient served.)

Objective:
- Maximize PatientsSeen, where PatientsSeen = TemperatureChecks + BloodTests

Constraints:
1. Staff time constraint:
   2 * TemperatureChecks + 10 * BloodTests ≤ 22000
2. Blood test minimum requirement:
   BloodTests ≥ 45
3. Temperature check ratio requirement:
   TemperatureChecks ≥ 5 * BloodTests

Model Comments:
- It is assumed that each test corresponds to a distinct patient.
- The decision variables are considered integers since tests are discrete, though they are declared as floats in the expected output schema.
- All time units are in minutes and the available capacity is given in minutes.

Expected Output Schema:
{
  "variables": {
    "TemperatureChecks": "float",
    "BloodTests": "float",
    "PatientsSeen": "float"
  },
  "objective": "float"
}'''

# Generated Code:
from ortools.linear_solver import pywraplp

def solve_linear_program():
    # Create the linear solver with the CBC backend.
    solver = pywraplp.Solver.CreateSolver('CBC_MIXED_INTEGER_PROGRAMMING')
    if not solver:
        print("Solver not created.")
        return None

    # Parameters
    time_TC = 2         # minutes per Temperature Check
    time_BT = 10        # minutes per Blood Test
    total_staff_minutes = 22000
    min_BT = 45
    TC_to_BT_ratio = 5

    # Decision Variables: Since tests must be integer, we declare them as integer variables.
    TemperatureChecks = solver.IntVar(0, solver.infinity(), 'TemperatureChecks')
    BloodTests = solver.IntVar(0, solver.infinity(), 'BloodTests')

    # The total number of patients seen (each test is a patient)
    # This is computed as TemperatureChecks + BloodTests.
    # Though not an independent variable here, we report the sum.
    
    # Constraints:
    # 1. Staff time constraint: 2*TemperatureChecks + 10*BloodTests <= 22000.
    solver.Add(time_TC * TemperatureChecks + time_BT * BloodTests <= total_staff_minutes)
    
    # 2. Blood test minimum requirement: BloodTests >= 45.
    solver.Add(BloodTests >= min_BT)
    
    # 3. Temperature check ratio constraint: TemperatureChecks >= 5 * BloodTests.
    solver.Add(TemperatureChecks >= TC_to_BT_ratio * BloodTests)
    
    # Objective function: maximize the total number of patients seen.
    objective = solver.Objective()
    objective.SetCoefficient(TemperatureChecks, 1)
    objective.SetCoefficient(BloodTests, 1)
    objective.SetMaximization()
    
    # Solve the problem and check the result.
    status = solver.Solve()
    result = {}
    
    if status == pywraplp.Solver.OPTIMAL:
        patients_seen = TemperatureChecks.solution_value() + BloodTests.solution_value()
        result['variables'] = {
            "TemperatureChecks": float(TemperatureChecks.solution_value()),
            "BloodTests": float(BloodTests.solution_value()),
            "PatientsSeen": float(patients_seen)
        }
        result['objective'] = float(objective.Value())
    else:
        result['error'] = "The problem does not have an optimal solution."
    
    return result

def main():
    # Since we only have one formulation in this problem description,
    # we call the linear programming implementation.
    lp_result = solve_linear_program()
    
    print("Optimization Results:")
    print(lp_result)

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Optimization Results:
{'variables': {'TemperatureChecks': 10775.0, 'BloodTests': 45.0, 'PatientsSeen': 10820.0}, 'objective': 10820.0}
'''

'''Expected Output:
Expected solution

: {'variables': {'TemperatureChecks': 10775.0, 'BloodTests': 45.0, 'PatientsSeen': 10820.0}, 'objective': 10820.0}'''

