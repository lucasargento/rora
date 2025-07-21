# Problem Description:
'''Problem description: A hot dog company can build two types of butcher shops, a small shop and a large shop. A small shop can make 30 hot dogs per day and requires 2 workers. A large shop can make 70 hot dogs per day and requires 4 workers. The company must make at least 500 hot dogs per day but they only have available 30 workers. How many of each butcher shop should the company build to minimize the total number of butcher shops?

Expected Output Schema:
{
  "variables": {
    "NumberOfSmallShops": "float",
    "NumberOfLargeShops": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- S: set of shop types = {Small, Large}

Parameters:
- hotDogs_per_day[Small] = 30 (hot dogs produced per day by a small shop)
- hotDogs_per_day[Large] = 70 (hot dogs produced per day by a large shop)
- workers_per_shop[Small] = 2 (workers required for a small shop)
- workers_per_shop[Large] = 4 (workers required for a large shop)
- min_hotDogs = 500 (minimum required hot dogs per day)
- available_workers = 30 (total available workers)

Variables:
- NumberOfSmallShops: integer ≥ 0 (number of small shops to build)
- NumberOfLargeShops: integer ≥ 0 (number of large shops to build)

Objective:
- Minimize total number of shops = NumberOfSmallShops + NumberOfLargeShops

Constraints:
1. Production Constraint: 
   30 * NumberOfSmallShops + 70 * NumberOfLargeShops ≥ min_hotDogs
2. Worker Constraint: 
   2 * NumberOfSmallShops + 4 * NumberOfLargeShops ≤ available_workers

Comments:
- All units are consistent (hot dogs/day, workers are counted per shop).
- The decision variables are integers since you cannot build a fraction of a shop.
- The model seeks to minimize the total number of shops while meeting daily hot dog production and labor availability requirements.

Expected Output Schema:
{
  "variables": {
    "NumberOfSmallShops": "integer >= 0",
    "NumberOfLargeShops": "integer >= 0"
  },
  "objective": "minimize NumberOfSmallShops + NumberOfLargeShops"
}'''

# Generated Code:
from ortools.linear_solver import pywraplp

def run_linear_solver_model():
    # Create the MIP solver with the CBC backend.
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Solver not created.")
        return None

    # Parameters
    hotDogs_small = 30  # hot dogs produced per day by a small shop
    hotDogs_large = 70  # hot dogs produced per day by a large shop
    workers_small = 2   # workers required per small shop
    workers_large = 4   # workers required per large shop
    min_hotDogs = 500   # minimum required hot dogs per day
    available_workers = 30  # total available workers

    # Variables: integer >= 0.
    NumberOfSmallShops = solver.IntVar(0, solver.infinity(), 'NumberOfSmallShops')
    NumberOfLargeShops = solver.IntVar(0, solver.infinity(), 'NumberOfLargeShops')

    # Constraint 1: Production Constraint
    solver.Add(hotDogs_small * NumberOfSmallShops + hotDogs_large * NumberOfLargeShops >= min_hotDogs)

    # Constraint 2: Worker Constraint
    solver.Add(workers_small * NumberOfSmallShops + workers_large * NumberOfLargeShops <= available_workers)

    # Objective: Minimize total number of shops.
    solver.Minimize(NumberOfSmallShops + NumberOfLargeShops)

    # Solve the model.
    status = solver.Solve()

    # Prepare solution output.
    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "variables": {
                "NumberOfSmallShops": NumberOfSmallShops.solution_value(),
                "NumberOfLargeShops": NumberOfLargeShops.solution_value()
            },
            "objective": NumberOfSmallShops.solution_value() + NumberOfLargeShops.solution_value()
        }
        print("Linear Solver Model Solution:")
        print("Status: OPTIMAL")
        print("NumberOfSmallShops =", NumberOfSmallShops.solution_value())
        print("NumberOfLargeShops =", NumberOfLargeShops.solution_value())
        print("Total shops (Objective) =", result["objective"])
    else:
        print("The problem does not have an optimal solution.")

    return result

def main():
    # Since only one formulation is given in the problem description,
    # we only implement one version using ortools.linear_solver.
    results = {}
    
    # Run the linear solver based optimization.
    results['LinearSolver'] = run_linear_solver_model()
    
    # Print structured output results for both implementations elegantly.
    print("\nFinal Structured Output:")
    print(results)

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Linear Solver Model Solution:
Status: OPTIMAL
NumberOfSmallShops = 1.0
NumberOfLargeShops = 7.0
Total shops (Objective) = 8.0

Final Structured Output:
{'LinearSolver': {'variables': {'NumberOfSmallShops': 1.0, 'NumberOfLargeShops': 7.0}, 'objective': 8.0}}
'''

'''Expected Output:
Expected solution

: {'variables': {'NumberOfSmallShops': 1.0, 'NumberOfLargeShops': 7.0}, 'objective': 8.0}'''

