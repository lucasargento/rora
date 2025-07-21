# Problem Description:
'''Problem description: Platinum in combination with palladium has been used as a catalyst in cars and it changes carbon monoxide, which is toxic, into carbon dioxide. An automotive company is comparing two different catalysts, a palladium-heavy catalyst and a platinum-heavy catalyst. The process with a palladium-heavy catalyst requires 15 units of platinum and 25 units of palladium and can perform the conversion to carbon dioxide at a rate of 5 units per second. A platinum-heavy catalyst requires 20 units of platinum and 14 units of palladium and converts to carbon dioxide at a rate of 4 units per second. There are 450 units of platinum and 390 units of palladium available. How many of each catalyst should be used to maximize the amount converted into carbon dioxide?

Expected Output Schema:
{
  "variables": {
    "CatalystUsage": {
      "0": "float",
      "1": "float"
    }
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- CATALYST: set of catalyst types = {PalladiumHeavy, PlatinumHeavy}

Parameters:
- platinum_req[c] = units of platinum required per catalyst type c
  • platinum_req[PalladiumHeavy] = 15 (units per catalyst)
  • platinum_req[PlatinumHeavy] = 20 (units per catalyst)
- palladium_req[c] = units of palladium required per catalyst type c
  • palladium_req[PalladiumHeavy] = 25 (units per catalyst)
  • palladium_req[PlatinumHeavy] = 14 (units per catalyst)
- conversion_rate[c] = conversion rate (units of carbon monoxide converted to carbon dioxide per second) per catalyst type c
  • conversion_rate[PalladiumHeavy] = 5 (units/second)
  • conversion_rate[PlatinumHeavy] = 4 (units/second)
- available_platinum = 450 (units of platinum available)
- available_palladium = 390 (units of palladium available)

Variables:
- CatalystUsage[c] for each c in CATALYST, representing the number of catalysts of type c to use
  • Domain: CatalystUsage[c] ≥ 0 (assuming continuous decision variables; if catalysts must be whole units, then they are integers)

Objective:
- Maximize total conversion rate per second = 
  conversion_rate[PalladiumHeavy] * CatalystUsage[PalladiumHeavy] + conversion_rate[PlatinumHeavy] * CatalystUsage[PlatinumHeavy]

Constraints:
1. Platinum availability constraint:
   platinum_req[PalladiumHeavy] * CatalystUsage[PalladiumHeavy] + platinum_req[PlatinumHeavy] * CatalystUsage[PlatinumHeavy] ≤ available_platinum
   (i.e., 15 * CatalystUsage[PalladiumHeavy] + 20 * CatalystUsage[PlatinumHeavy] ≤ 450)

2. Palladium availability constraint:
   palladium_req[PalladiumHeavy] * CatalystUsage[PalladiumHeavy] + palladium_req[PlatinumHeavy] * CatalystUsage[PlatinumHeavy] ≤ available_palladium
   (i.e., 25 * CatalystUsage[PalladiumHeavy] + 14 * CatalystUsage[PlatinumHeavy] ≤ 390)

-----------------------------------------------------------
Expected Output Schema:
{
  "variables": {
    "CatalystUsage": {
      "0": "float",     // corresponds to PalladiumHeavy catalyst
      "1": "float"      // corresponds to PlatinumHeavy catalyst
    }
  },
  "objective": "float"   // total conversion rate (units converted per second)"
}'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_linear_program():
    # Create solver instance using the GLOP backend for linear programming.
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Solver not created.")
        return None

    # Parameters
    # Platinum requirements per catalyst type: 15 for PalladiumHeavy, 20 for PlatinumHeavy
    platinum_req = [15, 20]
    # Palladium requirements per catalyst type: 25 for PalladiumHeavy, 14 for PlatinumHeavy
    palladium_req = [25, 14]
    # Conversion rates: 5 for PalladiumHeavy, 4 for PlatinumHeavy
    conversion_rate = [5, 4]
    # Available amounts
    available_platinum = 450
    available_palladium = 390

    # Variables:
    # CatalystUsage[0] corresponds to PalladiumHeavy catalyst (continuous)
    # CatalystUsage[1] corresponds to PlatinumHeavy catalyst (continuous)
    CatalystUsage = [solver.NumVar(0.0, solver.infinity(), 'CatalystUsage_0'),
                     solver.NumVar(0.0, solver.infinity(), 'CatalystUsage_1')]

    # Constraints:
    # Platinum constraint: 15 * CatalystUsage[0] + 20 * CatalystUsage[1] <= 450
    solver.Add(platinum_req[0] * CatalystUsage[0] + platinum_req[1] * CatalystUsage[1] <= available_platinum)

    # Palladium constraint: 25 * CatalystUsage[0] + 14 * CatalystUsage[1] <= 390
    solver.Add(palladium_req[0] * CatalystUsage[0] + palladium_req[1] * CatalystUsage[1] <= available_palladium)

    # Objective:
    # Maximize conversion rate: 5 * CatalystUsage[0] + 4 * CatalystUsage[1]
    objective = solver.Objective()
    objective.SetCoefficient(CatalystUsage[0], conversion_rate[0])
    objective.SetCoefficient(CatalystUsage[1], conversion_rate[1])
    objective.SetMaximization()

    # Solve the problem
    status = solver.Solve()

    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        # Retrieve the optimal values.
        catalyst_usage_solution = [CatalystUsage[0].solution_value(), CatalystUsage[1].solution_value()]
        total_conversion_rate = objective.Value()
        result = {
            "variables": {
                "CatalystUsage": {
                    "0": catalyst_usage_solution[0],
                    "1": catalyst_usage_solution[1]
                }
            },
            "objective": total_conversion_rate
        }
    else:
        print("No optimal solution found.")
        result = None
    return result

def main():
    # Only one formulation is provided, so we implement one model.
    lp_result = solve_linear_program()

    print("Results from the Linear Programming Model:")
    if lp_result is not None:
        print(lp_result)
    else:
        print("The model is infeasible or an error occurred.")

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Results from the Linear Programming Model:
{'variables': {'CatalystUsage': {'0': 5.172413793103451, '1': 18.620689655172413}}, 'objective': 100.3448275862069}
'''

'''Expected Output:
Expected solution

: {'variables': {'CatalystUsage': {'0': 5.172413793103448, '1': 18.620689655172413}}, 'objective': 100.34482758620689}'''

