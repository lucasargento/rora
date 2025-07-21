# Problem Description:
'''Problem description: A pharmacy has 3000 mg of morphine to make painkillers and sleeping pills. Each painkiller pill requires 10 mg of morphine and 3 units of digestive medicine. Each sleeping pill requires 6 mg of morphine and 5 units of digestive medicine. The pharmacy needs to make at least 50 painkiller pills. Since sleeping pills are more popular, at least 70% of the pills should be sleeping pills. How many of each should the pharmacy make to minimize the total amount of digestive medicine needed?

Expected Output Schema:
{
  "variables": {
    "PainkillerPills": "float",
    "SleepingPills": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- PillTypes = {Painkiller, Sleeping}

Parameters:
- totalMorphineAvailable = 3000 mg (total morphine available)
- morphinePerPainkiller = 10 mg (morphine needed per painkiller)
- morphinePerSleeping = 6 mg (morphine needed per sleeping pill)
- digestiveMedPerPainkiller = 3 units (digestive medicine needed per painkiller)
- digestiveMedPerSleeping = 5 units (digestive medicine needed per sleeping pill)
- minPainkillers = 50 (minimum number of painkiller pills required)
- minSleepingRatio = 0.70 (sleeping pills must be at least 70% of total pills)

Variables:
- PainkillerPills: number of painkiller pills to produce [nonnegative integer, units: pills]
- SleepingPills: number of sleeping pills to produce [nonnegative integer, units: pills]

Objective:
- Minimize total digestive medicine used, calculated as:
  TotalDigestiveMedicine = digestiveMedPerPainkiller * PainkillerPills + digestiveMedPerSleeping * SleepingPills

Constraints:
1. Morphine Constraint:
   morphinePerPainkiller * PainkillerPills + morphinePerSleeping * SleepingPills <= totalMorphineAvailable
   (i.e., 10 * PainkillerPills + 6 * SleepingPills <= 3000)

2. Minimum Painkiller Production:
   PainkillerPills >= minPainkillers
   (i.e., PainkillerPills >= 50)

3. Sleeping Pills Minimum Ratio:
   The fraction of sleeping pills among total pills must be at least 70%. This can be written as:
   SleepingPills >= minSleepingRatio * (PainkillerPills + SleepingPills)
   Rearranging the inequality:
   SleepingPills - 0.7 * SleepingPills >= 0.7 * PainkillerPills
   0.3 * SleepingPills >= 0.7 * PainkillerPills
   Thus, SleepingPills >= (0.7 / 0.3) * PainkillerPills  or equivalently SleepingPills >= (7/3) * PainkillerPills

Model Summary in Expected Output Schema:
{
  "variables": {
    "PainkillerPills": "integer, number of painkiller pills to produce [pills]",
    "SleepingPills": "integer, number of sleeping pills to produce [pills]"
  },
  "objective": "Minimize digestive medicine = 3 * PainkillerPills + 5 * SleepingPills"
}

Notes:
- All units are consistent with the problem description.
- Decision variables are defined as integers since you cannot produce fractional pills.
- The sleeping pills ratio inequality has been reformulated for ease of implementation.
- This model minimizes the total digestive medicine required, subject to morphine availability, a minimum production threshold for painkillers, and the requirement that sleeping pills form at least 70% of the total production.'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp
from ortools.sat.python import cp_model

def solve_with_linear_solver():
    # Create the linear solver using the CBC backend.
    solver = pywraplp.Solver.CreateSolver('CBC_MIXED_INTEGER_PROGRAMMING')
    if not solver:
        print("Linear Solver not available.")
        return None

    # Decision Variables: integer number of painkiller and sleeping pills.
    # Upper bounds: using morphine constraint, maximum painkiller pills is 3000/10 = 300, and sleeping pills is 3000/6 ~ 500.
    painkiller = solver.IntVar(0, 300, 'PainkillerPills')
    sleeping = solver.IntVar(0, 500, 'SleepingPills')

    # Constraints:
    # 1. Morphine Constraint: 10 * PainkillerPills + 6 * SleepingPills <= 3000
    solver.Add(10 * painkiller + 6 * sleeping <= 3000)

    # 2. Minimum painkiller production: PainkillerPills >= 50
    solver.Add(painkiller >= 50)

    # 3. Sleeping pills minimum ratio: SleepingPills >= (7/3)*PainkillerPills
    # Multiply both sides by 3 to avoid fractions: 3 * SleepingPills >= 7 * PainkillerPills
    solver.Add(3 * sleeping >= 7 * painkiller)

    # Objective: Minimize total digestive medicine used = 3 * PainkillerPills + 5 * SleepingPills
    objective = solver.Objective()
    objective.SetCoefficient(painkiller, 3)
    objective.SetCoefficient(sleeping, 5)
    objective.SetMinimization()

    status = solver.Solve()

    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result["variables"] = {
            "PainkillerPills": painkiller.solution_value(),
            "SleepingPills": sleeping.solution_value()
        }
        result["objective"] = objective.Value()
    else:
        result["error"] = "No optimal solution found with the linear solver."
    return result

def solve_with_cp_sat():
    # Create the CP-SAT model instance.
    model = cp_model.CpModel()

    # Decision Variables: integer number of painkiller and sleeping pills.
    # Based on our reasoning, we set bounds: Painkiller in [0,300] and Sleeping in [0,500].
    painkiller = model.NewIntVar(0, 300, 'PainkillerPills')
    sleeping = model.NewIntVar(0, 500, 'SleepingPills')

    # Constraints:
    # 1. Morphine Constraint: 10 * PainkillerPills + 6 * SleepingPills <= 3000
    model.Add(10 * painkiller + 6 * sleeping <= 3000)

    # 2. Minimum painkiller production: PainkillerPills >= 50
    model.Add(painkiller >= 50)

    # 3. Sleeping pills minimum ratio: SleepingPills >= (7/3)*PainkillerPills
    # Multiply both sides by 3: 3 * SleepingPills >= 7 * PainkillerPills
    model.Add(3 * sleeping >= 7 * painkiller)

    # Objective: Minimize total digestive medicine used: 3 * PainkillerPills + 5 * SleepingPills
    model.Minimize(3 * painkiller + 5 * sleeping)

    # Solve model.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    result = {}
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        result["variables"] = {
            "PainkillerPills": solver.Value(painkiller),
            "SleepingPills": solver.Value(sleeping)
        }
        result["objective"] = solver.ObjectiveValue()
    else:
        result["error"] = "No optimal solution found with CP-SAT solver."
    return result

def main():
    print("---- Linear Solver (CBC Mixed Integer Programming) Result ----")
    linear_result = solve_with_linear_solver()
    if "error" in linear_result:
        print("Error:", linear_result["error"])
    else:
        print("PainkillerPills:", linear_result["variables"]["PainkillerPills"])
        print("SleepingPills:", linear_result["variables"]["SleepingPills"])
        print("Objective (Total Digestive Medicine):", linear_result["objective"])

    print("\n---- CP-SAT Solver Result ----")
    cp_sat_result = solve_with_cp_sat()
    if "error" in cp_sat_result:
        print("Error:", cp_sat_result["error"])
    else:
        print("PainkillerPills:", cp_sat_result["variables"]["PainkillerPills"])
        print("SleepingPills:", cp_sat_result["variables"]["SleepingPills"])
        print("Objective (Total Digestive Medicine):", cp_sat_result["objective"])

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
---- Linear Solver (CBC Mixed Integer Programming) Result ----
PainkillerPills: 50.0
SleepingPills: 117.0
Objective (Total Digestive Medicine): 735.0

---- CP-SAT Solver Result ----
PainkillerPills: 50
SleepingPills: 117
Objective (Total Digestive Medicine): 735.0
'''

'''Expected Output:
Expected solution

: {'variables': {'PainkillerPills': 50.0, 'SleepingPills': 116.66666666666663}, 'objective': 733.3333333333331}'''

