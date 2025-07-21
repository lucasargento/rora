# Problem Description:
'''Problem description: A water salesman collects water from a glacier and transports it in either small or large kegs. A small keg can hold 40 liters of water while a large keg can hold 100 liters of water. The salesman has available at most 30 small kegs and 10 large kegs. Since small kegs are easier to carry, at least twice as may small kegs must be used than large kegs. If he can transport at most 25 kegs total and at least 5 kegs must be large, how many of each should he use to maximize the total amount of glacial water he can transport?

Expected Output Schema:
{
  "variables": {
    "NumSmallKegsUsed": "float",
    "NumLargeKegsUsed": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- Kegs: {Small, Large}

Parameters:
- CapacitySmall: capacity of a small keg in liters = 40 liters
- CapacityLarge: capacity of a large keg in liters = 100 liters
- MaxSmallKegsAvailable: maximum number of small kegs available = 30
- MaxLargeKegsAvailable: maximum number of large kegs available = 10
- MaxTotalKegsTransport: maximum number of kegs that can be transported = 25
- MinLargeKegsRequired: minimum number of large kegs to be used = 5
- MinSmallToLargeRatio: required ratio such that the number of small kegs used is at least twice that of large kegs (i.e., SmallKegsUsed >= 2 * LargeKegsUsed)

Variables:
- NumSmallKegsUsed: number of small kegs to use [integer, 0 <= NumSmallKegsUsed <= MaxSmallKegsAvailable]
- NumLargeKegsUsed: number of large kegs to use [integer, 0 <= NumLargeKegsUsed <= MaxLargeKegsAvailable]

Objective:
- Maximize TotalWaterTransported, where TotalWaterTransported = (CapacitySmall * NumSmallKegsUsed) + (CapacityLarge * NumLargeKegsUsed)
  (The unit is liters)

Constraints:
1. Keg Availability Constraints:
   - NumSmallKegsUsed <= MaxSmallKegsAvailable
   - NumLargeKegsUsed <= MaxLargeKegsAvailable
2. Total Kegs Constraint:
   - NumSmallKegsUsed + NumLargeKegsUsed <= MaxTotalKegsTransport
3. Minimum Large Kegs Constraint:
   - NumLargeKegsUsed >= MinLargeKegsRequired
4. Small-to-Large Ratio Constraint:
   - NumSmallKegsUsed >= MinSmallToLargeRatio * NumLargeKegsUsed

Comments:
- All parameters are in consistent units (kegs for counts and liters for volume).
- The decision variables are modeled as integers although the expected output schema mentions floats; in practice, kegs must be whole numbers.
- The model maximizes the total liters of glacial water that can be transported.

This structured model is self-contained and ready to be implemented in Python or OR-Tools code.'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp
from ortools.sat.python import cp_model

def solve_with_linear_solver():
    # Create the solver using CBC
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Failed to create solver.")
        return None

    # Parameters
    capacity_small = 40
    capacity_large = 100
    max_small = 30
    max_large = 10
    max_total = 25
    min_large = 5
    ratio = 2  # small >= 2 * large

    # Decision Variables (as integers)
    num_small = solver.IntVar(0, max_small, 'NumSmallKegsUsed')
    num_large = solver.IntVar(0, max_large, 'NumLargeKegsUsed')

    # Constraints
    # Total kegs constraint: num_small + num_large <= 25
    solver.Add(num_small + num_large <= max_total)
    # Minimum large kegs required: num_large >= 5
    solver.Add(num_large >= min_large)
    # Small-to-large ratio: num_small >= 2 * num_large
    solver.Add(num_small >= ratio * num_large)

    # Objective: Maximize total water transported
    solver.Maximize(capacity_small * num_small + capacity_large * num_large)

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "variables": {
                "NumSmallKegsUsed": float(num_small.solution_value()),
                "NumLargeKegsUsed": float(num_large.solution_value())
            },
            "objective": float(solver.Objective().Value())
        }
    else:
        result = {"error": "No optimal solution found using Linear Solver."}
    return result

def solve_with_cp_model():
    # Create CP model
    model = cp_model.CpModel()

    # Parameters
    capacity_small = 40
    capacity_large = 100
    max_small = 30
    max_large = 10
    max_total = 25
    min_large = 5
    ratio = 2  # small >= 2 * large

    # Decision Variables (CP-SAT integer variables)
    num_small = model.NewIntVar(0, max_small, 'NumSmallKegsUsed')
    num_large = model.NewIntVar(0, max_large, 'NumLargeKegsUsed')

    # Constraints
    # Total kegs constraint
    model.Add(num_small + num_large <= max_total)
    # Minimum large kegs constraint
    model.Add(num_large >= min_large)
    # Small-to-large ratio
    model.Add(num_small >= ratio * num_large)

    # Objective: maximize total water transported
    total_water = model.NewIntVar(0, capacity_small * max_small + capacity_large * max_large, 'TotalWater')
    model.Add(total_water == capacity_small * num_small + capacity_large * num_large)
    model.Maximize(total_water)

    # Solve the model
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        result = {
            "variables": {
                "NumSmallKegsUsed": float(solver.Value(num_small)),
                "NumLargeKegsUsed": float(solver.Value(num_large))
            },
            "objective": float(solver.Value(total_water))
        }
    else:
        result = {"error": "No optimal solution found using CP-SAT model."}
    return result

def main():
    # Solve using OR-Tools Linear Solver
    linear_solver_result = solve_with_linear_solver()
    
    # Solve using OR-Tools CP-SAT model
    cp_model_result = solve_with_cp_model()
    
    # Print results in a structured way
    print("Solution using OR-Tools Linear Solver:")
    print(linear_solver_result)
    print("\nSolution using OR-Tools CP-SAT Model:")
    print(cp_model_result)

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Solution using OR-Tools Linear Solver:
{'variables': {'NumSmallKegsUsed': 17.0, 'NumLargeKegsUsed': 8.0}, 'objective': 1480.0}

Solution using OR-Tools CP-SAT Model:
{'variables': {'NumSmallKegsUsed': 17.0, 'NumLargeKegsUsed': 8.0}, 'objective': 1480.0}
'''

'''Expected Output:
Expected solution

: {'variables': {'NumSmallKegsUsed': 17.0, 'NumLargeKegsUsed': 8.0}, 'objective': 1480.0}'''

