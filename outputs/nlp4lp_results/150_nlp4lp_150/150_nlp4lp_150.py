# Problem Description:
'''Problem description: A recycling company collects recycling from neighborhoods using small and large bins. A small bin requires 2 workers while a large bin requires 5 workers. A small bin can hold 25 units of recycling material and a large bin can hold 60 units of recycling material. The company has available 100 workers. Because most people don't recycle, the number of small bins must be three times the number of large bins. In addition, there must be at least 10 small bins and 4 large bins. How many of each bin type should be used to maximize the total amount of recycling material that can be collected?

Expected Output Schema:
{
  "variables": {
    "NumberSmallBins": "float",
    "NumberLargeBins": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- BINS: {Small, Large}

Parameters:
- workers_per_small: 2 (workers required per small bin)
- workers_per_large: 5 (workers required per large bin)
- capacity_small: 25 (units of recycling material held per small bin)
- capacity_large: 60 (units of recycling material held per large bin)
- total_workers: 100 (available workers)
- ratio_small_to_large: 3 (the number of small bins must equal 3 times the number of large bins)
- min_small: 10 (minimum number of small bins required)
- min_large: 4 (minimum number of large bins required)

Variables:
- NumberSmallBins: integer variable ≥ 0 (number of small bins to deploy)
- NumberLargeBins: integer variable ≥ 0 (number of large bins to deploy)

Objective:
- Maximize total capacity collected = (capacity_small * NumberSmallBins) + (capacity_large * NumberLargeBins)

Constraints:
1. Worker Constraint:
   - workers_per_small * NumberSmallBins + workers_per_large * NumberLargeBins ≤ total_workers
   - In other words: 2 * NumberSmallBins + 5 * NumberLargeBins ≤ 100

2. Ratio Constraint:
   - NumberSmallBins = ratio_small_to_large * NumberLargeBins
   - That is: NumberSmallBins = 3 * NumberLargeBins

3. Minimum Bin Constraints:
   - NumberSmallBins ≥ min_small  →  NumberSmallBins ≥ 10
   - NumberLargeBins ≥ min_large  →  NumberLargeBins ≥ 4

Additional Comments:
- All units are consistent: worker counts (workers/bin) and recycling capacity (units/bin).
- Although the ratio constraint determines NumberSmallBins exactly as three times NumberLargeBins, the lower bounds (10 for small and 4 for large) must be explicitly enforced to ensure feasibility.
- Decision variables are defined as integers since you cannot deploy a fractional bin.

This completes the mathematical model using the five-element framework.'''

# Generated Code:
from ortools.linear_solver import pywraplp

def model_linear():
    # Create the solver using SCIP which supports integer programming
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        print("Linear solver not available.")
        return None

    # Parameters
    workers_per_small = 2
    workers_per_large = 5
    capacity_small = 25
    capacity_large = 60
    total_workers = 100
    ratio_small_to_large = 3
    min_small = 10
    min_large = 4

    # Variables
    # Lower bounds are set using the given minimum constraints
    NumberSmallBins = solver.IntVar(min_small, solver.infinity(), "NumberSmallBins")
    NumberLargeBins = solver.IntVar(min_large, solver.infinity(), "NumberLargeBins")

    # Constraints

    # 1. Worker Constraint: 2 * NumberSmallBins + 5 * NumberLargeBins <= 100
    solver.Add(workers_per_small * NumberSmallBins + workers_per_large * NumberLargeBins <= total_workers)

    # 2. Ratio Constraint: NumberSmallBins = 3 * NumberLargeBins
    solver.Add(NumberSmallBins == ratio_small_to_large * NumberLargeBins)

    # 3. Minimum Bin Constraints are already enforced in variable lower bounds

    # Objective: Maximize total capacity collected
    # Total capacity = (25 * NumberSmallBins) + (60 * NumberLargeBins)
    objective = solver.Objective()
    objective.SetCoefficient(NumberSmallBins, capacity_small)
    objective.SetCoefficient(NumberLargeBins, capacity_large)
    objective.SetMaximization()

    # Solve the problem and return the results in a structured format
    status = solver.Solve()
    result = {}
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        result = {
            "NumberSmallBins": NumberSmallBins.solution_value(),
            "NumberLargeBins": NumberLargeBins.solution_value(),
            "objective": objective.Value()
        }
        print("Model 1 (Linear Optimization) Solution:")
        print(result)
    else:
        print("Model 1 did not find an optimal solution.")
    return result

def main():
    print("Running model(s) for the recycling bins optimization problem:")
    
    # Since only one formulation is provided, we run the linear model.
    sol_linear = model_linear()
    print("\nFinal Solution for Linear Model:")
    print(f"NumberSmallBins: {sol_linear.get('NumberSmallBins')}")
    print(f"NumberLargeBins: {sol_linear.get('NumberLargeBins')}")
    print(f"Objective (Total Capacity Collected): {sol_linear.get('objective')}")

if __name__ == "__main__":
    main()

'''Execution Results:
SUCCESS:
Running model(s) for the recycling bins optimization problem:
Model 1 (Linear Optimization) Solution:
{'NumberSmallBins': 27.0, 'NumberLargeBins': 9.0, 'objective': 1215.0}

Final Solution for Linear Model:
NumberSmallBins: 27.0
NumberLargeBins: 9.0
Objective (Total Capacity Collected): 1215.0
'''

'''Expected Output:
Expected solution

: {'variables': {'NumberSmallBins': 27.0, 'NumberLargeBins': 9.0}, 'objective': 1215.0}'''

