# Problem Description:
'''Problem description: A mine sends ore to the surface in small and large wagons. A small wagon hold 20 units of ore while a large wagon holds 50 units of ore. To avoid taking up too much space on the ramps, the number of small wagons must be at least twice as much as the number or large wagons. In addition, at least 10 large wagons must be used. If 2000 units of ore need to taken to the surface, minimize the total number of wagons needed.

Expected Output Schema:
{
  "variables": {
    "SmallWagons": "float",
    "LargeWagons": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''{
  "Sets": {
    "WagonTypes": ["Small", "Large"]
  },
  "Parameters": {
    "capacitySmall": 20,         // units of ore per small wagon
    "capacityLarge": 50,         // units of ore per large wagon
    "totalOre": 2000,            // total ore (in units) to be transported
    "minRatio": 2,               // minimum ratio: number of small wagons must be at least twice the number of large wagons
    "minLarge": 10               // minimum number of large wagons required
  },
  "Variables": {
    "SmallWagons": "integer >= 0",  // number of small wagons used
    "LargeWagons": "integer >= 0"   // number of large wagons used
  },
  "Objective": "Minimize total wagons = SmallWagons + LargeWagons",
  "Constraints": [
    "Ore capacity constraint: capacitySmall * SmallWagons + capacityLarge * LargeWagons = totalOre",
    "Ramp space constraint: SmallWagons >= minRatio * LargeWagons",
    "Minimum large wagons constraint: LargeWagons >= minLarge"
  ]
}'''

# Generated Code:
from ortools.linear_solver import pywraplp

def solve_linear_model():
    # Create the CBC solver.
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("CBC solver not available.")
        return None

    # Variables: integer, greater or equal to 0.
    # SmallWagons: number of small wagons used.
    # LargeWagons: number of large wagons used.
    small = solver.IntVar(0, solver.infinity(), 'SmallWagons')
    large = solver.IntVar(0, solver.infinity(), 'LargeWagons')

    # Parameters.
    capacitySmall = 20      # ore capacity per small wagon
    capacityLarge = 50      # ore capacity per large wagon
    totalOre = 2000         # total ore units to be transported
    minRatio = 2            # small wagons must be at least twice the large wagons
    minLarge = 10           # at least 10 large wagons required

    # Constraints.
    # 1. Ore capacity constraint: 20*SmallWagons + 50*LargeWagons == 2000.
    solver.Add(capacitySmall * small + capacityLarge * large == totalOre)
    # 2. Ramp space constraint: SmallWagons >= 2 * LargeWagons.
    solver.Add(small >= minRatio * large)
    # 3. Minimum large wagons constraint: LargeWagons >= 10.
    solver.Add(large >= minLarge)

    # Objective: minimize total number of wagons.
    solver.Minimize(small + large)

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "SmallWagons": small.solution_value(),
            "LargeWagons": large.solution_value(),
            "objective": solver.Objective().Value()
        }
        return result
    else:
        print("The problem does not have an optimal solution.")
        return None

def main():
    # Only one formulation is provided; so we solve one implementation.
    solution = solve_linear_model()

    print("Results for the Mixed Integer Linear Programming model:")
    if solution:
        print("SmallWagons =", solution["SmallWagons"])
        print("LargeWagons =", solution["LargeWagons"])
        print("Total number of wagons =", solution["objective"])

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Results for the Mixed Integer Linear Programming model:
SmallWagons = 45.0
LargeWagons = 22.0
Total number of wagons = 67.0
'''

'''Expected Output:
Expected solution

: {'variables': {'SmallWagons': 45.0, 'LargeWagons': 22.0}, 'objective': 67.0}'''

