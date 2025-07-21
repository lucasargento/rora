# Problem Description:
'''Problem description: A golf course is hosting an event and can transport guests using either golf carts or pull carts. A golf cart can take 4 guests while a pull cart can take 1 guest. Since golf carts take up a lot of space, at most 60% of carts can be golf carts. If the golf course needs to transport at least 80 guests, how many of each cart should be used to minimize the total number of carts needed?

Expected Output Schema:
{
  "variables": {
    "NumGolfCarts": "float",
    "NumPullCarts": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- CartTypes: the set of cart types used for transport. Although there are only two specific types (Golf Cart and Pull Cart), they are handled via their individual decision variables.

Parameters:
- CapacityGolfCart: the number of guests that a golf cart can carry (4 guests per cart).
- CapacityPullCart: the number of guests that a pull cart can carry (1 guest per cart).
- MinGuests: the minimum number of guests needed to be transported (80 guests).
- MaxGolfCartRatio: the maximum allowable ratio of golf carts to total carts (0.6, meaning at most 60% of all carts can be golf carts).

Variables:
- NumGolfCarts: number of golf carts to use (non-negative integer or float ≥ 0; interpreted as the count of golf carts).
- NumPullCarts: number of pull carts to use (non-negative integer or float ≥ 0; interpreted as the count of pull carts).

Objective:
- Minimize total carts used = NumGolfCarts + NumPullCarts.
  (The objective is to reduce the total number of carts deployed.)

Constraints:
1. Guest Transportation Constraint:
   - The combined guest capacity from golf carts and pull carts must be at least 80.
   - Formulated as: (CapacityGolfCart * NumGolfCarts) + (CapacityPullCart * NumPullCarts) ≥ MinGuests,
   - In numeric form: 4 * NumGolfCarts + 1 * NumPullCarts ≥ 80.
   
2. Golf Cart Ratio Constraint:
   - At most 60% of all carts used can be golf carts.
   - Formulated as: NumGolfCarts ≤ MaxGolfCartRatio * (NumGolfCarts + NumPullCarts),
   - Alternatively, after rearrangement: 2 * NumGolfCarts ≤ 3 * NumPullCarts.
   
Comments:
- All parameters are assumed to use consistent units (number/count for carts and guests).
- Decision variables are ideally integer-valued in a practical implementation, though they are represented as float in the output schema for flexibility.
  
Final Model Output Schema:
{
  "variables": {
    "NumGolfCarts": "float",
    "NumPullCarts": "float"
  },
  "objective": "float"
}'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_model_version1():
    # Model Version 1: Using the original Golf Cart Ratio Constraint:
    # NumGolfCarts <= 0.6 * (NumGolfCarts + NumPullCarts)
    # which can be reformulated as: 4 * NumGolfCarts - 6 * NumPullCarts <= 0.
    
    # Create the solver using CBC (for integer programming)
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Solver not created.")
        return None
    
    # Parameters
    capacityGolfCart = 4
    capacityPullCart = 1
    minGuests = 80

    # Decision Variables (using integer values)
    NumGolfCarts = solver.IntVar(0, solver.infinity(), 'NumGolfCarts')
    NumPullCarts = solver.IntVar(0, solver.infinity(), 'NumPullCarts')

    # Constraint 1: Guest Transportation: 4 * NumGolfCarts + 1 * NumPullCarts >= 80
    solver.Add(capacityGolfCart * NumGolfCarts + capacityPullCart * NumPullCarts >= minGuests)
    
    # Constraint 2: Golf Cart Ratio:
    # Original form: NumGolfCarts <= 0.6*(NumGolfCarts + NumPullCarts)
    # Rearranged: 0.4*NumGolfCarts - 0.6*NumPullCarts <= 0, multiply by 10:
    # 4*NumGolfCarts - 6*NumPullCarts <= 0
    solver.Add(4 * NumGolfCarts - 6 * NumPullCarts <= 0)
    
    # Objective: Minimize total carts used: NumGolfCarts + NumPullCarts
    solver.Minimize(NumGolfCarts + NumPullCarts)
    
    status = solver.Solve()
    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result["NumGolfCarts"] = NumGolfCarts.solution_value()
        result["NumPullCarts"] = NumPullCarts.solution_value()
        result["objective"] = (NumGolfCarts.solution_value() + NumPullCarts.solution_value())
    else:
        result["error"] = "The problem does not have an optimal solution."
    return result

def solve_model_version2():
    # Model Version 2: Using the alternative rearranged constraint:
    # Golf Cart Ratio Constraint: 2 * NumGolfCarts <= 3 * NumPullCarts
    
    # Create the solver using CBC (for integer programming)
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Solver not created.")
        return None
    
    # Parameters
    capacityGolfCart = 4
    capacityPullCart = 1
    minGuests = 80

    # Decision Variables (using integer values)
    NumGolfCarts = solver.IntVar(0, solver.infinity(), 'NumGolfCarts')
    NumPullCarts = solver.IntVar(0, solver.infinity(), 'NumPullCarts')

    # Constraint 1: Guest Transportation: 4 * NumGolfCarts + 1 * NumPullCarts >= 80
    solver.Add(capacityGolfCart * NumGolfCarts + capacityPullCart * NumPullCarts >= minGuests)
    
    # Constraint 2: Golf Cart Ratio (alternative form): 2 * NumGolfCarts <= 3 * NumPullCarts
    solver.Add(2 * NumGolfCarts <= 3 * NumPullCarts)
    
    # Objective: Minimize total carts used: NumGolfCarts + NumPullCarts
    solver.Minimize(NumGolfCarts + NumPullCarts)
    
    status = solver.Solve()
    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result["NumGolfCarts"] = NumGolfCarts.solution_value()
        result["NumPullCarts"] = NumPullCarts.solution_value()
        result["objective"] = (NumGolfCarts.solution_value() + NumPullCarts.solution_value())
    else:
        result["error"] = "The problem does not have an optimal solution."
    return result

def main():
    print("Results for Model Version 1 (Original Constraint Formulation):")
    result_v1 = solve_model_version1()
    if result_v1 is not None:
        print(result_v1)
    else:
        print("No result for Model Version 1.")
    
    print("\nResults for Model Version 2 (Alternative Rearranged Constraint):")
    result_v2 = solve_model_version2()
    if result_v2 is not None:
        print(result_v2)
    else:
        print("No result for Model Version 2.")

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Results for Model Version 1 (Original Constraint Formulation):
{'NumGolfCarts': 17.0, 'NumPullCarts': 12.0, 'objective': 29.0}

Results for Model Version 2 (Alternative Rearranged Constraint):
{'NumGolfCarts': 17.0, 'NumPullCarts': 12.0, 'objective': 29.0}
'''

'''Expected Output:
Expected solution

: {'variables': {'NumGolfCarts': 17.0, 'NumPullCarts': 12.0}, 'objective': 29.0}'''

