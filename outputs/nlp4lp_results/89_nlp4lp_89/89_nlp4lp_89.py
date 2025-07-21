# Problem Description:
'''Problem description: A clinic takes patient blood pressure either using an automatic machine or a manual machine. The automatic machine takes 10 minutes per patient while the manual machine takes 15 minutes per patient. Since the automatic machine frequently breaks, at least twice as many patients must have their blood pressure taken by the manual machine than the automatic machine. However, at least 20 patient can be processed by the automatic machine. If the clinic is open for 20000 minutes, maximize the number of patients whose blood pressure can be taken.

Expected Output Schema:
{
  "variables": {
    "AutomaticPatients": "float",
    "ManualPatients": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- DeviceTypes: {Automatic, Manual}

Parameters:
- time_automatic: 10 (minutes per patient)
- time_manual: 15 (minutes per patient)
- total_available_time: 20000 (minutes)
- minimum_automatic_patients: 20 (patients)
- manual_to_automatic_ratio: 2 (manual patients must be at least 2 times automatic patients)

Variables:
- AutomaticPatients: number of patients measured with the automatic machine (nonnegative continuous variable, units: patients)
- ManualPatients: number of patients measured with the manual machine (nonnegative continuous variable, units: patients)

Objective:
- Maximize total_patients = AutomaticPatients + ManualPatients

Constraints:
1. Time constraint: (time_automatic * AutomaticPatients) + (time_manual * ManualPatients) ≤ total_available_time  
   That is, 10 * AutomaticPatients + 15 * ManualPatients ≤ 20000

2. Machine reliability (ratio) constraint: ManualPatients ≥ manual_to_automatic_ratio * AutomaticPatients  
   That is, ManualPatients ≥ 2 * AutomaticPatients

3. Minimum automatic patients constraint: AutomaticPatients ≥ minimum_automatic_patients  
   That is, AutomaticPatients ≥ 20

Additional Notes:
- All time units are in minutes and patient counts are assumed to be represented as continuous values for modeling purposes (they can later be rounded or modeled as integers if needed).
- The objective is to maximize the number of patients processed within the available operating minutes.'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_with_linear_solver():
    # Create the linear solver with the GLOP backend.
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Error: Could not create solver.")
        return None

    # Parameters
    time_automatic = 10
    time_manual = 15
    total_available_time = 20000
    minimum_automatic_patients = 20
    manual_to_automatic_ratio = 2

    # Variables: continuous nonnegative values.
    AutomaticPatients = solver.NumVar(0.0, solver.infinity(), 'AutomaticPatients')
    ManualPatients = solver.NumVar(0.0, solver.infinity(), 'ManualPatients')

    # Constraints:
    # 1. Time constraint:
    #    10 * AutomaticPatients + 15 * ManualPatients <= 20000
    solver.Add(time_automatic * AutomaticPatients + time_manual * ManualPatients <= total_available_time)

    # 2. Ratio constraint: ManualPatients >= 2 * AutomaticPatients
    solver.Add(ManualPatients >= manual_to_automatic_ratio * AutomaticPatients)

    # 3. Minimum patients on automatic machine:
    solver.Add(AutomaticPatients >= minimum_automatic_patients)

    # Objective: maximize the total number of patients processed.
    objective = solver.Objective()
    objective.SetCoefficient(AutomaticPatients, 1)
    objective.SetCoefficient(ManualPatients, 1)
    objective.SetMaximization()

    # Solve the problem.
    status = solver.Solve()

    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "variables": {
                "AutomaticPatients": AutomaticPatients.solution_value(),
                "ManualPatients": ManualPatients.solution_value()
            },
            "objective": objective.Value()
        }
    else:
        result = {"error": "No optimal solution found."}
    return result

def main():
    # Since the formulation is unique, we solve using one implementation (linear programming)
    print("Solution using OR-Tools Linear Solver (GLOP):")
    result_linear = solve_with_linear_solver()
    print(result_linear)

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Solution using OR-Tools Linear Solver (GLOP):
{'variables': {'AutomaticPatients': 500.0, 'ManualPatients': 999.9999999999999}, 'objective': 1500.0}
'''

'''Expected Output:
Expected solution

: {'variables': {'AutomaticPatients': 500.0, 'ManualPatients': 1000.0}, 'objective': 1500.0}'''

