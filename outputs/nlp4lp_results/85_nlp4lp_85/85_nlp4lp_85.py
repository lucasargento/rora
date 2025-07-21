# Problem Description:
'''Problem description: A cleaning company uses a cleansing chemical and odor-removing chemical to clean a house. Each unit of the cleansing chemical takes 4 units to be effective while each unit of the odor-removing chemical takes 6 minutes to be effective. The company must use at least 100 units of the cleansing chemical. In total, at least 300 units of chemicals can be used per house. Further, because the cleansing chemical is strong, there can be at most twice the amount of cleansing chemical as odor-removing chemical. How many units of each should be used to minimize the total time it takes for a house to be cleaned?

Expected Output Schema:
{
  "variables": {
    "CleansingChemicalUnits": "float",
    "OdorRemovingChemicalUnits": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''The following is a complete formulation of the problem as a mathematical model using the five-element framework. In this formulation we assume that both chemicals are measured in "units" (each “unit” is an application measure) and the corresponding treatment times are measured in minutes. That is, one unit of cleansing chemical requires 4 minutes for effectiveness and one unit of odor‐removing chemical requires 6 minutes. We note that, although the problem states "units" for the cleansing chemical effectiveness and "minutes" for the odor-removing chemical, we assume that both are directly contributing to the overall cleaning time in minutes. If an alternative interpretation is required (for example, if the 4 in the cleansing case were a dimensionless cost factor rather than minutes), then the formulation can be adjusted accordingly. 

Below is the main formulation:

------------------------------------------------------------
Sets:
- ChemicalTypes: set of chemical types = {Cleansing, OdorRemoving}

Parameters:
- treatment_time_Cleansing: treatment time per unit of cleansing chemical = 4 minutes per unit 
- treatment_time_OdorRemoving: treatment time per unit of odor-removing chemical = 6 minutes per unit
- minimum_cleansing: minimum required units of cleansing chemical = 100 units
- minimum_total_units: minimum total units of chemicals = 300 units
- max_ratio: maximum ratio of cleansing to odor-removing chemical = 2   (i.e., CleansingUnits ≤ 2 * OdorRemovingUnits)

Variables:
- CleansingChemicalUnits (continuous, ≥ 0): Number of units of cleansing chemical to use [units]
- OdorRemovingChemicalUnits (continuous, ≥ 0): Number of units of odor-removing chemical to use [units]

Objective:
- Minimize total cleaning time (in minutes) defined as:
  total_cleaning_time = treatment_time_Cleansing * CleansingChemicalUnits + treatment_time_OdorRemoving * OdorRemovingChemicalUnits
  That is, Minimize: 4 * CleansingChemicalUnits + 6 * OdorRemovingChemicalUnits

Constraints:
1. Cleansing chemical minimum usage:
   CleansingChemicalUnits ≥ 100

2. Minimum total chemical usage:
   CleansingChemicalUnits + OdorRemovingChemicalUnits ≥ 300

3. Ratio constraint (due to the strength of the cleansing chemical):
   CleansingChemicalUnits ≤ 2 * OdorRemovingChemicalUnits

------------------------------------------------------------

For clarity, here is the expected output schema in JSON format as specified:

{
  "variables": {
    "CleansingChemicalUnits": "float",
    "OdorRemovingChemicalUnits": "float"
  },
  "objective": "float"
}

This model is now self-contained, logically consistent, and maps directly to a working implementation in code.'''

# Generated Code:
#!/usr/bin/env python3
"""
This script implements two separate formulations for the cleaning chemicals optimization problem.
Formulation 1 (Direct Time Interpretation):
  - Each unit of cleansing chemical contributes 4 minutes to cleaning time.
  - Each unit of odor‐removing chemical contributes 6 minutes to cleaning time.
  - Objective: Minimize 4 * CleansingChemicalUnits + 6 * OdorRemovingChemicalUnits.
Formulation 2 (Alternative Interpretation):
  - The cleansing chemical is considered a dimensionless (or fixed) cost factor,
    so only the odor‐removing chemical contributes cleaning time.
  - In this formulation the objective is: Minimize 6 * OdorRemovingChemicalUnits.
Both models use the same constraints:
  1. CleansingChemicalUnits >= 100.
  2. CleansingChemicalUnits + OdorRemovingChemicalUnits >= 300.
  3. CleansingChemicalUnits <= 2 * OdorRemovingChemicalUnits.
The results from both formulations are printed at the end.
"""

from ortools.linear_solver import pywraplp

def solve_model1():
    """Model 1: Direct time interpretation with objective = 4*X + 6*Y."""
    # Create solver using GLOP linear programming solver.
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Solver not created.")
        return None

    # Decision variables.
    # CleansingChemicalUnits: continuous >= 0.
    CleansingChemicalUnits = solver.NumVar(0.0, solver.infinity(), 'CleansingChemicalUnits')
    # OdorRemovingChemicalUnits: continuous >= 0.
    OdorRemovingChemicalUnits = solver.NumVar(0.0, solver.infinity(), 'OdorRemovingChemicalUnits')

    # Parameters.
    treatment_time_cleansing = 4.0  # minutes per unit for cleansing chemical.
    treatment_time_odor = 6.0       # minutes per unit for odor-removing chemical.
    minimum_cleansing = 100.0
    minimum_total_units = 300.0
    max_ratio = 2.0

    # Objective: minimize total cleaning time.
    objective = solver.Objective()
    objective.SetCoefficient(CleansingChemicalUnits, treatment_time_cleansing)
    objective.SetCoefficient(OdorRemovingChemicalUnits, treatment_time_odor)
    objective.SetMinimization()

    # Constraints.
    # 1. Minimum cleansing chemical usage.
    solver.Add(CleansingChemicalUnits >= minimum_cleansing)
    # 2. Minimum total chemical usage.
    solver.Add(CleansingChemicalUnits + OdorRemovingChemicalUnits >= minimum_total_units)
    # 3. Ratio constraint.
    solver.Add(CleansingChemicalUnits <= max_ratio * OdorRemovingChemicalUnits)

    status = solver.Solve()

    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "variables": {
                "CleansingChemicalUnits": CleansingChemicalUnits.solution_value(),
                "OdorRemovingChemicalUnits": OdorRemovingChemicalUnits.solution_value()
            },
            "objective": objective.Value()
        }
    else:
        result = {"error": "No optimal solution found in Model 1."}
    return result

def solve_model2():
    """Model 2: Alternative interpretation where cleansing chemical does not contribute to time.
       Objective = 6*OdorRemovingChemicalUnits.
    """
    # Create solver using GLOP linear programming solver.
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Solver not created.")
        return None

    # Decision variables.
    CleansingChemicalUnits = solver.NumVar(0.0, solver.infinity(), 'CleansingChemicalUnits')
    OdorRemovingChemicalUnits = solver.NumVar(0.0, solver.infinity(), 'OdorRemovingChemicalUnits')

    # Parameters.
    # In this model the cleansing chemical's time is not counted.
    treatment_time_odor = 6.0       # minutes per unit for odor-removing chemical.
    minimum_cleansing = 100.0
    minimum_total_units = 300.0
    max_ratio = 2.0

    # Objective: minimize total cleaning time which considers only odor-removing chemical.
    objective = solver.Objective()
    objective.SetCoefficient(OdorRemovingChemicalUnits, treatment_time_odor)
    objective.SetMinimization()

    # Constraints.
    solver.Add(CleansingChemicalUnits >= minimum_cleansing)
    solver.Add(CleansingChemicalUnits + OdorRemovingChemicalUnits >= minimum_total_units)
    solver.Add(CleansingChemicalUnits <= max_ratio * OdorRemovingChemicalUnits)

    status = solver.Solve()

    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "variables": {
                "CleansingChemicalUnits": CleansingChemicalUnits.solution_value(),
                "OdorRemovingChemicalUnits": OdorRemovingChemicalUnits.solution_value()
            },
            "objective": objective.Value()
        }
    else:
        result = {"error": "No optimal solution found in Model 2."}
    return result

def main():
    model1_result = solve_model1()
    model2_result = solve_model2()

    print("Model 1 (Direct Time Interpretation) Result:")
    print(model1_result)
    print("\nModel 2 (Alternative Interpretation) Result:")
    print(model2_result)

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Model 1 (Direct Time Interpretation) Result:
{'variables': {'CleansingChemicalUnits': 200.0, 'OdorRemovingChemicalUnits': 100.0}, 'objective': 1400.0}

Model 2 (Alternative Interpretation) Result:
{'variables': {'CleansingChemicalUnits': 200.0, 'OdorRemovingChemicalUnits': 100.0}, 'objective': 600.0}
'''

'''Expected Output:
Expected solution

: {'variables': {'CleansingChemicalUnits': 100.0, 'OdorRemovingChemicalUnits': 50.0}, 'objective': 700.0}'''

