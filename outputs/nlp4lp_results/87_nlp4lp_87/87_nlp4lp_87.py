# Problem Description:
'''Problem description: A doctor recommends her patient eat more fish and chicken to increase her protein and iron intake. Each fish meal contains 10 units of protein and 12 units of iron. Each chicken meal contains 15 units of protein and 8 units of iron. The patient needs to consume at least 130 units of protein and 120 units of iron. Since the chicken meal is less expensive, the patient prefers to consume at least twice as many chicken meals as fish meals. If each fish meal contains 7 units of fat and each chicken meal contains 10 units of fat, how many meals of each should she eat to minimize her fat intake?

Expected Output Schema:
{
  "variables": {
    "FishMeals": "float",
    "ChickenMeals": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Below is the complete and structured mathematical optimization model using the five-element framework. This model is fully self-contained based on the provided problem data and requirements.

------------------------------------------------------------
Sets:
- Meals: the set of meal types = {Fish, Chicken}

------------------------------------------------------------
Parameters:
- protein_fish: protein per fish meal = 10 units [units of protein/meal]
- protein_chicken: protein per chicken meal = 15 units [units of protein/meal]
- iron_fish: iron per fish meal = 12 units [units of iron/meal]
- iron_chicken: iron per chicken meal = 8 units [units of iron/meal]
- fat_fish: fat per fish meal = 7 units [units of fat/meal]
- fat_chicken: fat per chicken meal = 10 units [units of fat/meal]
- protein_requirement: minimum required protein = 130 units [units of protein]
- iron_requirement: minimum required iron = 120 units [units of iron]
- chicken_to_fish_ratio: minimum ratio of chicken to fish meals = 2  
  (i.e., the number of chicken meals must be at least twice the number of fish meals)

------------------------------------------------------------
Variables:
- FishMeals: number of fish meals consumed [float, continuous, nonnegative]
- ChickenMeals: number of chicken meals consumed [float, continuous, nonnegative]

------------------------------------------------------------
Objective:
Minimize total fat intake:
  TotalFat = fat_fish * FishMeals + fat_chicken * ChickenMeals
In terms of the given parameters:
  Minimize: 7 * FishMeals + 10 * ChickenMeals

------------------------------------------------------------
Constraints:
1. Protein intake constraint:
   protein_fish * FishMeals + protein_chicken * ChickenMeals >= protein_requirement
   i.e., 10 * FishMeals + 15 * ChickenMeals >= 130

2. Iron intake constraint:
   iron_fish * FishMeals + iron_chicken * ChickenMeals >= iron_requirement
   i.e., 12 * FishMeals + 8 * ChickenMeals >= 120

3. Chicken-to-fish meal ratio constraint:
   ChickenMeals >= chicken_to_fish_ratio * FishMeals
   i.e., ChickenMeals >= 2 * FishMeals

------------------------------------------------------------
Model Comments:
- All units are assumed to be consistent per meal as described.
- Although meals are discrete in practice, the variables are modeled as continuous (float) as defined in the expected output schema.
- The objective focuses solely on minimizing fat intake, while nutritional constraints ensure the patient meets her protein and iron needs, and the preference for a higher count of chicken meals is also respected.

------------------------------------------------------------
Expected Output Schema (for reference in implementation):
{
  "variables": {
    "FishMeals": "float",
    "ChickenMeals": "float"
  },
  "objective": "float"
}'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp
from ortools.sat.python import cp_model

def solve_with_linear_solver():
    # Solve using OR-Tools linear solver (continuous LP)
    # Create the solver using the GLOP backend.
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Linear solver unavailable.")
        return None

    # Variables: nonnegative continuous (floats)
    FishMeals = solver.NumVar(0.0, solver.infinity(), 'FishMeals')
    ChickenMeals = solver.NumVar(0.0, solver.infinity(), 'ChickenMeals')

    # Parameters as provided
    protein_fish = 10.0
    protein_chicken = 15.0
    iron_fish = 12.0
    iron_chicken = 8.0
    fat_fish = 7.0
    fat_chicken = 10.0
    protein_requirement = 130.0
    iron_requirement = 120.0
    chicken_to_fish_ratio = 2.0

    # Constraints:
    # 1. Protein intake: 10*FishMeals + 15*ChickenMeals >= 130
    solver.Add(protein_fish * FishMeals + protein_chicken * ChickenMeals >= protein_requirement)

    # 2. Iron intake: 12*FishMeals + 8*ChickenMeals >= 120
    solver.Add(iron_fish * FishMeals + iron_chicken * ChickenMeals >= iron_requirement)

    # 3. Chicken-to-fish ratio: ChickenMeals >= 2 * FishMeals
    solver.Add(ChickenMeals >= chicken_to_fish_ratio * FishMeals)

    # Objective: Minimize total fat intake = 7*FishMeals + 10*ChickenMeals
    objective = solver.Objective()
    objective.SetCoefficient(FishMeals, fat_fish)
    objective.SetCoefficient(ChickenMeals, fat_chicken)
    objective.SetMinimization()

    # Solve the model
    status = solver.Solve()
    
    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "variables": {
                "FishMeals": FishMeals.solution_value(),
                "ChickenMeals": ChickenMeals.solution_value()
            },
            "objective": objective.Value()
        }
    else:
        result = {"status": "No optimal solution found in Linear Solver."}
    return result

def solve_with_cp_model():
    # Solve using OR-Tools CP-SAT, using integer approximation.
    # Note: CP-SAT does not directly support floats.
    # We assume meals must be integer values. This is a slight variation from the continuous formulation.
    model = cp_model.CpModel()

    # Define an upper bound that is reasonable.
    ub = 1000

    # Variables: integer meals (nonnegative)
    FishMeals = model.NewIntVar(0, ub, 'FishMeals')
    ChickenMeals = model.NewIntVar(0, ub, 'ChickenMeals')

    # Parameters (all integers)
    protein_fish = 10
    protein_chicken = 15
    iron_fish = 12
    iron_chicken = 8
    fat_fish = 7
    fat_chicken = 10
    protein_requirement = 130
    iron_requirement = 120
    chicken_to_fish_ratio = 2  # ChickenMeals >= 2 * FishMeals

    # Constraints:
    # 1. Protein intake: 10*FishMeals + 15*ChickenMeals >= 130
    model.Add(protein_fish * FishMeals + protein_chicken * ChickenMeals >= protein_requirement)

    # 2. Iron intake: 12*FishMeals + 8*ChickenMeals >= 120
    model.Add(iron_fish * FishMeals + iron_chicken * ChickenMeals >= iron_requirement)

    # 3. Chicken-to-fish ratio: ChickenMeals >= 2 * FishMeals
    model.Add(ChickenMeals >= chicken_to_fish_ratio * FishMeals)

    # Objective: Minimize total fat intake = 7*FishMeals + 10*ChickenMeals
    # CP-SAT only accepts integer objective.
    model.Minimize(fat_fish * FishMeals + fat_chicken * ChickenMeals)

    # Create a solver and solve
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    result = {}
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        result = {
            "variables": {
                "FishMeals": solver.Value(FishMeals),
                "ChickenMeals": solver.Value(ChickenMeals)
            },
            "objective": solver.ObjectiveValue()
        }
    else:
        result = {"status": "No optimal solution found in CP-SAT model."}
    return result

def main():
    print("Results using Linear Solver (Continuous LP formulation):")
    linear_result = solve_with_linear_solver()
    print(linear_result)
    print("\nResults using CP-SAT (Integer approximation formulation):")
    cp_result = solve_with_cp_model()
    print(cp_result)

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Results using Linear Solver (Continuous LP formulation):
{'variables': {'FishMeals': 4.285714285714285, 'ChickenMeals': 8.571428571428571}, 'objective': 115.7142857142857}

Results using CP-SAT (Integer approximation formulation):
{'variables': {'FishMeals': 4, 'ChickenMeals': 9}, 'objective': 118.0}
'''

'''Expected Output:
Expected solution

: {'variables': {'FishMeals': 4.0, 'ChickenMeals': 9.0}, 'objective': 118.0}'''

