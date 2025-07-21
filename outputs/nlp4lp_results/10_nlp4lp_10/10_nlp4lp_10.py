# Problem Description:
'''Problem description: A glass factory makes two types of glass panes: a regular glass pane and a tempered glass pane. Both require time on a heating and cooling machine. Both machines are available for a maximum of 300 minutes per day. It takes 3 minutes in the heating machine and 5 minutes in the cooling machine to make one regular glass pane. It takes 5 minutes in the heating machine and 8 minutes in the cooling machine to make one tempered glass pane. The profit per pane of regular glass is $8 and the profit per pane of tempered glass is $10. How many panes of each glass type should the factory make to maximize profit? What is the maximum profit?

Expected Output Schema:
{
  "variables": {
    "QuantityRegular": "float",
    "QuantityTempered": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- GlassType: set of glass pane types = {Regular, Tempered}

Parameters:
- heating_time: minutes required on the heating machine per pane
  • heating_time for Regular = 3 minutes per pane
  • heating_time for Tempered = 5 minutes per pane
- cooling_time: minutes required on the cooling machine per pane
  • cooling_time for Regular = 5 minutes per pane
  • cooling_time for Tempered = 8 minutes per pane
- max_heating_time: maximum available time on the heating machine = 300 minutes per day
- max_cooling_time: maximum available time on the cooling machine = 300 minutes per day
- profit: profit per pane [USD]
  • profit for Regular = 8 USD per pane
  • profit for Tempered = 10 USD per pane

Variables:
- QuantityRegular: number of regular glass panes produced [float, ≥ 0]
- QuantityTempered: number of tempered glass panes produced [float, ≥ 0]

Objective:
- Maximize total profit = (8 * QuantityRegular) + (10 * QuantityTempered)

Constraints:
1. Heating machine time constraint:
  (3 * QuantityRegular) + (5 * QuantityTempered) ≤ 300
2. Cooling machine time constraint:
  (5 * QuantityRegular) + (8 * QuantityTempered) ≤ 300

Note: All times are in minutes and profits are in US dollars per pane. This model is fully consistent with the problem description and can be directly translated into Python or OR-Tools code.

Expected Output Schema:
{
  "variables": {
    "QuantityRegular": "float",
    "QuantityTempered": "float"
  },
  "objective": "float"
}'''

# Generated Code:
from ortools.linear_solver import pywraplp

def solve_linear_program():
    # Create the linear solver with the GLOP backend.
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Error: Linear solver not created.")
        return None

    # Declare decision variables:
    # QuantityRegular: number of regular glass panes produced (float, >= 0)
    QuantityRegular = solver.NumVar(0.0, solver.infinity(), 'QuantityRegular')
    # QuantityTempered: number of tempered glass panes produced (float, >= 0)
    QuantityTempered = solver.NumVar(0.0, solver.infinity(), 'QuantityTempered')

    # Constraints:
    # 1. Heating machine time constraint:
    #    3 * QuantityRegular + 5 * QuantityTempered <= 300
    solver.Add(3 * QuantityRegular + 5 * QuantityTempered <= 300)
    
    # 2. Cooling machine time constraint:
    #    5 * QuantityRegular + 8 * QuantityTempered <= 300
    solver.Add(5 * QuantityRegular + 8 * QuantityTempered <= 300)

    # Objective: Maximize total profit = (8 * QuantityRegular) + (10 * QuantityTempered)
    solver.Maximize(8 * QuantityRegular + 10 * QuantityTempered)

    # Solve the problem and return the result in the expected schema.
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "variables": {
                "QuantityRegular": QuantityRegular.solution_value(),
                "QuantityTempered": QuantityTempered.solution_value()
            },
            "objective": solver.Objective().Value()
        }
        return result
    else:
        return "The problem does not have an optimal solution."

def main():
    results = {}

    # We have one formulation based on the linear programming model.
    # Implementation 1: Using the ortools.linear_solver module.
    lp_result = solve_linear_program()
    results["LinearSolver"] = lp_result

    # Print results in a structured way.
    print("Optimization Results:")
    for model_name, result in results.items():
        print(f"\nModel: {model_name}")
        if isinstance(result, dict):
            print("Variables:")
            for var_name, value in result["variables"].items():
                print(f"  {var_name}: {value}")
            print(f"Objective Value: {result['objective']}")
        else:
            print(result)

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Optimization Results:

Model: LinearSolver
Variables:
  QuantityRegular: 59.99999999999999
  QuantityTempered: 0.0
Objective Value: 479.99999999999994
'''

'''Expected Output:
Expected solution

: {'variables': {'QuantityRegular': 60.0, 'QuantityTempered': 0.0}, 'objective': 480.0}'''

