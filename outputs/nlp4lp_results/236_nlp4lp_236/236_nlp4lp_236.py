# Problem Description:
'''Problem description: A hospital prepares batches of medication patches and anti-biotic creams. Each medication patch requires 3 minutes to prepare and 5 units of materials. Each anti-biotic cream requires 5 minutes to prepare and 6 units of materials. Since anti-biotic creams are used more often, there must be at least twice as many anti-biotic creams as medication patches. Due to storage reasons, the hospital can make at most 100 batches of medication patches and anti-biotic creams in total. The hospital has available 400 minutes of staff to spare and 530 units of materials. If each batch of medication patches can treat 3 people and each batch of anti-biotic cream can treat 2 people, how many batches of each should be made to maximize the number of people that can be treated?

Expected Output Schema:
{
  "variables": {
    "NumBatchesAntiBioticCream": "float",
    "NumBatchesMedicationPatch": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- P: set of product types = {MedicationPatch, AntiBioticCream}

Parameters:
- prepTimePatch: preparation time per batch of medication patches [minutes] = 3
- materialPatch: material required per batch of medication patches [material units] = 5
- treatPatch: number of people treated per batch of medication patches [people per batch] = 3
- prepTimeCream: preparation time per batch of anti-biotic creams [minutes] = 5
- materialCream: material required per batch of anti-biotic creams [material units] = 6
- treatCream: number of people treated per batch of anti-biotic creams [people per batch] = 2
- totalStaffTime: total staff time available [minutes] = 400
- totalMaterial: total material available [material units] = 530
- totalBatchesLimit: maximum total batches that can be stored [batches] = 100

Variables:
- NumBatchesMedicationPatch: number of batches of medication patches produced [non-negative real number]
- NumBatchesAntiBioticCream: number of batches of anti-biotic creams produced [non-negative real number]

Objective:
- Maximize the total number of people treated:
  Maximize (treatPatch * NumBatchesMedicationPatch + treatCream * NumBatchesAntiBioticCream)
  which translates to: Maximize (3 * NumBatchesMedicationPatch + 2 * NumBatchesAntiBioticCream)

Constraints:
1. Staff time constraint:
   (prepTimePatch * NumBatchesMedicationPatch + prepTimeCream * NumBatchesAntiBioticCream) ≤ totalStaffTime
   → 3 * NumBatchesMedicationPatch + 5 * NumBatchesAntiBioticCream ≤ 400
2. Material constraint:
   (materialPatch * NumBatchesMedicationPatch + materialCream * NumBatchesAntiBioticCream) ≤ totalMaterial
   → 5 * NumBatchesMedicationPatch + 6 * NumBatchesAntiBioticCream ≤ 530
3. Storage (batch) constraint:
   NumBatchesMedicationPatch + NumBatchesAntiBioticCream ≤ totalBatchesLimit
   → NumBatchesMedicationPatch + NumBatchesAntiBioticCream ≤ 100
4. Demand ratio constraint:
   The number of anti-biotic cream batches must be at least twice the number of medication patch batches:
   → NumBatchesAntiBioticCream ≥ 2 * NumBatchesMedicationPatch
5. Non-negativity:
   NumBatchesMedicationPatch ≥ 0, NumBatchesAntiBioticCream ≥ 0

Model Comments:
- Units are consistent: time in minutes and materials in material units.
- While batches are typically integers, the model variables are defined as non-negative real numbers (floats) to match the expected output schema. Adjust to integer requirements if necessary.'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp
import json

def solve_continuous_model():
    # Create the linear solver with the GLOP backend for continuous variables.
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Solver not created.")
        return None

    # Variables: non-negative continuous numbers.
    # NumBatchesMedicationPatch: number of batches of medication patches
    # NumBatchesAntiBioticCream: number of batches of anti-biotic creams
    med_patch = solver.NumVar(0.0, solver.infinity(), 'NumBatchesMedicationPatch')
    ab_creams = solver.NumVar(0.0, solver.infinity(), 'NumBatchesAntiBioticCream')

    # Parameters (constants)
    prepTimePatch = 3         # minutes per batch for medication patches
    prepTimeCream = 5         # minutes per batch for anti-biotic creams
    materialPatch = 5         # material units per batch for medication patches
    materialCream = 6         # material units per batch for anti-biotic creams
    treatPatch = 3            # people treated per batch of medication patches
    treatCream = 2            # people treated per batch of anti-biotic creams

    totalStaffTime = 400      # total available minutes of staff time
    totalMaterial = 530       # total available material units
    totalBatchesLimit = 100   # maximum total batches allowed

    # Constraints:
    # 1. Staff time constraint: 3*med_patch + 5*ab_creams <= 400
    solver.Add(prepTimePatch * med_patch + prepTimeCream * ab_creams <= totalStaffTime)

    # 2. Material constraint: 5*med_patch + 6*ab_creams <= 530
    solver.Add(materialPatch * med_patch + materialCream * ab_creams <= totalMaterial)

    # 3. Storage (batch) constraint: med_patch + ab_creams <= 100
    solver.Add(med_patch + ab_creams <= totalBatchesLimit)

    # 4. Demand ratio constraint: ab_creams >= 2 * med_patch
    solver.Add(ab_creams >= 2 * med_patch)

    # Objective:
    # Maximize the total people treated: 3*med_patch + 2*ab_creams
    objective = solver.Objective()
    objective.SetCoefficient(med_patch, treatPatch)
    objective.SetCoefficient(ab_creams, treatCream)
    objective.SetMaximization()

    status = solver.Solve()

    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "variables": {
                "NumBatchesMedicationPatch": med_patch.solution_value(),
                "NumBatchesAntiBioticCream": ab_creams.solution_value()
            },
            "objective": objective.Value()
        }
    else:
        result = {"message": "The problem does not have an optimal solution."}
    return result

def solve_integer_model():
    # Alternative formulation:
    # Although the expected formulation is continuous, we provide a version with integer variables 
    # since batches are typically integer numbers.
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        print("Integer solver not created.")
        return None

    # Variables: integer non-negative numbers.
    med_patch = solver.IntVar(0.0, solver.infinity(), 'NumBatchesMedicationPatch')
    ab_creams = solver.IntVar(0.0, solver.infinity(), 'NumBatchesAntiBioticCream')

    # Parameters
    prepTimePatch = 3
    prepTimeCream = 5
    materialPatch = 5
    materialCream = 6
    treatPatch = 3
    treatCream = 2

    totalStaffTime = 400
    totalMaterial = 530
    totalBatchesLimit = 100

    # Constraints
    solver.Add(prepTimePatch * med_patch + prepTimeCream * ab_creams <= totalStaffTime)
    solver.Add(materialPatch * med_patch + materialCream * ab_creams <= totalMaterial)
    solver.Add(med_patch + ab_creams <= totalBatchesLimit)
    solver.Add(ab_creams >= 2 * med_patch)

    # Objective: maximize 3*med_patch + 2*ab_creams
    objective = solver.Objective()
    objective.SetCoefficient(med_patch, treatPatch)
    objective.SetCoefficient(ab_creams, treatCream)
    objective.SetMaximization()

    status = solver.Solve()

    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "variables": {
                "NumBatchesMedicationPatch": med_patch.solution_value(),
                "NumBatchesAntiBioticCream": ab_creams.solution_value()
            },
            "objective": objective.Value()
        }
    else:
        result = {"message": "The integer problem does not have an optimal solution."}
    return result

def main():
    # Solve the continuous formulation first.
    continuous_result = solve_continuous_model()
    
    # Solve the integer formulation as an alternative version.
    integer_result = solve_integer_model()
    
    results = {
        "Continuous Formulation": continuous_result,
        "Integer Formulation": integer_result
    }
    
    # Print results as a JSON formatted string:
    print(json.dumps(results, indent=2))

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
{
  "Continuous Formulation": {
    "variables": {
      "NumBatchesMedicationPatch": 30.76923076923077,
      "NumBatchesAntiBioticCream": 61.538461538461526
    },
    "objective": 215.38461538461536
  },
  "Integer Formulation": {
    "variables": {
      "NumBatchesMedicationPatch": 30.0,
      "NumBatchesAntiBioticCream": 62.0
    },
    "objective": 213.99999999999997
  }
}
'''

'''Expected Output:
Expected solution

: {'variables': {'NumBatchesAntiBioticCream': 62.0, 'NumBatchesMedicationPatch': 30.0}, 'objective': 214.0}'''

