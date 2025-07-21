# Problem Description:
'''Problem description: A small chocolate shop makes milk chocolate and dark chocolate bars. Milk chocolate bars require 4 units of cocoa and 7 units of milk. Dark chocolate bars require 6 units of cocoa and 3 units of milk. The shop has 2000 units of cocoa and 1750 units of milk available. In addition since milk chocolate sells better, at least 2 times as many milk chocolate bars need to be made as dark chocolate bars.  If making a milk chocolate bar takes 15 minutes and making a dark chocolate bar takes 12 mins, how many of each should the make to minimize total production time?

Expected Output Schema:
{
  "variables": {
    "MilkBars": "float",
    "DarkBars": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Below is a complete and unambiguous mathematical model using the five-element structure.

--------------------------------------------------
Sets:
- P: set of chocolate bar types = {Milk, Dark}

--------------------------------------------------
Parameters:
- Cocoa_per_Milk: cocoa units required per milk chocolate bar = 4 [units/bar]
- Cocoa_per_Dark: cocoa units required per dark chocolate bar = 6 [units/bar]
- Milk_per_Milk: milk units required per milk chocolate bar = 7 [units/bar]
- Milk_per_Dark: milk units required per dark chocolate bar = 3 [units/bar]
- Total_Cocoa: total available cocoa = 2000 [units]
- Total_Milk: total available milk = 1750 [units]
- Time_Milk: production time per milk chocolate bar = 15 [minutes/bar]
- Time_Dark: production time per dark chocolate bar = 12 [minutes/bar]
- Ratio_Min: minimum ratio of milk chocolate bars to dark chocolate bars = 2 [milk bars per dark bar]

--------------------------------------------------
Variables:
- MilkBars: number of milk chocolate bars produced [nonnegative integer; units: bars]
- DarkBars: number of dark chocolate bars produced [nonnegative integer; units: bars]

--------------------------------------------------
Objective:
- Minimize total production time = (Time_Milk * MilkBars) + (Time_Dark * DarkBars)
  which translates to: Minimize 15 * MilkBars + 12 * DarkBars [minutes]

--------------------------------------------------
Constraints:
1. Cocoa availability constraint:
   4 * MilkBars + 6 * DarkBars ≤ 2000
   (Total cocoa used by both types cannot exceed available cocoa.)

2. Milk availability constraint:
   7 * MilkBars + 3 * DarkBars ≤ 1750
   (Total milk used by both types cannot exceed available milk.)

3. Production ratio constraint:
   MilkBars ≥ 2 * DarkBars
   (At least two milk chocolate bars must be produced for every dark chocolate bar.)

--------------------------------------------------

Additional Comments:
- All units are clearly stated in the parameter definitions.
- Decision variables are assumed to be integers since they represent countable bars. However, if divisibility is acceptable (or for relaxation purposes), they may be treated as continuous nonnegative variables.
- The model is self-contained and avoids duplications by directly referencing parameters in constraints and the objective.
- This complete formulation can be directly mapped to code using Python or OR-Tools.

--------------------------------------------------

Expected Output Schema:
{
  "variables": {
    "MilkBars": "float",
    "DarkBars": "float"
  },
  "objective": "float"
}'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_integer():
    # Create the solver using the CBC Mixed Integer Programming solver.
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Integer solver not available.")
        return None

    # Decision Variables: integer version. 
    MilkBars = solver.IntVar(0, solver.infinity(), 'MilkBars')
    DarkBars = solver.IntVar(0, solver.infinity(), 'DarkBars')

    # Parameters
    Cocoa_per_Milk = 4
    Cocoa_per_Dark = 6
    Milk_per_Milk = 7
    Milk_per_Dark = 3
    Total_Cocoa = 2000
    Total_Milk = 1750
    Time_Milk = 15
    Time_Dark = 12
    Ratio_Min = 2

    # Constraints
    # 1. Cocoa constraint: 4 * MilkBars + 6 * DarkBars <= 2000
    solver.Add(Cocoa_per_Milk * MilkBars + Cocoa_per_Dark * DarkBars <= Total_Cocoa)
    # 2. Milk constraint: 7 * MilkBars + 3 * DarkBars <= 1750
    solver.Add(Milk_per_Milk * MilkBars + Milk_per_Dark * DarkBars <= Total_Milk)
    # 3. Production ratio constraint: MilkBars >= 2 * DarkBars
    solver.Add(MilkBars >= Ratio_Min * DarkBars)

    # Objective: Minimize production time = 15 * MilkBars + 12 * DarkBars
    objective = solver.Objective()
    objective.SetCoefficient(MilkBars, Time_Milk)
    objective.SetCoefficient(DarkBars, Time_Dark)
    objective.SetMinimization()

    # Solve the problem and return the solution if found
    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL:
        solution = {
            "MilkBars": MilkBars.solution_value(),
            "DarkBars": DarkBars.solution_value(),
            "objective": objective.Value(),
        }
        return solution
    else:
        print("No optimal solution found for integer formulation.")
        return None

def solve_continuous():
    # Create the solver for continuous variables
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Continuous solver not available.")
        return None

    # Decision Variables: continuous version.
    MilkBars = solver.NumVar(0.0, solver.infinity(), 'MilkBars')
    DarkBars = solver.NumVar(0.0, solver.infinity(), 'DarkBars')

    # Parameters
    Cocoa_per_Milk = 4.0
    Cocoa_per_Dark = 6.0
    Milk_per_Milk = 7.0
    Milk_per_Dark = 3.0
    Total_Cocoa = 2000.0
    Total_Milk = 1750.0
    Time_Milk = 15.0
    Time_Dark = 12.0
    Ratio_Min = 2.0

    # Constraints
    # 1. Cocoa constraint: 4 * MilkBars + 6 * DarkBars <= 2000
    solver.Add(Cocoa_per_Milk * MilkBars + Cocoa_per_Dark * DarkBars <= Total_Cocoa)
    # 2. Milk constraint: 7 * MilkBars + 3 * DarkBars <= 1750
    solver.Add(Milk_per_Milk * MilkBars + Milk_per_Dark * DarkBars <= Total_Milk)
    # 3. Production ratio constraint: MilkBars >= 2 * DarkBars
    solver.Add(MilkBars >= Ratio_Min * DarkBars)

    # Objective: Minimize production time: 15 * MilkBars + 12 * DarkBars
    objective = solver.Objective()
    objective.SetCoefficient(MilkBars, Time_Milk)
    objective.SetCoefficient(DarkBars, Time_Dark)
    objective.SetMinimization()

    # Solve the problem and return the solution if found
    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL:
        solution = {
            "MilkBars": MilkBars.solution_value(),
            "DarkBars": DarkBars.solution_value(),
            "objective": objective.Value(),
        }
        return solution
    else:
        print("No optimal solution found for continuous formulation.")
        return None

def main():
    print("Integer Formulation Solution:")
    int_solution = solve_integer()
    if int_solution is not None:
        print(int_solution)
    else:
        print("Integer formulation did not find an optimal solution.")

    print("\nContinuous Formulation Solution:")
    cont_solution = solve_continuous()
    if cont_solution is not None:
        print(cont_solution)
    else:
        print("Continuous formulation did not find an optimal solution.")

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Integer Formulation Solution:
{'MilkBars': 0.0, 'DarkBars': 0.0, 'objective': 0.0}

Continuous Formulation Solution:
{'MilkBars': 0.0, 'DarkBars': 0.0, 'objective': 0.0}
'''

'''Expected Output:
Expected solution

: {'variables': {'MilkBars': -0.0, 'DarkBars': -0.0}, 'objective': 0.0}'''

