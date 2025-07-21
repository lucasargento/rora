# Problem Description:
'''Problem description: A dentist has 3000 units of resin to fill cavities in both molars and canines. Molars require 20 units of resin and 3 units of pain killer. Canines require 15 units of resin and 2.3 units of pain killer. Since this dentist sees more cavities in canines, at least 60% of cavities filled must be in canines. In addition, the dentist must reserve materials to fill at least 45 molars. How many of each type of teeth should the dentist schedule to fill to minimize the amount of pain killer needed?

Expected Output Schema:
{
  "variables": {
    "NumberMolars": "float",
    "NumberCanines": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Below is the complete mathematical optimization model using the five-element structure.

--------------------------------------------------

Sets:
- T: set of tooth types = {Molars, Canines}

Parameters:
- resin_total = 3000 (total resin available, in resin units)
- resin_per_molar = 20 (resin required per molar, in resin units)
- resin_per_canine = 15 (resin required per canine, in resin units)
- painkiller_per_molar = 3 (pain killer required per molar, in pain killer units)
- painkiller_per_canine = 2.3 (pain killer required per canine, in pain killer units)
- min_molars = 45 (minimum number of molar fillings to schedule)
- min_canine_ratio = 0.6 (at least 60% of all cavities must be canines)

Variables:
- NumberMolars: number of molars to fill [float ≥ 0]
- NumberCanines: number of canines to fill [float ≥ 0]

Objective:
- Minimize total pain killer usage = (painkiller_per_molar * NumberMolars) + (painkiller_per_canine * NumberCanines)

Constraints:
1. Resin constraint:
   - resin_per_molar * NumberMolars + resin_per_canine * NumberCanines ≤ resin_total
   - (20 * NumberMolars) + (15 * NumberCanines) ≤ 3000

2. Canine ratio constraint (at least 60% of all filled teeth must be canines):
   - NumberCanines ≥ min_canine_ratio * (NumberMolars + NumberCanines)
   - This can be rearranged to: NumberCanines ≥ 1.5 * NumberMolars

3. Minimum molars constraint:
   - NumberMolars ≥ min_molars
   - NumberMolars ≥ 45

--------------------------------------------------

The expected output in the prescribed schema is:

{
  "variables": {
    "NumberMolars": "float",
    "NumberCanines": "float"
  },
  "objective": "minimize (3 * NumberMolars) + (2.3 * NumberCanines)"
}

Notes:
- The decision variables are defined as floats for ease of modeling. In practical scheduling, these may need to be integers.
- The unit of resin is assumed consistent across the parameters. Similarly, the pain killer units are assumed to be uniform.
- The canine ratio constraint has been reformulated from the statement “at least 60% of cavities filled must be in canines” to: NumberCanines ≥ 1.5 * NumberMolars.
- The structure above is self-contained and clear for straightforward translation into Python or OR-Tools code.'''

# Generated Code:
from ortools.linear_solver import pywraplp

def solve_linear_program():
    # Create the linear solver with the GLOP backend for continuous problems.
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Solver not created.")
        return None
    infinity = solver.infinity()

    # Decision Variables:
    # NumberMolars: number of molars to fill, lower bound is 45 (minimum molars constraint)
    NumberMolars = solver.NumVar(45, infinity, "NumberMolars")
    # NumberCanines: number of canines to fill, lower bound is 0
    NumberCanines = solver.NumVar(0, infinity, "NumberCanines")

    # Constraints:

    # 1. Resin constraint:
    #   20 * NumberMolars + 15 * NumberCanines ≤ 3000
    solver.Add(20 * NumberMolars + 15 * NumberCanines <= 3000)

    # 2. Canine ratio constraint:
    #   NumberCanines ≥ 1.5 * NumberMolars  (reformulated from "at least 60% must be canines")
    solver.Add(NumberCanines >= 1.5 * NumberMolars)

    # Objective:
    # Minimize total pain killer usage: 3 * NumberMolars + 2.3 * NumberCanines
    solver.Minimize(3 * NumberMolars + 2.3 * NumberCanines)

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        # Return a dictionary with the decision variables and the objective value.
        return {
            "NumberMolars": NumberMolars.solution_value(),
            "NumberCanines": NumberCanines.solution_value(),
            "Objective": solver.Objective().Value()
        }
    else:
        return None

def main():
    # Since only a single formulation is provided, we solve one model.
    solution_lp = solve_linear_program()

    print("Optimization Results:")
    if solution_lp is not None:
        print("Linear Programming Model:")
        print("  NumberMolars   =", solution_lp["NumberMolars"])
        print("  NumberCanines  =", solution_lp["NumberCanines"])
        print("  Objective (minimized pain killer usage) =", solution_lp["Objective"])
    else:
        print("No feasible solution found for the linear programming model.")

if __name__ == "__main__":
    main()

'''Execution Results:
SUCCESS:
Optimization Results:
Linear Programming Model:
  NumberMolars   = 45.0
  NumberCanines  = 67.5
  Objective (minimized pain killer usage) = 290.25
'''

'''Expected Output:
Expected solution

: {'variables': {'NumberMolars': 45.0, 'NumberCanines': 68.0}, 'objective': 291.4}'''

