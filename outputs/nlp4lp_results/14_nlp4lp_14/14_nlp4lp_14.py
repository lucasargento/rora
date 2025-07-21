# Problem Description:
'''Problem description: My grandma is required to take two medicines Z1 and D3 everyday. She needs to take at least 5 grams of Z1 and 10 grams of D3 everyday. These medicines are available in two pills named Zodiac and Sunny. One pill of Zodiac contains 1.3 grams of Z1 while one pill of Sunny contains 1.2 grams of Z1. On the other hand, one pill of Zodiac contains 1.5 grams of D3 and one pill of Sunny contains 5 grams of D3. The cost per pill of Zodiac is $1 and the cost per pill of Sunny is $3. Formulate a LP such that the medicine requirement can be fulfilled at the lowest cost.

Expected Output Schema:
{
  "variables": {
    "QuantityZodiac": "float",
    "QuantitySunny": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- PILL: set of pill types = {Zodiac, Sunny}

Parameters:
- cost[p]: cost per pill for each pill type p, where cost[Zodiac] = 1 (USD per pill) and cost[Sunny] = 3 (USD per pill)
- Z1_content[p]: grams of medicine Z1 per pill of type p, where Z1_content[Zodiac] = 1.3 (grams per pill) and Z1_content[Sunny] = 1.2 (grams per pill)
- D3_content[p]: grams of medicine D3 per pill of type p, where D3_content[Zodiac] = 1.5 (grams per pill) and D3_content[Sunny] = 5 (grams per pill)
- min_Z1: minimum required grams of medicine Z1 per day, min_Z1 = 5 (grams)
- min_D3: minimum required grams of medicine D3 per day, min_D3 = 10 (grams)

Variables:
- Quantity[p]: number of pills of type p to take per day
  - In particular, define:
    - QuantityZodiac = Quantity[Zodiac] (decision variable for Zodiac pills, nonnegative integer)
    - QuantitySunny = Quantity[Sunny] (decision variable for Sunny pills, nonnegative integer)
  - (Note: Although pills are naturally integer, if a continuous relaxation is acceptable, these can be treated as nonnegative floats.)

Objective:
- Minimize Total_Cost = cost[Zodiac] * QuantityZodiac + cost[Sunny] * QuantitySunny
  (Minimization is in USD per day)

Constraints:
1. Z1 constraint: 1.3 * QuantityZodiac + 1.2 * QuantitySunny ≥ min_Z1  
   (This ensures at least 5 grams of medicine Z1 are taken)
2. D3 constraint: 1.5 * QuantityZodiac + 5 * QuantitySunny ≥ min_D3  
   (This ensures at least 10 grams of medicine D3 are taken)
3. Nonnegativity constraint: QuantityZodiac ≥ 0 and QuantitySunny ≥ 0

--------------------------------------------
JSON expected output schema:

{
  "variables": {
    "QuantityZodiac": "float",
    "QuantitySunny": "float"
  },
  "objective": "float"
}

This structured model fully represents the medicine requirement optimization problem.'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_continuous():
    """Solve the LP formulation using continuous decision variables."""
    # Create the solver using the GLOP backend for continuous LP.
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        return None

    # Variables: quantities of Zodiac and Sunny (continuous nonnegative values).
    QuantityZodiac = solver.NumVar(0.0, solver.infinity(), 'QuantityZodiac')
    QuantitySunny = solver.NumVar(0.0, solver.infinity(), 'QuantitySunny')
    
    # Parameters
    cost_zodiac = 1
    cost_sunny = 3

    Z1_content_zodiac = 1.3
    Z1_content_sunny = 1.2
    D3_content_zodiac = 1.5
    D3_content_sunny = 5

    min_Z1 = 5
    min_D3 = 10

    # Constraints
    # Z1 constraint: 1.3 * QuantityZodiac + 1.2 * QuantitySunny >= 5
    solver.Add(Z1_content_zodiac * QuantityZodiac + Z1_content_sunny * QuantitySunny >= min_Z1)
    
    # D3 constraint: 1.5 * QuantityZodiac + 5 * QuantitySunny >= 10
    solver.Add(D3_content_zodiac * QuantityZodiac + D3_content_sunny * QuantitySunny >= min_D3)
    
    # Objective: Minimize cost = 1 * QuantityZodiac + 3 * QuantitySunny
    objective = solver.Objective()
    objective.SetCoefficient(QuantityZodiac, cost_zodiac)
    objective.SetCoefficient(QuantitySunny, cost_sunny)
    objective.SetMinimization()
    
    # Solve the problem.
    status = solver.Solve()
    
    # Process results:
    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "model": "Continuous LP",
            "variables": {
                "QuantityZodiac": QuantityZodiac.solution_value(),
                "QuantitySunny": QuantitySunny.solution_value()
            },
            "objective": objective.Value()
        }
    else:
        result = {
            "model": "Continuous LP",
            "error": "The problem does not have an optimal solution."
        }
    
    return result

def solve_integer():
    """Solve the MILP formulation using integer decision variables."""
    # Create the solver using CBC for MILP.
    solver = pywraplp.Solver.CreateSolver('CBC_MIXED_INTEGER_PROGRAMMING')
    if not solver:
        return None

    # Variables: quantities of Zodiac and Sunny (integer nonnegative values).
    # Although pills are naturally integers.
    QuantityZodiac = solver.IntVar(0.0, solver.infinity(), 'QuantityZodiac')
    QuantitySunny = solver.IntVar(0.0, solver.infinity(), 'QuantitySunny')
    
    # Parameters
    cost_zodiac = 1
    cost_sunny = 3

    Z1_content_zodiac = 1.3
    Z1_content_sunny = 1.2
    D3_content_zodiac = 1.5
    D3_content_sunny = 5

    min_Z1 = 5
    min_D3 = 10

    # Constraints
    solver.Add(Z1_content_zodiac * QuantityZodiac + Z1_content_sunny * QuantitySunny >= min_Z1)
    solver.Add(D3_content_zodiac * QuantityZodiac + D3_content_sunny * QuantitySunny >= min_D3)
    
    # Objective
    objective = solver.Objective()
    objective.SetCoefficient(QuantityZodiac, cost_zodiac)
    objective.SetCoefficient(QuantitySunny, cost_sunny)
    objective.SetMinimization()

    # Solve the problem.
    status = solver.Solve()

    # Process results:
    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "model": "Integer MILP",
            "variables": {
                "QuantityZodiac": QuantityZodiac.solution_value(),
                "QuantitySunny": QuantitySunny.solution_value()
            },
            "objective": objective.Value()
        }
    else:
        result = {
            "model": "Integer MILP",
            "error": "The problem does not have an optimal solution."
        }
    
    return result

def main():
    continuous_result = solve_continuous()
    integer_result = solve_integer()
    
    # Output both results in a structured manner.
    print("Solution Results:")
    print("-----------------")
    if continuous_result:
        print("Continuous LP Formulation:")
        if "error" in continuous_result:
            print(" Error:", continuous_result["error"])
        else:
            print("   QuantityZodiac =", continuous_result["variables"]["QuantityZodiac"])
            print("   QuantitySunny  =", continuous_result["variables"]["QuantitySunny"])
            print("   Objective Value =", continuous_result["objective"])
    else:
        print("Continuous LP solver not available.")
    
    print()
    
    if integer_result:
        print("Integer MILP Formulation:")
        if "error" in integer_result:
            print(" Error:", integer_result["error"])
        else:
            print("   QuantityZodiac =", integer_result["variables"]["QuantityZodiac"])
            print("   QuantitySunny  =", integer_result["variables"]["QuantitySunny"])
            print("   Objective Value =", integer_result["objective"])
    else:
        print("Integer MILP solver not available.")

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Solution Results:
-----------------
Continuous LP Formulation:
   QuantityZodiac = 2.7659574468085113
   QuantitySunny  = 1.1702127659574466
   Objective Value = 6.276595744680851

Integer MILP Formulation:
   QuantityZodiac = 4.0
   QuantitySunny  = 1.0
   Objective Value = 7.0
'''

'''Expected Output:
Expected solution

: {'variables': {'QuantityZodiac': 4.0, 'QuantitySunny': 1.0}, 'objective': 7.0}'''

