# Problem Description:
'''Problem description: A student takes calcium pills and vitamin D pills one after the other. Each calcium pill takes 5 minutes to be effective while each vitamin D pill takes 6 minutes to be effective. Over a month, the student must take at least 130 pills of medication and at least 40 should be vitamin D pills because they enhance the absorption of calcium in the body. Since vitamin D is complimentary to calcium, the student must take more calcium pills than vitamin D pills. How many pills of each should the student take to minimize the total time it takes for the medication to be effective?

Expected Output Schema:
{
  "variables": {
    "NumberCalciumPills": "float",
    "NumberVitaminDPills": "float",
    "TotalTime": "float",
    "IsCalciumTaken": "float",
    "IsVitaminDTaken": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Below is one valid formulation of the problem using the five‐element framework. In this formulation we assume that the pill counts are integer decision variables, and we introduce binary indicator variables (IsCalciumTaken and IsVitaminDTaken) to flag whether any pills of the respective type are taken. (A sufficiently large constant M is used to link the pill count and the binary indicator. In practice, M can be chosen to be any number that safely bounds the possible number of pills taken – for instance, 200.) Note that all times are in minutes and counts are whole numbers.

------------------------------------------------------------
Sets:
• P = {Calcium, VitaminD}                    # Pill types

------------------------------------------------------------
Parameters:
• effective_time_p: time (in minutes) for a pill of type p to be effective
  – effective_time_Calcium = 5 minutes
  – effective_time_VitaminD = 6 minutes

• min_total_pills = 130                    # At least 130 pills overall
• min_VitaminD_pills = 40                    # At least 40 vitamin D pills

• M = 200                          # A large constant (upper bound on pills)

------------------------------------------------------------
Variables:
• NumberCalciumPills [nonnegative integer]  # Number of calcium pills taken [pills]
• NumberVitaminDPills [nonnegative integer]  # Number of vitamin D pills taken [pills]
• TotalTime [continuous]                # Total elapsed time for pills to become effective [minutes]

• IsCalciumTaken [binary: 0 or 1]             # 1 if any calcium pill is taken, 0 otherwise
• IsVitaminDTaken [binary: 0 or 1]            # 1 if any vitamin D pill is taken, 0 otherwise

------------------------------------------------------------
Objective:
Minimize TotalTime, where
  TotalTime = (5 * NumberCalciumPills) + (6 * NumberVitaminDPills)
         # Total time in minutes for all pills to become effective

------------------------------------------------------------
Constraints:
1. Total Pill Count Constraint:
  NumberCalciumPills + NumberVitaminDPills ≥ min_total_pills
               # Total number of pills must be at least 130

2. Vitamin D Minimum Constraint:
  NumberVitaminDPills ≥ min_VitaminD_pills
               # At least 40 vitamin D pills must be taken

3. Calcium Dominance Constraint:
  NumberCalciumPills ≥ NumberVitaminDPills + 1
                # More calcium pills than vitamin D pills

4. Linking Binary Variables for Calcium:
  NumberCalciumPills ≤ M * IsCalciumTaken
  NumberCalciumPills ≥ IsCalciumTaken
                # If any calcium pill is taken then IsCalciumTaken = 1

5. Linking Binary Variables for Vitamin D:
  NumberVitaminDPills ≤ M * IsVitaminDTaken
  NumberVitaminDPills ≥ IsVitaminDTaken
                # If any vitamin D pill is taken then IsVitaminDTaken = 1

------------------------------------------------------------
This structured model fully represents the problem where the student minimizes the total effective time by choosing the number of calcium and vitamin D pills, while satisfying the monthly pill count, vitamin D minimum, and the requirement that there are more calcium pills than vitamin D pills.'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp
from ortools.sat.python import cp_model

# Parameters
CALCIUM_EFFECTIVE_TIME = 5    # in minutes
VITAMIND_EFFECTIVE_TIME = 6   # in minutes
MIN_TOTAL_PILLS = 130
MIN_VITAMIND_PILLS = 40
M = 200  # sufficiently large constant

def solve_with_linear_solver():
    # Create the MIP solver with CBC backend.
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Linear solver not found.")
        return None

    # Decision Variables
    NumberCalciumPills = solver.IntVar(0, solver.infinity(), 'NumberCalciumPills')
    NumberVitaminDPills = solver.IntVar(0, solver.infinity(), 'NumberVitaminDPills')
    # Binary indicator variables: 0 or 1.
    IsCalciumTaken = solver.IntVar(0, 1, 'IsCalciumTaken')
    IsVitaminDTaken = solver.IntVar(0, 1, 'IsVitaminDTaken')

    # Total Time: continuous variable.
    TotalTime = solver.NumVar(0, solver.infinity(), 'TotalTime')

    # Objective: Minimize total time = 5*calcium + 6*vitaminD
    solver.Add(TotalTime == CALCIUM_EFFECTIVE_TIME * NumberCalciumPills + VITAMIND_EFFECTIVE_TIME * NumberVitaminDPills)
    solver.Minimize(TotalTime)

    # Constraints:
    # 1. Total Pill Count Constraint: NumberCalciumPills + NumberVitaminDPills >= 130
    solver.Add(NumberCalciumPills + NumberVitaminDPills >= MIN_TOTAL_PILLS)

    # 2. Vitamin D Minimum Constraint: NumberVitaminDPills >= 40
    solver.Add(NumberVitaminDPills >= MIN_VITAMIND_PILLS)

    # 3. Calcium Dominance Constraint: NumberCalciumPills >= NumberVitaminDPills + 1
    solver.Add(NumberCalciumPills >= NumberVitaminDPills + 1)

    # 4. Linking Binary Variables for Calcium:
    solver.Add(NumberCalciumPills <= M * IsCalciumTaken)
    solver.Add(NumberCalciumPills >= IsCalciumTaken)

    # 5. Linking Binary Variables for Vitamin D:
    solver.Add(NumberVitaminDPills <= M * IsVitaminDTaken)
    solver.Add(NumberVitaminDPills >= IsVitaminDTaken)

    status = solver.Solve()

    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "NumberCalciumPills": NumberCalciumPills.solution_value(),
            "NumberVitaminDPills": NumberVitaminDPills.solution_value(),
            "TotalTime": TotalTime.solution_value(),
            "IsCalciumTaken": IsCalciumTaken.solution_value(),
            "IsVitaminDTaken": IsVitaminDTaken.solution_value(),
            "objective": solver.Objective().Value()
        }
    else:
        print("The linear solver did not find an optimal solution.")
    return result

def solve_with_cp_model():
    model = cp_model.CpModel()

    # Decision Variables
    NumberCalciumPills = model.NewIntVar(0, M, 'NumberCalciumPills')
    NumberVitaminDPills = model.NewIntVar(0, M, 'NumberVitaminDPills')
    IsCalciumTaken = model.NewBoolVar('IsCalciumTaken')
    IsVitaminDTaken = model.NewBoolVar('IsVitaminDTaken')

    # We will represent TotalTime as an integer variable.
    # Upper bound can be calculated as worst case: if all pills are vitamin D, time = 6*M.
    TotalTime = model.NewIntVar(0, 6 * M, 'TotalTime')

    # Define TotalTime = 5*NumberCalciumPills + 6*NumberVitaminDPills
    model.Add(TotalTime == CALCIUM_EFFECTIVE_TIME * NumberCalciumPills + VITAMIND_EFFECTIVE_TIME * NumberVitaminDPills)

    # Constraints:
    # 1. Total Pill Count Constraint: NumberCalciumPills + NumberVitaminDPills >= 130
    model.Add(NumberCalciumPills + NumberVitaminDPills >= MIN_TOTAL_PILLS)

    # 2. Vitamin D Minimum Constraint: NumberVitaminDPills >= 40
    model.Add(NumberVitaminDPills >= MIN_VITAMIND_PILLS)

    # 3. Calcium Dominance Constraint: NumberCalciumPills >= NumberVitaminDPills + 1
    model.Add(NumberCalciumPills >= NumberVitaminDPills + 1)

    # 4. Linking Binary Variables for Calcium:
    model.Add(NumberCalciumPills <= M * IsCalciumTaken)
    model.Add(NumberCalciumPills >= IsCalciumTaken)

    # 5. Linking Binary Variables for Vitamin D:
    model.Add(NumberVitaminDPills <= M * IsVitaminDTaken)
    model.Add(NumberVitaminDPills >= IsVitaminDTaken)

    # Objective: Minimize TotalTime
    model.Minimize(TotalTime)

    # Solve the model.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    result = {}
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        result = {
            "NumberCalciumPills": solver.Value(NumberCalciumPills),
            "NumberVitaminDPills": solver.Value(NumberVitaminDPills),
            "TotalTime": solver.Value(TotalTime),
            "IsCalciumTaken": solver.Value(IsCalciumTaken),
            "IsVitaminDTaken": solver.Value(IsVitaminDTaken),
            "objective": solver.ObjectiveValue()
        }
    else:
        print("The CP-SAT solver did not find an optimal solution.")
    return result

def main():
    print("==== Solution using OR-Tools Linear Solver (CBC) ====")
    linear_result = solve_with_linear_solver()
    if linear_result:
        print(linear_result)
    else:
        print("No solution found using the linear solver.")

    print("\n==== Solution using OR-Tools CP-SAT Solver ====")
    cp_result = solve_with_cp_model()
    if cp_result:
        print(cp_result)
    else:
        print("No solution found using the CP-SAT solver.")

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
==== Solution using OR-Tools Linear Solver (CBC) ====
{'NumberCalciumPills': 90.0, 'NumberVitaminDPills': 40.0, 'TotalTime': 690.0, 'IsCalciumTaken': 1.0, 'IsVitaminDTaken': 1.0, 'objective': 690.0}

==== Solution using OR-Tools CP-SAT Solver ====
{'NumberCalciumPills': 90, 'NumberVitaminDPills': 40, 'TotalTime': 690, 'IsCalciumTaken': 1, 'IsVitaminDTaken': 1, 'objective': 690.0}
'''

'''Expected Output:
Expected solution

: {'variables': {'NumberCalciumPills': 2000000000.0, 'NumberVitaminDPills': 40.0, 'TotalTime': 0.0, 'IsCalciumTaken': 1.0, 'IsVitaminDTaken': 1.0}, 'objective': 0.0}'''

