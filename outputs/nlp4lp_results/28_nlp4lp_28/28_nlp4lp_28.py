# Problem Description:
'''Problem description: A flooring company produces engineered hardwood and vinyl planks. Their sales forecasts show an expected demand of at least 20,000 square foot of hardwood and 10,000 square feet of vinyl planks each week. To satisfy a shipping contract, a total of at least 60,000 square feet of flooring much be shipped each week. Due to a labor shortage issue, no more than 50,000 square feet of hardwood and 30,000  square feet of vinyl  can be produced weekly. If a square foot of hardwood flooring yields a profit of $2.5 and a square foot of vinyl planks produces a $3 profit, how many of each type of flooring should be made weekly to maximize the company's profit?

Expected Output Schema:
{
  "variables": {
    "ProductionHardwood": "float",
    "ProductionVinyl": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- F: set of flooring types = {Hardwood, Vinyl}

Parameters:
- profit_Hardwood: profit per square foot of hardwood flooring = 2.5 USD/sq ft
- profit_Vinyl: profit per square foot of vinyl planks = 3 USD/sq ft
- min_demand_Hardwood: minimum required production for hardwood due to sales forecast = 20,000 sq ft/week
- min_demand_Vinyl: minimum required production for vinyl due to sales forecast = 10,000 sq ft/week
- min_total_shipping: minimum combined production to satisfy the shipping contract = 60,000 sq ft/week
- max_capacity_Hardwood: maximum production of hardwood due to labor shortage = 50,000 sq ft/week
- max_capacity_Vinyl: maximum production of vinyl due to labor shortage = 30,000 sq ft/week

Variables:
- ProductionHardwood (float, continuous, ≥ 0): square feet of hardwood produced per week
- ProductionVinyl (float, continuous, ≥ 0): square feet of vinyl produced per week

Objective:
- Maximize Total Profit = (profit_Hardwood * ProductionHardwood) + (profit_Vinyl * ProductionVinyl)

Constraints:
1. Hardwood Minimum Demand: ProductionHardwood ≥ min_demand_Hardwood
2. Vinyl Minimum Demand: ProductionVinyl ≥ min_demand_Vinyl
3. Combined Shipping Requirement: ProductionHardwood + ProductionVinyl ≥ min_total_shipping
4. Hardwood Maximum Capacity: ProductionHardwood ≤ max_capacity_Hardwood
5. Vinyl Maximum Capacity: ProductionVinyl ≤ max_capacity_Vinyl

Note: All units are expressed in square feet per week for production capacity and demand, and in USD per square foot for profit. This complete model can be directly mapped to Python or OR-Tools code for implementation.'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_with_linear_solver():
    # Create the linear solver using the GLOP backend.
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        return None, "Solver not created."

    # Parameters
    profit_Hardwood = 2.5
    profit_Vinyl = 3.0
    min_demand_Hardwood = 20000.0
    min_demand_Vinyl = 10000.0
    min_total_shipping = 60000.0
    max_capacity_Hardwood = 50000.0
    max_capacity_Vinyl = 30000.0

    # Variables: continuous production amounts in square feet per week.
    ProductionHardwood = solver.NumVar(0.0, max_capacity_Hardwood, 'ProductionHardwood')
    ProductionVinyl = solver.NumVar(0.0, max_capacity_Vinyl, 'ProductionVinyl')

    # Constraints
    # 1. Hardwood Minimum Demand: ProductionHardwood >= 20000
    solver.Add(ProductionHardwood >= min_demand_Hardwood)
    # 2. Vinyl Minimum Demand: ProductionVinyl >= 10000
    solver.Add(ProductionVinyl >= min_demand_Vinyl)
    # 3. Combined Shipping Requirement: ProductionHardwood + ProductionVinyl >= 60000
    solver.Add(ProductionHardwood + ProductionVinyl >= min_total_shipping)
    # 4. Hardwood Maximum Capacity (already defined in variable domain): ProductionHardwood <= 50000
    # 5. Vinyl Maximum Capacity (already defined in variable domain): ProductionVinyl <= 30000

    # Objective: Maximize profit = 2.5 * ProductionHardwood + 3 * ProductionVinyl
    objective = solver.Objective()
    objective.SetCoefficient(ProductionHardwood, profit_Hardwood)
    objective.SetCoefficient(ProductionVinyl, profit_Vinyl)
    objective.SetMaximization()

    # Solve the model.
    status = solver.Solve()

    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result["variables"] = {
            "ProductionHardwood": ProductionHardwood.solution_value(),
            "ProductionVinyl": ProductionVinyl.solution_value()
        }
        result["objective"] = objective.Value()
    else:
        result["error"] = "The problem does not have an optimal solution."

    return result, None

def main():
    results = {}
    # Only one formulation is implemented using the linear solver.
    lin_result, error = solve_with_linear_solver()
    if error:
        results["LinearSolverModel"] = {"error": error}
    else:
        results["LinearSolverModel"] = lin_result

    # Print the output in a structured format.
    # The expected schema is:
    # {
    #   "variables": {
    #     "ProductionHardwood": <value>,
    #     "ProductionVinyl": <value>
    #   },
    #   "objective": <objective_value>
    # }
    print(results["LinearSolverModel"])

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
{'variables': {'ProductionHardwood': 50000.0, 'ProductionVinyl': 30000.0}, 'objective': 215000.0}
'''

'''Expected Output:
Expected solution

: {'variables': {'ProductionHardwood': 50000.0, 'ProductionVinyl': 30000.0}, 'objective': 215000.0}'''

