# Problem Description:
'''Problem description: Bob wants to design a diet consisting of protein bars and noodles. Assume that each serving of noodles costs $5 and contains 600 calories and 1.5 grams of protein. Assume that each serving of protein bar costs $2.5 and contains 250 calories and 5 grams of protein. He's interested in spending as little money as possible but he wants to ensure that his meals have at least 2000 calories and at least 16 grams of protein per day. Formulate a linear programming problem that will help minimize the cost of the diet.

Expected Output Schema:
{
  "variables": {
    "ServingsNoodles": "float",
    "ServingsProteinBars": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- Items: {Noodles, ProteinBars}

Parameters:
- cost_Noodles: 5 (USD per serving of noodles)
- cost_ProteinBars: 2.5 (USD per serving of protein bars)
- calories_Noodles: 600 (calories per serving of noodles)
- calories_ProteinBars: 250 (calories per serving of protein bars)
- protein_Noodles: 1.5 (grams of protein per serving of noodles)
- protein_ProteinBars: 5 (grams of protein per serving of protein bars)
- calorie_requirement: 2000 (minimum total calories per day)
- protein_requirement: 16 (minimum total grams of protein per day)

Variables:
- ServingsNoodles: number of servings of noodles (continuous, non-negative)
- ServingsProteinBars: number of servings of protein bars (continuous, non-negative)

Objective:
- Minimize total cost = cost_Noodles * ServingsNoodles + cost_ProteinBars * ServingsProteinBars

Constraints:
- Calorie constraint: calories_Noodles * ServingsNoodles + calories_ProteinBars * ServingsProteinBars ≥ calorie_requirement
- Protein constraint: protein_Noodles * ServingsNoodles + protein_ProteinBars * ServingsProteinBars ≥ protein_requirement

------------------------------------------
Expected Output Schema:
{
  "variables": {
    "ServingsNoodles": "float",
    "ServingsProteinBars": "float"
  },
  "objective": "float"
}'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_diet_lp():
    # Create the linear solver using the GLOP backend.
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        return None, None

    # Variables
    # ServingsNoodles: number of servings of noodles (continuous, non-negative)
    ServingsNoodles = solver.NumVar(0.0, solver.infinity(), 'ServingsNoodles')
    # ServingsProteinBars: number of servings of protein bars (continuous, non-negative)
    ServingsProteinBars = solver.NumVar(0.0, solver.infinity(), 'ServingsProteinBars')

    # Parameters
    cost_Noodles = 5.0         # USD per serving of noodles
    cost_ProteinBars = 2.5     # USD per serving of protein bars
    calories_Noodles = 600     # calories per serving of noodles
    calories_ProteinBars = 250 # calories per serving of protein bars
    protein_Noodles = 1.5      # grams of protein per serving of noodles
    protein_ProteinBars = 5.0  # grams of protein per serving of protein bars
    calorie_requirement = 2000
    protein_requirement = 16

    # Objective: Minimize total cost
    objective = solver.Objective()
    objective.SetCoefficient(ServingsNoodles, cost_Noodles)
    objective.SetCoefficient(ServingsProteinBars, cost_ProteinBars)
    objective.SetMinimization()

    # Constraints:
    # Calorie constraint: calories_Noodles * ServingsNoodles + calories_ProteinBars * ServingsProteinBars >= calorie_requirement
    calorie_constraint = solver.Constraint(calorie_requirement, solver.infinity(), 'calorie_constraint')
    calorie_constraint.SetCoefficient(ServingsNoodles, calories_Noodles)
    calorie_constraint.SetCoefficient(ServingsProteinBars, calories_ProteinBars)
    
    # Protein constraint: protein_Noodles * ServingsNoodles + protein_ProteinBars * ServingsProteinBars >= protein_requirement
    protein_constraint = solver.Constraint(protein_requirement, solver.infinity(), 'protein_constraint')
    protein_constraint.SetCoefficient(ServingsNoodles, protein_Noodles)
    protein_constraint.SetCoefficient(ServingsProteinBars, protein_ProteinBars)
    
    # Solve the problem and check the result.
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        solution = {
            "ServingsNoodles": ServingsNoodles.solution_value(),
            "ServingsProteinBars": ServingsProteinBars.solution_value()
        }
        objective_value = objective.Value()
    else:
        solution = None
        objective_value = None

    return solution, objective_value

def main():
    results = {}
    
    # Version 1: Linear Programming Formulation using ortools.linear_solver
    solution_lp, objective_lp = solve_diet_lp()
    if solution_lp is not None:
        results["Version 1 (LP Model)"] = {
            "variables": {
                "ServingsNoodles": solution_lp["ServingsNoodles"],
                "ServingsProteinBars": solution_lp["ServingsProteinBars"]
            },
            "objective": objective_lp
        }
    else:
        results["Version 1 (LP Model)"] = "No optimal solution found."
    
    # Print results in a structured way.
    print("Optimization Results:")
    for version, result in results.items():
        print(f"\n{version}:")
        if isinstance(result, dict):
            print("Variables:")
            for var, value in result["variables"].items():
                print(f"  {var}: {value}")
            print("Objective Value:")
            print(f"  {result['objective']}")
        else:
            print(result)

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Optimization Results:

Version 1 (LP Model):
Variables:
  ServingsNoodles: 2.2857142857142856
  ServingsProteinBars: 2.5142857142857142
Objective Value:
  17.71428571428571
'''

'''Expected Output:
Expected solution

: {'variables': {'ServingsNoodles': 2.2857142857142856, 'ServingsProteinBars': 2.5142857142857142}, 'objective': 17.71428571428571}'''

