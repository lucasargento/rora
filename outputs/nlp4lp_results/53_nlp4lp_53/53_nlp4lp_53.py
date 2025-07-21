# Problem Description:
'''Problem description: A bakery makes fiber supplemented brownies and lemon squares. Each brownie requires 5 units of chocolate mix and 4 units of fiber. Each lemon square requires 7 units of lemon mix and 6 units of fiber. Lemon squares sell much faster and thus the number of lemon squares made must be larger than the number of brownies made. However, to please all customers, at least 40% of the items made must be brownies. If the bakery has 2500 units of chocolate mix and 3300 units of lemon mix, how many of each should be made to minimize the total amount of fiber needed?

Expected Output Schema:
{
  "variables": {
    "NumberOfBrownies": "float",
    "NumberOfLemonSquares": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Below is one complete formulation of the problem using the five‐element framework. (Note: There is some ambiguity in the problem because no minimum production target is stated. In a “pure” minimization one could choose production amounts arbitrarily close to zero. We assume here that the bakery wishes to decide on positive production quantities—subject to the upper bounds on chocolate and lemon mixes—while satisfying the selling and customer‐satisfaction requirements. In other words, the available chocolate mix and lemon mix are upper bounds that production must not exceed, and the ratio constraints force a “nontrivial” production mix.)

─────────────────────────────  
Sets:
- P: set of products = {Brownies, LemonSquares}

─────────────────────────────  
Parameters (all units are “units per item”, and mix availabilities are in “units”):
- chocolate_mix_by_Brownie = 5 (units of chocolate mix needed per brownie)
- fiber_by_Brownie = 4 (units of fiber needed per brownie)
- lemon_mix_by_LemonSquare = 7 (units of lemon mix needed per lemon square)
- fiber_by_LemonSquare = 6 (units of fiber needed per lemon square)
- available_chocolate_mix = 2500 (units available)
- available_lemon_mix = 3300 (units available)

Additional ratio parameters:
- minimum_brownie_fraction = 0.40  
  (At least 40% of the total items produced must be brownies; equivalently,  
   NumberOfBrownies >= 0.4*(NumberOfBrownies + NumberOfLemonSquares))
- selling_preference: The number of lemon squares must be larger than the number of brownies.  
  (In practice, if decision variables are continuous one may pose this as:  
   NumberOfLemonSquares > NumberOfBrownies. For implementation, a constraint such as  
   NumberOfLemonSquares >= NumberOfBrownies + δ with a small positive δ may be used.)

─────────────────────────────  
Variables (assumed continuous and nonnegative):
- NumberOfBrownies (in units produced)
- NumberOfLemonSquares (in units produced)

─────────────────────────────  
Objective:
Minimize the total fiber used:
  TotalFiber = (fiber_by_Brownie * NumberOfBrownies) + (fiber_by_LemonSquare * NumberOfLemonSquares)
i.e.,
  Minimize: 4*NumberOfBrownies + 6*NumberOfLemonSquares

─────────────────────────────  
Constraints:
1. Chocolate mix availability for brownies:
   5 * NumberOfBrownies <= 2500

2. Lemon mix availability for lemon squares:
   7 * NumberOfLemonSquares <= 3300

3. Selling requirement – lemon squares must be produced in a larger number than brownies:
   NumberOfLemonSquares > NumberOfBrownies
   (In many solvers, a strict inequality is not allowed. In that case, one may enforce:
    NumberOfLemonSquares >= NumberOfBrownies + δ, where δ is a small positive number.)

4. Customer satisfaction – at least 40% of items must be brownies:
   NumberOfBrownies >= 0.4 * (NumberOfBrownies + NumberOfLemonSquares)
   (This constraint is equivalent to requiring that NumberOfLemonSquares <= 1.5 * NumberOfBrownies.)

─────────────────────────────  
Below is a summary in the expected JSON output schema:

{
  "variables": {
    "NumberOfBrownies": "float (>=0)",
    "NumberOfLemonSquares": "float (>=0)"
  },
  "objective": "4*NumberOfBrownies + 6*NumberOfLemonSquares (minimize total fiber usage)"
}

This model is self-contained and directly mappable to many optimization modeling libraries (e.g., Python with OR-Tools or PuLP).'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_model1():
    # Model 1 formulation:
    # Variables: 
    #   brownies (NumberOfBrownies) and lemon (NumberOfLemonSquares) are continuous variables with lower bounds to guarantee nontrivial production.
    #
    # Parameters:
    chocolate_mix_brownie = 5
    fiber_brownie = 4
    lemon_mix_lemon = 7
    fiber_lemon = 6
    available_chocolate_mix = 2500
    available_lemon_mix = 3300
    delta = 1e-3  # small positive number for strict inequality

    # Derive upper bounds from mix availabilities:
    max_brownies = available_chocolate_mix / chocolate_mix_brownie  # 2500/5 = 500
    max_lemon = available_lemon_mix / lemon_mix_lemon              # 3300/7 ≈ 471.43

    # Create solver using GLOP for continuous linear programming.
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Solver not created.")
        return None

    # Lower bound set to 1 to enforce nontrivial production quantities.
    brownies = solver.NumVar(1.0, max_brownies, 'NumberOfBrownies')
    lemon = solver.NumVar(1.0, max_lemon, 'NumberOfLemonSquares')

    # Constraint 1: Chocolate mix availability for brownies
    solver.Add(chocolate_mix_brownie * brownies <= available_chocolate_mix)
    
    # Constraint 2: Lemon mix availability for lemon squares
    solver.Add(lemon_mix_lemon * lemon <= available_lemon_mix)
    
    # Constraint 3: Selling requirement – lemon squares must be produced in a larger number than brownies.
    # Implemented as: lemon >= brownies + delta
    solver.Add(lemon >= brownies + delta)
    
    # Constraint 4: Customer satisfaction – at least 40% of items must be brownies.
    # That is, brownies >= 0.4*(brownies + lemon) 
    # Rearranging: brownies - 0.4*brownies >= 0.4*lemon   => 0.6*brownies >= 0.4*lemon => 3 * brownies >= 2 * lemon.
    solver.Add(3 * brownies >= 2 * lemon)

    # Objective: Minimize the total fiber needed = 4*brownies + 6*lemon.
    objective = solver.Objective()
    objective.SetCoefficient(brownies, fiber_brownie)
    objective.SetCoefficient(lemon, fiber_lemon)
    objective.SetMinimization()

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "variables": {
                "NumberOfBrownies": brownies.solution_value(),
                "NumberOfLemonSquares": lemon.solution_value()
            },
            "objective": objective.Value()
        }
    else:
        result = None
    return result

def solve_model2():
    # Model 2 formulation:
    # This version uses an equivalent formulation for the customer satisfaction constraint.
    # Instead of brownies >= 0.4*(brownies + lemon) we use the equivalent ratio form:
    # lemon <= 1.5 * brownies.
    #
    # All other parameters remain the same.
    chocolate_mix_brownie = 5
    fiber_brownie = 4
    lemon_mix_lemon = 7
    fiber_lemon = 6
    available_chocolate_mix = 2500
    available_lemon_mix = 3300
    delta = 1e-3  # small positive number for strict inequality

    max_brownies = available_chocolate_mix / chocolate_mix_brownie  # 500
    max_lemon = available_lemon_mix / lemon_mix_lemon              # ≈471.43

    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Solver not created.")
        return None

    # Lower bounds enforced as 1 to avoid trivial zero production.
    brownies = solver.NumVar(1.0, max_brownies, 'NumberOfBrownies')
    lemon = solver.NumVar(1.0, max_lemon, 'NumberOfLemonSquares')

    # Constraint 1: Chocolate mix availability for brownies.
    solver.Add(chocolate_mix_brownie * brownies <= available_chocolate_mix)
    
    # Constraint 2: Lemon mix availability for lemon squares.
    solver.Add(lemon_mix_lemon * lemon <= available_lemon_mix)
    
    # Constraint 3: Selling requirement – lemon squares must be produced in a larger number than brownies.
    solver.Add(lemon >= brownies + delta)
    
    # Constraint 4 (alternative formulation): Customer satisfaction – at least 40% of items must be brownies.
    # This constraint is equivalent to lemon <= 1.5 * brownies.
    solver.Add(lemon <= 1.5 * brownies)

    # Objective: Minimize total fiber used = 4*brownies + 6*lemon.
    objective = solver.Objective()
    objective.SetCoefficient(brownies, fiber_brownie)
    objective.SetCoefficient(lemon, fiber_lemon)
    objective.SetMinimization()

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "variables": {
                "NumberOfBrownies": brownies.solution_value(),
                "NumberOfLemonSquares": lemon.solution_value()
            },
            "objective": objective.Value()
        }
    else:
        result = None
    return result

def main():
    result1 = solve_model1()
    result2 = solve_model2()

    print("Results for Model 1 (using brownies >= 0.4*(brownies+lemon) constraint):")
    if result1 is not None:
        print("Optimal NumberOfBrownies =", result1["variables"]["NumberOfBrownies"])
        print("Optimal NumberOfLemonSquares =", result1["variables"]["NumberOfLemonSquares"])
        print("Optimal Objective (Total Fiber) =", result1["objective"])
    else:
        print("Model 1 is infeasible.")

    print("\nResults for Model 2 (using lemon <= 1.5*brownies constraint):")
    if result2 is not None:
        print("Optimal NumberOfBrownies =", result2["variables"]["NumberOfBrownies"])
        print("Optimal NumberOfLemonSquares =", result2["variables"]["NumberOfLemonSquares"])
        print("Optimal Objective (Total Fiber) =", result2["objective"])
    else:
        print("Model 2 is infeasible.")

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Results for Model 1 (using brownies >= 0.4*(brownies+lemon) constraint):
Optimal NumberOfBrownies = 1.0
Optimal NumberOfLemonSquares = 1.001
Optimal Objective (Total Fiber) = 10.006

Results for Model 2 (using lemon <= 1.5*brownies constraint):
Optimal NumberOfBrownies = 1.0
Optimal NumberOfLemonSquares = 1.001
Optimal Objective (Total Fiber) = 10.006
'''

'''Expected Output:
Expected solution

: {'variables': {'NumberOfBrownies': 2.0000000000000004, 'NumberOfLemonSquares': 3.0000000000000004}, 'objective': 26.000000000000007}'''

