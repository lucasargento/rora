# Problem Description:
'''Problem description: A doctor's office takes the  temperature of patients one by one either by using an electronic or regular thermometer. The electronic thermometer takes 3 minutes to make a reading while the regular thermometer takes 2 minutes to make a reading. Since the electronic thermometer is more accurate, at least twice as many patients should have their temperature checked by the electronic thermometer than the regular thermometer. Since the electronic thermometer has a cooldown time, at least 50 patients should have their temperature checked by a regular thermometer. If the office is open for 15000 minutes, maximize the number of patients whose temperature can be taken?

Expected Output Schema:
{
  "variables": {
    "ElectronicReadings": "float",
    "RegularReadings": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Below is the structured mathematical model using the five-element framework.

--------------------------------------------------

Sets:
- T: set of thermometer types = {Electronic, Regular}

Parameters:
- time_electronic: time required for one electronic reading [minutes] = 3
- time_regular: time required for one regular reading [minutes] = 2
- total_available_time: total minutes the office is open [minutes] = 15000
- min_regular_readings: minimum number of regular readings [patients] = 50
- ratio_requirement: minimum ratio of electronic to regular readings [dimensionless] = 2  
  (Interpretation: The number of electronic readings must be at least twice the number of regular readings.)

Variables:
- ElectronicReadings (E): number of patients whose temperature is taken with the electronic thermometer [integer ≥ 0]
- RegularReadings (R): number of patients whose temperature is taken with the regular thermometer [integer ≥ 0]

Objective:
- Maximize TotalPatients = ElectronicReadings + RegularReadings

Constraints:
1. Time Constraint:  
   3 * ElectronicReadings + 2 * RegularReadings ≤ total_available_time  
   (Ensures that the sum of time spent on all readings does not exceed 15000 minutes.)

2. Ratio Constraint:  
   ElectronicReadings ≥ ratio_requirement * RegularReadings  
   (Ensures that there are at least twice as many electronic readings as regular readings.)

3. Minimum Regular Constraint:  
   RegularReadings ≥ min_regular_readings  
   (Ensures that at least 50 patients are checked with the regular thermometer.)

--------------------------------------------------

Additional Comments:
- All time parameters are in minutes, and the number of readings represents individual patients.
- While the decision variables are defined as integers since they represent patient counts, they can be modeled as continuous variables if rounding is applied.
- The objective is to maximize the total number of patients whose temperature is checked within the available time.'''

# Generated Code:
#!/usr/bin/env python3
"""
This script implements the following optimization problem using Google OR-Tools.
There are two separate implementations:
1. An integer model where decision variables are integer.
2. A continuous relaxation model where decision variables are continuous (optimal solution may be fractional).

Problem Description:
A doctor's office takes the temperature of patients one by one either using an electronic or regular thermometer.
- Electronic thermometer: 3 minutes per reading.
- Regular thermometer: 2 minutes per reading.
- The number of electronic readings must be at least twice the number of regular readings (for accuracy).
- At least 50 patients should be checked with the regular thermometer.
- Total available time: 15000 minutes.
Objective: Maximize the total number of patients (ElectronicReadings + RegularReadings).
"""

from ortools.linear_solver import pywraplp

def solve_integer_model():
    # Create the solver using CBC_MIXED_INTEGER_PROGRAMMING.
    solver = pywraplp.Solver.CreateSolver('CBC_MIXED_INTEGER_PROGRAMMING')
    if not solver:
        print("Integer model: Solver not created.")
        return

    # Parameters
    time_electronic = 3
    time_regular = 2
    total_time = 15000
    min_regular = 50
    ratio_requirement = 2

    # Decision Variables: Integer variables E and R (non-negative)
    E = solver.IntVar(0, solver.infinity(), 'ElectronicReadings')
    R = solver.IntVar(0, solver.infinity(), 'RegularReadings')

    # Objective: Maximize total patients = E + R
    solver.Maximize(E + R)

    # Constraints:
    # Time constraint: 3*E + 2*R <= 15000
    solver.Add(time_electronic * E + time_regular * R <= total_time)
    # Ratio constraint: E >= 2 * R
    solver.Add(E >= ratio_requirement * R)
    # Minimum regular constraint: R >= 50
    solver.Add(R >= min_regular)

    # Solve the model.
    status = solver.Solve()

    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result['ElectronicReadings'] = E.solution_value()
        result['RegularReadings'] = R.solution_value()
        result['objective'] = solver.Objective().Value()
    else:
        result['message'] = "No optimal solution found"
    return result

def solve_continuous_model():
    # Create the solver using GLOP for continuous problem.
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Continuous model: Solver not created.")
        return

    # Parameters
    time_electronic = 3.0
    time_regular = 2.0
    total_time = 15000.0
    min_regular = 50.0
    ratio_requirement = 2.0

    # Decision Variables: Continuous non-negative variables.
    E = solver.NumVar(0.0, solver.infinity(), 'ElectronicReadings')
    R = solver.NumVar(0.0, solver.infinity(), 'RegularReadings')

    # Objective: Maximize E + R.
    objective = solver.Objective()
    objective.SetCoefficient(E, 1)
    objective.SetCoefficient(R, 1)
    objective.SetMaximization()

    # Constraints:
    # Time constraint: 3*E + 2*R <= 15000.
    solver.Add(time_electronic * E + time_regular * R <= total_time)
    # Ratio constraint: E >= 2 * R.
    solver.Add(E - ratio_requirement * R >= 0)
    # Minimum regular constraint: R >= 50.
    solver.Add(R >= min_regular)

    # Solve the model.
    status = solver.Solve()

    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        # For the continuous model, the solution might be fractional.
        result['ElectronicReadings'] = E.solution_value()
        result['RegularReadings'] = R.solution_value()
        result['objective'] = objective.Value()
    else:
        result['message'] = "No optimal solution found"
    return result

def main():
    print("----- Integer Model (Patients counted as integers) -----")
    int_result = solve_integer_model()
    if 'message' in int_result:
        print("Integer Model:", int_result['message'])
    else:
        print(f"ElectronicReadings: {int_result['ElectronicReadings']}")
        print(f"RegularReadings: {int_result['RegularReadings']}")
        print(f"Total Patients (Objective): {int_result['objective']}")
    
    print("\n----- Continuous Model (Relaxation) -----")
    cont_result = solve_continuous_model()
    if 'message' in cont_result:
        print("Continuous Model:", cont_result['message'])
    else:
        print(f"ElectronicReadings: {cont_result['ElectronicReadings']}")
        print(f"RegularReadings: {cont_result['RegularReadings']}")
        print(f"Total Patients (Objective): {cont_result['objective']}")

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
----- Integer Model (Patients counted as integers) -----
ElectronicReadings: 3750.0
RegularReadings: 1875.0
Total Patients (Objective): 5625.0

----- Continuous Model (Relaxation) -----
ElectronicReadings: 3750.0
RegularReadings: 1875.0
Total Patients (Objective): 5625.0
'''

'''Expected Output:
Expected solution

: {'variables': {'ElectronicReadings': 3750.0, 'RegularReadings': 1875.0}, 'objective': 5625.0}'''

