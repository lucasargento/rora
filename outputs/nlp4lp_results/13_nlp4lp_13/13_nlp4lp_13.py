# Problem Description:
'''Problem description: My family has decided to invest in real state for the first time. Currently, they have $600,000 to invest, some in apartments and the rest in townhouses. The money invested in apartments must not be greater than $200,000. They have decided that the money invested in apartments must be at least a half as much as that in townhouses.  If the apartments earn 10%, and the townhouses earn 15%, how much money should they invest in each to maximize profit?

Expected Output Schema:
{
  "variables": {
    "InvestmentApartments": "float",
    "InvestmentTownhouses": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- S: set of property types = {Apartments, Townhouses}

Parameters:
- TotalInvestment: total available funds for investment = 600000 (USD)
- MaxApartmentInvestment: maximum allowed funds for apartments = 200000 (USD)
- ReturnApartment: profit rate for apartments = 0.10 (profit per dollar)
- ReturnTownhouse: profit rate for townhouses = 0.15 (profit per dollar)
- MinApartmentToTownhouseRatio: minimum ratio of apartment investment to townhouse investment = 0.5

Variables:
- InvestmentApartments: amount invested in apartments (continuous, USD, ≥ 0)
- InvestmentTownhouses: amount invested in townhouses (continuous, USD, ≥ 0)

Objective:
- Maximize total profit = (ReturnApartment × InvestmentApartments) + (ReturnTownhouse × InvestmentTownhouses)

Constraints:
1. Budget constraint: InvestmentApartments + InvestmentTownhouses ≤ TotalInvestment
2. Apartment cap: InvestmentApartments ≤ MaxApartmentInvestment
3. Ratio constraint: InvestmentApartments ≥ MinApartmentToTownhouseRatio × InvestmentTownhouses
4. Nonnegativity: InvestmentApartments ≥ 0 and InvestmentTownhouses ≥ 0

--------------------------------------------------
Expected Output Schema:
{
  "variables": {
    "InvestmentApartments": "float",
    "InvestmentTownhouses": "float"
  },
  "objective": "float"
}'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_investment_problem():
    # Create the solver using the GLOP backend (linear programming solver)
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Solver not created.")
        return None

    # Parameters
    total_investment = 600000.0
    max_apartment_investment = 200000.0
    return_apartment = 0.10
    return_townhouse = 0.15
    min_apartment_to_townhouse_ratio = 0.5

    # Variables: amounts invested in apartments and townhouses (continuous, non-negative)
    invest_apartments = solver.NumVar(0.0, max_apartment_investment, 'InvestmentApartments')
    invest_townhouses = solver.NumVar(0.0, total_investment, 'InvestmentTownhouses')

    # Constraints
    # 1. Budget constraint: investment in apartments + townhouses <= total available funds.
    solver.Add(invest_apartments + invest_townhouses <= total_investment)

    # 2. Apartment cap: investment in apartments <= maximum allowed for apartments.
    solver.Add(invest_apartments <= max_apartment_investment)

    # 3. Ratio constraint: investment in apartments must be at least half as much as that in townhouses.
    solver.Add(invest_apartments >= min_apartment_to_townhouse_ratio * invest_townhouses)

    # Objective: maximize total profit
    # Profit = return_apartment * invest_apartments + return_townhouse * invest_townhouses
    objective = solver.Objective()
    objective.SetCoefficient(invest_apartments, return_apartment)
    objective.SetCoefficient(invest_townhouses, return_townhouse)
    objective.SetMaximization()

    # Solve the problem
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        solution = {
            "variables": {
                "InvestmentApartments": invest_apartments.solution_value(),
                "InvestmentTownhouses": invest_townhouses.solution_value()
            },
            "objective": objective.Value()
        }
        return solution
    else:
        return {"message": "The problem does not have an optimal solution."}

def main():
    # Since only one formulation is provided, we implement one separate model.
    result_model = solve_investment_problem()
    
    # Structured output for the model result.
    print("Results for Investment Optimization Model:")
    if "message" in result_model:
        print(result_model["message"])
    else:
        print("InvestmentApartments =", result_model["variables"]["InvestmentApartments"])
        print("InvestmentTownhouses =", result_model["variables"]["InvestmentTownhouses"])
        print("Optimal Profit =", result_model["objective"])

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Results for Investment Optimization Model:
InvestmentApartments = 200000.0
InvestmentTownhouses = 400000.0
Optimal Profit = 80000.0
'''

'''Expected Output:
Expected solution

: {'variables': {'InvestmentApartments': 200000.0, 'InvestmentTownhouses': 400000.0}, 'objective': 80000.0}'''

