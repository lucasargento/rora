# Problem Description:
'''Problem description: A smoothie shop has a promotion for their two smoothies; an acai berry smoothie and a banana chocolate smoothie. It takes 7 units of acai berries and 3 units of water to make the acai berry smoothie. It takes 6 units of banana chocolate and 4 units of water to make the banana chocolate smoothie. Banana chocolate smoothies are more popular and thus the number of banana chocolate smoothies made must be more than the number of acai berry smoothies made. However, the acai berry smoothies have a loyal customer base, and at least 35% of the smoothies made must be acai berry smoothies. If the smoothie shop has 3500 units of acai berries and 3200 units of banana chocolate, to reduce the total amount of water, how many of each smoothie type should be made?

Expected Output Schema:
{
  "variables": {
    "AcaiSmoothies": "float",
    "BananaSmoothies": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Below is one precise formulation of the problem in the five‐element framework. In this model, we assume that the decision variables (number of smoothies to produce) may be treated as continuous values. (In a practical implementation they would likely be integers.) Note that the “more than” constraint is modeled by requiring the number of banana chocolate smoothies to be at least one unit in excess of the acai berry smoothies. An alternative formulation could relax this by allowing noninteger values and then enforcing a strict inequality by a small epsilon; here, we assume integer decisions so that BananaSmoothies ≥ AcaiSmoothies + 1.

──────────────────────────────
Sets:
- S = {SmoothieTypes} with S = {Acai, Banana}

──────────────────────────────
Parameters:
- acaiBerryPerAcai = 7    // units of acai berries required per acai berry smoothie [units/smoothie]
- waterPerAcai = 3        // units of water required per acai berry smoothie [units/smoothie]
- bananaPerBanana = 6     // units of banana chocolate required per banana chocolate smoothie [units/smoothie]
- waterPerBanana = 4      // units of water required per banana chocolate smoothie [units/smoothie]
- availableAcai = 3500      // total available acai berries [units]
- availableBanana = 3200    // total available banana chocolate [units]
- minAcaiFraction = 0.35  // minimum fraction of total smoothies that must be acai berry smoothies
- epsilon = 1             // minimum additional unit to enforce strict “more than” (banana smoothies > acai smoothies)

──────────────────────────────
Variables:
- AcaiSmoothies: number of acai berry smoothies to produce [nonnegative integer, units]
- BananaSmoothies: number of banana chocolate smoothies to produce [nonnegative integer, units]

──────────────────────────────
Objective:
Minimize total water used = (waterPerAcai * AcaiSmoothies) + (waterPerBanana * BananaSmoothies)
[Units: water units]

──────────────────────────────
Constraints:
1. Acai ingredient availability:
   acaiBerryPerAcai * AcaiSmoothies ≤ availableAcai
   (i.e., 7 * AcaiSmoothies ≤ 3500)

2. Banana chocolate ingredient availability:
   bananaPerBanana * BananaSmoothies ≤ availableBanana
   (i.e., 6 * BananaSmoothies ≤ 3200)

3. Production popularity constraint (“banana smoothies must be more than acai smoothies”):
   BananaSmoothies ≥ AcaiSmoothies + epsilon
   (i.e., BananaSmoothies ≥ AcaiSmoothies + 1)

4. Loyal customer base constraint (at least 35% of smoothies must be acai berry):
   AcaiSmoothies ≥ minAcaiFraction * (AcaiSmoothies + BananaSmoothies)
   (i.e., AcaiSmoothies ≥ 0.35 * (AcaiSmoothies + BananaSmoothies))

──────────────────────────────
Expected Output Schema:
{
  "variables": {
    "AcaiSmoothies": "float",
    "BananaSmoothies": "float"
  },
  "objective": "float"
}

This model is complete, adheres to the data given, and is written with simple expressions so it can be easily implemented (for example, in Python using OR-Tools).'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_integer_model():
    # Create the integer solver using CBC (Mixed Integer Programming)
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Integer solver creation failed.")
        return None

    # Parameters
    acaiBerryPerAcai = 7    # units of acai berries per acai smoothie
    waterPerAcai = 3        # water units per acai smoothie
    bananaPerBanana = 6     # units of banana chocolate per banana smoothie
    waterPerBanana = 4      # water units per banana smoothie
    availableAcai = 3500    # total available acai berries
    availableBanana = 3200  # total available banana chocolate
    minAcaiFraction = 0.35  # minimum fraction of acai smoothies
    epsilon = 1             # minimum extra unit for banana smoothies

    # Decision Variables (nonnegative integers)
    AcaiSmoothies = solver.IntVar(0, solver.infinity(), 'AcaiSmoothies')
    BananaSmoothies = solver.IntVar(0, solver.infinity(), 'BananaSmoothies')

    # Constraints
    # 1. Acai ingredient availability: 7 * AcaiSmoothies <= 3500
    solver.Add(acaiBerryPerAcai * AcaiSmoothies <= availableAcai)
    # 2. Banana chocolate ingredient availability: 6 * BananaSmoothies <= 3200
    solver.Add(bananaPerBanana * BananaSmoothies <= availableBanana)
    # 3. Banana smoothies must exceed acai smoothies by at least epsilon: BananaSmoothies >= AcaiSmoothies + 1
    solver.Add(BananaSmoothies >= AcaiSmoothies + epsilon)
    # 4. Loyal customer base constraint: at least 35% of total smoothies must be acai berry smoothies
    solver.Add(AcaiSmoothies >= minAcaiFraction * (AcaiSmoothies + BananaSmoothies))

    # Objective: minimize total water used = 3 * AcaiSmoothies + 4 * BananaSmoothies
    objective = solver.Objective()
    objective.SetCoefficient(AcaiSmoothies, waterPerAcai)
    objective.SetCoefficient(BananaSmoothies, waterPerBanana)
    objective.SetMinimization()

    # Solve the problem
    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "AcaiSmoothies": AcaiSmoothies.solution_value(),
            "BananaSmoothies": BananaSmoothies.solution_value(),
            "objective": objective.Value()
        }
        return result
    else:
        print("No optimal solution found for the integer model.")
        return None

def solve_continuous_model():
    # Create the continuous solver using GLOP (Linear Programming)
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Continuous solver creation failed.")
        return None

    # Parameters
    acaiBerryPerAcai = 7    # units of acai berries per acai smoothie
    waterPerAcai = 3        # water units per acai smoothie
    bananaPerBanana = 6     # units of banana chocolate per banana smoothie
    waterPerBanana = 4      # water units per banana smoothie
    availableAcai = 3500    # total available acai berries
    availableBanana = 3200  # total available banana chocolate
    minAcaiFraction = 0.35  # minimum fraction of acai smoothies
    epsilon = 1             # for continuous, enforce at least 1 unit difference
    
    # Decision Variables (nonnegative continuous values)
    AcaiSmoothies = solver.NumVar(0.0, solver.infinity(), 'AcaiSmoothies')
    BananaSmoothies = solver.NumVar(0.0, solver.infinity(), 'BananaSmoothies')

    # Constraints
    # 1. Acai ingredient availability
    solver.Add(acaiBerryPerAcai * AcaiSmoothies <= availableAcai)
    # 2. Banana chocolate ingredient availability
    solver.Add(bananaPerBanana * BananaSmoothies <= availableBanana)
    # 3. Banana smoothies must be more than acai smoothies: BananaSmoothies >= AcaiSmoothies + 1
    solver.Add(BananaSmoothies >= AcaiSmoothies + epsilon)
    # 4. Loyal customer base constraint: AcaiSmoothies >= 0.35*(AcaiSmoothies + BananaSmoothies)
    solver.Add(AcaiSmoothies >= minAcaiFraction * (AcaiSmoothies + BananaSmoothies))

    # Objective: minimize total water used = 3*AcaiSmoothies + 4*BananaSmoothies
    solver.Minimize(waterPerAcai * AcaiSmoothies + waterPerBanana * BananaSmoothies)

    # Solve the problem
    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "AcaiSmoothies": AcaiSmoothies.solution_value(),
            "BananaSmoothies": BananaSmoothies.solution_value(),
            "objective": solver.Objective().Value()
        }
        return result
    else:
        print("No optimal solution found for the continuous model.")
        return None

def main():
    int_result = solve_integer_model()
    cont_result = solve_continuous_model()

    print("Integer Model Result:")
    if int_result:
        print(int_result)
    else:
        print("Integer model did not find an optimal solution.")

    print("\nContinuous Model Result:")
    if cont_result:
        print(cont_result)
    else:
        print("Continuous model did not find an optimal solution.")

if __name__ == "__main__":
    main()

'''Execution Results:
SUCCESS:
Integer Model Result:
{'AcaiSmoothies': 2.0, 'BananaSmoothies': 3.0, 'objective': 18.0}

Continuous Model Result:
{'AcaiSmoothies': 1.1666666666666663, 'BananaSmoothies': 2.166666666666666, 'objective': 12.166666666666664}
'''

'''Expected Output:
Expected solution

: {'variables': {'AcaiSmoothies': 0.0, 'BananaSmoothies': 0.0}, 'objective': 0.0}'''

