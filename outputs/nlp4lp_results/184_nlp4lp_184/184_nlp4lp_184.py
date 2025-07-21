# Problem Description:
'''Problem description: A man takes two supplements to get his daily iron and calcium requirements. A pill of supplement A has 5 units of iron and 10 units of calcium. A pill of supplement B contains 4 units of iron and 15 units of calcium.  The man needs a minimum of 40 units of iron and 50 units of calcium per day. If the cost per pill of supplement A is $2 and the cost per pill of supplement B is  $3, how many of each should he buy to minimize costs?

Expected Output Schema:
{
  "variables": {
    "NumPillsSupplement": {
      "0": "float",
      "1": "float"
    }
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- S: the set of supplements = {A, B}

Parameters:
- iron_in_pill: iron content per pill for each supplement, where iron_in_pill[A] = 5 (units of iron per pill of A) and iron_in_pill[B] = 4 (units of iron per pill of B)
- calcium_in_pill: calcium content per pill for each supplement, where calcium_in_pill[A] = 10 (units of calcium per pill of A) and calcium_in_pill[B] = 15 (units of calcium per pill of B)
- cost_per_pill: cost for each supplement, where cost_per_pill[A] = 2 (dollars per pill of A) and cost_per_pill[B] = 3 (dollars per pill of B)
- required_iron: minimum daily iron requirement = 40 (units)
- required_calcium: minimum daily calcium requirement = 50 (units)

Variables:
- NumPillsSupplement[p] for each p in S where:
  • NumPillsSupplement[A] (number of pills of supplement A) is an integer ≥ 0 (or continuous non-negative if integer integrality is relaxed)
  • NumPillsSupplement[B] (number of pills of supplement B) is an integer ≥ 0 (or continuous non-negative if integer integrality is relaxed)

Objective:
- Minimize total_cost = cost_per_pill[A] * NumPillsSupplement[A] + cost_per_pill[B] * NumPillsSupplement[B]

Constraints:
1. Iron requirement constraint:
   • iron_in_pill[A] * NumPillsSupplement[A] + iron_in_pill[B] * NumPillsSupplement[B] ≥ required_iron
   • That is, 5 * NumPillsSupplement[A] + 4 * NumPillsSupplement[B] ≥ 40

2. Calcium requirement constraint:
   • calcium_in_pill[A] * NumPillsSupplement[A] + calcium_in_pill[B] * NumPillsSupplement[B] ≥ required_calcium
   • That is, 10 * NumPillsSupplement[A] + 15 * NumPillsSupplement[B] ≥ 50

--------------------------------------------------------------------------------
Expected Output Schema (as a JSON-like structure):
{
  "variables": {
    "NumPillsSupplement": {
      "A": "integer ≥ 0",
      "B": "integer ≥ 0"
    }
  },
  "objective": "total_cost (minimize): 2 * NumPillsSupplement[A] + 3 * NumPillsSupplement[B]"
}'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_linear_program():
    # Create the solver using the CBC backend.
    solver = pywraplp.Solver.CreateSolver('CBC_MIXED_INTEGER_PROGRAMMING')
    if not solver:
        print("Solver not created.")
        return None

    # Data: parameters for the supplements problem.
    required_iron = 40
    required_calcium = 50

    # Supplement A: iron=5, calcium=10, cost =2
    # Supplement B: iron=4, calcium=15, cost =3

    # Variables: number of pills for each supplement, integer >= 0.
    numA = solver.IntVar(0, solver.infinity(), 'NumPills_A')
    numB = solver.IntVar(0, solver.infinity(), 'NumPills_B')

    # Constraint 1: Iron requirement -> 5 * numA + 4 * numB >= 40
    solver.Add(5 * numA + 4 * numB >= required_iron)

    # Constraint 2: Calcium requirement -> 10 * numA + 15 * numB >= 50
    solver.Add(10 * numA + 15 * numB >= required_calcium)

    # Objective: minimize total cost = 2 * numA + 3 * numB
    solver.Minimize(2 * numA + 3 * numB)

    status = solver.Solve()
    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result['variables'] = {
            "NumPillsSupplement": {
                "A": int(numA.solution_value()),
                "B": int(numB.solution_value())
            }
        }
        result['objective'] = solver.Objective().Value()
        print("----- OR-Tools Linear Solver (CBC_MIXED_INTEGER_PROGRAMMING) Solution -----")
        print("Number of pills supplement A:", int(numA.solution_value()))
        print("Number of pills supplement B:", int(numB.solution_value()))
        print("Minimum cost:", solver.Objective().Value())
    elif status == pywraplp.Solver.INFEASIBLE:
        print("The problem is infeasible.")
    else:
        print("The solver did not find an optimal solution.")

    return result

def main():
    print("Running optimization for the supplements problem...\n")
    result = solve_linear_program()
    if result:
        # Print result in the expected JSON-like structure.
        print("\nExpected Output Schema:")
        print("{")
        print('  "variables": {')
        print('    "NumPillsSupplement": {')
        print('      "A": "integer ≥ 0",')
        print('      "B": "integer ≥ 0"')
        print("    }")
        print("  },")
        print('  "objective": "total_cost (minimize): 2 * NumPillsSupplement[A] + 3 * NumPillsSupplement[B]"')
        print("}")
    
if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Running optimization for the supplements problem...

----- OR-Tools Linear Solver (CBC_MIXED_INTEGER_PROGRAMMING) Solution -----
Number of pills supplement A: 8
Number of pills supplement B: 0
Minimum cost: 16.0

Expected Output Schema:
{
  "variables": {
    "NumPillsSupplement": {
      "A": "integer ≥ 0",
      "B": "integer ≥ 0"
    }
  },
  "objective": "total_cost (minimize): 2 * NumPillsSupplement[A] + 3 * NumPillsSupplement[B]"
}
'''

'''Expected Output:
Expected solution

: {'variables': {'NumPillsSupplement': {'0': 8.0, '1': 0.0}}, 'objective': 16.0}'''

