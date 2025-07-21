# Problem Description:
'''Problem description: An art store makes large and small art pieces. The store has available 100 units of paint, 50 units of glitter, and 70 units of glue. To make a large art piece requires 4 units of paint, 3 units of glitter, and 5 units of glue. To make a small art piece requires 2 units of paint, 1 unit of glitter, and 2 units of glue. The store must make at least 5 units of each large and small art pieces. If the profit per large art piece is $30 and the profit per small art piece is $15, how many of each should be made to maximize profit?

Expected Output Schema:
{
  "variables": {
    "NumberLarge": "float",
    "NumberSmall": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- P: set of art piece types = {Large, Small}

Parameters:
- total_paint: 100 (total available paint units)
- total_glitter: 50 (total available glitter units)
- total_glue: 70 (total available glue units)
- paint_usage_Large: 4 (paint units required per large art piece)
- glitter_usage_Large: 3 (glitter units required per large art piece)
- glue_usage_Large: 5 (glue units required per large art piece)
- paint_usage_Small: 2 (paint units required per small art piece)
- glitter_usage_Small: 1 (glitter unit required per small art piece)
- glue_usage_Small: 2 (glue units required per small art piece)
- profit_Large: 30 (profit per large art piece in dollars)
- profit_Small: 15 (profit per small art piece in dollars)
- min_production: 5 (minimum number of each art piece to be made)

Variables:
- NumberLarge: integer decision variable representing the number of large art pieces produced (units, integer ≥ min_production)
- NumberSmall: integer decision variable representing the number of small art pieces produced (units, integer ≥ min_production)

Objective:
- Maximize Total Profit = profit_Large * NumberLarge + profit_Small * NumberSmall

Constraints:
1. Paint constraint: paint_usage_Large * NumberLarge + paint_usage_Small * NumberSmall ≤ total_paint
2. Glitter constraint: glitter_usage_Large * NumberLarge + glitter_usage_Small * NumberSmall ≤ total_glitter
3. Glue constraint: glue_usage_Large * NumberLarge + glue_usage_Small * NumberSmall ≤ total_glue
4. Minimum production for large art pieces: NumberLarge ≥ min_production
5. Minimum production for small art pieces: NumberSmall ≥ min_production

Notes:
- All units in the parameters are consistent with the respective resource quantities in the problem statement.
- The decision variables are defined as integers because the art pieces are discrete items.
- This model assumes that all resource usage (paint, glitter, and glue) is consumed at the time of production and that the available units of each resource are fully available in the production period.'''

# Generated Code:
from ortools.linear_solver import pywraplp

def solve_model():
    # Create the MIP solver with the CBC backend.
    solver = pywraplp.Solver.CreateSolver('CBC_MIXED_INTEGER_PROGRAMMING')
    if solver is None:
        print("CBC solver unavailable.")
        return None

    # Parameters
    total_paint = 100          # total available paint units
    total_glitter = 50         # total available glitter units
    total_glue = 70            # total available glue units

    paint_usage_Large = 4      # paint units required per large art piece
    glitter_usage_Large = 3    # glitter units required per large art piece
    glue_usage_Large = 5       # glue units required per large art piece

    paint_usage_Small = 2      # paint units required per small art piece
    glitter_usage_Small = 1    # glitter unit required per small art piece
    glue_usage_Small = 2       # glue units required per small art piece

    profit_Large = 30          # profit per large art piece in dollars
    profit_Small = 15          # profit per small art piece in dollars

    min_production = 5         # minimum number of each art piece to be made

    # Decision Variables
    # NumberLarge and NumberSmall are integer variables with a lower bound of min_production.
    NumberLarge = solver.IntVar(min_production, solver.infinity(), 'NumberLarge')
    NumberSmall = solver.IntVar(min_production, solver.infinity(), 'NumberSmall')

    # Constraints
    # Paint constraint: paint_usage_Large * NumberLarge + paint_usage_Small * NumberSmall <= total_paint
    solver.Add(paint_usage_Large * NumberLarge + paint_usage_Small * NumberSmall <= total_paint)

    # Glitter constraint: glitter_usage_Large * NumberLarge + glitter_usage_Small * NumberSmall <= total_glitter
    solver.Add(glitter_usage_Large * NumberLarge + glitter_usage_Small * NumberSmall <= total_glitter)

    # Glue constraint: glue_usage_Large * NumberLarge + glue_usage_Small * NumberSmall <= total_glue
    solver.Add(glue_usage_Large * NumberLarge + glue_usage_Small * NumberSmall <= total_glue)

    # Objective: Maximize Total Profit = profit_Large * NumberLarge + profit_Small * NumberSmall
    objective = solver.Objective()
    objective.SetCoefficient(NumberLarge, profit_Large)
    objective.SetCoefficient(NumberSmall, profit_Small)
    objective.SetMaximization()

    # Solve the problem
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        solution = {
            "NumberLarge": NumberLarge.solution_value(),
            "NumberSmall": NumberSmall.solution_value(),
            "objective": objective.Value()
        }
        return solution
    elif status == pywraplp.Solver.FEASIBLE:
        solution = {
            "NumberLarge": NumberLarge.solution_value(),
            "NumberSmall": NumberSmall.solution_value(),
            "objective": objective.Value()
        }
        print("A feasible solution was found (but optimality not proven).")
        return solution
    else:
        print("No solution found. The problem appears to be infeasible.")
        return None

def main():
    # Solve the art pieces production optimization problem using formulation version 1.
    sol1 = solve_model()

    # Prepare results in a structured way.
    if sol1:
        print("Results for Art Pieces Production Problem (Version 1):")
        print("-------------------------------------------------------")
        print("NumberLarge:", sol1["NumberLarge"])
        print("NumberSmall:", sol1["NumberSmall"])
        print("Maximum Profit:", sol1["objective"])
    else:
        print("The problem is infeasible for Version 1.")

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Results for Art Pieces Production Problem (Version 1):
-------------------------------------------------------
NumberLarge: 5.0
NumberSmall: 22.0
Maximum Profit: 480.0
'''

'''Expected Output:
Expected solution

: {'variables': {'NumberLarge': 5.2, 'NumberSmall': 22.0}, 'objective': 486.0}'''

