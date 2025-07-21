# Problem Description:
'''Problem description: A grape farmer transports his grapes in either small crates or large crates. A small crate can take 200 grapes while a large crate can take 500.  Because his customers prefer smaller crates, at least 3 times as many small crates must be used than large crates. The farmer has available at most 100 small crates and at most 50 large crates. In addition, his truck can take at most 60 crates total and he must use at least 10 large crates. How many of each crate should he use to maximize the total number of grapes he can transport?

Expected Output Schema:
{
  "variables": {
    "NumSmallCrates": "float",
    "NumLargeCrates": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Below is a complete structured reformulation of the problem following the five-element framework.

-------------------------------------------------------------
Sets:
- C: set of crate types = {Small, Large}

-------------------------------------------------------------
Parameters:
- capacity_small: number of grapes a small crate can hold = 200 (grapes per crate)
- capacity_large: number of grapes a large crate can hold = 500 (grapes per crate)
- max_small: maximum number of small crates available = 100 (crates)
- max_large: maximum number of large crates available = 50 (crates)
- truck_capacity: maximum total number of crates the truck can carry = 60 (crates)
- min_large: minimum number of large crates required = 10 (crates)
- ratio: required ratio such that the number of small crates is at least 3 times the number of large crates = 3 (dimensionless)

-------------------------------------------------------------
Variables:
- NumSmallCrates: number of small crates used [integer ≥ 0] (crates)
- NumLargeCrates: number of large crates used [integer ≥ 0] (crates)

-------------------------------------------------------------
Objective:
- Maximize TotalGrapes: total number of grapes transported
  Expression: TotalGrapes = capacity_small * NumSmallCrates + capacity_large * NumLargeCrates

-------------------------------------------------------------
Constraints:
1. Small crate availability:
   NumSmallCrates ≤ max_small

2. Large crate availability:
   NumLargeCrates ≤ max_large

3. Truck capacity constraint:
   NumSmallCrates + NumLargeCrates ≤ truck_capacity

4. Customer preference ratio constraint:
   NumSmallCrates ≥ ratio * NumLargeCrates

5. Minimum large crates requirement:
   NumLargeCrates ≥ min_large

-------------------------------------------------------------

Comments:
- All parameters use consistent units: crate counts for availability and truck capacity, and grapes per crate for capacities.
- Although the model treats the decision variables as integers (since crates are discrete items), the variables are declared as integer in an implementation to ensure feasibility.
- This model directly maximizes the total grapes transported while respecting both physical constraints (crate availability, truck load) and market preferences (more small crates than large).

This five-element formulation is complete, self-contained, and directly mappable to Python or OR-Tools.'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_model_linear():
    # Create the linear solver with the CBC backend.
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Could not create solver.")
        return None

    # Parameters
    capacity_small = 200         # Grapes per small crate
    capacity_large = 500         # Grapes per large crate
    max_small = 100              # Maximum small crates available
    max_large = 50               # Maximum large crates available
    truck_capacity = 60          # Maximum total crates the truck can transport
    min_large = 10               # Minimum large crates that must be used
    ratio = 3                    # At least 'ratio' times as many small crates as large crates

    # Decision Variables
    # NumSmallCrates: integer in [0, max_small]
    # NumLargeCrates: integer in [min_large, max_large] - note min_large is set as the lower bound per constraint
    num_small = solver.IntVar(0, max_small, "NumSmallCrates")
    num_large = solver.IntVar(min_large, max_large, "NumLargeCrates")

    # Constraints

    # 1. Truck capacity constraint: total number of crates cannot exceed truck's capacity.
    solver.Add(num_small + num_large <= truck_capacity)

    # 2. Customer preference ratio: number of small crates must be at least 'ratio' times the large crates.
    solver.Add(num_small >= ratio * num_large)

    # (Availability constraints are automatically handled by the bounds on num_small and num_large.)

    # Objective: Maximize the total grapes transported.
    # Expression: capacity_small * num_small + capacity_large * num_large
    solver.Maximize(capacity_small * num_small + capacity_large * num_large)

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        # Construct and return the result in the required schema.
        result = {
            "variables": {
                "NumSmallCrates": num_small.solution_value(),
                "NumLargeCrates": num_large.solution_value()
            },
            "objective": solver.Objective().Value()
        }
        return result
    else:
        print("The problem does not have an optimal solution.")
        return None

def main():
    # Since only one mathematical formulation is provided, we implement one model using the linear solver.
    result_linear = solve_model_linear()

    # Display results in a structured way.
    print("===== Linear/MIP Model Optimal Solution =====")
    if result_linear:
        print("Variables:")
        print("  NumSmallCrates =", result_linear["variables"]["NumSmallCrates"])
        print("  NumLargeCrates =", result_linear["variables"]["NumLargeCrates"])
        print("Objective:")
        print("  Total Grapes Transported =", result_linear["objective"])
    else:
        print("No optimal solution found for the linear model.")

if __name__ == "__main__":
    main()

'''Execution Results:
SUCCESS:
===== Linear/MIP Model Optimal Solution =====
Variables:
  NumSmallCrates = 45.0
  NumLargeCrates = 15.0
Objective:
  Total Grapes Transported = 16500.0
'''

'''Expected Output:
Expected solution

: {'variables': {'NumSmallCrates': 45.0, 'NumLargeCrates': 15.0}, 'objective': 16500.0}'''

