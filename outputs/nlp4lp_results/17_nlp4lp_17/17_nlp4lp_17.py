# Problem Description:
'''Problem description: A candy store mixes regular candy and sour candy to prepare two products, regular mix and sour surprise mix. Each kilogram of the regular mix contains 0.8 kg of regular candy and 0.2 kg of sour candy. The profit per kilogram of the regular mix is $3. Each kilogram of the sour surprise mix contains 0.1 kg of regular candy and 0.9 kg of sour candy. The profit per kilogram of the sour surprise mix is $5. The candy store has 80 kg of regular candy and 60 kg of sour candy available. How many kilograms of each type of candy mix should be created to maximize profits?

Expected Output Schema:
{
  "variables": {
    "ProductionMix": {
      "0": "float",
      "1": "float"
    }
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- Mixes: set of candy mixes = {RegularMix, SourSurpriseMix}

Parameters:
- profit[m]: profit per kilogram of mix m [USD per kg] where
  - profit[RegularMix] = 3
  - profit[SourSurpriseMix] = 5
- reg_requirement[m]: kilograms of regular candy required per kilogram of mix m [kg per kg] where
  - reg_requirement[RegularMix] = 0.8
  - reg_requirement[SourSurpriseMix] = 0.1
- sour_requirement[m]: kilograms of sour candy required per kilogram of mix m [kg per kg] where
  - sour_requirement[RegularMix] = 0.2
  - sour_requirement[SourSurpriseMix] = 0.9
- avail_reg: total available regular candy [kg] = 80
- avail_sour: total available sour candy [kg] = 60

Variables:
- x[m]: kilograms of mix m to produce [continuous, kg] for each m in Mixes, with x[m] ≥ 0

Objective:
- Maximize total profit = profit[RegularMix] * x[RegularMix] + profit[SourSurpriseMix] * x[SourSurpriseMix]

Constraints:
1. Regular candy availability: 
   reg_requirement[RegularMix] * x[RegularMix] + reg_requirement[SourSurpriseMix] * x[SourSurpriseMix] ≤ avail_reg
   (i.e., 0.8 * x[RegularMix] + 0.1 * x[SourSurpriseMix] ≤ 80)
2. Sour candy availability:
   sour_requirement[RegularMix] * x[RegularMix] + sour_requirement[SourSurpriseMix] * x[SourSurpriseMix] ≤ avail_sour
   (i.e., 0.2 * x[RegularMix] + 0.9 * x[SourSurpriseMix] ≤ 60)

Notes:
- All quantities are in kilograms.
- The decision variables x[m] are continuous, assuming fractional kilograms can be produced.
- This model assumes that all available candy is produced in the current period (i.e., no carryover stock effects).'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp
import json

def solve_linear_program():
    # Create the linear solver with the GLOP backend.
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Solver not created.")
        return None

    # VARIABLES
    # x0: kilograms of RegularMix, x1: kilograms of SourSurpriseMix
    x0 = solver.NumVar(0.0, solver.infinity(), 'RegularMix')
    x1 = solver.NumVar(0.0, solver.infinity(), 'SourSurpriseMix')

    # PARAMETERS
    # profit per kg for mixes
    profit0 = 3
    profit1 = 5

    # resource consumption requirements (kg per kg mix)
    reg_req0 = 0.8  # RegularMix requires 0.8 kg of regular candy per kg mix
    reg_req1 = 0.1  # SourSurpriseMix requires 0.1 kg of regular candy per kg mix

    sour_req0 = 0.2  # RegularMix requires 0.2 kg of sour candy per kg mix
    sour_req1 = 0.9  # SourSurpriseMix requires 0.9 kg of sour candy per kg mix

    # available resources
    avail_reg = 80
    avail_sour = 60

    # OBJECTIVE: Maximize profit
    solver.Maximize(profit0 * x0 + profit1 * x1)

    # CONSTRAINTS
    # 1. Regular candy constraint:
    solver.Add(reg_req0 * x0 + reg_req1 * x1 <= avail_reg)
    # 2. Sour candy constraint:
    solver.Add(sour_req0 * x0 + sour_req1 * x1 <= avail_sour)

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "variables": {
                "ProductionMix": {
                    "0": x0.solution_value(),
                    "1": x1.solution_value()
                }
            },
            "objective": solver.Objective().Value()
        }
        return result
    elif status == pywraplp.Solver.INFEASIBLE:
        print("The problem is infeasible.")
        return None
    else:
        print("The solver did not find an optimal solution.")
        return None

def main():
    results = {}

    # Since the problem formulation is unique and unambiguous, we implement just one version here.
    linear_program_results = solve_linear_program()
    results["LinearProgram"] = linear_program_results

    # Print the structured results in JSON format.
    print(json.dumps(results, indent=2))

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
{
  "LinearProgram": {
    "variables": {
      "ProductionMix": {
        "0": 94.28571428571428,
        "1": 45.71428571428571
      }
    },
    "objective": 511.4285714285714
  }
}
'''

'''Expected Output:
Expected solution

: {'variables': {'ProductionMix': {'0': 94.28571428571428, '1': 45.71428571428571}}, 'objective': 511.4285714285714}'''

