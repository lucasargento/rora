# Problem Description:
'''Problem description: A bakery makes almond and pistachio croissants. An almond croissant requires 5 units of butter and 8 units of flour. A pistachio croissant requires 3 units of butter and 6 units of flour. The bakery has available 600 units of butter and 800 units of flour. Since the almond croissant is more popular, at least 3 times as many almond croissants should be made as pistachio croissants. If making an almond croissant takes 12 minutes and making a pistachio croissant takes 10 minutes, how many of each should be made to minimize the total production time?

Expected Output Schema:
{
  "variables": {
    "QuantityAlmondCroissant": "float",
    "QuantityPistachioCroissant": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- Product: {Almond, Pistachio}

Parameters:
- butter_per_almond = 5 (butter units needed per almond croissant)
- butter_per_pistachio = 3 (butter units needed per pistachio croissant)
- flour_per_almond = 8 (flour units needed per almond croissant)
- flour_per_pistachio = 6 (flour units needed per pistachio croissant)
- total_butter = 600 (available butter units)
- total_flour = 800 (available flour units)
- time_almond = 12 (production time per almond croissant in minutes)
- time_pistachio = 10 (production time per pistachio croissant in minutes)
- popularity_ratio = 3 (almond croissants must be at least 3 times the pistachio croissants)

Variables:
- QuantityAlmondCroissant (x_almond): number of almond croissants to produce, assumed integer and nonnegative.
- QuantityPistachioCroissant (x_pistachio): number of pistachio croissants to produce, assumed integer and nonnegative.

Objective:
- Minimize total production time = time_almond * x_almond + time_pistachio * x_pistachio
  In other words, minimize (12 * QuantityAlmondCroissant + 10 * QuantityPistachioCroissant).

Constraints:
1. Butter constraint: butter_per_almond * x_almond + butter_per_pistachio * x_pistachio ≤ total_butter  
   That is, 5 * QuantityAlmondCroissant + 3 * QuantityPistachioCroissant ≤ 600.
2. Flour constraint: flour_per_almond * x_almond + flour_per_pistachio * x_pistachio ≤ total_flour  
   That is, 8 * QuantityAlmondCroissant + 6 * QuantityPistachioCroissant ≤ 800.
3. Popularity constraint: x_almond ≥ popularity_ratio * x_pistachio  
   That is, QuantityAlmondCroissant ≥ 3 * QuantityPistachioCroissant.
4. Nonnegativity: x_almond, x_pistachio ≥ 0 and integer.

--------------------------------------------------

For clarity (expected output schema for a coding agent):

{
  "variables": {
    "QuantityAlmondCroissant": "integer (>=0)",
    "QuantityPistachioCroissant": "integer (>=0)"
  },
  "objective": "Minimize 12 * QuantityAlmondCroissant + 10 * QuantityPistachioCroissant"
}

This completes the structured mathematical model using the five-element framework.'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_croissant_problem():
    # Create the solver using CBC MIP solver.
    solver = pywraplp.Solver.CreateSolver('CBC_MIXED_INTEGER_PROGRAMMING')
    if not solver:
        print("Solver not available.")
        return None

    # VARIABLES
    # x_almond: number of almond croissants (integer, >= 0)
    # x_pistachio: number of pistachio croissants (integer, >= 0)
    x_almond = solver.IntVar(0, solver.infinity(), 'QuantityAlmondCroissant')
    x_pistachio = solver.IntVar(0, solver.infinity(), 'QuantityPistachioCroissant')

    # PARAMETERS
    butter_per_almond = 5
    butter_per_pistachio = 3
    flour_per_almond = 8
    flour_per_pistachio = 6
    total_butter = 600
    total_flour = 800
    time_almond = 12
    time_pistachio = 10
    popularity_ratio = 3

    # CONSTRAINTS
    # 1. Butter constraint: 5 * x_almond + 3 * x_pistachio <= 600
    solver.Add(butter_per_almond * x_almond + butter_per_pistachio * x_pistachio <= total_butter)

    # 2. Flour constraint: 8 * x_almond + 6 * x_pistachio <= 800
    solver.Add(flour_per_almond * x_almond + flour_per_pistachio * x_pistachio <= total_flour)

    # 3. Popularity constraint: x_almond >= 3 * x_pistachio
    solver.Add(x_almond >= popularity_ratio * x_pistachio)

    # OBJECTIVE: Minimize total production time = 12 * x_almond + 10 * x_pistachio
    objective = solver.Objective()
    objective.SetCoefficient(x_almond, time_almond)
    objective.SetCoefficient(x_pistachio, time_pistachio)
    objective.SetMinimization()

    # Solve the problem
    status = solver.Solve()

    # Store results into a dictionary for structured output
    result = {
        "model": "Croissant Production (Almond and Pistachio)",
        "status": "",
        "variables": {},
        "objective": None
    }

    if status == pywraplp.Solver.OPTIMAL:
        result["status"] = "OPTIMAL"
        result["variables"]["QuantityAlmondCroissant"] = int(x_almond.solution_value())
        result["variables"]["QuantityPistachioCroissant"] = int(x_pistachio.solution_value())
        result["objective"] = objective.Value()
    elif status == pywraplp.Solver.FEASIBLE:
        result["status"] = "FEASIBLE but not proven optimal"
        result["variables"]["QuantityAlmondCroissant"] = int(x_almond.solution_value())
        result["variables"]["QuantityPistachioCroissant"] = int(x_pistachio.solution_value())
        result["objective"] = objective.Value()
    else:
        result["status"] = "No solution found."
    
    return result

def main():
    # Since only one formulation of the problem is provided, we only call one implementation.
    result1 = solve_croissant_problem()

    # Output the results in a structured way
    print("Results for Croissant Production Problem (Implementation 1):")
    if result1:
        print("Status:", result1["status"])
        if result1["status"] in ["OPTIMAL", "FEASIBLE but not proven optimal"]:
            print("Quantity Almond Croissant:", result1["variables"]["QuantityAlmondCroissant"])
            print("Quantity Pistachio Croissant:", result1["variables"]["QuantityPistachioCroissant"])
            print("Total Production Time:", result1["objective"])
        else:
            print("No feasible solution found.")
    else:
        print("Error in solving the problem.")

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Results for Croissant Production Problem (Implementation 1):
Status: OPTIMAL
Quantity Almond Croissant: 0
Quantity Pistachio Croissant: 0
Total Production Time: 0.0
'''

'''Expected Output:
Expected solution

: {'variables': {'QuantityAlmondCroissant': -0.0, 'QuantityPistachioCroissant': -0.0}, 'objective': 0.0}'''

