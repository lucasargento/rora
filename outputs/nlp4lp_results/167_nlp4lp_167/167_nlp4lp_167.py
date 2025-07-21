# Problem Description:
'''Problem description: A magic school sends letters to student either by carrier pigeons or owls. A carrier pigeon can carry two letters at a time and requires 3 treats for service. An owl can carry 5 letters at a time and requires 5 treats for service.  At most 40% of the birds can be owls. In addition, the school only has 1000 treats available and at least 20 carrier pigeons must be uses. How many of each bird can be used to maximize the total number of letters that can be sent.

Expected Output Schema:
{
  "variables": {
    "NumPigeons": "float",
    "NumOwls": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- BIRDS: set of bird types = {CarrierPigeon, Owl}

Parameters:
- LettersPerPigeon: number of letters carried per carrier pigeon = 2 [letters/bird]
- LettersPerOwl: number of letters carried per owl = 5 [letters/bird]
- TreatsPerPigeon: treats required for one carrier pigeon service = 3 [treats/bird]
- TreatsPerOwl: treats required for one owl service = 5 [treats/bird]
- MaxTreats: total treats available = 1000 [treats]
- MaxOwlRatio: maximum fraction of birds that can be owls = 0.40 [fraction]
- MinPigeons: minimum number of carrier pigeons required = 20 [birds]

Variables:
- NumPigeons: number of carrier pigeons to use; integer variable, NumPigeons ≥ 0
- NumOwls: number of owls to use; integer variable, NumOwls ≥ 0

Objective:
- Maximize TotalLettersSent = LettersPerPigeon * NumPigeons + LettersPerOwl * NumOwls
  (This represents the total number of letters that can be sent.)

Constraints:
1. Treats constraint: TreatsPerPigeon * NumPigeons + TreatsPerOwl * NumOwls ≤ MaxTreats  
   (Ensures total treats consumed by both types of birds do not exceed available treats.)
2. Owl ratio constraint: NumOwls ≤ MaxOwlRatio * (NumPigeons + NumOwls)  
   (Ensures that at most 40% of the birds are owls.)
   - This constraint can be algebraically rearranged if needed as: NumOwls ≤ (MaxOwlRatio / (1 - MaxOwlRatio)) * NumPigeons.
   - With MaxOwlRatio = 0.40, it becomes: NumOwls ≤ (0.40/0.60)*NumPigeons = (2/3)*NumPigeons.
3. Minimum carrier pigeons constraint: NumPigeons ≥ MinPigeons  
   (Guarantees that at least 20 carrier pigeons are used.)

---

Expected Output Schema:
{
  "variables": {
    "NumPigeons": "integer >= 20",
    "NumOwls": "integer >= 0"
  },
  "objective": "Maximize TotalLettersSent = 2*NumPigeons + 5*NumOwls"
}'''

# Generated Code:
from ortools.linear_solver import pywraplp

def solve_version1():
    # Version 1: Owl ratio constraint as NumOwls <= 0.40*(NumPigeons+NumOwls)
    # This formulation is implemented as 0.60*NumOwls - 0.40*NumPigeons <= 0, which is equivalent.
    
    # Create the solver using CBC backend.
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        return None

    # Parameters
    LettersPerPigeon = 2
    LettersPerOwl = 5
    TreatsPerPigeon = 3
    TreatsPerOwl = 5
    MaxTreats = 1000
    MaxOwlRatio = 0.40
    MinPigeons = 20

    # Decision Variables: Both are integers.
    NumPigeons = solver.IntVar(MinPigeons, solver.infinity(), 'NumPigeons')
    NumOwls = solver.IntVar(0, solver.infinity(), 'NumOwls')

    # Constraint 1: Treats constraint.
    solver.Add(TreatsPerPigeon * NumPigeons + TreatsPerOwl * NumOwls <= MaxTreats)

    # Constraint 2: Owl ratio constraint (version1)
    # Original formulation: NumOwls <= 0.40 * (NumPigeons + NumOwls)
    # Rearranging: NumOwls - 0.40*NumOwls <= 0.40*NumPigeons  --> 0.60*NumOwls <= 0.40*NumPigeons
    # Which can be added as follows:
    solver.Add(0.60 * NumOwls - 0.40 * NumPigeons <= 0)

    # Objective: Maximize total letters sent = 2*NumPigeons + 5*NumOwls
    objective = solver.Objective()
    objective.SetCoefficient(NumPigeons, LettersPerPigeon)
    objective.SetCoefficient(NumOwls, LettersPerOwl)
    objective.SetMaximization()

    status = solver.Solve()

    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result['NumPigeons'] = NumPigeons.solution_value()
        result['NumOwls'] = NumOwls.solution_value()
        result['TotalLettersSent'] = objective.Value()
    else:
        result['error'] = 'No optimal solution found in Version 1.'
    return result

def solve_version2():
    # Version 2: Owl ratio constraint as NumOwls <= (2/3)*NumPigeons (simplified version)
    
    # Create the solver using CBC backend.
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        return None

    # Parameters
    LettersPerPigeon = 2
    LettersPerOwl = 5
    TreatsPerPigeon = 3
    TreatsPerOwl = 5
    MaxTreats = 1000
    MinPigeons = 20

    # Decision Variables: Both are integers.
    NumPigeons = solver.IntVar(MinPigeons, solver.infinity(), 'NumPigeons')
    NumOwls = solver.IntVar(0, solver.infinity(), 'NumOwls')

    # Constraint 1: Treats constraint.
    solver.Add(TreatsPerPigeon * NumPigeons + TreatsPerOwl * NumOwls <= MaxTreats)

    # Constraint 2: Owl ratio constraint (version2)
    # Simplified formulation: NumOwls <= (2/3) * NumPigeons, implemented as: 3 * NumOwls <= 2 * NumPigeons.
    solver.Add(3 * NumOwls <= 2 * NumPigeons)

    # Objective: Maximize total letters sent = 2*NumPigeons + 5*NumOwls
    objective = solver.Objective()
    objective.SetCoefficient(NumPigeons, LettersPerPigeon)
    objective.SetCoefficient(NumOwls, LettersPerOwl)
    objective.SetMaximization()

    status = solver.Solve()

    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result['NumPigeons'] = NumPigeons.solution_value()
        result['NumOwls'] = NumOwls.solution_value()
        result['TotalLettersSent'] = objective.Value()
    else:
        result['error'] = 'No optimal solution found in Version 2.'
    return result

def main():
    print("Results for Optimization Problem (Magic School Letters):\n")

    result_v1 = solve_version1()
    result_v2 = solve_version2()

    print("Version 1 (Owl ratio as NumOwls <= 0.40*(NumPigeons+NumOwls)):")
    if 'error' in result_v1:
        print(result_v1['error'])
    else:
        print("  NumPigeons =", result_v1['NumPigeons'])
        print("  NumOwls    =", result_v1['NumOwls'])
        print("  Total Letters Sent =", result_v1['TotalLettersSent'])
    
    print("\nVersion 2 (Owl ratio as NumOwls <= (2/3)*NumPigeons):")
    if 'error' in result_v2:
        print(result_v2['error'])
    else:
        print("  NumPigeons =", result_v2['NumPigeons'])
        print("  NumOwls    =", result_v2['NumOwls'])
        print("  Total Letters Sent =", result_v2['TotalLettersSent'])

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Results for Optimization Problem (Magic School Letters):

Version 1 (Owl ratio as NumOwls <= 0.40*(NumPigeons+NumOwls)):
  NumPigeons = 158.0
  NumOwls    = 105.0
  Total Letters Sent = 841.0

Version 2 (Owl ratio as NumOwls <= (2/3)*NumPigeons):
  NumPigeons = 158.0
  NumOwls    = 105.0
  Total Letters Sent = 841.0
'''

'''Expected Output:
Expected solution

: {'variables': {'NumPigeons': 158.0, 'NumOwls': 105.0}, 'objective': 841.0}'''

