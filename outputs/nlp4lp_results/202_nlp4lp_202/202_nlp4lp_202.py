# Problem Description:
'''Problem description: An amusement park has two types of games: throwing and climbing games. Throwing games attract 15 customers every hour and climbing games attract 8 customers every hour. Throwing games costs the amusement park $2 in prizes per hour whereas climbing games cost $3 in prizes per hour. Since throwing games yield the most profit, there must be at least twice as many throwing games as climbing games. However, at least 5 games must be climbing. If the amusement park can have at most $100 in prizes every hour, maximize the total number of customers attracted every hour.

Expected Output Schema:
{
  "variables": {
    "ThrowingGames": "float",
    "ClimbingGames": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- GAMES: set of game types = {Throwing, Climbing}

Parameters:
- customers_per_hour:
    - Throwing: 15 (customers per hour per throwing game)
    - Climbing: 8 (customers per hour per climbing game)
- prize_cost_per_hour:
    - Throwing: 2 (USD per hour per throwing game)
    - Climbing: 3 (USD per hour per climbing game)
- max_prize_budget: 100 (USD available per hour for prizes)
- min_climbing_games: 5 (minimum number of climbing games)
- throwing_to_climbing_ratio: 2 (there must be at least 2 throwing games per climbing game)

Variables:
- ThrowingGames: number of throwing games operated (integer, ≥ 0)
- ClimbingGames: number of climbing games operated (integer, ≥ 0)

Objective:
- Maximize total_customers = (15 * ThrowingGames) + (8 * ClimbingGames)
  (This represents the total number of customers attracted per hour.)

Constraints:
1. Prize budget constraint:
   (2 * ThrowingGames) + (3 * ClimbingGames) ≤ 100
   [Ensures the total prizes cost per hour does not exceed 100 USD.]

2. Ratio constraint:
   ThrowingGames ≥ 2 * ClimbingGames
   [Ensures that there are at least twice as many throwing games as climbing games.]

3. Minimum climbing games constraint:
   ClimbingGames ≥ 5
   [Ensures at least 5 climbing games are operated.]

Note:
- All parameters are expressed in units matching "per hour" for both customer attraction and prize cost.
- Decision variables are assumed to be integers because they represent the number of games.
- This model is self-contained and directly maps to many optimization solvers (e.g., Python’s OR-Tools).

Expected Output Schema:
{
  "variables": {
    "ThrowingGames": "integer",
    "ClimbingGames": "integer"
  },
  "objective": "maximize (15 * ThrowingGames) + (8 * ClimbingGames)"
}'''

# Generated Code:
from ortools.linear_solver import pywraplp

def solve_model():
    # Create the MIP solver using the CBC backend.
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Solver not created.")
        return None

    # Variable declarations (integer variables >= 0)
    # ThrowingGames: number of throwing games to operate
    # ClimbingGames: number of climbing games to operate
    ThrowingGames = solver.IntVar(0, solver.infinity(), 'ThrowingGames')
    ClimbingGames = solver.IntVar(0, solver.infinity(), 'ClimbingGames')
    
    # Constraint 1: Prize budget constraint:
    # 2 * ThrowingGames + 3 * ClimbingGames ≤ 100
    solver.Add(2 * ThrowingGames + 3 * ClimbingGames <= 100)
    
    # Constraint 2: Throwing to Climbing ratio constraint:
    # ThrowingGames ≥ 2 * ClimbingGames
    solver.Add(ThrowingGames >= 2 * ClimbingGames)
    
    # Constraint 3: Minimum climbing games:
    # ClimbingGames ≥ 5
    solver.Add(ClimbingGames >= 5)
    
    # Objective: Maximize (15 * ThrowingGames) + (8 * ClimbingGames)
    objective = solver.Objective()
    objective.SetCoefficient(ThrowingGames, 15)
    objective.SetCoefficient(ClimbingGames, 8)
    objective.SetMaximization()
    
    status = solver.Solve()
    
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        solution = {
            "variables": {
                "ThrowingGames": ThrowingGames.solution_value(),
                "ClimbingGames": ClimbingGames.solution_value()
            },
            "objective": objective.Value()
        }
        return solution
    else:
        print("No feasible solution found.")
        return None

def main():
    # Solve the problem using the first (and only) formulation.
    solution1 = solve_model()
    
    print("Model Implementation 1:")
    if solution1:
        print("Optimal solution:")
        print("  ThrowingGames =", solution1["variables"]["ThrowingGames"])
        print("  ClimbingGames =", solution1["variables"]["ClimbingGames"])
        print("Maximum total customers per hour =", solution1["objective"])
    else:
        print("Problem is infeasible.")

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Model Implementation 1:
Optimal solution:
  ThrowingGames = 42.0
  ClimbingGames = 5.0
Maximum total customers per hour = 670.0
'''

'''Expected Output:
Expected solution

: {'variables': {'ThrowingGames': 42.0, 'ClimbingGames': 5.0}, 'objective': 670.0}'''

