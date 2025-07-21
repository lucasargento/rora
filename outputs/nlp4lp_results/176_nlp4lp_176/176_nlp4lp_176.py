# Problem Description:
'''Problem description: A young boy is trying to grow taller by drinking milk and eating vegetables. He wants to get a minimum of 100 units of calcium and 50 units of iron per day. A glass of milk costs $1 and contains 40 units of calcium and 25 units of iron. A plate of vegetables costs $2 and contains 15 units of calcium and 30 units of iron. How many of each should he consume to minimize his cost?

Expected Output Schema:
{
  "variables": {
    "MilkAmount": "float",
    "VegetablesAmount": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- FoodItems: the set of food items available = {Milk, Vegetables}

Parameters:
- cost_Milk: cost per glass of milk [USD per glass] = 1
- cost_Vegetables: cost per plate of vegetables [USD per plate] = 2
- calcium_Milk: calcium content per glass of milk [units per glass] = 40
- calcium_Vegetables: calcium content per plate of vegetables [units per plate] = 15
- iron_Milk: iron content per glass of milk [units per glass] = 25
- iron_Vegetables: iron content per plate of vegetables [units per plate] = 30
- required_calcium: minimum daily calcium requirement [units] = 100
- required_iron: minimum daily iron requirement [units] = 50

Variables:
- MilkAmount: number of glasses of milk to consume per day [continuous variable, units: glasses, MilkAmount ≥ 0]
- VegetablesAmount: number of plates of vegetables to consume per day [continuous variable, units: plates, VegetablesAmount ≥ 0]

Objective:
- Minimize total cost = cost_Milk * MilkAmount + cost_Vegetables * VegetablesAmount
  (The objective represents the total daily expenditure on milk and vegetables in USD.)

Constraints:
- Calcium requirement: calcium_Milk * MilkAmount + calcium_Vegetables * VegetablesAmount ≥ required_calcium
  (Ensures that the total calcium intake is at least 100 units per day.)
- Iron requirement: iron_Milk * MilkAmount + iron_Vegetables * VegetablesAmount ≥ required_iron
  (Ensures that the total iron intake is at least 50 units per day.)

Expected Output Schema:
{
  "variables": {
    "MilkAmount": "float",
    "VegetablesAmount": "float"
  },
  "objective": "float"
}'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_with_linear_solver():
    # Create the linear solver using the GLOP backend (for continuous LPs)
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Solver not created.")
        return None

    # Parameters
    cost_Milk = 1
    cost_Vegetables = 2
    calcium_Milk = 40
    calcium_Vegetables = 15
    iron_Milk = 25
    iron_Vegetables = 30
    required_calcium = 100
    required_iron = 50

    # Variables: continuous and non-negative
    MilkAmount = solver.NumVar(0.0, solver.infinity(), 'MilkAmount')
    VegetablesAmount = solver.NumVar(0.0, solver.infinity(), 'VegetablesAmount')

    # Constraints:
    # Calcium requirement: 40 * MilkAmount + 15 * VegetablesAmount ≥ 100
    solver.Add(calcium_Milk * MilkAmount + calcium_Vegetables * VegetablesAmount >= required_calcium)
    # Iron requirement: 25 * MilkAmount + 30 * VegetablesAmount ≥ 50
    solver.Add(iron_Milk * MilkAmount + iron_Vegetables * VegetablesAmount >= required_iron)

    # Objective: minimize cost = 1 * MilkAmount + 2 * VegetablesAmount
    objective = solver.Objective()
    objective.SetCoefficient(MilkAmount, cost_Milk)
    objective.SetCoefficient(VegetablesAmount, cost_Vegetables)
    objective.SetMinimization()

    # Solve the problem.
    status = solver.Solve()

    # Prepare the result in the standard output schema.
    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result["variables"] = {
            "MilkAmount": MilkAmount.solution_value(),
            "VegetablesAmount": VegetablesAmount.solution_value()
        }
        result["objective"] = objective.Value()
    else:
        result["error"] = "The problem does not have an optimal solution."

    return result

def main():
    # Since the formulation provided has only one clear mathematical model,
    # we run a single implementation using the linear solver.
    print("Solution using OR-Tools Linear Solver (GLOP):")
    result_linear = solve_with_linear_solver()
    print(result_linear)

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Solution using OR-Tools Linear Solver (GLOP):
{'variables': {'MilkAmount': 2.5, 'VegetablesAmount': 0.0}, 'objective': 2.5}
'''

'''Expected Output:
Expected solution

: {'variables': {'MilkAmount': 2.5, 'VegetablesAmount': 0.0}, 'objective': 2.5}'''

