# Problem Description:
'''Problem description: Mrs. Watson wants to invest in the real-estate market and has a total budget of at most $760000. She has two choices which include condos and detached houses. Each dollar invested in condos yields a $0.50 profit and each dollar invested in detached houses yields a $1 profit. A minimum of 20% of all money invested must be in condos, and at least $20000 must be in detached houses. Formulate an LP that can be used to maximize total profit earned from Mrs. Watson's investment.

Expected Output Schema:
{
  "variables": {
    "InvestmentCondos": "float",
    "InvestmentDetachedHouses": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- InvestmentOptions: set of investment types = {Condos, DetachedHouses}

Parameters:
- total_budget: total available investment budget = 760000 dollars
- profit_per_dollar_condos: profit per dollar invested in condos = 0.50 dollars per dollar
- profit_per_dollar_detached: profit per dollar invested in detached houses = 1.00 dollar per dollar
- min_percent_condos: minimum percentage of total investment that must be in condos = 0.20 (20%)
- min_detached_investment: minimum dollar amount that must be invested in detached houses = 20000 dollars

Variables:
- InvestmentCondos: amount invested in condos (continuous variable, ≥ 0) [in dollars]
- InvestmentDetachedHouses: amount invested in detached houses (continuous variable, ≥ 0) [in dollars]

Objective:
- Maximize total profit = (profit_per_dollar_condos * InvestmentCondos) + (profit_per_dollar_detached * InvestmentDetachedHouses)

Constraints:
1. Budget Constraint: InvestmentCondos + InvestmentDetachedHouses ≤ total_budget
2. Detached House Minimum Constraint: InvestmentDetachedHouses ≥ min_detached_investment
3. Condos Investment Ratio Constraint: InvestmentCondos ≥ min_percent_condos * (InvestmentCondos + InvestmentDetachedHouses)'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_investment_lp():
    # Create the linear solver with GLOP backend (for LPs)
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Solver not found.")
        return None

    # Parameters
    total_budget = 760000.0
    profit_condos = 0.50
    profit_detached = 1.0
    min_percent_condos = 0.20
    min_detached_investment = 20000.0

    # Variables: amounts invested in condos and detached houses (continuous variables, >= 0)
    investment_condos = solver.NumVar(0.0, total_budget, 'InvestmentCondos')
    investment_detached = solver.NumVar(0.0, total_budget, 'InvestmentDetachedHouses')

    # Constraints
    # 1. Budget constraint: condos + detached ≤ total_budget
    solver.Add(investment_condos + investment_detached <= total_budget)

    # 2. Detached house minimum constraint: detached ≥ min_detached_investment
    solver.Add(investment_detached >= min_detached_investment)

    # 3. Condos investment ratio constraint:
    #    investment_condos >= 0.20*(investment_condos + investment_detached)
    #    This can be rewritten as:  investment_condos - 0.20*investment_condos >= 0.20*investment_detached
    #    i.e., 0.80*investment_condos >= 0.20*investment_detached  => 4*investment_condos >= investment_detached
    solver.Add(4 * investment_condos >= investment_detached)

    # Objective: Maximize total profit = (0.50 * investment_condos) + (1.00 * investment_detached)
    solver.Maximize(profit_condos * investment_condos + profit_detached * investment_detached)

    # Solve the problem
    status = solver.Solve()

    # Prepare the result in the expected schema
    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result['InvestmentCondos'] = investment_condos.solution_value()
        result['InvestmentDetachedHouses'] = investment_detached.solution_value()
        result['objective'] = solver.Objective().Value()
        print("Solution for LP using ortools.linear_solver:")
        print("Investment in Condos: ${:.2f}".format(result['InvestmentCondos']))
        print("Investment in Detached Houses: ${:.2f}".format(result['InvestmentDetachedHouses']))
        print("Total Profit: ${:.2f}".format(result['objective']))
    elif status == pywraplp.Solver.FEASIBLE:
        print("A feasible solution was found, but it may not be optimal.")
    else:
        print("The problem does not have an optimal solution.")

    return result

def main():
    # Since the mathematical formulation does not propose multiple ambiguous versions,
    # we implement a single LP formulation using ortools.linear_solver.
    result_lp = solve_investment_lp()
    # If in future multiple formulations exist, each can be solved separately and printed here.
    # For now, we only have one formulation.

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Solution for LP using ortools.linear_solver:
Investment in Condos: $152000.00
Investment in Detached Houses: $608000.00
Total Profit: $684000.00
'''

'''Expected Output:
Expected solution

: {'variables': {'InvestmentCondos': 152000.0, 'InvestmentDetachedHouses': 608000.0}, 'objective': 684000.0}'''

