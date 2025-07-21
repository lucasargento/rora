# Problem Description:
'''Problem description: A woman on a diet needs to eat two types of meal preps, a smoothie and a protein bar. Each smoothie contains 2 units of protein and 300 calories. Each protein bar contains 7 units of protein and 250 calories. The woman must eat 2 times more protein bars than smoothies. If the woman can consume at most 2000 calories, how many of each should she eat or drink to maximize her protein intake?

Expected Output Schema:
{
  "variables": {
    "NumberSmoothies": "float",
    "NumberProteinBars": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- M: set of meal prep types = {Smoothie, ProteinBar}

Parameters:
- protein_Smoothie: protein content per smoothie (2 protein units per smoothie)
- protein_ProteinBar: protein content per protein bar (7 protein units per bar)
- calories_Smoothie: calories per smoothie (300 calories per smoothie)
- calories_ProteinBar: calories per protein bar (250 calories per bar)
- calorie_limit: maximum calories allowed per day (2000 calories)
- bar_to_smoothie_ratio: ratio of protein bars to smoothies (2 bars per smoothie)

Variables:
- NumberSmoothies: number of smoothies consumed [continuous, non-negative; units: count]
- NumberProteinBars: number of protein bars consumed [continuous, non-negative; units: count]

Objective:
- Maximize total protein intake = protein_Smoothie * NumberSmoothies + protein_ProteinBar * NumberProteinBars

Constraints:
1. Calorie constraint:
   calories_Smoothie * NumberSmoothies + calories_ProteinBar * NumberProteinBars <= calorie_limit
   (i.e., 300 * NumberSmoothies + 250 * NumberProteinBars <= 2000)
2. Bar-to-smoothie ratio constraint:
   NumberProteinBars = bar_to_smoothie_ratio * NumberSmoothies
   (i.e., NumberProteinBars = 2 * NumberSmoothies)

----------------------------------
Expected Output Schema Example:

{
  "variables": {
    "NumberSmoothies": "float",
    "NumberProteinBars": "float"
  },
  "objective": "float"
}'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp
from ortools.sat.python import cp_model

def solve_with_linear_solver():
    # Create GLOP linear programming solver instance.
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Failed to create solver.")
        return None
    
    # Variables (continuous non-negative)
    NumberSmoothies = solver.NumVar(0.0, solver.infinity(), "NumberSmoothies")
    NumberProteinBars = solver.NumVar(0.0, solver.infinity(), "NumberProteinBars")
    
    # Parameters:
    protein_Smoothie = 2
    protein_ProteinBar = 7
    calories_Smoothie = 300
    calories_ProteinBar = 250
    calorie_limit = 2000
    bar_to_smoothie_ratio = 2  # protein bars = 2 * smoothies
    
    # Constraints:
    # 1. Calorie constraint: 300*Smoothies + 250*ProteinBars <= 2000
    solver.Add(calories_Smoothie * NumberSmoothies + calories_ProteinBar * NumberProteinBars <= calorie_limit)
    
    # 2. Bar-to-smoothie ratio constraint: ProteinBars = 2 * Smoothies
    solver.Add(NumberProteinBars == bar_to_smoothie_ratio * NumberSmoothies)
    
    # Objective: maximize total protein intake = 2*Smoothies + 7*ProteinBars
    objective = solver.Objective()
    objective.SetCoefficient(NumberSmoothies, protein_Smoothie)
    objective.SetCoefficient(NumberProteinBars, protein_ProteinBar)
    objective.SetMaximization()
    
    status = solver.Solve()
    
    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "variables": {
                "NumberSmoothies": NumberSmoothies.solution_value(),
                "NumberProteinBars": NumberProteinBars.solution_value()
            },
            "objective": objective.Value()
        }
    else:
        result = {"error": "No optimal solution found."}
    return result

def solve_with_cp_model():
    # In this CP-SAT model, we use integer variables because CP-SAT is tailored for integer optimization.
    # We'll create bounds that are reasonable given the calorie constraint.
    model = cp_model.CpModel()
    
    # Define reasonable upper-bounds using calorie limit (e.g., maximum smoothies = 2000/300 ≈ 6.67, so use 10)
    NumberSmoothies = model.NewIntVar(0, 10, "NumberSmoothies")
    # For protein bars, since they must be 2 * smoothies, the maximum is 20.
    NumberProteinBars = model.NewIntVar(0, 20, "NumberProteinBars")
    
    # Parameters:
    protein_Smoothie = 2
    protein_ProteinBar = 7
    calories_Smoothie = 300
    calories_ProteinBar = 250
    calorie_limit = 2000
    bar_to_smoothie_ratio = 2  # protein bars = 2 * smoothies
    
    # Constraints:
    # 1. Calorie constraint: 300*Smoothies + 250*ProteinBars <= 2000
    model.Add(calories_Smoothie * NumberSmoothies + calories_ProteinBar * NumberProteinBars <= calorie_limit)
    
    # 2. Bar-to-smoothie ratio constraint: ProteinBars = 2 * Smoothies
    model.Add(NumberProteinBars == bar_to_smoothie_ratio * NumberSmoothies)
    
    # Objective: maximize total protein intake = 2*Smoothies + 7*ProteinBars
    protein_expr = protein_Smoothie * NumberSmoothies + protein_ProteinBar * NumberProteinBars
    model.Maximize(protein_expr)

    # Solve model.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    
    result = {}
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        result = {
            "variables": {
                "NumberSmoothies": solver.Value(NumberSmoothies),
                "NumberProteinBars": solver.Value(NumberProteinBars)
            },
            "objective": solver.ObjectiveValue()
        }
    else:
        result = {"error": "No optimal solution found."}
    return result

def main():
    # Solve using the linear solver model
    linear_solver_result = solve_with_linear_solver()
    # Solve using the CP-SAT model
    cp_model_result = solve_with_cp_model()
    
    # Print results for both implementations in a structured way.
    print("Results using Google OR-Tools Linear Solver:")
    print(linear_solver_result)
    print("\nResults using Google OR-Tools CP-SAT Model:")
    print(cp_model_result)

if __name__ == "__main__":
    main()

'''Execution Results:
SUCCESS:
Results using Google OR-Tools Linear Solver:
{'variables': {'NumberSmoothies': 2.500000000000001, 'NumberProteinBars': 4.999999999999999}, 'objective': 39.99999999999999}

Results using Google OR-Tools CP-SAT Model:
{'variables': {'NumberSmoothies': 2, 'NumberProteinBars': 4}, 'objective': 32.0}
'''

'''Expected Output:
Expected solution

: {'variables': {'NumberSmoothies': 2.0, 'NumberProteinBars': 4.0}, 'objective': 32.0}'''

