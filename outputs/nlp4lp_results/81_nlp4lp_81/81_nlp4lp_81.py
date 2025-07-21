# Problem Description:
'''Problem description: A man on a strict diet only drinks meal replacement drinks from two brands, alpha and omega. The alpha brand drink contains 30 grams of protein, 20 grams of sugar, and 350 calories per bottle. The omega brand drink contains 20 grams of protein, 15 grams of sugar, and 300 calories per bottle. The man wants to get at least 100 grams of protein and 2000 calories. In addition, because the omega brand drink contains tiny amounts of caffeine, at most 35% of the drink should be omega brand. How many bottles of each should he drink to minimize his sugar intake?

Expected Output Schema:
{
  "variables": {
    "QuantityAlpha": "float",
    "QuantityOmega": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- B: set of drink brands = {alpha, omega}

Parameters:
- protein[b]: grams of protein per bottle for brand b, with protein[alpha] = 30 and protein[omega] = 20
- sugar[b]: grams of sugar per bottle for brand b, with sugar[alpha] = 20 and sugar[omega] = 15
- calories[b]: calories per bottle for brand b, with calories[alpha] = 350 and calories[omega] = 300
- required_protein: minimum required protein in grams, 100
- required_calories: minimum required calories, 2000
- max_omega_fraction: maximum allowable fraction of omega bottles, 0.35  
  (Note: This limit is with respect to the total number of bottles consumed)

Variables:
- QuantityAlpha: number of alpha brand bottles to drink (nonnegative integer; units: bottles)
- QuantityOmega: number of omega brand bottles to drink (nonnegative integer; units: bottles)

Objective:
- Minimize total sugar intake = (sugar[alpha] * QuantityAlpha) + (sugar[omega] * QuantityOmega)
  (Units: grams of sugar)

Constraints:
1. Protein requirement:
   (protein[alpha] * QuantityAlpha) + (protein[omega] * QuantityOmega) >= required_protein
2. Calorie requirement:
   (calories[alpha] * QuantityAlpha) + (calories[omega] * QuantityOmega) >= required_calories
3. Omega fraction constraint:
   QuantityOmega <= max_omega_fraction * (QuantityAlpha + QuantityOmega)
   (This ensures that at most 35% of the total bottles are omega brand)

---

Expected Output Schema:
{
  "variables": {
    "QuantityAlpha": "float",
    "QuantityOmega": "float"
  },
  "objective": "float"
}'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_with_linear_solver():
    # Create the MIP solver using CBC.
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Linear solver not available.")
        return None

    # Data
    protein_alpha = 30
    protein_omega = 20
    sugar_alpha = 20
    sugar_omega = 15
    calories_alpha = 350
    calories_omega = 300
    required_protein = 100
    required_calories = 2000
    max_omega_fraction = 0.35

    # Variables: number of bottles for alpha and omega.
    # According to the formulation, these should be nonnegative integers.
    QuantityAlpha = solver.IntVar(0, solver.infinity(), 'QuantityAlpha')
    QuantityOmega = solver.IntVar(0, solver.infinity(), 'QuantityOmega')

    # Objective: Minimize total sugar intake.
    solver.Minimize(sugar_alpha * QuantityAlpha + sugar_omega * QuantityOmega)

    # Constraint 1: Protein requirement.
    solver.Add(protein_alpha * QuantityAlpha + protein_omega * QuantityOmega >= required_protein)

    # Constraint 2: Calorie requirement.
    solver.Add(calories_alpha * QuantityAlpha + calories_omega * QuantityOmega >= required_calories)

    # Constraint 3: Omega fraction constraint.
    # Constraint: QuantityOmega <= max_omega_fraction * (QuantityAlpha + QuantityOmega)
    # Rearranging: QuantityOmega - max_omega_fraction * (QuantityAlpha + QuantityOmega) <= 0
    # => (1 - max_omega_fraction) * QuantityOmega - max_omega_fraction * QuantityAlpha <= 0
    solver.Add((1 - max_omega_fraction) * QuantityOmega - max_omega_fraction * QuantityAlpha <= 0)

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        solution = {
            "variables": {
                "QuantityAlpha": QuantityAlpha.solution_value(),
                "QuantityOmega": QuantityOmega.solution_value()
            },
            "objective": solver.Objective().Value()
        }
        return solution
    elif status == pywraplp.Solver.FEASIBLE:
        print("A feasible solution was found, but it might not be optimal.")
        solution = {
            "variables": {
                "QuantityAlpha": QuantityAlpha.solution_value(),
                "QuantityOmega": QuantityOmega.solution_value()
            },
            "objective": solver.Objective().Value()
        }
        return solution
    else:
        return "The problem does not have any feasible solution"

def main():
    print("Solution using the Linear Solver formulation:")
    linear_solution = solve_with_linear_solver()
    if isinstance(linear_solution, dict):
        print(linear_solution)
    else:
        print(linear_solution)

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Solution using the Linear Solver formulation:
{'variables': {'QuantityAlpha': 4.0, 'QuantityOmega': 2.0}, 'objective': 110.0}
'''

'''Expected Output:
Expected solution

: {'variables': {'QuantityAlpha': 3.909774436090226, 'QuantityOmega': 2.1052631578947367}, 'objective': 109.77443609022556}'''

