# Problem Description:
'''Problem description: A company make both liquid and foam hand sanitizer. Liquid hand sanitizer requires 40 units of water and 50 units of alcohol. Foam hand sanitizer requires 60 units of water and 40 units of alcohol. The company has available 2000 units of water and 2100 units of alcohol. The number of foam hand sanitizers made must exceed the number of liquid hand sanitizers. In addition, at most 30 liquid hand sanitizers can be made. If each liquid hand sanitizer can clean 30 hands and each foam hand sanitizer can clean 20 hands, how many of each should the company make to maximize the number of hands that can be cleaned?

Expected Output Schema:
{
  "variables": {
    "Production": [
      "float"
    ]
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- P: set of hand sanitizer types = {Liquid, Foam}

Parameters:
- water_required: water units required per unit produced, with values:
  - water_required["Liquid"] = 40 units per liquid sanitizer
  - water_required["Foam"] = 60 units per foam sanitizer
- alcohol_required: alcohol units required per unit produced, with values:
  - alcohol_required["Liquid"] = 50 units per liquid sanitizer
  - alcohol_required["Foam"] = 40 units per foam sanitizer
- available_water: total available water = 2000 units
- available_alcohol: total available alcohol = 2100 units
- hands_cleaned_per_unit: number of hands cleaned per unit produced, with values:
  - hands_cleaned_per_unit["Liquid"] = 30 hands per liquid sanitizer
  - hands_cleaned_per_unit["Foam"] = 20 hands per foam sanitizer
- max_liquid: maximum number of liquid hand sanitizers possible = 30

Variables:
- x["Liquid"]: number of liquid hand sanitizers to produce (integer, ≥ 0)
- x["Foam"]: number of foam hand sanitizers to produce (integer, ≥ 0)

Objective:
- Maximize total_hands_cleaned = (hands_cleaned_per_unit["Liquid"] * x["Liquid"]) + (hands_cleaned_per_unit["Foam"] * x["Foam"])
  (Units: hands cleaned)

Constraints:
1. Water availability:
   water_required["Liquid"] * x["Liquid"] + water_required["Foam"] * x["Foam"] ≤ available_water
   i.e., 40*x["Liquid"] + 60*x["Foam"] ≤ 2000
2. Alcohol availability:
   alcohol_required["Liquid"] * x["Liquid"] + alcohol_required["Foam"] * x["Foam"] ≤ available_alcohol
   i.e., 50*x["Liquid"] + 40*x["Foam"] ≤ 2100
3. Production limit for liquid hand sanitizer:
   x["Liquid"] ≤ max_liquid
   i.e., x["Liquid"] ≤ 30
4. Foam production must exceed liquid production:
   x["Foam"] ≥ x["Liquid"] + 1
   (Ensures the number of foam sanitizers is strictly greater than the number of liquid sanitizers)
5. Non-negativity and integrality:
   x["Liquid"] ∈ integers, x["Liquid"] ≥ 0
   x["Foam"] ∈ integers, x["Foam"] ≥ 0

Comments:
- All units are consistent: resource units for water and alcohol, count units for produced sanitizers, and number of hands cleaned.
- The production numbers are assumed to be integer values since you cannot produce a fraction of a sanitizer.
- The constraint x["Foam"] ≥ x["Liquid"] + 1 ensures that foam production strictly exceeds liquid production.

This structured model fully represents the real-world optimization problem.'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_with_linear_solver():
    # Create the mip solver with SCIP backend.
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        print("Solver not created.")
        return None

    # Sets (for clarity in naming)
    P_liquid = "Liquid"
    P_foam = "Foam"

    # Parameters
    water_required = {P_liquid: 40, P_foam: 60}
    alcohol_required = {P_liquid: 50, P_foam: 40}
    available_water = 2000
    available_alcohol = 2100
    hands_cleaned_per_unit = {P_liquid: 30, P_foam: 20}
    max_liquid = 30

    # Variables: integer production of hand sanitizers.
    x_liquid = solver.IntVar(0, max_liquid, 'x_liquid')
    # For foam, the upper bound can be set high enough (e.g., available_water / water_required["Foam"])
    x_foam = solver.IntVar(0, solver.infinity(), 'x_foam')

    # Constraints
    # 1. Water availability: 40*x_liquid + 60*x_foam <= 2000
    solver.Add(water_required[P_liquid] * x_liquid + water_required[P_foam] * x_foam <= available_water)

    # 2. Alcohol availability: 50*x_liquid + 40*x_foam <= 2100
    solver.Add(alcohol_required[P_liquid] * x_liquid + alcohol_required[P_foam] * x_foam <= available_alcohol)

    # 3. The liquid production upper bound is already enforced in variable creation.
    # 4. Foam production must exceed liquid production: x_foam >= x_liquid + 1
    solver.Add(x_foam >= x_liquid + 1)

    # Objective: Maximize total hands cleaned: 30*x_liquid + 20*x_foam
    objective = solver.Objective()
    objective.SetCoefficient(x_liquid, hands_cleaned_per_unit[P_liquid])
    objective.SetCoefficient(x_foam, hands_cleaned_per_unit[P_foam])
    objective.SetMaximization()

    # Solve the problem
    status = solver.Solve()

    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result['status'] = "OPTIMAL"
        result['variables'] = {
            "Production": {
                P_liquid: x_liquid.solution_value(),
                P_foam: x_foam.solution_value()
            }
        }
        result['objective'] = objective.Value()
    elif status == pywraplp.Solver.FEASIBLE:
        result['status'] = "FEASIBLE"
        result['message'] = "A feasible solution was found, but it may not be optimal."
    else:
        result['status'] = "INFEASIBLE"
        result['message'] = "No solution exists for the given problem."

    return result

def main():
    # Since the formulation provided is unique, we only implement one version using the linear solver.
    results_linear = solve_with_linear_solver()

    # Presenting results in a structured manner:
    print("=== Linear Solver Optimization Results ===")
    if results_linear:
        if results_linear.get('status') == "OPTIMAL":
            production = results_linear['variables']['Production']
            print(f"Status    : {results_linear['status']}")
            print(f"Liquid Production: {production['Liquid']}")
            print(f"Foam Production  : {production['Foam']}")
            print(f"Max Hands Cleaned: {results_linear['objective']}")
        else:
            print(results_linear.get('message', 'No valid result available.'))
    else:
        print("No result returned from the linear solver.")

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
=== Linear Solver Optimization Results ===
Status    : OPTIMAL
Liquid Production: 19.0
Foam Production  : 20.0
Max Hands Cleaned: 970.0
'''

'''Expected Output:
Expected solution

: {'variables': {'Production': [42.0, 0.0]}, 'objective': 1260.0}'''

