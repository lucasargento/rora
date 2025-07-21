# Problem Description:
'''Problem description: A crepe store sells chocolate and peanut butter crepes. A chocolate crepe requires 3 units of chocolate spread and 6 units of crepe mix. A peanut butter crepe requires 4 units of peanut butter spread and 7 units of crepe mix. Recently, the peanut butter crepe has been more popular and therefore the number of peanut butter crepes made must exceed the number of chocolate crepes made. However at least 25% of the crepes made should be chocolate. The store has available 400 units of chocolate spread and 450 units of peanut butter spread. How many of each should the store make to minimize the total amount of crepe mix needed?

Expected Output Schema:
{
  "variables": {
    "NumberOfChocolateCrepes": "float",
    "NumberOfPeanutButterCrepes": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- CrepeTypes = {Chocolate, PeanutButter}

Parameters:
- chocSpreadPerChocolate = 3 units of chocolate spread per chocolate crepe
- mixPerChocolate = 6 units of crepe mix per chocolate crepe
- pbSpreadPerPeanutButter = 4 units of peanut butter spread per peanut butter crepe
- mixPerPeanutButter = 7 units of crepe mix per peanut butter crepe
- availableChocSpread = 400 units of chocolate spread
- availablePBSpread = 450 units of peanut butter spread
  (Note: All resource parameters are assumed in the same unit as specified in the problem.)

Variables:
- NumberOfChocolateCrepes (x): number of chocolate crepes to produce; continuous (or integer) with x ≥ 0
- NumberOfPeanutButterCrepes (y): number of peanut butter crepes to produce; continuous (or integer) with y ≥ 0

Objective:
- Minimize total crepe mix used = mixPerChocolate * x + mixPerPeanutButter * y
  In expression form: minimize 6*x + 7*y  (units: crepe mix units)

Constraints:
1. Chocolate spread availability:
   - chocSpreadPerChocolate * x ≤ availableChocSpread
   - 3*x ≤ 400

2. Peanut butter spread availability:
   - pbSpreadPerPeanutButter * y ≤ availablePBSpread
   - 4*y ≤ 450

3. Popularity requirement (peanut butter crepes exceed chocolate crepes):
   - y must be strictly greater than x.
     • For modeling purposes (if using continuous variables) one may enforce: y ≥ x + ε (with ε a very small positive number)
     • If treating x and y as integers then: y ≥ x + 1

4. Minimum chocolate proportion (at least 25% of crepes made should be chocolate):
   - NumberOfChocolateCrepes must be at least 25% of total crepes, i.e.,
     x ≥ 0.25*(x + y)
   - Multiplying both sides by 4 gives: 4*x ≥ x + y   or equivalently 3*x ≥ y

5. Nonnegativity:
   - x ≥ 0
   - y ≥ 0

--------------------------------------------------
Based on the expected output schema, here is a JSON snippet that identifies the decision variables and the objective function:

{
  "variables": {
    "NumberOfChocolateCrepes": "float (>= 0, and ideally integer if crepes must be whole)",
    "NumberOfPeanutButterCrepes": "float (>= 0, and ideally integer if crepes must be whole)"
  },
  "objective": "minimize 6 * NumberOfChocolateCrepes + 7 * NumberOfPeanutButterCrepes"
}

Model Comments:
- Resource constraints ensure that the production does not exceed available chocolate spread (3 units per chocolate crepe) and peanut butter spread (4 units per peanut butter crepe).
- The popularity condition (peanut butter crepes exceed chocolate crepes) is modeled as y ≥ x + ε to capture the strict inequality. When implementing with integer variables, you may use y ≥ x + 1.
- The 25% minimum chocolate crepe condition is algebraically equivalent to 3*x ≥ y.
- The objective minimizes the total usage of crepe mix (6 units per chocolate crepe and 7 units per peanut butter crepe), which is the resource to be conserved.

This structured formulation fully represents the original problem using the five-element framework.'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_continuous():
    # Create a solver using the GLOP linear programming solver.
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Solver not found for continuous model.")
        return None

    # Decision Variables: continuous variables >= 0.
    x = solver.NumVar(0.0, solver.infinity(), 'NumberOfChocolateCrepes')
    y = solver.NumVar(0.0, solver.infinity(), 'NumberOfPeanutButterCrepes')

    # Resource constraints:
    # Chocolate spread: 3 * x <= 400
    solver.Add(3 * x <= 400)
    # Peanut butter spread: 4 * y <= 450
    solver.Add(4 * y <= 450)

    # Popularity requirement: peanut butter crepes exceed chocolate crepes.
    # Using an epsilon to represent strict inequality.
    solver.Add(y >= x + 1e-6)

    # Minimum 25% chocolate proportion: x >= 0.25*(x+y) ==> 3*x >= y.
    solver.Add(3 * x >= y)

    # Objective: Minimize total crepe mix used = 6*x + 7*y.
    objective = solver.Objective()
    objective.SetCoefficient(x, 6)
    objective.SetCoefficient(y, 7)
    objective.SetMinimization()

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL:
        return {
            "NumberOfChocolateCrepes": x.solution_value(),
            "NumberOfPeanutButterCrepes": y.solution_value(),
            "Objective": objective.Value()
        }
    else:
        return None

def solve_integer():
    # Create a solver using the CBC mixed-integer programming solver.
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Solver not found for integer model.")
        return None

    # For integer variables, we define bounds from resource constraints.
    # Maximum chocolate crepes are limited by chocolate spread: floor(400/3)
    max_chocolate = 400 // 3
    # Maximum peanut butter crepes by peanut butter spread: floor(450/4)
    max_peanutbutter = 450 // 4

    # Decision Variables: integer variables >= 0.
    x = solver.IntVar(0, max_chocolate, 'NumberOfChocolateCrepes')
    y = solver.IntVar(0, max_peanutbutter, 'NumberOfPeanutButterCrepes')

    # Resource constraints:
    solver.Add(3 * x <= 400)
    solver.Add(4 * y <= 450)

    # Popularity requirement: enforce integer strict inequality: y >= x + 1.
    solver.Add(y >= x + 1)

    # Minimum 25% chocolate proportion: 3*x >= y.
    solver.Add(3 * x >= y)

    # Objective: Minimize total crepe mix used = 6*x + 7*y.
    objective = solver.Objective()
    objective.SetCoefficient(x, 6)
    objective.SetCoefficient(y, 7)
    objective.SetMinimization()

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL:
        return {
            "NumberOfChocolateCrepes": x.solution_value(),
            "NumberOfPeanutButterCrepes": y.solution_value(),
            "Objective": objective.Value()
        }
    else:
        return None

def main():
    continuous_solution = solve_continuous()
    integer_solution = solve_integer()

    print("Continuous Model Solution:")
    if continuous_solution:
        print(continuous_solution)
    else:
        print("No optimal solution found for the continuous model.")

    print("\nInteger Model Solution:")
    if integer_solution:
        print(integer_solution)
    else:
        print("No optimal solution found for the integer model.")

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Continuous Model Solution:
{'NumberOfChocolateCrepes': 4.999999999999999e-07, 'NumberOfPeanutButterCrepes': 1.4999999999999998e-06, 'Objective': 1.35e-05}

Integer Model Solution:
{'NumberOfChocolateCrepes': 1.0, 'NumberOfPeanutButterCrepes': 2.0, 'Objective': 20.0}
'''

'''Expected Output:
Expected solution

: {'variables': {'NumberOfChocolateCrepes': 1.0, 'NumberOfPeanutButterCrepes': 2.0}, 'objective': 20.0}'''

