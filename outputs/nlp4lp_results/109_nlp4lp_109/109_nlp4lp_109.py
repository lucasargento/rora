# Problem Description:
'''Problem description: A patient in the hospital can take two different pain killers, pain killer 1 and pain killer 2. Per dose, pain killer 1 delivers 0.5 units of medicine to the legs and 0.8 units of medicine to the back. Per dose, pain killer 2 delivers 0.7 units of medicine to the legs and 0.4 units of medicine to the back. In, addition pain killer 1 deliver 0.3 units of sleeping medicine and pain killer 2 delivers 0.6 units of sleeping medicine. At most 8 units of sleep medicine should be delivered and at least 4 units of medicine should be delivered to the legs. How many doses of each should be taken to maximize the amount of medicine delivered to the back?

Expected Output Schema:
{
  "variables": {
    "NumDoses": {
      "0": "float",
      "1": "float"
    }
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- P: set of pain killers = {1, 2}

Parameters:
- legs_per_dose[p]: medicine units delivered to the legs per dose for pain killer p
  • For pain killer 1: 0.5 [units/dose]
  • For pain killer 2: 0.7 [units/dose]
- back_per_dose[p]: medicine units delivered to the back per dose for pain killer p
  • For pain killer 1: 0.8 [units/dose]
  • For pain killer 2: 0.4 [units/dose]
- sleep_per_dose[p]: sleeping medicine units delivered per dose for pain killer p
  • For pain killer 1: 0.3 [units/dose]
  • For pain killer 2: 0.6 [units/dose]
- max_sleep: maximum allowed sleep medicine = 8 [units]
- min_legs: minimum required legs medicine = 4 [units]

Variables:
- doses[p]: number of doses of pain killer p to be administered [continuous float ≥ 0]
  • doses[1]: doses of pain killer 1
  • doses[2]: doses of pain killer 2

Objective:
- Maximize total back medicine delivered = back_per_dose[1] * doses[1] + back_per_dose[2] * doses[2]

Constraints:
1. Sleep medicine constraint:
   - sleep_per_dose[1] * doses[1] + sleep_per_dose[2] * doses[2] ≤ max_sleep
     (i.e., 0.3 * doses[1] + 0.6 * doses[2] ≤ 8)
2. Legs medicine constraint:
   - legs_per_dose[1] * doses[1] + legs_per_dose[2] * doses[2] ≥ min_legs
     (i.e., 0.5 * doses[1] + 0.7 * doses[2] ≥ 4)

-------------------------------------------------

This completes the model, which is fully consistent and self-contained for implementation in Python or OR-Tools.'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_linear_model():
    # Create the linear solver with the GLOP backend (for LP).
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Solver not available.")
        return None

    # Define variables: doses for pain killer 1 and pain killer 2 (continuous >= 0).
    # We use index 0 for Pain Killer 1 and index 1 for Pain Killer 2.
    doses = {}
    doses[0] = solver.NumVar(0.0, solver.infinity(), 'doses_1')
    doses[1] = solver.NumVar(0.0, solver.infinity(), 'doses_2')

    # Parameters:
    # Medicine delivered per dose (as specified).
    legs_per_dose = {0: 0.5, 1: 0.7}
    back_per_dose = {0: 0.8, 1: 0.4}
    sleep_per_dose = {0: 0.3, 1: 0.6}
    max_sleep = 8.0
    min_legs = 4.0

    # Constraint 1: Sleep medicine constraint.
    # 0.3 * doses[0] + 0.6 * doses[1] <= 8
    sleep_constraint = solver.Add(sleep_per_dose[0]*doses[0] + sleep_per_dose[1]*doses[1] <= max_sleep)

    # Constraint 2: Legs medicine constraint.
    # 0.5 * doses[0] + 0.7 * doses[1] >= 4
    legs_constraint = solver.Add(legs_per_dose[0]*doses[0] + legs_per_dose[1]*doses[1] >= min_legs)

    # Objective: Maximize back medicine delivered = 0.8 * doses[0] + 0.4 * doses[1]
    objective = solver.Objective()
    objective.SetCoefficient(doses[0], back_per_dose[0])
    objective.SetCoefficient(doses[1], back_per_dose[1])
    objective.SetMaximization()

    # Solve the problem.
    status = solver.Solve()

    if status != pywraplp.Solver.OPTIMAL:
        print("The problem does not have an optimal solution.")
        return None

    # Prepare the result in the expected output schema.
    result = {
        "variables": {
            "NumDoses": {
                "0": doses[0].solution_value(),
                "1": doses[1].solution_value()
            }
        },
        "objective": objective.Value()
    }
    return result

def main():
    results = {}
    results['Linear_Solver_Model'] = solve_linear_model()
    
    # If needed to support multiple implementations, each would be added separately.
    # For now, we only have one implementation.
    
    # Print the results in a structured way.
    print("Optimal solutions:")
    for model_name, result in results.items():
        if result is None:
            print(f"{model_name}: No optimal solution found.")
        else:
            print(f"{model_name}:")
            print("  Variables (NumDoses):")
            for index, value in result["variables"]["NumDoses"].items():
                print(f"    Dose for pain killer {int(index)+1}: {value}")
            print(f"  Objective (Total back medicine delivered): {result['objective']}")

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Optimal solutions:
Linear_Solver_Model:
  Variables (NumDoses):
    Dose for pain killer 1: 26.666666666666668
    Dose for pain killer 2: 0.0
  Objective (Total back medicine delivered): 21.333333333333336
'''

'''Expected Output:
Expected solution

: {'variables': {'NumDoses': {'0': 0.0, '1': 11.428571428571429}}, 'objective': 6.857142857142857}'''

