# Problem Description:
'''Problem description: A honey farmer sells his honey in glass and plastic jars. A glass jar can hold 250 ml of honey while a plastic jar can hold 300 ml of honey. Since glass jars are more expensive, at least twice as many plastic jars must be filled as glass jars. However, at least 20 glass jars should be filled. If the farmer has 20000 ml of honey, how many jars of each should be filled to maximize the total number of bottles filled?

Expected Output Schema:
{
  "variables": {
    "GlassJarsFilled": "float",
    "PlasticJarsFilled": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Below is the complete structured model using the five-element framework.

-------------------------------------------------

Sets:
- Jars: {Glass, Plastic}

Parameters:
- glass_capacity: capacity of one glass jar (250 ml per jar)
- plastic_capacity: capacity of one plastic jar (300 ml per jar)
- total_honey: total available honey (20000 ml)
- min_glass: minimum number of glass jars that must be filled (20 jars)
- plastic_to_glass_ratio: minimum ratio of plastic to glass jars that must be filled (at least 2 plastic jars per glass jar)

Variables:
- GlassJarsFilled: number of glass jars filled [integer, ≥ 0]
- PlasticJarsFilled: number of plastic jars filled [integer, ≥ 0]

Objective:
- Maximize the total jars filled = GlassJarsFilled + PlasticJarsFilled

Constraints:
1. Honey Availability Constraint:
   (glass_capacity * GlassJarsFilled) + (plastic_capacity * PlasticJarsFilled) ≤ total_honey
   i.e., 250 * GlassJarsFilled + 300 * PlasticJarsFilled ≤ 20000

2. Ratio Constraint:
   PlasticJarsFilled ≥ plastic_to_glass_ratio * GlassJarsFilled
   i.e., PlasticJarsFilled ≥ 2 * GlassJarsFilled

3. Minimum Glass Jars Requirement:
   GlassJarsFilled ≥ min_glass
   i.e., GlassJarsFilled ≥ 20

-------------------------------------------------

Below is a JSON representation of the variables and objective as specified:

{
  "variables": {
    "GlassJarsFilled": "float",
    "PlasticJarsFilled": "float"
  },
  "objective": "maximize (GlassJarsFilled + PlasticJarsFilled)"
}'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_linear_model():
    # Create the solver using CBC (an open-source MILP solver)
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Solver not created.")
        return None

    # -------------------------
    # Define variables
    # -------------------------
    # GlassJarsFilled and PlasticJarsFilled are integer variables (>= 0)
    glass = solver.IntVar(0, solver.infinity(), 'GlassJarsFilled')
    plastic = solver.IntVar(0, solver.infinity(), 'PlasticJarsFilled')

    # -------------------------
    # Add constraints
    # -------------------------
    # Constraint 1: Honey Availability Constraint
    # 250 * GlassJarsFilled + 300 * PlasticJarsFilled <= 20000
    solver.Add(250 * glass + 300 * plastic <= 20000)

    # Constraint 2: Ratio Constraint
    # PlasticJarsFilled >= 2 * GlassJarsFilled
    solver.Add(plastic >= 2 * glass)

    # Constraint 3: Minimum Glass Jars Requirement
    # GlassJarsFilled >= 20
    solver.Add(glass >= 20)

    # -------------------------
    # Define objective
    # -------------------------
    # Maximize (GlassJarsFilled + PlasticJarsFilled)
    solver.Maximize(glass + plastic)

    # -------------------------
    # Solve the model
    # -------------------------
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        return {
            "GlassJarsFilled": glass.solution_value(),
            "PlasticJarsFilled": plastic.solution_value(),
            "TotalJarsFilled": solver.Objective().Value()
        }
    else:
        return None

def main():
    results = {}

    # Implementation 1: Using ortools.linear_solver (based on the provided formulation)
    sol1 = solve_linear_model()
    if sol1:
        results["Implementation 1"] = {
            "variables": {
                "GlassJarsFilled": sol1["GlassJarsFilled"],
                "PlasticJarsFilled": sol1["PlasticJarsFilled"]
            },
            "objective": sol1["TotalJarsFilled"]
        }
    else:
        results["Implementation 1"] = "No optimal solution found."

    # If additional formulations were provided, they could be implemented in separate functions.
    # For now, only one formulation is implemented.

    # Print the structured results for all implementations
    print("Optimal solutions for all implementations:")
    for impl, res in results.items():
        print(f"{impl}: {res}")

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Optimal solutions for all implementations:
Implementation 1: {'variables': {'GlassJarsFilled': 23.0, 'PlasticJarsFilled': 47.0}, 'objective': 70.0}
'''

'''Expected Output:
Expected solution

: {'variables': {'GlassJarsFilled': 20.0, 'PlasticJarsFilled': 50.0}, 'objective': 70.0}'''

