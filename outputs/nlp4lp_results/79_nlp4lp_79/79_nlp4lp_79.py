# Problem Description:
'''Problem description: A candy company is making peach flavored candy and cherry flavored candy. Each pack of peach flavored candy requires 3 units of peach flavoring and 5 units of special syrup. Each pack of cherry flavored candy requires 5 units of cherry flavoring and 4 units of special syrup. The company has available 3000 units of peach flavoring and 4000 units of cherry flavoring. Peach candy is much more popular and thus the number of peach candy packs must be larger than the number of cherry candy packs. In addition, at least 30% of the pack must be cherry flavored. How many of each should be made to minimize the total amount of special syrup used?

Expected Output Schema:
{
  "variables": {
    "NumberOfPeachPacks": "float",
    "NumberOfCherryPacks": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Below is the complete formulation following the five‐element structure.

---------------------------------------------------------
Sets:
- CandyTypes: {Peach, Cherry}

---------------------------------------------------------
Parameters:
- peach_flavor_per_pack (Peach candy): 3 units per pack
- cherry_flavor_per_pack (Cherry candy): 5 units per pack
- syrup_per_pack_peach (Peach candy): 5 units per pack
- syrup_per_pack_cherry (Cherry candy): 4 units per pack
- available_peach_flavor: 3000 units  
- available_cherry_flavor: 4000 units  
- cherry_min_share: 0.30    (minimum share of total packs that must be cherry)

Notes on units: All “units” are assumed to be consistent (e.g., units of flavoring or syrup per pack).

---------------------------------------------------------
Variables:
- NumberOfPeachPacks: number of peach flavored candy packs produced (nonnegative integer; can be modeled as integer or continuous if approximations are acceptable)
- NumberOfCherryPacks: number of cherry flavored candy packs produced (nonnegative integer; similarly, integer or continuous)

---------------------------------------------------------
Objective:
Minimize TotalSyrupUsed, where
  TotalSyrupUsed = syrup_per_pack_peach * NumberOfPeachPacks + syrup_per_pack_cherry * NumberOfCherryPacks

In other words, minimize 5 * NumberOfPeachPacks + 4 * NumberOfCherryPacks

---------------------------------------------------------
Constraints:
1. Peach flavoring availability:  
   peach_flavor_per_pack * NumberOfPeachPacks <= available_peach_flavor  
   i.e., 3 * NumberOfPeachPacks <= 3000

2. Cherry flavoring availability:  
   cherry_flavor_per_pack * NumberOfCherryPacks <= available_cherry_flavor  
   i.e., 5 * NumberOfCherryPacks <= 4000

3. Popularity constraint (peach candy is much more popular):  
   NumberOfPeachPacks > NumberOfCherryPacks

4. Composition constraint (at least 30% of the total packs must be cherry flavored):  
   NumberOfCherryPacks >= cherry_min_share * (NumberOfPeachPacks + NumberOfCherryPacks)  
   This can be rearranged as:  
   NumberOfPeachPacks <= (1/cherry_min_share - 1) * NumberOfCherryPacks  
   Since 1/0.30 - 1 equals 7/3 (approximately 2.333), the inequality becomes:  
   NumberOfPeachPacks <= (7/3) * NumberOfCherryPacks

5. Non-negativity:  
   NumberOfPeachPacks >= 0,  NumberOfCherryPacks >= 0

---------------------------------------------------------
Summary in the Expected Output Schema:

{
  "variables": {
    "NumberOfPeachPacks": "float (nonnegative, ideally integer)",
    "NumberOfCherryPacks": "float (nonnegative, ideally integer)"
  },
  "objective": "Minimize 5 * NumberOfPeachPacks + 4 * NumberOfCherryPacks (minimizes total syrup used)"
}

---------------------------------------------------------
This complete model is ready for implementation in an optimization solver (or as a guideline for an OR-Tools/Python script).'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_candy_problem():
    # Create the MIP solver using the CBC backend.
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Solver not created.")
        return None

    # Variables: number of packs produced for peach and cherry.
    # They are nonnegative integers.
    peach = solver.IntVar(0, solver.infinity(), 'NumberOfPeachPacks')
    cherry = solver.IntVar(0, solver.infinity(), 'NumberOfCherryPacks')

    # Parameters (as provided in the formulation)
    peach_flavor_per_pack = 3   # units per peach candy pack
    cherry_flavor_per_pack = 5  # units per cherry candy pack
    syrup_per_pack_peach = 5    # units of syrup for peach candy pack
    syrup_per_pack_cherry = 4   # units of syrup for cherry candy pack
    available_peach_flavor = 3000
    available_cherry_flavor = 4000
    cherry_min_share = 0.30  # at least 30% of the total packs must be cherry flavored

    # Constraint 1: Peach flavoring availability
    # 3 * NumberOfPeachPacks <= 3000
    solver.Add(peach_flavor_per_pack * peach <= available_peach_flavor)

    # Constraint 2: Cherry flavoring availability
    # 5 * NumberOfCherryPacks <= 4000
    solver.Add(cherry_flavor_per_pack * cherry <= available_cherry_flavor)

    # Constraint 3: Popularity constraint: peach packs must be strictly larger than cherry packs.
    # For integer variables, strict inequality can be modeled as:
    solver.Add(peach >= cherry + 1)

    # Constraint 4: Composition constraint (at least 30% of total packs must be cherry flavored):
    # cherry >= 0.30*(peach + cherry)
    # Rearranged: peach <= (1/cherry_min_share - 1)*cherry.
    # Since 1/0.30 - 1 = 7/3, we use equivalent form:
    # peach <= (7/3)*cherry, to avoid precision issues multiply by 3:
    solver.Add(3 * peach <= 7 * cherry)

    # Objective: minimize total syrup used.
    # TotalSyrupUsed = 5 * NumberOfPeachPacks + 4 * NumberOfCherryPacks
    objective = solver.Objective()
    objective.SetCoefficient(peach, syrup_per_pack_peach)
    objective.SetCoefficient(cherry, syrup_per_pack_cherry)
    objective.SetMinimization()

    # Solve the model.
    status = solver.Solve()

    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result['variables'] = {
            "NumberOfPeachPacks": peach.solution_value(),
            "NumberOfCherryPacks": cherry.solution_value()
        }
        result['objective'] = objective.Value()
        print("Solution for Model 1 (Linear Formulation):")
        print("NumberOfPeachPacks =", peach.solution_value())
        print("NumberOfCherryPacks =", cherry.solution_value())
        print("Optimal Total Syrup Used =", objective.Value())
    else:
        print("The problem does not have an optimal solution.")

    return result

def main():
    # Currently, we have one formulation for the candy production problem.
    result1 = solve_candy_problem()
    
    # If additional formulations were available, they would be implemented as separate functions.
    # Then, call them here and print their results in a structured way.
    if result1 is not None:
        print("\nStructured Output for Model 1:")
        print("{")
        print('  "variables": {')
        print('    "NumberOfPeachPacks": "float (nonnegative, ideally integer)",')
        print('    "NumberOfCherryPacks": "float (nonnegative, ideally integer)"')
        print("  },")
        print('  "objective": "Minimize 5 * NumberOfPeachPacks + 4 * NumberOfCherryPacks (minimizes total syrup used)"')
        print("}")
    
if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Solution for Model 1 (Linear Formulation):
NumberOfPeachPacks = 2.0
NumberOfCherryPacks = 1.0
Optimal Total Syrup Used = 14.0

Structured Output for Model 1:
{
  "variables": {
    "NumberOfPeachPacks": "float (nonnegative, ideally integer)",
    "NumberOfCherryPacks": "float (nonnegative, ideally integer)"
  },
  "objective": "Minimize 5 * NumberOfPeachPacks + 4 * NumberOfCherryPacks (minimizes total syrup used)"
}
'''

'''Expected Output:
Expected solution

: {'variables': {'NumberOfPeachPacks': 0.0, 'NumberOfCherryPacks': 0.0}, 'objective': 0.0}'''

