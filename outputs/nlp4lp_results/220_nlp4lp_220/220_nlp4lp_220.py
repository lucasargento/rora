# Problem Description:
'''Problem description: A mask making company ships masks to their retail stores using small boxes and large boxes. A small box holds 25 masks whereas a large box holds 45 masks. Since small boxes are easier to stack and will be used first to stock stores, there must be at least three times as many small boxes as large boxes. Additionally, at least 5 large boxes must be used. If at least 750 masks are required to be distributed, how many of each size of box should be used to minimize the total number of boxes needed?

Expected Output Schema:
{
  "variables": {
    "NumberSmallBoxes": "float",
    "NumberLargeBoxes": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- BoxTypes = {Small, Large}

Parameters:
- small_box_capacity = 25      // Each small box holds 25 masks (masks per box)
- large_box_capacity = 45      // Each large box holds 45 masks (masks per box)
- min_large_boxes = 5          // At least 5 large boxes must be used (boxes)
- min_total_masks = 750        // At least 750 masks must be distributed (masks)
- ratio_small_to_large = 3     // There must be at least three times as many small boxes as large boxes

Variables:
- NumberSmallBoxes: integer, >= 0    // Number of small boxes used
- NumberLargeBoxes: integer, >= 0    // Number of large boxes used

Objective:
- Minimize total boxes used =
  NumberSmallBoxes + NumberLargeBoxes

Constraints:
1. Capacity constraint (mask requirement):
   small_box_capacity * NumberSmallBoxes + large_box_capacity * NumberLargeBoxes >= min_total_masks
   (i.e., 25 * NumberSmallBoxes + 45 * NumberLargeBoxes >= 750)

2. Ratio constraint (use small boxes first):
   NumberSmallBoxes >= ratio_small_to_large * NumberLargeBoxes
   (i.e., NumberSmallBoxes >= 3 * NumberLargeBoxes)

3. Minimum large boxes constraint:
   NumberLargeBoxes >= min_large_boxes
   (i.e., NumberLargeBoxes >= 5)

------------------------------------------------------------
Expected Output Schema:
{
  "variables": {
    "NumberSmallBoxes": "float",
    "NumberLargeBoxes": "float"
  },
  "objective": "float"
}'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_model_version1():
    # Create the MIP solver with SCIP backend.
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        print("Solver not created.")
        return None

    # Parameters
    small_box_capacity = 25
    large_box_capacity = 45
    min_large_boxes = 5
    min_total_masks = 750
    ratio_small_to_large = 3

    # Variables: integer non-negative variables.
    NumberSmallBoxes = solver.IntVar(0, solver.infinity(), 'NumberSmallBoxes')
    NumberLargeBoxes = solver.IntVar(0, solver.infinity(), 'NumberLargeBoxes')

    # Constraint 1: Total mask capacity requirement.
    # 25 * NumberSmallBoxes + 45 * NumberLargeBoxes >= 750
    solver.Add(small_box_capacity * NumberSmallBoxes + large_box_capacity * NumberLargeBoxes >= min_total_masks)

    # Constraint 2: Ratio constraint: There must be at least three times as many small boxes as large boxes.
    solver.Add(NumberSmallBoxes >= ratio_small_to_large * NumberLargeBoxes)

    # Constraint 3: At least 5 large boxes must be used.
    solver.Add(NumberLargeBoxes >= min_large_boxes)

    # Objective: Minimize total number of boxes used.
    objective = solver.Objective()
    objective.SetCoefficient(NumberSmallBoxes, 1)
    objective.SetCoefficient(NumberLargeBoxes, 1)
    objective.SetMinimization()

    # Solve the model.
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "variables": {
                "NumberSmallBoxes": NumberSmallBoxes.solution_value(),
                "NumberLargeBoxes": NumberLargeBoxes.solution_value()
            },
            "objective": objective.Value()
        }
        return result
    elif status == pywraplp.Solver.FEASIBLE:
        print("A feasible solution was found, but it might not be optimal.")
        result = {
            "variables": {
                "NumberSmallBoxes": NumberSmallBoxes.solution_value(),
                "NumberLargeBoxes": NumberLargeBoxes.solution_value()
            },
            "objective": objective.Value()
        }
        return result
    else:
        print("The problem does not have an optimal solution.")
        return None

def main():
    # Since our mathematical formulation gives only one version,
    # we call the single implementation model.
    solution_v1 = solve_model_version1()

    # Print the solution in structured way.
    if solution_v1 is not None:
        print("Version 1 (Linear Programming Model) Optimal Solution:")
        print(solution_v1)
    else:
        print("No optimal solution found for Version 1.")

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Version 1 (Linear Programming Model) Optimal Solution:
{'variables': {'NumberSmallBoxes': 21.0, 'NumberLargeBoxes': 5.0}, 'objective': 26.0}
'''

'''Expected Output:
Expected solution

: {'variables': {'NumberSmallBoxes': 21.0, 'NumberLargeBoxes': 5.0}, 'objective': 26.0}'''

