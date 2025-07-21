# Problem Description:
'''Problem description: Both subsoil and topsoil need to be added to a garden bed. One bag of subsoil requires 10 units of water to hydrate while one bag of topsoil requires 6 units of water to hydrate every day. The truck used to transport the dirt has limited capacity and therefore, the farmer has available 150 bags of topsoil and subsoil combined. In addition, at least 10 bags of topsoil must be used. Since the topsoil is more expensive, at most 30% of all bags of soil can be topsoil. How many bags of each should be bought to minimize the total amount of water required to hydrate the garden bed?

Expected Output Schema:
{
  "variables": {
    "SubsoilBags": "float",
    "TopsoilBags": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- SoilType: the set of soil types = {subsoil, topsoil}

Parameters:
- waterSubsoil = 10 (water units required per bag of subsoil per day)
- waterTopsoil = 6 (water units required per bag of topsoil per day)
- maxTotalBags = 150 (maximum total number of bags available)
- minTopsoilBags = 10 (minimum number of topsoil bags required)
- topsoilFractionLimit = 0.30 (at most 30% of all bags can be topsoil)
  • Note: The constraint topsoilBags ≤ topsoilFractionLimit × (subsoilBags + topsoilBags) can be equivalently linearized as:
    0.7 × topsoilBags ≤ 0.3 × subsoilBags, or equivalently, 7 × topsoilBags ≤ 3 × subsoilBags.

Variables:
- subsoilBags: number of subsoil bags used [integer, ≥ 0]
- topsoilBags: number of topsoil bags used [integer, ≥ 0]

Objective:
- Minimize totalWater = waterSubsoil × subsoilBags + waterTopsoil × topsoilBags
  • That is, minimize totalWater = 10 × subsoilBags + 6 × topsoilBags

Constraints:
1. Total bags constraint: subsoilBags + topsoilBags ≤ maxTotalBags
2. Minimum topsoil constraint: topsoilBags ≥ minTopsoilBags
3. Topsoil proportion constraint: 7 × topsoilBags ≤ 3 × subsoilBags  
   • This linear formulation enforces that topsoilBags ≤ 0.30 × (subsoilBags + topsoilBags).

Notes:
- All units are consistent: water is measured in water units per day per bag, and bag counts are whole units.
- Both decision variables are defined as integers to reflect the discrete number of bags. 

Expected Output Schema:
{
  "variables": {
    "SubsoilBags": "float",  // here representing an integer number (≥ 0)
    "TopsoilBags": "float"   // here representing an integer number (≥ 0)
  },
  "objective": "float"        // total water required: 10 × SubsoilBags + 6 × TopsoilBags
}'''

# Generated Code:
#!/usr/bin/env python3
"""
This script implements two separate formulations of the same soil hydration optimization problem using Google OR-Tools.
Both formulations represent the constraint on topsoil proportion differently but are equivalent.
Formulation 1 uses the linearized constraint: 7 * TopsoilBags ≤ 3 * SubsoilBags.
Formulation 2 uses the original interpretation: TopsoilBags ≤ 0.3 * (SubsoilBags + TopsoilBags), which is algebraically equivalent.
Both models are solved using ortools.linear_solver.
"""

from ortools.linear_solver import pywraplp

def solve_model_formulation1():
    # Create the solver with CBC backend
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Solver not created.")
        return None

    # Parameters
    water_subsoil = 10
    water_topsoil = 6
    max_total_bags = 150
    min_topsoil_bags = 10

    # Variables: integers >= 0
    subsoilBags = solver.IntVar(0, max_total_bags, 'SubsoilBags')
    topsoilBags = solver.IntVar(0, max_total_bags, 'TopsoilBags')

    # Objective: minimize water usage = 10 * subsoilBags + 6 * topsoilBags
    solver.Minimize(water_subsoil * subsoilBags + water_topsoil * topsoilBags)

    # Constraint 1: Total bags constraint: subsoilBags + topsoilBags <= 150
    solver.Add(subsoilBags + topsoilBags <= max_total_bags)

    # Constraint 2: Minimum topsoil constraint: topsoilBags >= 10
    solver.Add(topsoilBags >= min_topsoil_bags)

    # Constraint 3 (Formulation 1): Topsoil proportion constraint: 7 * topsoilBags <= 3 * subsoilBags
    solver.Add(7 * topsoilBags <= 3 * subsoilBags)

    # Solve the model
    status = solver.Solve()

    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "SubsoilBags": subsoilBags.solution_value(),
            "TopsoilBags": topsoilBags.solution_value(),
            "objective": solver.Objective().Value()
        }
    else:
        result = {"error": "The problem does not have an optimal solution."}
    return result

def solve_model_formulation2():
    # Create the solver with CBC backend
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Solver not created.")
        return None

    # Parameters
    water_subsoil = 10
    water_topsoil = 6
    max_total_bags = 150
    min_topsoil_bags = 10

    # Variables: integers, >= 0
    s = solver.IntVar(0, max_total_bags, 'SubsoilBags')
    t = solver.IntVar(0, max_total_bags, 'TopsoilBags')

    # Objective: minimize total water = 10 * s + 6 * t
    solver.Minimize(water_subsoil * s + water_topsoil * t)

    # Constraint 1: Total bags: s + t <= 150
    solver.Add(s + t <= max_total_bags)

    # Constraint 2: At least 10 topsoil bags: t >= 10
    solver.Add(t >= min_topsoil_bags)

    # Constraint 3 (Formulation 2): Original topsoil proportion constraint:
    # TopsoilBags <= 0.3*(SubsoilBags + TopsoilBags)
    # Which can be rewritten as: t - 0.3*t <= 0.3*s, i.e., 0.7*t <= 0.3*s,
    # and further multiplying by 10 gives: 7*t <= 3*s.
    solver.Add(7 * t <= 3 * s)

    # Solve the model
    status = solver.Solve()

    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "SubsoilBags": s.solution_value(),
            "TopsoilBags": t.solution_value(),
            "objective": solver.Objective().Value()
        }
    else:
        result = {"error": "The problem does not have an optimal solution."}
    return result

def main():
    result1 = solve_model_formulation1()
    result2 = solve_model_formulation2()

    print("Results for Formulation 1 (Using constraint: 7 * TopsoilBags <= 3 * SubsoilBags):")
    if "error" in result1:
        print(result1["error"])
    else:
        print(result1)

    print("\nResults for Formulation 2 (Using constraint: TopsoilBags <= 0.3*(SubsoilBags + TopsoilBags)):")
    if "error" in result2:
        print(result2["error"])
    else:
        print(result2)

if __name__ == "__main__":
    main()

'''Execution Results:
SUCCESS:
Results for Formulation 1 (Using constraint: 7 * TopsoilBags <= 3 * SubsoilBags):
{'SubsoilBags': 24.0, 'TopsoilBags': 10.0, 'objective': 300.0}

Results for Formulation 2 (Using constraint: TopsoilBags <= 0.3*(SubsoilBags + TopsoilBags)):
{'SubsoilBags': 24.0, 'TopsoilBags': 10.0, 'objective': 300.0}
'''

'''Expected Output:
Expected solution

: {'variables': {'SubsoilBags': 24.0, 'TopsoilBags': 10.0}, 'objective': 300.0}'''

