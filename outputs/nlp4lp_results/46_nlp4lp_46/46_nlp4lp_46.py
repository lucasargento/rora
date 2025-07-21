# Problem Description:
'''Problem description: A bubble tea shop sells mango and lychee bubble tea. Each mango bubble tea requires 4 units of mango juice and 8 units of tea. Each lychee bubble tea requires 6 units of lychee juice and 6 units of tea. The shop has available 2000 units of mango juice and 3000 units of lychee juice. At least 40% of the bubble teas made must be lychee flavored. However, mango bubble tea sells better and thus the number of mango bubble teas made must be large than the number of lychee bubble teas made. How many of each bubble tea flavor should be made to minimize the total amount of tea needed?

Expected Output Schema:
{
  "variables": {
    "NumberOfMangoBubbleTeas": "float",
    "NumberOfLycheeBubbleTeas": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- F: set of bubble tea flavors = {Mango, Lychee}

Parameters:
- mangoJuicePerMango: amount of mango juice required per Mango bubble tea [units] = 4
- teaPerMango: amount of tea required per Mango bubble tea [units] = 8
- lycheeJuicePerLychee: amount of lychee juice required per Lychee bubble tea [units] = 6
- teaPerLychee: amount of tea required per Lychee bubble tea [units] = 6
- totalMangoJuice: total available mango juice [units] = 2000
- totalLycheeJuice: total available lychee juice [units] = 3000
- minLycheeFraction: minimum fraction of total bubble teas that must be lychee [fraction] = 0.4
- minMangoExcess: minimum excess of Mango bubble teas over Lychee bubble teas (to enforce Mango > Lychee) [units] = 1  
  (Note: Since strict inequalities cannot be enforced in LPs, we assume Mango count must be at least 1 unit greater than Lychee count.)

Variables:
- NumberOfMangoBubbleTeas (continuous, ≥ 0): number of Mango bubble teas to produce [bubbles]
- NumberOfLycheeBubbleTeas (continuous, ≥ 0): number of Lychee bubble teas to produce [bubbles]

Objective:
- Minimize total tea usage = (teaPerMango * NumberOfMangoBubbleTeas) + (teaPerLychee * NumberOfLycheeBubbleTeas)
  which is: minimize (8 * NumberOfMangoBubbleTeas + 6 * NumberOfLycheeBubbleTeas)

Constraints:
1. Mango Juice Constraint:
   - mangoJuicePerMango * NumberOfMangoBubbleTeas ≤ totalMangoJuice  
   That is: 4 * NumberOfMangoBubbleTeas ≤ 2000

2. Lychee Juice Constraint:
   - lycheeJuicePerLychee * NumberOfLycheeBubbleTeas ≤ totalLycheeJuice  
   That is: 6 * NumberOfLycheeBubbleTeas ≤ 3000

3. Flavor Composition Constraint (at least 40% must be Lychee):
   - NumberOfLycheeBubbleTeas ≥ minLycheeFraction * (NumberOfMangoBubbleTeas + NumberOfLycheeBubbleTeas)
   Rearranging, this is equivalent to: NumberOfMangoBubbleTeas ≤ (1 - minLycheeFraction) / minLycheeFraction * NumberOfLycheeBubbleTeas  
   With minLycheeFraction = 0.4, we have: NumberOfMangoBubbleTeas ≤ (0.6/0.4) * NumberOfLycheeBubbleTeas = 1.5 * NumberOfLycheeBubbleTeas

4. Mango Preference Constraint (Mango bubble teas must be produced in a larger number than Lychee bubble teas):
   - NumberOfMangoBubbleTeas ≥ NumberOfLycheeBubbleTeas + minMangoExcess  
   That is: NumberOfMangoBubbleTeas ≥ NumberOfLycheeBubbleTeas + 1

---------------------------------------------------
Expected Output Schema:
{
  "variables": {
    "NumberOfMangoBubbleTeas": "float",
    "NumberOfLycheeBubbleTeas": "float"
  },
  "objective": "float"
}'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_bubble_tea_problem():
    # Create the linear solver using the GLOP backend (for linear programming)
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Solver not created.")
        return None

    # Parameters
    mangoJuicePerMango = 4
    teaPerMango = 8
    lycheeJuicePerLychee = 6
    teaPerLychee = 6
    totalMangoJuice = 2000
    totalLycheeJuice = 3000
    minLycheeFraction = 0.4
    minMangoExcess = 1  # Mango count must be at least 1 unit greater than Lychee count

    # Variables (Continuous and non-negative)
    NumberOfMangoBubbleTeas = solver.NumVar(0, solver.infinity(), 'NumberOfMangoBubbleTeas')
    NumberOfLycheeBubbleTeas = solver.NumVar(0, solver.infinity(), 'NumberOfLycheeBubbleTeas')

    # Constraints

    # 1. Mango Juice Constraint: 4 * Mango ≤ 2000
    solver.Add(mangoJuicePerMango * NumberOfMangoBubbleTeas <= totalMangoJuice)

    # 2. Lychee Juice Constraint: 6 * Lychee ≤ 3000
    solver.Add(lycheeJuicePerLychee * NumberOfLycheeBubbleTeas <= totalLycheeJuice)

    # 3. Flavor Composition Constraint: 
    #    NumberOfLycheeBubbleTeas >= 0.4 * (Mango + Lychee)
    #    Equivalent: Mango <= (1 - 0.4)/0.4 * Lychee = 1.5 * Lychee
    solver.Add(NumberOfMangoBubbleTeas <= 1.5 * NumberOfLycheeBubbleTeas)

    # 4. Mango Preference Constraint: Mango ≥ Lychee + 1
    solver.Add(NumberOfMangoBubbleTeas >= NumberOfLycheeBubbleTeas + minMangoExcess)

    # Objective: Minimize total tea consumption = 8*Mango + 6*Lychee
    objective = solver.Objective()
    objective.SetCoefficient(NumberOfMangoBubbleTeas, teaPerMango)
    objective.SetCoefficient(NumberOfLycheeBubbleTeas, teaPerLychee)
    objective.SetMinimization()

    # Solve the model
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        solution = {
            "variables": {
                "NumberOfMangoBubbleTeas": NumberOfMangoBubbleTeas.solution_value(),
                "NumberOfLycheeBubbleTeas": NumberOfLycheeBubbleTeas.solution_value()
            },
            "objective": objective.Value()
        }
        return solution
    else:
        print("The problem does not have an optimal solution.")
        return None

def main():
    # Since there's only one formulation proposed, we create a single model solution.
    solution1 = solve_bubble_tea_problem()

    # Display results in a structured way:
    if solution1:
        print("Solution for Bubble Tea Production Problem (Formulation 1):")
        print("---------------------------------------------------------")
        print(f"NumberOfMangoBubbleTeas: {solution1['variables']['NumberOfMangoBubbleTeas']}")
        print(f"NumberOfLycheeBubbleTeas: {solution1['variables']['NumberOfLycheeBubbleTeas']}")
        print(f"Total Tea Used (Objective Value): {solution1['objective']}")
    else:
        print("No optimal solution found for Formulation 1.")

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Solution for Bubble Tea Production Problem (Formulation 1):
---------------------------------------------------------
NumberOfMangoBubbleTeas: 2.9999999999999996
NumberOfLycheeBubbleTeas: 1.9999999999999996
Total Tea Used (Objective Value): 35.99999999999999
'''

'''Expected Output:
Expected solution

: {'variables': {'NumberOfMangoBubbleTeas': 0.0, 'NumberOfLycheeBubbleTeas': 0.0}, 'objective': 0.0}'''

