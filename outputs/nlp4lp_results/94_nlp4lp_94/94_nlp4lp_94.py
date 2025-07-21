# Problem Description:
'''Problem description: Both fertilizer and seeds need to be added to a lawn. One unit of fertilizer takes 0.5 minutes to be effective while one unit of seeds takes 1.5 minutes to be effective. There can be at most 300 units of fertilizer and seeds combined added to the lawn. In addition at least 50 units of fertilizer need to be added. Since the lawn is really patchy, there can be at most twice the amount of fertilizer as seeds. How many units of each should be added to minimize the total time it takes for the lawn to be ready?

Expected Output Schema:
{
  "variables": {
    "FertilizerUnits": "float",
    "SeedsUnits": "float",
    "TotalTime": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- Ingredient: A set representing the two types of lawn treatment inputs = {Fertilizer, Seeds}

Parameters:
- time_per_fertilizer: 0.5 (minutes per unit of Fertilizer)
- time_per_seeds: 1.5 (minutes per unit of Seeds)
- max_total_units: 300 (maximum combined units of Fertilizer and Seeds allowed)
- min_fertilizer_units: 50 (minimum units of Fertilizer required)
- fertilizer_to_seeds_ratio: 2 (Fertilizer units can be at most twice the Seeds units)

Variables:
- FertilizerUnits: continuous variable representing the number of Fertilizer units to add (units, ≥ 0)
- SeedsUnits: continuous variable representing the number of Seeds units to add (units, ≥ 0)
- TotalTime: continuous variable representing the total time required for the lawn to be ready (minutes)

Objective:
- Minimize TotalTime, which is computed as (time_per_fertilizer * FertilizerUnits) + (time_per_seeds * SeedsUnits)

Constraints:
1. Total Units Constraint: FertilizerUnits + SeedsUnits ≤ max_total_units  
   (Ensures that the combined units of inputs do not exceed 300 units)

2. Minimum Fertilizer Constraint: FertilizerUnits ≥ min_fertilizer_units  
   (Guarantees that at least 50 units of Fertilizer are added)

3. Fertilizer-to-Seeds Ratio Constraint: FertilizerUnits ≤ fertilizer_to_seeds_ratio * SeedsUnits  
   (Limits the Fertilizer to at most twice the number of Seeds)

Additional Model Comments:
- All units are assumed to be in the same measurement (units for inputs and minutes for time), ensuring consistency.  
- The decision variables are treated as continuous because fractional units may be acceptable unless the context requires integer amounts.  
- TotalTime is a calculated quantity that directly reflects the weighted sum of the units selected for each treatment input.'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_model_A():
    # Model A: Introduce an explicit TotalTime variable.
    # Create the linear solver using GLOP (continuous LP solver)
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Solver not created for Model A.")
        return None

    # Variables
    # FertilizerUnits: at least 50
    fertilizer = solver.NumVar(50.0, solver.infinity(), "FertilizerUnits")
    # SeedsUnits: non-negative (no explicit lower bound besides 0)
    seeds = solver.NumVar(0.0, solver.infinity(), "SeedsUnits")
    # TotalTime: explicitly defined variable that equals 0.5 * fertilizer + 1.5 * seeds.
    total_time = solver.NumVar(0.0, solver.infinity(), "TotalTime")
    
    # Constraints
    # 1. Total Units Constraint: FertilizerUnits + SeedsUnits <= 300
    solver.Add(fertilizer + seeds <= 300.0)
    
    # 2. Minimum Fertilizer Constraint:
    # Already set fertilizer lower bound = 50 on variable creation
    
    # 3. Fertilizer-to-Seeds Ratio Constraint: FertilizerUnits <= 2 * SeedsUnits
    solver.Add(fertilizer <= 2 * seeds)
    
    # Constraint to define TotalTime
    solver.Add(total_time == 0.5 * fertilizer + 1.5 * seeds)
    
    # Objective: Minimize TotalTime
    objective = solver.Objective()
    objective.SetCoefficient(total_time, 1)
    objective.SetMinimization()
    
    status = solver.Solve()
    
    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "FertilizerUnits": fertilizer.solution_value(),
            "SeedsUnits": seeds.solution_value(),
            "TotalTime": total_time.solution_value(),
            "objective": objective.Value()
        }
        return result
    else:
        print("No optimal solution found in Model A.")
        return None

def solve_model_B():
    # Model B: Do not explicitly create a TotalTime variable.
    # Instead, compute objective as 0.5 * FertilizerUnits + 1.5 * SeedsUnits.
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Solver not created for Model B.")
        return None

    # Variables
    fertilizer = solver.NumVar(50.0, solver.infinity(), "FertilizerUnits")
    seeds = solver.NumVar(0.0, solver.infinity(), "SeedsUnits")
    
    # Constraints
    solver.Add(fertilizer + seeds <= 300.0)
    solver.Add(fertilizer <= 2 * seeds)
    
    # Objective: Minimize (0.5 * fertilizer + 1.5 * seeds)
    objective = solver.Objective()
    objective.SetCoefficient(fertilizer, 0.5)
    objective.SetCoefficient(seeds, 1.5)
    objective.SetMinimization()
    
    status = solver.Solve()
    
    if status == pywraplp.Solver.OPTIMAL:
        # Manually calculate TotalTime as the objective function value.
        total_time_value = 0.5 * fertilizer.solution_value() + 1.5 * seeds.solution_value()
        result = {
            "FertilizerUnits": fertilizer.solution_value(),
            "SeedsUnits": seeds.solution_value(),
            "TotalTime": total_time_value,
            "objective": objective.Value()
        }
        return result
    else:
        print("No optimal solution found in Model B.")
        return None

def main():
    print("Solving using Model A (with explicit TotalTime variable):")
    model_a_result = solve_model_A()
    if model_a_result:
        print({
            "model": "A",
            "variables": {
                "FertilizerUnits": model_a_result["FertilizerUnits"],
                "SeedsUnits": model_a_result["SeedsUnits"],
                "TotalTime": model_a_result["TotalTime"]
            },
            "objective": model_a_result["objective"]
        })
    else:
        print("Model A: Infeasible problem.")
    
    print("\nSolving using Model B (computing TotalTime implicitly):")
    model_b_result = solve_model_B()
    if model_b_result:
        print({
            "model": "B",
            "variables": {
                "FertilizerUnits": model_b_result["FertilizerUnits"],
                "SeedsUnits": model_b_result["SeedsUnits"],
                "TotalTime": model_b_result["TotalTime"]
            },
            "objective": model_b_result["objective"]
        })
    else:
        print("Model B: Infeasible problem.")

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Solving using Model A (with explicit TotalTime variable):
{'model': 'A', 'variables': {'FertilizerUnits': 50.0, 'SeedsUnits': 25.0, 'TotalTime': 62.5}, 'objective': 62.5}

Solving using Model B (computing TotalTime implicitly):
{'model': 'B', 'variables': {'FertilizerUnits': 50.0, 'SeedsUnits': 25.0, 'TotalTime': 62.5}, 'objective': 62.5}
'''

'''Expected Output:
Expected solution

: {'variables': {'FertilizerUnits': 50.0, 'SeedsUnits': 25.0, 'TotalTime': 37.5}, 'objective': 37.5}'''

