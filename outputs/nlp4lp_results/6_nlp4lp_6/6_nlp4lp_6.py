# Problem Description:
'''Problem description: A farmer wants to mix his animal feeds, Feed A and Feed B, in such a way that the mixture will contain a minimum of 30 units of protein and 50 units of fat. Feed A costs $100 per kilogram and contains 10 units of protein and 8 units of fat. Feed B costs $80 per kilogram and contains 7 units of protein and 15 units of fat. Determine the minimum cost of the mixture.

Expected Output Schema:
{
  "variables": {
    "QuantityFeedA": "float",
    "QuantityFeedB": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Below is the complete five-element structured mathematical model for the problem:

------------------------------------------------------------
Sets:
- F = {FeedA, FeedB} 
  (Each element in F represents a type of animal feed.)

Parameters:
- cost[FeedA] = 100 USD per kilogram  
- cost[FeedB] = 80 USD per kilogram  
- protein[FeedA] = 10 units protein per kilogram  
- protein[FeedB] = 7 units protein per kilogram  
- fat[FeedA] = 8 units fat per kilogram  
- fat[FeedB] = 15 units fat per kilogram  
- min_protein = 30 units (minimum required total protein)  
- min_fat = 50 units (minimum required total fat)  
  (All feed quantities are measured in kilograms. Protein and fat units are assumed to be consistent across feeds.)

Variables:
- QuantityFeedA: quantity of Feed A to use (continuous, in kilograms, QuantityFeedA ≥ 0)
- QuantityFeedB: quantity of Feed B to use (continuous, in kilograms, QuantityFeedB ≥ 0)

Objective:
- Minimize total cost = (cost[FeedA] * QuantityFeedA) + (cost[FeedB] * QuantityFeedB)
  (This represents the total expenditure in USD for the feed mixture.)

Constraints:
1. Protein requirement: (protein[FeedA] * QuantityFeedA) + (protein[FeedB] * QuantityFeedB) ≥ min_protein  
   (At least 30 units of protein must be present in the mixture.)

2. Fat requirement: (fat[FeedA] * QuantityFeedA) + (fat[FeedB] * QuantityFeedB) ≥ min_fat  
   (At least 50 units of fat must be present in the mixture.)

------------------------------------------------------------

Note:  
- The units across all parameters are consistent (USD per kilogram, units per kilogram, etc.).  
- No additional data has been assumed beyond what is specified.  
- This structure and variable naming are intended for a clear implementation in Python or OR-Tools.

The expected output schema corresponding to the model is:

{
  "variables": {
    "QuantityFeedA": "float",
    "QuantityFeedB": "float"
  },
  "objective": "float"
}'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_feed_mixture_lp():
    # Create the solver using the GLOP backend (for linear programming).
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Linear solver not available.")
        return None

    # Parameters
    cost_A = 100    # USD per kilogram for Feed A
    cost_B = 80     # USD per kilogram for Feed B
    protein_A = 10  # units protein per kg for Feed A
    protein_B = 7   # units protein per kg for Feed B
    fat_A = 8       # units fat per kg for Feed A
    fat_B = 15      # units fat per kg for Feed B
    min_protein = 30  # minimum required protein units
    min_fat = 50      # minimum required fat units

    # Variables: quantities of Feed A and Feed B (in kilograms)
    QuantityFeedA = solver.NumVar(0, solver.infinity(), 'QuantityFeedA')
    QuantityFeedB = solver.NumVar(0, solver.infinity(), 'QuantityFeedB')

    # Constraints
    # Protein constraint: 10 * QuantityFeedA + 7 * QuantityFeedB >= 30
    solver.Add(protein_A * QuantityFeedA + protein_B * QuantityFeedB >= min_protein)
    # Fat constraint: 8 * QuantityFeedA + 15 * QuantityFeedB >= 50
    solver.Add(fat_A * QuantityFeedA + fat_B * QuantityFeedB >= min_fat)

    # Objective Function: Minimize cost = 100 * QuantityFeedA + 80 * QuantityFeedB
    objective = solver.Objective()
    objective.SetCoefficient(QuantityFeedA, cost_A)
    objective.SetCoefficient(QuantityFeedB, cost_B)
    objective.SetMinimization()

    # Solve the problem
    status = solver.Solve()

    # Check and return the result in expected schema
    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "variables": {
                "QuantityFeedA": QuantityFeedA.solution_value(),
                "QuantityFeedB": QuantityFeedB.solution_value()
            },
            "objective": objective.Value()
        }
        return result
    elif status == pywraplp.Solver.INFEASIBLE:
        print("The problem is infeasible.")
    else:
        print("The solver returned with a non-optimal status:", status)
    return None

def main():
    # Solve using the Linear Programming formulation.
    result_lp = solve_feed_mixture_lp()
    if result_lp:
        print("Result using ortools.linear_solver (Linear Programming):")
        print(result_lp)

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Result using ortools.linear_solver (Linear Programming):
{'variables': {'QuantityFeedA': 1.0638297872340425, 'QuantityFeedB': 2.765957446808511}, 'objective': 327.6595744680851}
'''

'''Expected Output:
Expected solution

: {'variables': {'QuantityFeedA': 1.0638297872340428, 'QuantityFeedB': 2.765957446808511}, 'objective': 327.6595744680851}'''

