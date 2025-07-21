# Problem Description:
'''Problem description: A grilled cheese shop sells a light and heavy grilled cheese sandwich. A light grilled cheese sandwich requires 2 slices of bread and 3 slices of cheese. A heavy grilled cheese sandwich requires 3 slices of bread and 5 slices of cheese. Since most people who come to the store love grilled cheese, the store must make at least 3 times as many heavy grilled cheese sandwiches as light grilled cheese sandwiches. The store has available 300 slices of bread and 500 slices of cheese. If a light grilled cheese sandwich takes 10 minutes to make and a heavy grilled cheese sandwich takes 15 minutes to make, how many of each should they make to minimize the total production time?

Expected Output Schema:
{
  "variables": {
    "LightSandwiches": "float",
    "HeavySandwiches": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- SandwichTypes = {Light, Heavy}

Parameters:
- breadSlicesAvailable = 300               (total available bread slices)
- cheeseSlicesAvailable = 500              (total available cheese slices)
- breadPerLight = 2                        (bread slices needed per light sandwich)
- cheesePerLight = 3                       (cheese slices needed per light sandwich)
- breadPerHeavy = 3                        (bread slices needed per heavy sandwich)
- cheesePerHeavy = 5                       (cheese slices needed per heavy sandwich)
- timePerLight = 10                        (production time in minutes for a light sandwich)
- timePerHeavy = 15                        (production time in minutes for a heavy sandwich)
- minHeavyToLightRatio = 3                 (heavy sandwiches must be at least 3 times the light sandwiches)

Variables:
- LightSandwiches: continuous or integer ≥ 0    (number of light grilled cheese sandwiches to produce)
- HeavySandwiches: continuous or integer ≥ 0    (number of heavy grilled cheese sandwiches to produce)

Objective:
- Minimize totalProductionTime = (timePerLight * LightSandwiches) + (timePerHeavy * HeavySandwiches)
  (total production time in minutes)

Constraints:
1. Bread usage constraint:
   (breadPerLight * LightSandwiches) + (breadPerHeavy * HeavySandwiches) ≤ breadSlicesAvailable
   i.e., (2 * LightSandwiches) + (3 * HeavySandwiches) ≤ 300

2. Cheese usage constraint:
   (cheesePerLight * LightSandwiches) + (cheesePerHeavy * HeavySandwiches) ≤ cheeseSlicesAvailable
   i.e., (3 * LightSandwiches) + (5 * HeavySandwiches) ≤ 500

3. Sandwich ratio constraint:
   HeavySandwiches ≥ minHeavyToLightRatio * LightSandwiches
   i.e., HeavySandwiches ≥ 3 * LightSandwiches

Model Comments:
- All parameters are in consistent units (slices for ingredients, minutes for time).
- Although the expected schema defines the decision variables as floats, in practice, sandwich counts are typically integer values.
- The objective is to minimize the total production time while respecting the available quantities of bread and cheese and the required sandwich ratio.

This complete and structured model follows the five-element framework and accurately represents the original problem.'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp
from ortools.sat.python import cp_model

def solve_continuous_lp():
    # Create the linear solver with the GLOP backend for continuous LP.
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        return None

    # Variables (continuous, non-negative)
    LightSandwiches = solver.NumVar(0.0, solver.infinity(), 'LightSandwiches')
    HeavySandwiches = solver.NumVar(0.0, solver.infinity(), 'HeavySandwiches')

    # Constraints
    # 1. Bread: (2 * LightSandwiches) + (3 * HeavySandwiches) <= 300
    solver.Add(2 * LightSandwiches + 3 * HeavySandwiches <= 300)
    # 2. Cheese: (3 * LightSandwiches) + (5 * HeavySandwiches) <= 500
    solver.Add(3 * LightSandwiches + 5 * HeavySandwiches <= 500)
    # 3. Sandwich ratio: HeavySandwiches >= 3 * LightSandwiches
    solver.Add(HeavySandwiches >= 3 * LightSandwiches)

    # Objective function: Minimize total production time = 10 * LightSandwiches + 15 * HeavySandwiches
    solver.Minimize(10 * LightSandwiches + 15 * HeavySandwiches)

    status = solver.Solve()

    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        # Build the output structured dict
        result = {
            "variables": {
                "LightSandwiches": LightSandwiches.solution_value(),
                "HeavySandwiches": HeavySandwiches.solution_value()
            },
            "objective": solver.Objective().Value()
        }
    else:
        result = {"error": "No optimal solution found in continuous LP model."}
    return result

def solve_integer_cp_sat():
    # Create CP-SAT model for the integer formulation.
    model = cp_model.CpModel()

    # Define upper bounds for variables based on capacity:
    # For LightSandwiches, maximum if all resources devoted to light sandwiches:
    max_light = 150  # from bread constraint: 300/2 = 150, and cheese: 500/3 ~166, so 150 is safe.
    # For HeavySandwiches, maximum is 100 (from bread:300/3, cheese:500/5)
    max_heavy = 100

    LightSandwiches = model.NewIntVar(0, max_light, 'LightSandwiches')
    HeavySandwiches = model.NewIntVar(0, max_heavy, 'HeavySandwiches')

    # Constraints:
    # 1. Bread: 2*Light + 3*Heavy <= 300
    model.Add(2 * LightSandwiches + 3 * HeavySandwiches <= 300)
    # 2. Cheese: 3*Light + 5*Heavy <= 500
    model.Add(3 * LightSandwiches + 5 * HeavySandwiches <= 500)
    # 3. Ratio: Heavy >= 3 * Light
    model.Add(HeavySandwiches >= 3 * LightSandwiches)

    # Objective: Minimize 10*Light + 15*Heavy
    # In CP-SAT, objective must be integer; coefficients are integers.
    model.Minimize(10 * LightSandwiches + 15 * HeavySandwiches)

    # Solve the model.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    result = {}
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        result = {
            "variables": {
                "LightSandwiches": solver.Value(LightSandwiches),
                "HeavySandwiches": solver.Value(HeavySandwiches)
            },
            "objective": solver.ObjectiveValue()
        }
    else:
        result = {"error": "No optimal solution found in integer CP-SAT model."}
    return result

def main():
    print("Continuous LP (using ortools.linear_solver) solution:")
    cont_result = solve_continuous_lp()
    print(cont_result)
    print("\nInteger CP-SAT (using ortools.sat.python.cp_model) solution:")
    int_result = solve_integer_cp_sat()
    print(int_result)

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Continuous LP (using ortools.linear_solver) solution:
{'variables': {'LightSandwiches': 0.0, 'HeavySandwiches': 0.0}, 'objective': 0.0}

Integer CP-SAT (using ortools.sat.python.cp_model) solution:
{'variables': {'LightSandwiches': 0, 'HeavySandwiches': 0}, 'objective': 0.0}
'''

'''Expected Output:
Expected solution

: {'variables': {'LightSandwiches': 0.0, 'HeavySandwiches': 0.0}, 'objective': 0.0}'''

