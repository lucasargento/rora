# Problem Description:
'''Problem description: Maple Oil processes three types of crude oil: light oil, non-sticky oil and heavy oil. Each tank of light oil produces a net revenue of $550, each tank of non-sticky oil produces a net revenue of $750, and each tank of heavy oil produces a net revenue of $950. To process a tank of light oil, 3 units of compound A and 3 units of compound B are required. To process a tank of non-sticky oil, 6 units of compound A and 2 units of compound B are required. To process a tank of heavy oil, 9 units of compound A and 3 units of compound B are required. Currently the company has 250 units of compound A and 150 units of compound B to process. How many full or partial tanks of each oil should the company process so that net revenue is maximized?

Expected Output Schema:
{
  "variables": {
    "NumTanksProcessed": {
      "0": "float",
      "1": "float",
      "2": "float"
    }
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- OilTypes: set of oil types = {Light, NonSticky, Heavy}

Parameters:
- revenue[o] : net revenue per tank processed for oil type o [USD per tank]
  • revenue[Light] = 550
  • revenue[NonSticky] = 750
  • revenue[Heavy] = 950
- compoundA_req[o] : amount of Compound A required per tank for oil type o [units per tank]
  • compoundA_req[Light] = 3
  • compoundA_req[NonSticky] = 6
  • compoundA_req[Heavy] = 9
- compoundB_req[o] : amount of Compound B required per tank for oil type o [units per tank]
  • compoundB_req[Light] = 3
  • compoundB_req[NonSticky] = 2
  • compoundB_req[Heavy] = 3
- available_CompoundA: total available units of Compound A = 250 [units]
- available_CompoundB: total available units of Compound B = 150 [units]

Variables:
- tanks[o] : number of tanks processed for oil type o, where o in OilTypes [continuous, nonnegative]
  (Interpretation: Number of full or partial tanks processed for each oil type)

Objective:
- Maximize total net revenue = sum over o in OilTypes of (revenue[o] * tanks[o])
  (Units: USD; Interpretation: Total net revenue from processing tanks)

Constraints:
1. Compound A Constraint:
  sum over o in OilTypes of (compoundA_req[o] * tanks[o]) ≤ available_CompoundA
  (Ensures that Compound A used does not exceed 250 units)

2. Compound B Constraint:
  sum over o in OilTypes of (compoundB_req[o] * tanks[o]) ≤ available_CompoundB
  (Ensures that Compound B used does not exceed 150 units)'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_linear_optimization():
    # Create the linear solver with GLOP backend.
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Error: Could not create solver.")
        return None

    # Define variables:
    # tanks[0]: number of light oil tanks processed
    # tanks[1]: number of non-sticky oil tanks processed
    # tanks[2]: number of heavy oil tanks processed
    light = solver.NumVar(0, solver.infinity(), "light")
    nonsticky = solver.NumVar(0, solver.infinity(), "nonsticky")
    heavy = solver.NumVar(0, solver.infinity(), "heavy")

    # Define parameters for revenues and compound requirements.
    # Revenue per tank for each oil type.
    revenue_light = 550
    revenue_nonsticky = 750
    revenue_heavy = 950

    # Compound requirements per tank.
    # Compound A requirements per tank.
    compoundA_req_light = 3
    compoundA_req_nonsticky = 6
    compoundA_req_heavy = 9
    # Compound B requirements per tank.
    compoundB_req_light = 3
    compoundB_req_nonsticky = 2
    compoundB_req_heavy = 3

    # Available compounds.
    available_CompoundA = 250
    available_CompoundB = 150

    # Constraints:
    # 1. Compound A Constraint:
    solver.Add(compoundA_req_light * light +
               compoundA_req_nonsticky * nonsticky +
               compoundA_req_heavy * heavy <= available_CompoundA)
    # 2. Compound B Constraint:
    solver.Add(compoundB_req_light * light +
               compoundB_req_nonsticky * nonsticky +
               compoundB_req_heavy * heavy <= available_CompoundB)

    # Define objective: maximize total net revenue.
    objective = solver.Objective()
    objective.SetCoefficient(light, revenue_light)
    objective.SetCoefficient(nonsticky, revenue_nonsticky)
    objective.SetCoefficient(heavy, revenue_heavy)
    objective.SetMaximization()

    # Solve the problem.
    status = solver.Solve()

    result = {}
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        result["variables"] = {
            "NumTanksProcessed": {
                "0": light.solution_value(),
                "1": nonsticky.solution_value(),
                "2": heavy.solution_value()
            }
        }
        result["objective"] = objective.Value()
        print("Linear Optimization (GLOP) Solution:")
        print(result)
    else:
        print("No solution found for the linear optimization model.")
        result = None

    return result

def main():
    # Only one formulation is proposed (linear programming), so we run one implementation.
    sol_linear = solve_linear_optimization()
    
if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Linear Optimization (GLOP) Solution:
{'variables': {'NumTanksProcessed': {'0': 33.33333333333334, '1': 24.999999999999996, '2': 0.0}}, 'objective': 37083.333333333336}
'''

'''Expected Output:
Expected solution

: {'variables': {'NumTanksProcessed': {'0': 33.333333333333336, '1': 25.0, '2': 0.0}}, 'objective': 37083.333333333336}'''

