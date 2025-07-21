# Problem Description:
'''Problem description: A sailor can eat either a crab cakes or a lobster roll for his meals. He needs to ensure he gets at least 80 units of vitamin A and 100 units of vitamin C. Each crab cake contains 5 units of vitamin A and 7 units of vitamin C. Each lobster roll contains 8 units of vitamin A and 4 units of vitamin C. In addition, since lobster is more expensive, at most 40% of his meals should be lobster rolls. If each crab cake contains 4 units of unsaturated fat and each lobster roll contains 6 units of unsaturated fat, how many of each should he eat to minimize his unsaturated fat intake?

Expected Output Schema:
{
  "variables": {
    "QuantityCrabCake": "float",
    "QuantityLobsterRoll": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- M: set of meal types = {CrabCake, LobsterRoll}

Parameters:
- vitaminA_per_CrabCake = 5 [units of vitamin A per crab cake]
- vitaminC_per_CrabCake = 7 [units of vitamin C per crab cake]
- vitaminA_per_LobsterRoll = 8 [units of vitamin A per lobster roll]
- vitaminC_per_LobsterRoll = 4 [units of vitamin C per lobster roll]
- unsatFat_per_CrabCake = 4 [units of unsaturated fat per crab cake]
- unsatFat_per_LobsterRoll = 6 [units of unsaturated fat per lobster roll]
- required_vitaminA = 80 [units of vitamin A]
- required_vitaminC = 100 [units of vitamin C]
- max_lobster_ratio = 0.4 [maximum fraction of meals that can be lobster rolls]

Variables:
- QuantityCrabCake, a decision variable representing the number of crab cakes to consume [continuous nonnegative, assumed to be integer if meals must be whole units]
- QuantityLobsterRoll, a decision variable representing the number of lobster rolls to consume [continuous nonnegative, assumed to be integer if meals must be whole units]

Objective:
- Minimize total unsaturated fat intake = (unsatFat_per_CrabCake * QuantityCrabCake) + (unsatFat_per_LobsterRoll * QuantityLobsterRoll)

Constraints:
1. Vitamin A requirement: (vitaminA_per_CrabCake * QuantityCrabCake) + (vitaminA_per_LobsterRoll * QuantityLobsterRoll) >= required_vitaminA
2. Vitamin C requirement: (vitaminC_per_CrabCake * QuantityCrabCake) + (vitaminC_per_LobsterRoll * QuantityLobsterRoll) >= required_vitaminC
3. Lobster roll meal ratio constraint: QuantityLobsterRoll <= max_lobster_ratio * (QuantityCrabCake + QuantityLobsterRoll)

Notes:
- All parameter units are consistent with the meal description.
- Decision variables may be modeled as integers if fractional meals are not allowed.
- This model minimizes the consumption of unsaturated fat while satisfying the nutritional constraints and the meal composition guideline.

---

Expected Output Schema:
{
  "variables": {
    "QuantityCrabCake": "float",
    "QuantityLobsterRoll": "float"
  },
  "objective": "float"
}'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_continuous_model():
    # Create solver using GLOP which supports continuous variables.
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        return None

    # Parameters
    vitaminA_per_CrabCake = 5
    vitaminC_per_CrabCake = 7
    vitaminA_per_LobsterRoll = 8
    vitaminC_per_LobsterRoll = 4
    unsatFat_per_CrabCake = 4
    unsatFat_per_LobsterRoll = 6
    required_vitaminA = 80
    required_vitaminC = 100
    max_lobster_ratio = 0.4

    # Decision Variables (continuous)
    # Quantity of Crab Cakes and Lobster Rolls
    QuantityCrabCake = solver.NumVar(0, solver.infinity(), 'QuantityCrabCake')
    QuantityLobsterRoll = solver.NumVar(0, solver.infinity(), 'QuantityLobsterRoll')

    # Constraints
    # Vitamin A constraint: 5 * QuantityCrabCake + 8 * QuantityLobsterRoll >= 80
    solver.Add(vitaminA_per_CrabCake * QuantityCrabCake + vitaminA_per_LobsterRoll * QuantityLobsterRoll >= required_vitaminA)
    # Vitamin C constraint: 7 * QuantityCrabCake + 4 * QuantityLobsterRoll >= 100
    solver.Add(vitaminC_per_CrabCake * QuantityCrabCake + vitaminC_per_LobsterRoll * QuantityLobsterRoll >= required_vitaminC)
    # Lobster roll meal ratio constraint:
    # QuantityLobsterRoll <= max_lobster_ratio * (QuantityCrabCake + QuantityLobsterRoll)
    # This can be rearranged as: 0.6 * QuantityLobsterRoll <= 0.4 * QuantityCrabCake => 3 * QuantityLobsterRoll <= 2 * QuantityCrabCake
    solver.Add(3 * QuantityLobsterRoll <= 2 * QuantityCrabCake)

    # Objective: minimize unsaturated fat intake
    solver.Minimize(unsatFat_per_CrabCake * QuantityCrabCake + unsatFat_per_LobsterRoll * QuantityLobsterRoll)

    status = solver.Solve()

    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result['QuantityCrabCake'] = QuantityCrabCake.solution_value()
        result['QuantityLobsterRoll'] = QuantityLobsterRoll.solution_value()
        result['objective'] = solver.Objective().Value()
    else:
        result['error'] = 'No optimal solution found in continuous model.'

    return result

def solve_integer_model():
    # Create solver for Mixed Integer Programming using CBC.
    solver = pywraplp.Solver.CreateSolver('CBC_MIXED_INTEGER_PROGRAMMING')
    if not solver:
        return None

    # Parameters
    vitaminA_per_CrabCake = 5
    vitaminC_per_CrabCake = 7
    vitaminA_per_LobsterRoll = 8
    vitaminC_per_LobsterRoll = 4
    unsatFat_per_CrabCake = 4
    unsatFat_per_LobsterRoll = 6
    required_vitaminA = 80
    required_vitaminC = 100
    max_lobster_ratio = 0.4

    # Decision Variables (integer)
    # Assume meals must be whole units so variables are integer.
    QuantityCrabCake = solver.IntVar(0, solver.infinity(), 'QuantityCrabCake')
    QuantityLobsterRoll = solver.IntVar(0, solver.infinity(), 'QuantityLobsterRoll')

    # Constraints
    # Vitamin A requirement: 5 * QuantityCrabCake + 8 * QuantityLobsterRoll >= 80
    solver.Add(vitaminA_per_CrabCake * QuantityCrabCake + vitaminA_per_LobsterRoll * QuantityLobsterRoll >= required_vitaminA)
    # Vitamin C requirement: 7 * QuantityCrabCake + 4 * QuantityLobsterRoll >= 100
    solver.Add(vitaminC_per_CrabCake * QuantityCrabCake + vitaminC_per_LobsterRoll * QuantityLobsterRoll >= required_vitaminC)
    # Lobster roll meal ratio constraint: QuantityLobsterRoll <= 0.4*(QuantityCrabCake+QuantityLobsterRoll)
    # As before, transformed to: 3*QuantityLobsterRoll <= 2*QuantityCrabCake
    solver.Add(3 * QuantityLobsterRoll <= 2 * QuantityCrabCake)

    # Objective: minimize unsaturated fat intake = 4 * QuantityCrabCake + 6 * QuantityLobsterRoll
    solver.Minimize(unsatFat_per_CrabCake * QuantityCrabCake + unsatFat_per_LobsterRoll * QuantityLobsterRoll)

    status = solver.Solve()

    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result['QuantityCrabCake'] = QuantityCrabCake.solution_value()
        result['QuantityLobsterRoll'] = QuantityLobsterRoll.solution_value()
        result['objective'] = solver.Objective().Value()
    else:
        result['error'] = 'No optimal solution found in integer model.'

    return result

def main():
    continuous_result = solve_continuous_model()
    integer_result = solve_integer_model()

    print("Continuous Model Result:")
    if 'error' in continuous_result:
        print("Error:", continuous_result['error'])
    else:
        print("Solution:")
        print("QuantityCrabCake =", continuous_result['QuantityCrabCake'])
        print("QuantityLobsterRoll =", continuous_result['QuantityLobsterRoll'])
        print("Objective (Total Unsaturated Fat) =", continuous_result['objective'])
    
    print("\nInteger Model Result:")
    if 'error' in integer_result:
        print("Error:", integer_result['error'])
    else:
        print("Solution:")
        print("QuantityCrabCake =", integer_result['QuantityCrabCake'])
        print("QuantityLobsterRoll =", integer_result['QuantityLobsterRoll'])
        print("Objective (Total Unsaturated Fat) =", integer_result['objective'])

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Continuous Model Result:
Solution:
QuantityCrabCake = 13.333333333333332
QuantityLobsterRoll = 1.6666666666666676
Objective (Total Unsaturated Fat) = 63.333333333333336

Integer Model Result:
Solution:
QuantityCrabCake = 16.0
QuantityLobsterRoll = 0.0
Objective (Total Unsaturated Fat) = 64.0
'''

'''Expected Output:
Expected solution

: {'variables': {'QuantityCrabCake': 13.333333333333332, 'QuantityLobsterRoll': 1.6666666666666665}, 'objective': 63.33333333333333}'''

