# Problem Description:
'''Problem description: Super Shop sells cat paw snacks and gold shark snacks in bulk. It plans to sell them into two snack mix products. The first mix contains 20% cat paw snacks and 80% gold shark snacks. The second mix contains 35% cat paw snacks and 65% gold shark snacks. The store has on hand 20 kg of cat paw snacks and 50 kg of gold shark snacks. If the profit per kg of the first mix is $12 and the profit per kg of the second mix is $15, how many kg of each should be prepared to maximize profit?

Expected Output Schema:
{
  "variables": {
    "Mix1": "float",
    "Mix2": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- Mixes = {Mix1, Mix2}

Parameters:
- profit_Mix1: profit per kg for Mix1 = 12 [USD/kg]
- profit_Mix2: profit per kg for Mix2 = 15 [USD/kg]
- catpaw_frac_Mix1: fraction of cat paw snacks in Mix1 = 0.20 [kg cat paw per kg mix]
- goldshark_frac_Mix1: fraction of gold shark snacks in Mix1 = 0.80 [kg gold shark per kg mix]
- catpaw_frac_Mix2: fraction of cat paw snacks in Mix2 = 0.35 [kg cat paw per kg mix]
- goldshark_frac_Mix2: fraction of gold shark snacks in Mix2 = 0.65 [kg gold shark per kg mix]
- catpaw_available: available cat paw snacks = 20 [kg]
- goldshark_available: available gold shark snacks = 50 [kg]

Variables:
- x_Mix1: kilograms of Mix1 to prepare (continuous, ≥ 0) [kg]
- x_Mix2: kilograms of Mix2 to prepare (continuous, ≥ 0) [kg]

Objective:
- Maximize total profit = (profit_Mix1 * x_Mix1) + (profit_Mix2 * x_Mix2)
  (This represents the total profit in USD.)

Constraints:
- Cat paw snack constraint:
  (catpaw_frac_Mix1 * x_Mix1) + (catpaw_frac_Mix2 * x_Mix2) ≤ catpaw_available
  (Ensures that the total kg of cat paw snacks used in both mixes does not exceed 20 kg.)
- Gold shark snack constraint:
  (goldshark_frac_Mix1 * x_Mix1) + (goldshark_frac_Mix2 * x_Mix2) ≤ goldshark_available
  (Ensures that the total kg of gold shark snacks used in both mixes does not exceed 50 kg.)'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_linear_model():
    # Create the linear solver with the GLOP backend.
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Solver not created.")
        return None

    # Parameters
    profit_mix1 = 12.0  # USD per kg for Mix1
    profit_mix2 = 15.0  # USD per kg for Mix2

    catpaw_frac_mix1 = 0.20  # fraction of cat paw in Mix1
    goldshark_frac_mix1 = 0.80  # fraction of gold shark in Mix1

    catpaw_frac_mix2 = 0.35  # fraction of cat paw in Mix2
    goldshark_frac_mix2 = 0.65  # fraction of gold shark in Mix2

    catpaw_available = 20.0  # available kg of cat paw snacks
    goldshark_available = 50.0  # available kg of gold shark snacks

    # Variables: kg of each mix to prepare (continuous, ≥ 0)
    x_mix1 = solver.NumVar(0.0, solver.infinity(), 'x_mix1')
    x_mix2 = solver.NumVar(0.0, solver.infinity(), 'x_mix2')

    # Constraints
    # Cat paw snack constraint: 0.20 * x_mix1 + 0.35 * x_mix2 ≤ 20
    solver.Add(catpaw_frac_mix1 * x_mix1 + catpaw_frac_mix2 * x_mix2 <= catpaw_available)

    # Gold shark snack constraint: 0.80 * x_mix1 + 0.65 * x_mix2 ≤ 50
    solver.Add(goldshark_frac_mix1 * x_mix1 + goldshark_frac_mix2 * x_mix2 <= goldshark_available)

    # Objective: Maximize profit = 12 * x_mix1 + 15 * x_mix2
    objective = solver.Objective()
    objective.SetCoefficient(x_mix1, profit_mix1)
    objective.SetCoefficient(x_mix2, profit_mix2)
    objective.SetMaximization()

    # Solve the problem.
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        solution = {
            "Mix1": x_mix1.solution_value(),
            "Mix2": x_mix2.solution_value(),
            "objective": objective.Value()
        }
        return solution
    elif status == pywraplp.Solver.INFEASIBLE:
        print("The problem is infeasible.")
        return None
    else:
        print("The solver ended with status", status)
        return None

def main():
    print("Solving Super Shop Snack Mix Optimization Problem using OR-Tools Linear Solver\n")

    # Since only one formulation has been provided,
    # we create only one implementation.
    result_linear = solve_linear_model()

    if result_linear is not None:
        print("Linear Solver Model Solution:")
        print("Mix1 (kg): {:.4f}".format(result_linear["Mix1"]))
        print("Mix2 (kg): {:.4f}".format(result_linear["Mix2"]))
        print("Total Profit (USD): {:.4f}\n".format(result_linear["objective"]))
        # Additionally, printing the result in the expected JSON output schema:
        output_schema = {
            "variables": {
                "Mix1": result_linear["Mix1"],
                "Mix2": result_linear["Mix2"]
            },
            "objective": result_linear["objective"]
        }
        print("Output Schema:")
        print(output_schema)
    else:
        print("No feasible solution found.")

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Solving Super Shop Snack Mix Optimization Problem using OR-Tools Linear Solver

Linear Solver Model Solution:
Mix1 (kg): 30.0000
Mix2 (kg): 40.0000
Total Profit (USD): 960.0000

Output Schema:
{'variables': {'Mix1': 29.99999999999998, 'Mix2': 40.00000000000002}, 'objective': 960.0000000000001}
'''

'''Expected Output:
Expected solution

: {'variables': {'Mix1': 1.0, 'Mix2': 0.0}, 'objective': 12.0}'''

