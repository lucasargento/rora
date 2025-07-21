# Problem Description:
'''Problem description: A gem factory has two drills, a high intensity one and a low intensity one. Each day, the high intensity drill can process 50 gems and requires 50 units of water to dissipate heat. Each day, the low intensity drill can process 30 gems and requires 20 units of water to dissipate heat. Each day the factory must process 800 gems and they have available 700 units of water. Since the high intensity drill produces a lot of noise pollution, at most 40% of the drills can be high intensity ones. Further, at least 10 should be low intensity drills. How many of each drill should be used to minimize the total number of drills needed?

Expected Output Schema:
{
  "variables": {
    "HighDrills": "float",
    "LowDrills": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Below is a complete formulation of the problem using the five-element framework.

--------------------------------------------------
Sets:
- DrillType: {High, Low}
  (We distinguish between high intensity drills and low intensity drills.)

--------------------------------------------------
Parameters:
- gems_per_drill:
  • High = 50 gems per drill per day
  • Low = 30 gems per drill per day
- water_per_drill:
  • High = 50 water units per drill per day
  • Low = 20 water units per drill per day
- gem_target = 800 gems per day (total gems to be processed)
- water_available = 700 water units per day
- max_high_percentage = 0.4
  (At most 40% of the drills used can be high intensity.)
- min_low_drills = 10
  (At least 10 low intensity drills must be used.)
  
  // Note: All water and gem units are assumed to be measured per day.

--------------------------------------------------
Variables:
- HighDrills: integer ≥ 0
  (Number of high intensity drills to use)
- LowDrills: integer ≥ 0
  (Number of low intensity drills to use)

--------------------------------------------------
Objective:
- Minimize total_drills = HighDrills + LowDrills
  (We want to minimize the total number of drills deployed.)

--------------------------------------------------
Constraints:
1. Gem Processing Constraint:
   50 * HighDrills + 30 * LowDrills ≥ gem_target
   (Combined processing capacity must cover at least 800 gems.)

2. Water Usage Constraint:
   50 * HighDrills + 20 * LowDrills ≤ water_available
   (Combined water usage of all drills cannot exceed 700 units.)

3. High Drill Percentage Constraint:
   HighDrills ≤ max_high_percentage * (HighDrills + LowDrills)
   (No more than 40% of the total drills can be high intensity.)

4. Minimum Low Drills Constraint:
   LowDrills ≥ min_low_drills
   (There must be at least 10 low intensity drills.)

--------------------------------------------------
Model Comments:
- The decision variables are defined as integers because they represent counts of drills.
- The gem production and water usage parameters are given per day; therefore, the constraints ensure daily processing meets the gem target without exceeding the available water.
- The constraint on the percentage of high intensity drills is formulated relative to the total number of drills.
- The objective is simply to minimize the total number of drills needed while satisfying all production and resource requirements.
  
--------------------------------------------------
Expected Output Schema (for reference):
{
  "variables": {
    "HighDrills": "integer >= 0",
    "LowDrills": "integer >= 0"
  },
  "objective": "minimize (HighDrills + LowDrills)"
}'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_with_linear_solver():
    # Create the solver using the CBC backend.
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Solver not created.")
        return None

    # Decision Variables:
    # HighDrills and LowDrills are integer variables with lower bound 0.
    HighDrills = solver.IntVar(0, solver.infinity(), 'HighDrills')
    LowDrills = solver.IntVar(0, solver.infinity(), 'LowDrills')

    # Parameters.
    gems_target = 800               # Gems to be processed per day.
    water_available = 700           # Water available per day.
    min_low_drills = 10             # Minimum number of low intensity drills required.
    
    # Gems per drill and water use per drill.
    gems_per_high = 50
    gems_per_low = 30
    water_per_high = 50
    water_per_low = 20

    # Add production constraint (Gems Processing Constraint)
    # 50 * HighDrills + 30 * LowDrills >= 800
    solver.Add(gems_per_high * HighDrills + gems_per_low * LowDrills >= gems_target)

    # Add water usage constraint (Water Usage Constraint).
    # 50 * HighDrills + 20 * LowDrills <= 700
    solver.Add(water_per_high * HighDrills + water_per_low * LowDrills <= water_available)

    # High Drill Percentage Constraint:
    # HighDrills <= 0.4 * (HighDrills + LowDrills)
    # Multiply both sides by 10 to eliminate decimals:
    # 10*HighDrills <= 4*(HighDrills + LowDrills)
    # Simplify: 10*HighDrills - 4*HighDrills - 4*LowDrills <= 0 --> 6*HighDrills - 4*LowDrills <= 0
    solver.Add(6 * HighDrills - 4 * LowDrills <= 0)

    # Minimum low drills constraint.
    # LowDrills >= 10
    solver.Add(LowDrills >= min_low_drills)

    # Objective: minimize total drills = HighDrills + LowDrills
    objective = solver.Objective()
    objective.SetCoefficient(HighDrills, 1)
    objective.SetCoefficient(LowDrills, 1)
    objective.SetMinimization()

    status = solver.Solve()

    result = {}
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        # Collect the solution.
        result["variables"] = {
            "HighDrills": HighDrills.solution_value(),
            "LowDrills": LowDrills.solution_value()
        }
        result["objective"] = objective.Value()
    else:
        result["message"] = "No feasible solution found."

    return result

def main():
    results = {}

    # Solve using the linear solver formulation.
    results["LinearSolver"] = solve_with_linear_solver()

    # Print the results in a structured way.
    print("Optimization Results:")
    for model_name, res in results.items():
        print(f"\nModel: {model_name}")
        if "message" in res:
            print(res["message"])
        else:
            print("Solution:")
            print(f"  HighDrills = {res['variables']['HighDrills']}")
            print(f"  LowDrills  = {res['variables']['LowDrills']}")
            print(f"Objective (Total drills) = {res['objective']}")

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Optimization Results:

Model: LinearSolver
Solution:
  HighDrills = 7.0
  LowDrills  = 15.0
Objective (Total drills) = 22.0
'''

'''Expected Output:
Expected solution

: {'variables': {'HighDrills': 7.0, 'LowDrills': 15.0}, 'objective': 22.0}'''

