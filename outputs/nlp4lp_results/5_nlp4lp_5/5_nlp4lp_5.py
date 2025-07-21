# Problem Description:
'''Problem description: A chair produced by Elm Furniture yields a profit of $43, while every dresser yields a $52 profit. Each week, 17 gallons of stain and 11 lengths of oak wood are available. Each chair requires 1.4 gallons of stain and 2 lengths of oak wood, while each dresser requires 1.1 gallons of stain and 3 lengths of oak wood. Determine the maximum profit.

Expected Output Schema:
{
  "variables": {
    "NumberOfChairs": "float",
    "NumberOfDressers": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Below is the complete five‐element model for the Elm Furniture production problem.

------------------------------------------------------------
Sets:
- P: set of products = {Chair, Dresser}

------------------------------------------------------------
Parameters:
- profit_Chair: profit per chair produced [$ per chair] = 43
- profit_Dresser: profit per dresser produced [$ per dresser] = 52
- stain_available: total gallons of stain available per week [gallons] = 17
- oak_available: total lengths of oak wood available per week [lengths] = 11
- stain_required_Chair: gallons of stain required per chair [gallons/chair] = 1.4
- stain_required_Dresser: gallons of stain required per dresser [gallons/dresser] = 1.1
- oak_required_Chair: lengths of oak wood required per chair [lengths/chair] = 2
- oak_required_Dresser: lengths of oak wood required per dresser [lengths/dresser] = 3

------------------------------------------------------------
Variables:
- NumberOfChairs: number of chairs to produce [nonnegative continuous, measured in units]
- NumberOfDressers: number of dressers to produce [nonnegative continuous, measured in units]

------------------------------------------------------------
Objective:
- Maximize Total Profit = (profit_Chair * NumberOfChairs) + (profit_Dresser * NumberOfDressers)

------------------------------------------------------------
Constraints:
1. Stain Constraint: (stain_required_Chair * NumberOfChairs) + (stain_required_Dresser * NumberOfDressers) ≤ stain_available  
   (This ensures the weekly consumption of stain does not exceed 17 gallons.)

2. Oak Wood Constraint: (oak_required_Chair * NumberOfChairs) + (oak_required_Dresser * NumberOfDressers) ≤ oak_available  
   (This ensures the weekly consumption of oak wood does not exceed 11 lengths.)

------------------------------------------------------------
Note:
- We assume that the production quantities can be fractional (as indicated by “float” in the expected output). If only whole units are feasible, then NumberOfChairs and NumberOfDressers should be declared as integers.
- All units have been consistently assigned based on the problem description.

------------------------------------------------------------
Expected Output Schema:
{
  "variables": {
    "NumberOfChairs": "float",
    "NumberOfDressers": "float"
  },
  "objective": "float"
}'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_continuous_model():
    # Create a linear solver with the GLOP backend (for continuous variables)
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Could not create solver for continuous model.")
        return None

    # Parameters
    profit_chair = 43
    profit_dresser = 52
    stain_available = 17
    oak_available = 11
    stain_required_chair = 1.4
    stain_required_dresser = 1.1
    oak_required_chair = 2
    oak_required_dresser = 3

    # Variables: continuous production (can be fractional)
    NumberOfChairs = solver.NumVar(0.0, solver.infinity(), 'NumberOfChairs')
    NumberOfDressers = solver.NumVar(0.0, solver.infinity(), 'NumberOfDressers')

    # Constraints
    # Stain constraint: 1.4 * NumberOfChairs + 1.1 * NumberOfDressers <= 17
    solver.Add(stain_required_chair * NumberOfChairs + stain_required_dresser * NumberOfDressers <= stain_available)
    # Oak wood constraint: 2 * NumberOfChairs + 3 * NumberOfDressers <= 11
    solver.Add(oak_required_chair * NumberOfChairs + oak_required_dresser * NumberOfDressers <= oak_available)

    # Objective: Maximize profit = 43 * NumberOfChairs + 52 * NumberOfDressers
    objective = solver.Objective()
    objective.SetCoefficient(NumberOfChairs, profit_chair)
    objective.SetCoefficient(NumberOfDressers, profit_dresser)
    objective.SetMaximization()

    # Solve
    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL:
        solution = {
            "NumberOfChairs": NumberOfChairs.solution_value(),
            "NumberOfDressers": NumberOfDressers.solution_value(),
            "objective": objective.Value()
        }
        return solution
    else:
        print("The continuous model does not have an optimal solution.")
        return None

def solve_integer_model():
    # Create a linear solver with the CBC_MIXED_INTEGER_PROGRAMMING backend (for integers)
    solver = pywraplp.Solver.CreateSolver('CBC_MIXED_INTEGER_PROGRAMMING')
    if not solver:
        print("Could not create solver for integer model.")
        return None

    # Parameters
    profit_chair = 43
    profit_dresser = 52
    stain_available = 17
    oak_available = 11
    stain_required_chair = 1.4
    stain_required_dresser = 1.1
    oak_required_chair = 2
    oak_required_dresser = 3

    # Variables: integer production (whole units only)
    NumberOfChairs = solver.IntVar(0, solver.infinity(), 'NumberOfChairs')
    NumberOfDressers = solver.IntVar(0, solver.infinity(), 'NumberOfDressers')

    # Constraints
    # Stain constraint: 1.4 * NumberOfChairs + 1.1 * NumberOfDressers <= 17
    solver.Add(stain_required_chair * NumberOfChairs + stain_required_dresser * NumberOfDressers <= stain_available)
    # Oak wood constraint: 2 * NumberOfChairs + 3 * NumberOfDressers <= oak_available
    solver.Add(oak_required_chair * NumberOfChairs + oak_required_dresser * NumberOfDressers <= oak_available)

    # Objective: Maximize profit = 43 * NumberOfChairs + 52 * NumberOfDressers
    objective = solver.Objective()
    objective.SetCoefficient(NumberOfChairs, profit_chair)
    objective.SetCoefficient(NumberOfDressers, profit_dresser)
    objective.SetMaximization()

    # Solve
    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL:
        solution = {
            "NumberOfChairs": NumberOfChairs.solution_value(),
            "NumberOfDressers": NumberOfDressers.solution_value(),
            "objective": objective.Value()
        }
        return solution
    else:
        print("The integer model does not have an optimal solution.")
        return None

def main():
    print("Solving Elm Furniture Production Problem\n")
    
    print("Continuous Model (Fractional Production Allowed):")
    continuous_solution = solve_continuous_model()
    if continuous_solution:
        print(continuous_solution)
    else:
        print("No optimal solution found for the continuous model.")
    
    print("\nInteger Model (Whole Units Production):")
    integer_solution = solve_integer_model()
    if integer_solution:
        print(integer_solution)
    else:
        print("No optimal solution found for the integer model.")

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Solving Elm Furniture Production Problem

Continuous Model (Fractional Production Allowed):
{'NumberOfChairs': 5.5, 'NumberOfDressers': 0.0, 'objective': 236.5}

Integer Model (Whole Units Production):
{'NumberOfChairs': 4.0, 'NumberOfDressers': 1.0, 'objective': 224.0}
'''

'''Expected Output:
Expected solution

: {'variables': {'NumberOfChairs': 4.0, 'NumberOfDressers': 1.0}, 'objective': 224.0}'''

