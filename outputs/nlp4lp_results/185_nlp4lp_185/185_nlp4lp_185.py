# Problem Description:
'''Problem description: A fashion company sells regular handbags and premium handbags made of higher quality material. They can sell regular handbags at a profit of $30 each and premium handbags at a profit of $180 each. The total monthly cost of manufacturing is $200 per regular handbag and $447 per premium handbag. The company has a total budget of $250000 and can sell at most 475 handbags of either type per month. How many of each handbag should they sell to maximize its monthly profit?

Expected Output Schema:
{
  "variables": {
    "NumberRegularHandbags": "float",
    "NumberPremiumHandbags": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
• HandbagTypes = {Regular, Premium}

Parameters:
• profit_regular = 30 (USD profit per regular handbag sold)
• profit_premium = 180 (USD profit per premium handbag sold)
• cost_regular = 200 (USD manufacturing cost per regular handbag)
• cost_premium = 447 (USD manufacturing cost per premium handbag)
• budget_total = 250000 (USD available monthly manufacturing budget)
• max_handbags = 475 (maximum total handbags that can be sold per month)

Variables:
• NumberRegularHandbags ∈ ℝ, with NumberRegularHandbags ≥ 0  
  (Decision variable representing the number of regular handbags to sell. Although handbags are discrete items, we denote them as floats per the expected schema.)
• NumberPremiumHandbags ∈ ℝ, with NumberPremiumHandbags ≥ 0  
  (Decision variable representing the number of premium handbags to sell.)

Objective:
Maximize TotalProfit = (profit_regular × NumberRegularHandbags) + (profit_premium × NumberPremiumHandbags)
  (Units: USD; this is the monthly net profit from sales. The stated profits per unit are assumed to be net figures, while manufacturing costs are used solely to enforce the budget constraint.)

Constraints:
1. Manufacturing Budget Constraint:
  (cost_regular × NumberRegularHandbags) + (cost_premium × NumberPremiumHandbags) ≤ budget_total  
  (The total manufacturing cost for producing the handbags must not exceed the available monthly budget, with costs in USD per handbag.)

2. Sales Capacity Constraint:
  NumberRegularHandbags + NumberPremiumHandbags ≤ max_handbags  
  (The total number of handbags sold per month, regardless of type, cannot exceed the maximum sales capacity.)

-------------------------------------------------
Expected Output Schema:
{
  "variables": {
    "NumberRegularHandbags": "float",
    "NumberPremiumHandbags": "float"
  },
  "objective": "float"
}'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_linear_model():
    # Create the linear solver with the GLOP backend.
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Solver not found.")
        return None

    # PARAMETERS
    profit_regular = 30      # profit per regular handbag sold (USD)
    profit_premium = 180     # profit per premium handbag sold (USD)
    cost_regular = 200       # manufacturing cost per regular handbag (USD)
    cost_premium = 447       # manufacturing cost per premium handbag (USD)
    budget_total = 250000    # total monthly manufacturing budget (USD)
    max_handbags = 475       # maximum handbags that can be sold per month

    # VARIABLES (as floats as per expectation)
    NumberRegularHandbags = solver.NumVar(0, solver.infinity(), 'NumberRegularHandbags')
    NumberPremiumHandbags = solver.NumVar(0, solver.infinity(), 'NumberPremiumHandbags')

    # CONSTRAINTS
    # 1. Manufacturing Budget Constraint:
    #    (cost_regular * NumberRegularHandbags) + (cost_premium * NumberPremiumHandbags) <= budget_total
    solver.Add(cost_regular * NumberRegularHandbags + cost_premium * NumberPremiumHandbags <= budget_total)

    # 2. Sales Capacity Constraint:
    #    NumberRegularHandbags + NumberPremiumHandbags <= max_handbags
    solver.Add(NumberRegularHandbags + NumberPremiumHandbags <= max_handbags)

    # OBJECTIVE: maximize profit
    objective = solver.Objective()
    objective.SetCoefficient(NumberRegularHandbags, profit_regular)
    objective.SetCoefficient(NumberPremiumHandbags, profit_premium)
    objective.SetMaximization()

    # Solve the problem
    status = solver.Solve()

    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result["variables"] = {
            "NumberRegularHandbags": NumberRegularHandbags.solution_value(),
            "NumberPremiumHandbags": NumberPremiumHandbags.solution_value()
        }
        result["objective"] = objective.Value()
    else:
        result["message"] = "The problem does not have an optimal solution."

    return result

def main():
    # Since the mathematical formulation provided a single formulation,
    # we are using one implementation based on the linear programming model.
    linear_model_result = solve_linear_model()

    print("Solution for Linear Model:")
    if "message" in linear_model_result:
        print(linear_model_result["message"])
    else:
        print("NumberRegularHandbags:", linear_model_result["variables"]["NumberRegularHandbags"])
        print("NumberPremiumHandbags:", linear_model_result["variables"]["NumberPremiumHandbags"])
        print("Optimal objective value (Total Profit):", linear_model_result["objective"])

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Solution for Linear Model:
NumberRegularHandbags: 0.0
NumberPremiumHandbags: 475.0
Optimal objective value (Total Profit): 85500.0
'''

'''Expected Output:
Expected solution

: {'variables': {'NumberRegularHandbags': -0.0, 'NumberPremiumHandbags': 475.0}, 'objective': 85500.0}'''

