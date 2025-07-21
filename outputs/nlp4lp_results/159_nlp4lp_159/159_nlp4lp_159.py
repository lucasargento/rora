# Problem Description:
'''Problem description: A factory transports rice to the city in horse-drawn carts that are either medium or large size. A medium sized cart requires 2 horses and can carry 30 kg of rice. A large sized cart requires 4 horses and can carry 70 kg of rice.  The factory has 60 horses available. Because the horses don't get along well, the number of medium sized carts must be three times the number of large sized carts. In addition, there must be at least 5 medium sized carts and at least 5 large sized carts. How many of each cart size should be used to maximize the amount of rice that can be transported?

Expected Output Schema:
{
  "variables": {
    "NumberMediumCarts": "float",
    "NumberLargeCarts": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- CART_TYPES: {Medium, Large}

Parameters:
- horses_required: a mapping of cart types to the number of horses needed per cart; specifically, horses_required[Medium] = 2 and horses_required[Large] = 4.
- capacity: a mapping of cart types to the kilograms (kg) of rice each cart can transport; specifically, capacity[Medium] = 30 and capacity[Large] = 70.
- total_horses: the total number of horses available = 60.
- medium_to_large_ratio: the factor relating medium carts to large carts = 3 (i.e., NumberMediumCarts = 3 * NumberLargeCarts).
- min_carts: a mapping that defines the minimum number of carts for each type; min_carts[Medium] = 5 and min_carts[Large] = 5.

Variables:
- NumberMediumCarts: integer variable representing the number of medium-sized carts used (units: carts).
- NumberLargeCarts: integer variable representing the number of large-sized carts used (units: carts).

Objective:
- Maximize the total amount of rice transported.
  This is computed as:
    TotalRiceTransported = (capacity[Medium] * NumberMediumCarts) + (capacity[Large] * NumberLargeCarts)

Constraints:
1. Horse Availability Constraint:
   - The total number of horses used by both cart types must not exceed total_horses.
   - Expressed as: (horses_required[Medium] * NumberMediumCarts) + (horses_required[Large] * NumberLargeCarts) <= total_horses

2. Cart Ratio Constraint:
   - The number of medium carts must equal three times the number of large carts.
   - Expressed as: NumberMediumCarts = medium_to_large_ratio * NumberLargeCarts

3. Minimum Cart Constraints:
   - Ensure there are at least the minimum required carts for each type.
   - Expressed as:
       NumberMediumCarts >= min_carts[Medium]
       NumberLargeCarts >= min_carts[Large]'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_with_linear_solver():
    # Create the solver using the CBC backend.
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Solver not created.")
        return None

    # Parameters
    horses_required = {'Medium': 2, 'Large': 4}
    capacity = {'Medium': 30, 'Large': 70}
    total_horses = 60
    medium_to_large_ratio = 3
    min_carts = {'Medium': 5, 'Large': 5}

    # Decision Variables:
    # Number of Medium carts (integer, >= min requirement)
    NumberMediumCarts = solver.IntVar(min_carts['Medium'], solver.infinity(), 'NumberMediumCarts')
    # Number of Large carts (integer, >= min requirement)
    NumberLargeCarts = solver.IntVar(min_carts['Large'], solver.infinity(), 'NumberLargeCarts')

    # Constraint 1: Horse Availability Constraint
    # (2 * NumberMediumCarts) + (4 * NumberLargeCarts) <= 60
    solver.Add(horses_required['Medium'] * NumberMediumCarts +
               horses_required['Large'] * NumberLargeCarts <= total_horses)

    # Constraint 2: Cart Ratio Constraint: NumberMediumCarts = 3 * NumberLargeCarts
    solver.Add(NumberMediumCarts == medium_to_large_ratio * NumberLargeCarts)

    # Constraint 3 is already embedded in the variable lower bounds.

    # Objective: Maximize total rice transported
    # TotalRiceTransported = 30 * NumberMediumCarts + 70 * NumberLargeCarts
    objective = solver.Objective()
    objective.SetCoefficient(NumberMediumCarts, capacity['Medium'])
    objective.SetCoefficient(NumberLargeCarts, capacity['Large'])
    objective.SetMaximization()

    status = solver.Solve()

    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "variables": {
                "NumberMediumCarts": NumberMediumCarts.solution_value(),
                "NumberLargeCarts": NumberLargeCarts.solution_value()
            },
            "objective": objective.Value()
        }
    else:
        print("No optimal solution found.")
        result = None

    return result

def main():
    # Solve the problem using the OR-Tools linear solver
    linear_solver_result = solve_with_linear_solver()

    print("----- Results from OR-Tools Linear Solver -----")
    if linear_solver_result:
        print("Optimal solution:")
        print("NumberMediumCarts =", linear_solver_result["variables"]["NumberMediumCarts"])
        print("NumberLargeCarts =", linear_solver_result["variables"]["NumberLargeCarts"])
        print("Total Rice Transported =", linear_solver_result["objective"])
    else:
        print("No solution found using the linear solver.")

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
----- Results from OR-Tools Linear Solver -----
Optimal solution:
NumberMediumCarts = 18.0
NumberLargeCarts = 6.0
Total Rice Transported = 960.0
'''

'''Expected Output:
Expected solution

: {'variables': {'NumberMediumCarts': 18.0, 'NumberLargeCarts': 6.0}, 'objective': 960.0}'''

