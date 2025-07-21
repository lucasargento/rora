# Problem Description:
'''Problem description: A hospital purchases two pills available for the patients to take one at a time. One pill is taken as a prevention and another is taken for treatment. The prevention pill takes 15 dollars to make while the treatment pill takes 25 dollars to make. Since the prevention pill is in higher demand, the hospital must purchase at least two times as many prevention pills as treatment pills. In addition, the hospital must purchase at least 50 treatment pills. If the clinic only has a budget of 10000 dollars, maximize the number of patients that can be treated.

Expected Output Schema:
{
  "variables": {
    "NumPreventionPills": "float",
    "NumTreatmentPills": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Below is a complete reformulation of the hospital’s pill-purchasing decision problem using the five‐element structure. In our interpretation, the goal is to maximize the total number of patients that can be served by the hospital. We assume that each purchased pill (whether prevention or treatment) is administered to one patient. (Note: Although pills are discrete, the expected output indicates “float” variables; you may later restrict these to integers if that is required.)

------------------------------------------------------------
Sets:
• PillType: the set of pill types = {Prevention, Treatment}

------------------------------------------------------------
Parameters:
• cost_Prevention = 15 dollars per prevention pill (manufacturing cost)
• cost_Treatment = 25 dollars per treatment pill (manufacturing cost)
• min_TreatmentPills = 50 pills (the hospital must purchase at least 50 treatment pills)
• prevention_ratio = 2 (the number of prevention pills must be at least 2 times the number of treatment pills)
• Budget = 10000 dollars (total available budget)
• Note: All monetary units are in dollars and all pill counts are in number of pills.

------------------------------------------------------------
Variables:
• NumPreventionPills: number of prevention pills purchased [float ≥ 0]
• NumTreatmentPills: number of treatment pills purchased [float ≥ 0]

------------------------------------------------------------
Objective:
• Maximize the total number of patients treated = NumPreventionPills + NumTreatmentPills  
  (Assumption: each pill purchased is administered to one patient.)

------------------------------------------------------------
Constraints:
1. Budget constraint:
   cost_Prevention * NumPreventionPills + cost_Treatment * NumTreatmentPills ≤ Budget  
   i.e., 15 * NumPreventionPills + 25 * NumTreatmentPills ≤ 10000

2. Prevention to treatment ratio constraint:
   The hospital must have at least two times as many prevention pills as treatment pills  
   i.e., NumPreventionPills ≥ prevention_ratio * NumTreatmentPills

3. Minimum treatment pills constraint:
   NumTreatmentPills ≥ min_TreatmentPills  
   i.e., NumTreatmentPills ≥ 50

------------------------------------------------------------

Below is the answer in the expected JSON output schema:

{
  "variables": {
    "NumPreventionPills": "float",
    "NumTreatmentPills": "float"
  },
  "objective": "Maximize NumPreventionPills + NumTreatmentPills subject to: 15*NumPreventionPills + 25*NumTreatmentPills <= 10000, NumPreventionPills >= 2*NumTreatmentPills, and NumTreatmentPills >= 50."
}

This formulation is self-contained and sets the stage for a working implementation.'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_with_linear_solver():
    # Create the linear solver with the GLOP backend.
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        return None

    # Variables: as described, they are non-negative floats.
    # Even though treatment pills must be at least 50, we set its lower bound to 50.
    num_prevention = solver.NumVar(0.0, solver.infinity(), 'NumPreventionPills')
    num_treatment = solver.NumVar(50.0, solver.infinity(), 'NumTreatmentPills')
    
    # Constraints:
    # 1. Budget constraint: 15*num_prevention + 25*num_treatment <= 10000
    solver.Add(15 * num_prevention + 25 * num_treatment <= 10000)
    
    # 2. Prevention to treatment ratio constraint: num_prevention >= 2 * num_treatment
    solver.Add(num_prevention >= 2 * num_treatment)
    
    # Objective: maximize the total number of pills (i.e., patients treated)
    objective = solver.Objective()
    objective.SetCoefficient(num_prevention, 1)
    objective.SetCoefficient(num_treatment, 1)
    objective.SetMaximization()
    
    # Solve the problem and return the result
    status = solver.Solve()
    
    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "NumPreventionPills": num_prevention.solution_value(),
            "NumTreatmentPills": num_treatment.solution_value(),
            "ObjectiveValue": objective.Value()
        }
        return result
    else:
        return {"message": "The problem does not have an optimal solution."}

def main():
    # Only one model formulation was provided, so we implement it using the linear solver.
    linear_solver_result = solve_with_linear_solver()
    
    # Structure the output for clear display
    results = {}
    results["LinearSolverModel"] = linear_solver_result
    
    print(results)

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
{'LinearSolverModel': {'NumPreventionPills': 583.3333333333334, 'NumTreatmentPills': 50.0, 'ObjectiveValue': 633.3333333333334}}
'''

'''Expected Output:
Expected solution

: {'variables': {'NumPreventionPills': 362.0, 'NumTreatmentPills': 181.0}, 'objective': 181.0}'''

