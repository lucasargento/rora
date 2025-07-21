# Problem Description:
'''Problem description: A florist transports his flowers to stores in small bouquets and large bouquets. A small bouquet has 5 flowers while a large bouquet has 10 flowers. The florist can transport at most 80 small bouquets and 50 large bouquets. In total, he can transport at most 70 bouquets and he must transport at least 20 large bouquets. Since small bouquets are more popular, he must transport at least twice as many small bouquets as large bouquets. How many of each bouquet should he transport to maximize the total number of flowers that reach the stores?

Expected Output Schema:
{
  "variables": {
    "SmallBouquets": "float",
    "LargeBouquets": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Below is a complete five‐element formulation of the florist’s bouquet transportation problem.

------------------------------------------------------------
Sets:
• B = {Small, Large} 
  (B represents the bouquet types: Small bouquets and Large bouquets)

------------------------------------------------------------
Parameters:
• flowersPerSmall = 5         [flowers per small bouquet]
• flowersPerLarge = 10        [flowers per large bouquet]
• maxSmall = 80             [maximum number of small bouquets that can be transported]
• maxLarge = 50             [maximum number of large bouquets that can be transported]
• maxTotalBouquets = 70       [maximum total bouquets that can be transported]
• minLarge = 20             [minimum number of large bouquets required]
• ratioSmallToLarge = 2       [small bouquets must be at least twice the large bouquets]

------------------------------------------------------------
Variables:
• SmallBouquets: number of small bouquets to transport [decision variable, nonnegative; value expected as float even though the practical value should be an integer]
• LargeBouquets: number of large bouquets to transport [decision variable, nonnegative; value expected as float even though the practical value should be an integer]

------------------------------------------------------------
Objective:
Maximize total flowers transported = (flowersPerSmall * SmallBouquets) + (flowersPerLarge * LargeBouquets)
 Units: flowers

------------------------------------------------------------
Constraints:
1. Small bouquet capacity:         SmallBouquets ≤ maxSmall
2. Large bouquet capacity:          LargeBouquets ≤ maxLarge
3. Total bouquet capacity:          SmallBouquets + LargeBouquets ≤ maxTotalBouquets
4. Minimum large bouquets:         LargeBouquets ≥ minLarge
5. Popularity ratio (at least twice as many small bouquets as large):  SmallBouquets ≥ ratioSmallToLarge * LargeBouquets

------------------------------------------------------------
Comments:
• All parameter units are consistent (quantities of bouquets and flowers).  
• Though the expected output schema indicates float types for decision variables, note that bouquet counts are inherently integer values.  
• The objective and constraints are expressed using simple linear expressions to facilitate implementation in modeling tools (e.g., Python with OR-Tools).

------------------------------------------------------------

For quick reference, here is a JSON snippet conforming to the expected output schema:

{
  "variables": {
    "SmallBouquets": "float",
    "LargeBouquets": "float"
  },
  "objective": "float"
}'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_bouquet_problem():
    # Data (parameters)
    flowersPerSmall = 5
    flowersPerLarge = 10
    maxSmall = 80
    maxLarge = 50
    maxTotalBouquets = 70
    minLarge = 20
    ratioSmallToLarge = 2

    # Create the linear solver with the GLOP backend.
    # Since this is a linear optimization problem with continuous variables (expected as float),
    # we use the linear solver.
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Could not create solver.")
        return None

    # Decision Variables:
    # Note: Though the decision variables represent counts (thus naturally integers),
    # the expected output schema requests floats.
    SmallBouquets = solver.NumVar(0.0, maxSmall, 'SmallBouquets')
    # We can set a lower bound of minLarge by either constraint or by defining the variable.
    LargeBouquets = solver.NumVar(minLarge, maxLarge, 'LargeBouquets')

    # Constraints:
    # 1. Small bouquet capacity: SmallBouquets <= maxSmall is already handled by variable's upper bound.
    # 2. Large bouquet capacity: LargeBouquets <= maxLarge is already handled by variable's upper bound.
    # 3. Total bouquet capacity: SmallBouquets + LargeBouquets <= maxTotalBouquets.
    solver.Add(SmallBouquets + LargeBouquets <= maxTotalBouquets)

    # 4. Minimum large bouquets: LargeBouquets >= minLarge is already handled by variable's lower bound.
    # 5. Popularity ratio: SmallBouquets >= ratioSmallToLarge * LargeBouquets.
    solver.Add(SmallBouquets >= ratioSmallToLarge * LargeBouquets)

    # Objective: Maximize total flowers = 5*SmallBouquets + 10*LargeBouquets
    objective = solver.Objective()
    objective.SetCoefficient(SmallBouquets, flowersPerSmall)
    objective.SetCoefficient(LargeBouquets, flowersPerLarge)
    objective.SetMaximization()

    # Solve the problem.
    status = solver.Solve()

    # Prepare results dictionary.
    results = {}

    if status == pywraplp.Solver.OPTIMAL:
        results['SmallBouquets'] = SmallBouquets.solution_value()
        results['LargeBouquets'] = LargeBouquets.solution_value()
        results['objective'] = objective.Value()
    else:
        results['error'] = "The problem does not have an optimal solution."

    return results

def main():
    # There is only one formulation in the provided description.
    # If there were more than one formulation, we would call each implementation separately.
    solution = solve_bouquet_problem()
    
    print("Bouquet Transportation Problem Results:")
    if 'error' in solution:
        print("Error:", solution['error'])
    else:
        print("SmallBouquets =", solution['SmallBouquets'])
        print("LargeBouquets =", solution['LargeBouquets'])
        print("Total Flowers Transported =", solution['objective'])

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Bouquet Transportation Problem Results:
SmallBouquets = 46.666666666666664
LargeBouquets = 23.333333333333332
Total Flowers Transported = 466.66666666666663
'''

'''Expected Output:
Expected solution

: {'variables': {'SmallBouquets': 47.0, 'LargeBouquets': 23.0}, 'objective': 465.0}'''

