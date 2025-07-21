# Problem Description:
'''Problem description: A researcher is outsourcing annotations and has two options: a specialized third-party or a common third-party annotation company. The specialized company can annotate at a rate of 60 images per hour whereas the common company can annotate at a rate of 40 images per hour. However, the specialized company charges $100 per hour and the common company charges $72 per hour. The researcher has deadlines to meet and must complete a dataset of at least 10,000 images. They also have some special images that only the specialized company can annotate. Therefore, at least a third of work must be allocated to the specialized company. How should the researcher distribute the annotations to the two companies to minimize the cost of annotating the whole dataset?

Expected Output Schema:
{
  "variables": {
    "SpecializedHours": "float",
    "CommonHours": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Below is one clear formulation using the five-element structure.

────────────────────────────
Sets:
- Company: the set of annotation service providers = {Specialized, Common}

────────────────────────────
Parameters:
- specialized_rate = 60          (images per hour, rate at which the specialized company annotates)
- common_rate = 40               (images per hour, rate at which the common company annotates)
- cost_specialized = 100         (USD per hour for the specialized company)
- cost_common = 72               (USD per hour for the common company)
- min_images_total = 10000       (minimum total number of images to be annotated)
- specialized_min_frac = 1/3     (at least one-third of the total annotation work must be handled by the specialized company)

────────────────────────────
Variables:
- SpecializedHours: continuous nonnegative number of hours to be allocated to the specialized company
- CommonHours: continuous nonnegative number of hours to be allocated to the common company

────────────────────────────
Objective:
Minimize total cost = (cost_specialized * SpecializedHours) + (cost_common * CommonHours)
(This minimizes the overall payment in USD for the outsourced annotation work.)

────────────────────────────
Constraints:
1. Total image annotation constraint:
   (specialized_rate * SpecializedHours) + (common_rate * CommonHours) >= min_images_total
   (Ensures that at least 10,000 images are annotated.)
   
2. Specialized work fraction constraint:
   (specialized_rate * SpecializedHours) >= specialized_min_frac * [ (specialized_rate * SpecializedHours) + (common_rate * CommonHours) ]
   (Enforces that at least one-third of the annotated images are done by the specialized company.)
   
   Note: This constraint can be algebraically simplified. Multiplying both sides by 3 gives:
   3 * (specialized_rate * SpecializedHours) >= (specialized_rate * SpecializedHours) + (common_rate * CommonHours)
   For the given rates this is:
   3*60*SpecializedHours >= 60*SpecializedHours + 40*CommonHours  →  180*SpecializedHours >= 60*SpecializedHours + 40*CommonHours
   Subtracting 60*SpecializedHours from both sides:
   120*SpecializedHours >= 40*CommonHours  →  CommonHours <= 3 * SpecializedHours

────────────────────────────
For expected output to be used by the downstream agent, the following JSON is provided:

{
  "variables": {
    "SpecializedHours": "float, continuous >= 0",
    "CommonHours": "float, continuous >= 0"
  },
  "objective": "Minimize total cost = 100*SpecializedHours + 72*CommonHours (USD)"
}

────────────────────────────
Comments:
- The units are consistent: hours for decision variables, images per hour for annotation rates, and USD per hour for costs.
- The specialized work fraction has been modeled directly in terms of images annotated. The equivalent simplified constraint (CommonHours <= 3*SpecializedHours) is also valid.
- This formulation is faithful to the problem description and can be straightforwardly implemented in a typical optimization framework.'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_model1():
    # Model 1: Using the original specialized work fraction constraint.
    # Create the solver using GLOP (linear programming).
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        return None

    # Parameters
    specialized_rate = 60    # images per hour for specialized company
    common_rate = 40         # images per hour for common company
    cost_specialized = 100   # USD per hour for specialized company
    cost_common = 72         # USD per hour for common company
    min_images_total = 10000
    specialized_min_frac = 1/3

    # Variables: hours allocated to each company (non-negative continuous numbers).
    specialized_hours = solver.NumVar(0.0, solver.infinity(), 'SpecializedHours')
    common_hours = solver.NumVar(0.0, solver.infinity(), 'CommonHours')

    # Constraint 1: Total images annotated must be at least min_images_total.
    solver.Add(specialized_rate * specialized_hours + common_rate * common_hours >= min_images_total)

    # Constraint 2 (Model 1): At least one-third of the annotated images must be done by the specialized company.
    # Original formulation: specialized_rate * SpecializedHours >= specialized_min_frac * (specialized_rate * SpecializedHours + common_rate * CommonHours)
    solver.Add(specialized_rate * specialized_hours >= specialized_min_frac * (specialized_rate * specialized_hours + common_rate * common_hours))

    # Objective: Minimize total cost.
    objective = solver.Objective()
    objective.SetCoefficient(specialized_hours, cost_specialized)
    objective.SetCoefficient(common_hours, cost_common)
    objective.SetMinimization()

    status = solver.Solve()

    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result['SpecializedHours'] = specialized_hours.solution_value()
        result['CommonHours'] = common_hours.solution_value()
        result['Objective'] = objective.Value()
    else:
        result['message'] = 'No optimal solution found for Model 1.'
    return result

def solve_model2():
    # Model 2: Using the simplified constraint: CommonHours <= 3 * SpecializedHours.
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        return None

    # Parameters (same as Model 1)
    specialized_rate = 60
    common_rate = 40
    cost_specialized = 100
    cost_common = 72
    min_images_total = 10000

    # Variables
    specialized_hours = solver.NumVar(0.0, solver.infinity(), 'SpecializedHours')
    common_hours = solver.NumVar(0.0, solver.infinity(), 'CommonHours')

    # Constraint 1: Total image annotation constraint.
    solver.Add(specialized_rate * specialized_hours + common_rate * common_hours >= min_images_total)

    # Constraint 2 (Model 2): Simplified specialized fraction constraint:
    # Derived as: CommonHours <= 3 * SpecializedHours
    solver.Add(common_hours <= 3 * specialized_hours)

    # Objective: Minimize total cost.
    objective = solver.Objective()
    objective.SetCoefficient(specialized_hours, cost_specialized)
    objective.SetCoefficient(common_hours, cost_common)
    objective.SetMinimization()

    status = solver.Solve()

    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result['SpecializedHours'] = specialized_hours.solution_value()
        result['CommonHours'] = common_hours.solution_value()
        result['Objective'] = objective.Value()
    else:
        result['message'] = 'No optimal solution found for Model 2.'
    return result

def main():
    result1 = solve_model1()
    result2 = solve_model2()

    print("Optimization Results:")
    print("--------------------------------------------------")
    print("Model 1 (Original Constraint):")
    if 'message' in result1:
        print(result1['message'])
    else:
        print(f"  SpecializedHours: {result1['SpecializedHours']:.4f}")
        print(f"  CommonHours:      {result1['CommonHours']:.4f}")
        print(f"  Total Cost:       {result1['Objective']:.4f} USD")
    print("--------------------------------------------------")
    print("Model 2 (Simplified Constraint):")
    if 'message' in result2:
        print(result2['message'])
    else:
        print(f"  SpecializedHours: {result2['SpecializedHours']:.4f}")
        print(f"  CommonHours:      {result2['CommonHours']:.4f}")
        print(f"  Total Cost:       {result2['Objective']:.4f} USD")
    print("--------------------------------------------------")

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Optimization Results:
--------------------------------------------------
Model 1 (Original Constraint):
  SpecializedHours: 166.6667
  CommonHours:      0.0000
  Total Cost:       16666.6667 USD
--------------------------------------------------
Model 2 (Simplified Constraint):
  SpecializedHours: 166.6667
  CommonHours:      0.0000
  Total Cost:       16666.6667 USD
--------------------------------------------------
'''

'''Expected Output:
Expected solution

: {'variables': {'SpecializedHours': 166.66666666666666, 'CommonHours': 0.0}, 'objective': 16666.666666666664}'''

