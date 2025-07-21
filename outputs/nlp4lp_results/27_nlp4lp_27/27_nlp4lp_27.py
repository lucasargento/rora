# Problem Description:
'''Problem description: Mark has 50 acres of land available to grow potatoes and cucumbers that he sells at a farmers' market. He must grow at least 12 acres of potatoes and 15 acres of cucumbers to meet his contract. Mark prefers to grow more cucumbers than potatoes, but he only has enough resources to grow at most twice the amount of cucumbers as potatoes. If the profit per acre of potatoes is $500 and the profit per acre of cucumbers is $650, how many acres of each should he grow to maximize his profit? What is that profit?

Expected Output Schema:
{
  "variables": {
    "AcresPotatoes": "float",
    "AcresCucumbers": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- CROP: set of crops = {Potatoes, Cucumbers}

Parameters:
- TotalAcres: total acres of land available [acres] = 50
- MinAcresPotatoes: minimum acres required for Potatoes [acres] = 12
- MinAcresCucumbers: minimum acres required for Cucumbers [acres] = 15
- ProfitPotatoes: profit per acre of Potatoes [USD per acre] = 500
- ProfitCucumbers: profit per acre of Cucumbers [USD per acre] = 650
- MaxCucumberToPotatoRatio: maximum allowable ratio of Cucumbers to Potatoes [unitless] = 2

Variables:
- AcresPotatoes: acres allocated to growing Potatoes [float, continuous, acres, >= 0]
- AcresCucumbers: acres allocated to growing Cucumbers [float, continuous, acres, >= 0]

Objective:
- Maximize TotalProfit = (ProfitPotatoes * AcresPotatoes) + (ProfitCucumbers * AcresCucumbers)

Constraints:
1. Total Land Constraint:
   - AcresPotatoes + AcresCucumbers ≤ TotalAcres
2. Minimum Acreage Constraints:
   - AcresPotatoes ≥ MinAcresPotatoes
   - AcresCucumbers ≥ MinAcresCucumbers
3. Preference Constraint (Mark prefers to grow more Cucumbers than Potatoes):
   - AcresCucumbers ≥ AcresPotatoes
4. Resource Limitation Constraint:
   - AcresCucumbers ≤ MaxCucumberToPotatoRatio * AcresPotatoes

Additional comments:
- All parameters and variables are expressed in consistent units (acres for land and USD per acre for profit).
- The model uses continuous variables making it suitable for implementation in linear programming solvers.
- The Preference Constraint ensures that the acreage for Cucumbers is at least equal to that for Potatoes, reflecting Mark’s desire to plant more Cucumbers.
- The Resource Limitation Constraint ensures that the acreage of Cucumbers does not exceed twice the acreage of Potatoes, reflecting resource restrictions.'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_linear_program():
    # Create the linear solver using the GLOP backend.
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        return {"error": "Linear solver not created."}
    
    # Parameters
    total_acres = 50.0
    min_potatoes = 12.0
    min_cucumbers = 15.0
    profit_potatoes = 500.0
    profit_cucumbers = 650.0
    max_cucumber_to_potato_ratio = 2.0
    
    # Variables: continuous variables for acres allocated to each crop.
    # Lower bounds are set based on the minimum acreage requirements.
    acres_potatoes = solver.NumVar(min_potatoes, solver.infinity(), "AcresPotatoes")
    acres_cucumbers = solver.NumVar(min_cucumbers, solver.infinity(), "AcresCucumbers")
    
    # Constraint 1: Total land constraint
    solver.Add(acres_potatoes + acres_cucumbers <= total_acres)
    
    # Constraint 2: Preference constraint: Mark prefers more cucumbers than potatoes.
    solver.Add(acres_cucumbers >= acres_potatoes)
    
    # Constraint 3: Resource limitation: at most twice the amount of cucumbers as potatoes.
    solver.Add(acres_cucumbers <= max_cucumber_to_potato_ratio * acres_potatoes)
    
    # Objective: maximize total profit = 500 * acres_potatoes + 650 * acres_cucumbers
    objective = solver.Objective()
    objective.SetCoefficient(acres_potatoes, profit_potatoes)
    objective.SetCoefficient(acres_cucumbers, profit_cucumbers)
    objective.SetMaximization()
    
    # Solve the model.
    status = solver.Solve()
    
    # Process the result.
    if status != pywraplp.Solver.OPTIMAL:
        return {"error": "The problem does not have an optimal solution."}
    
    result = {
        "variables": {
            "AcresPotatoes": acres_potatoes.solution_value(),
            "AcresCucumbers": acres_cucumbers.solution_value()
        },
        "objective": objective.Value()
    }
    
    return result

def main():
    # Since only one formulation was provided (a linear program), we implement only one model.
    lp_result = solve_linear_program()
    
    # Structure the output for clear presentation.
    print("Results from the Linear Programming formulation:")
    if "error" in lp_result:
        print(lp_result["error"])
    else:
        print("Optimal Acres for Potatoes:", lp_result["variables"]["AcresPotatoes"])
        print("Optimal Acres for Cucumbers:", lp_result["variables"]["AcresCucumbers"])
        print("Maximum Profit:", lp_result["objective"])
    
if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Results from the Linear Programming formulation:
Optimal Acres for Potatoes: 16.666666666666668
Optimal Acres for Cucumbers: 33.333333333333336
Maximum Profit: 30000.0
'''

'''Expected Output:
Expected solution

: {'variables': {'AcresPotatoes': 16.666666666666668, 'AcresCucumbers': 33.33333333333333}, 'objective': 30000.0}'''

