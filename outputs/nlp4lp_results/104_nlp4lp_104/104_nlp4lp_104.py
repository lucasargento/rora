# Problem Description:
'''Problem description: A patient takes anxiety medication and anti-depressants one after the other. Each unit of anxiety medication takes 3 minutes to be effective while each unit of anti-depressant takes 5 minutes to be effective. The patient must take at least 100 units of medication and at least 30 should be anxiety medication. Since the anxiety medication is strong, the patient can take at most twice the amount of anxiety medication as anti-depressants. How many units of each should the patient take to minimize the total time it take for the medication to be effective?

Expected Output Schema:
{
  "variables": {
    "AnxietyUnits": "float",
    "AntidepressantUnits": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Below is the structured mathematical model using the five-element framework.

----------------------------------------------------------------
Sets:
- MED: set of medication types = {Anxiety, Antidepressant}  
  (Note: Although the two medications can be handled separately, we list them here for clarity.)

Parameters:
- timeAnxiety = 3 (minutes per unit of anxiety medication)
- timeAntidepressant = 5 (minutes per unit of antidepressant medication)
- minTotalUnits = 100 (minimum total medication units required)
- minAnxietyUnits = 30 (minimum anxiety medication units required)
- maxAnxietyToAntidepressantRatio = 2 (anxiety medication units cannot exceed twice the number of antidepressant units)

Variables:
- AnxietyUnits: number of units of anxiety medication to take [float, units ≥ 0]
- AntidepressantUnits: number of units of antidepressant medication to take [float, units ≥ 0]

Objective:
- Minimize total medication effective time = (timeAnxiety * AnxietyUnits) + (timeAntidepressant * AntidepressantUnits)

Constraints:
1. Total medication requirement: AnxietyUnits + AntidepressantUnits ≥ minTotalUnits  
   (Ensure at least 100 units of medication are taken in total.)
2. Minimum anxiety medication: AnxietyUnits ≥ minAnxietyUnits  
   (Ensure at least 30 units of anxiety medication are taken.)
3. Ratio constraint for anxiety medication strength: AnxietyUnits ≤ maxAnxietyToAntidepressantRatio * AntidepressantUnits  
   (Since anxiety medication is stronger, it must be at most twice the number of antidepressant units.)

----------------------------------------------------------------

Comments:
- All time units are in minutes.
- The decision variables are defined as continuous values, though they represent "units." In practice, if only integer units are allowed, the variable type can be adjusted accordingly.
- The objective is to minimize the total effective time for the medication to work, assuming that the effects are additive.

Expected Output Schema:
{
  "variables": {
    "AnxietyUnits": "float",
    "AntidepressantUnits": "float"
  },
  "objective": "float"
}'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_continuous_model():
    # Create the solver with the GLOP backend (for continuous LP).
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        return None, "Solver not created for continuous model."
    
    # Parameters
    timeAnxiety = 3         # minutes per unit of anxiety medication
    timeAntidepressant = 5  # minutes per unit of antidepressant medication
    minTotalUnits = 100     # minimum total medication units required
    minAnxietyUnits = 30    # minimum anxiety medication units required
    maxRatio = 2            # AnxietyUnits <= 2 * AntidepressantUnits

    # Variables: Continuous variables (float, non-negative)
    AnxietyUnits = solver.NumVar(0.0, solver.infinity(), 'AnxietyUnits')
    AntidepressantUnits = solver.NumVar(0.0, solver.infinity(), 'AntidepressantUnits')

    # Constraints
    # 1. Total medication requirement: AnxietyUnits + AntidepressantUnits >= 100.
    solver.Add(AnxietyUnits + AntidepressantUnits >= minTotalUnits)
    # 2. Minimum anxiety medication: AnxietyUnits >= 30.
    solver.Add(AnxietyUnits >= minAnxietyUnits)
    # 3. Ratio constraint: AnxietyUnits <= 2 * AntidepressantUnits.
    solver.Add(AnxietyUnits <= maxRatio * AntidepressantUnits)

    # Objective: Minimize total effective time = 3*AnxietyUnits + 5*AntidepressantUnits.
    objective = solver.Objective()
    objective.SetCoefficient(AnxietyUnits, timeAnxiety)
    objective.SetCoefficient(AntidepressantUnits, timeAntidepressant)
    objective.SetMinimization()

    # Solve the model
    status = solver.Solve()

    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result['AnxietyUnits'] = AnxietyUnits.solution_value()
        result['AntidepressantUnits'] = AntidepressantUnits.solution_value()
        result['objective'] = objective.Value()
    else:
        result['error'] = "The continuous model does not have an optimal solution."
    return result, None

def solve_integer_model():
    # Create the solver with the CBC backend (for integer programming).
    solver = pywraplp.Solver.CreateSolver('CBC_MIXED_INTEGER_PROGRAMMING')
    if not solver:
        return None, "Solver not created for integer model."

    # Parameters (same as continuous)
    timeAnxiety = 3         # minutes per unit of anxiety medication
    timeAntidepressant = 5  # minutes per unit of antidepressant medication
    minTotalUnits = 100     # minimum total medication units required
    minAnxietyUnits = 30    # minimum anxiety medication units required
    maxRatio = 2            # AnxietyUnits <= 2 * AntidepressantUnits

    # Variables: Integer variables (non-negative integers)
    AnxietyUnits = solver.IntVar(0, solver.infinity(), 'AnxietyUnits')
    AntidepressantUnits = solver.IntVar(0, solver.infinity(), 'AntidepressantUnits')

    # Constraints
    # 1. Total medication requirement: AnxietyUnits + AntidepressantUnits >= 100.
    solver.Add(AnxietyUnits + AntidepressantUnits >= minTotalUnits)
    # 2. Minimum anxiety medication: AnxietyUnits >= 30.
    solver.Add(AnxietyUnits >= minAnxietyUnits)
    # 3. Ratio constraint: AnxietyUnits <= 2 * AntidepressantUnits.
    solver.Add(AnxietyUnits <= maxRatio * AntidepressantUnits)

    # Objective: Minimize total effective time = 3*AnxietyUnits + 5*AntidepressantUnits.
    objective = solver.Objective()
    objective.SetCoefficient(AnxietyUnits, timeAnxiety)
    objective.SetCoefficient(AntidepressantUnits, timeAntidepressant)
    objective.SetMinimization()

    # Solve the model
    status = solver.Solve()

    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result['AnxietyUnits'] = AnxietyUnits.solution_value()
        result['AntidepressantUnits'] = AntidepressantUnits.solution_value()
        result['objective'] = objective.Value()
    else:
        result['error'] = "The integer model does not have an optimal solution."
    return result, None

def main():
    # Solve continuous model
    continuous_result, error_c = solve_continuous_model()
    # Solve integer model
    integer_result, error_i = solve_integer_model()

    # Print the results in a structured way.
    print("Continuous Model (Float Variables):")
    if error_c:
        print("  Error:", error_c)
    else:
        print("  AnxietyUnits:", continuous_result.get('AnxietyUnits'))
        print("  AntidepressantUnits:", continuous_result.get('AntidepressantUnits'))
        print("  Objective (Total Time):", continuous_result.get('objective'))
    
    print("\nInteger Model (Integer Variables):")
    if error_i:
        print("  Error:", error_i)
    else:
        print("  AnxietyUnits:", integer_result.get('AnxietyUnits'))
        print("  AntidepressantUnits:", integer_result.get('AntidepressantUnits'))
        print("  Objective (Total Time):", integer_result.get('objective'))

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Continuous Model (Float Variables):
  AnxietyUnits: 66.66666666666667
  AntidepressantUnits: 33.333333333333336
  Objective (Total Time): 366.6666666666667

Integer Model (Integer Variables):
  AnxietyUnits: 66.0
  AntidepressantUnits: 34.0
  Objective (Total Time): 368.0
'''

'''Expected Output:
Expected solution

: {'variables': {'AnxietyUnits': 66.66666666666667, 'AntidepressantUnits': 33.333333333333336}, 'objective': 366.6666666666667}'''

