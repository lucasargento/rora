# Problem Description:
'''Problem description: A flooring company produces engineered laminate planks and carpets. The chief marketer reports an expected demand of at least 15,000 square feet of laminate planks and 5,000 square feet of carpets each week. The shipping contract requires a total of at least 50,000 square feet of products each week. However, due to a shortage of raw materials, no more than 40,000 square feet of laminate planks and 20,000 square feet of carpets can be produced weekly. If a square foot of laminate planks produces a $2.1 profit and a square foot of carpets yields a $3.3 profit, how many of each type of product should be made weekly to maximize the company's profit?

Expected Output Schema:
{
  "variables": {
    "LaminateProduction": "float",
    "CarpetProduction": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- P: set of products = {LaminatePlanks, Carpets}

Parameters:
- min_demand_Laminate: minimum square feet required for laminate planks per week = 15,000 [sq ft]
- min_demand_Carpets: minimum square feet required for carpets per week = 5,000 [sq ft]
- total_shipping_min: minimum total square feet required for shipping per week = 50,000 [sq ft]
- max_capacity_Laminate: maximum production capacity for laminate planks per week = 40,000 [sq ft]
- max_capacity_Carpets: maximum production capacity for carpets per week = 20,000 [sq ft]
- profit_Laminate: profit per square foot for laminate planks = 2.1 [USD per sq ft]
- profit_Carpets: profit per square foot for carpets = 3.3 [USD per sq ft]

Variables:
- LaminateProduction: weekly production of laminate planks [continuous, in sq ft] (>= 0)
- CarpetProduction: weekly production of carpets [continuous, in sq ft] (>= 0)

Objective:
Maximize total profit defined as:
   Total Profit = profit_Laminate * LaminateProduction + profit_Carpets * CarpetProduction

Constraints:
1. Laminate demand constraint: LaminateProduction >= min_demand_Laminate
2. Carpets demand constraint: CarpetProduction >= min_demand_Carpets
3. Total shipping constraint: LaminateProduction + CarpetProduction >= total_shipping_min
4. Laminate production capacity constraint: LaminateProduction <= max_capacity_Laminate
5. Carpets production capacity constraint: CarpetProduction <= max_capacity_Carpets

-------------------------------------------------
Output in the expected JSON schema:

{
  "variables": {
    "LaminateProduction": "float (weekly sq ft produced for laminate planks)",
    "CarpetProduction": "float (weekly sq ft produced for carpets)"
  },
  "objective": "2.1 * LaminateProduction + 3.3 * CarpetProduction"
}'''

# Generated Code:
from ortools.linear_solver import pywraplp
import json

def solve_with_linear_solver():
    # Create the linear solver with GLOP backend.
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        return None

    # Parameters
    min_demand_laminate = 15000
    min_demand_carpets = 5000
    total_shipping_min = 50000
    max_capacity_laminate = 40000
    max_capacity_carpets = 20000
    profit_laminate = 2.1
    profit_carpets = 3.3

    # Variables: continuous production amounts (in square feet)
    laminate = solver.NumVar(0.0, max_capacity_laminate, 'LaminateProduction')
    carpets = solver.NumVar(0.0, max_capacity_carpets, 'CarpetProduction')

    # Constraints:
    # 1. Minimum demand constraints
    solver.Add(laminate >= min_demand_laminate)
    solver.Add(carpets >= min_demand_carpets)

    # 2. Total shipping minimum constraint
    solver.Add(laminate + carpets >= total_shipping_min)

    # (Capacity constraints are already enforced by variable upper bounds)

    # Objective: maximize profit
    objective = solver.Objective()
    objective.SetCoefficient(laminate, profit_laminate)
    objective.SetCoefficient(carpets, profit_carpets)
    objective.SetMaximization()

    # Solve the problem
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        solution = {
            "variables": {
                "LaminateProduction": f"{laminate.solution_value()} (weekly sq ft produced for laminate planks)",
                "CarpetProduction": f"{carpets.solution_value()} (weekly sq ft produced for carpets)"
            },
            "objective": objective.Value()
        }
    else:
        solution = {"message": "No optimal solution found or the problem is infeasible."}

    return solution

def main():
    results = {}

    # Implementation using linear solver (GLOP)
    results["LinearSolver"] = solve_with_linear_solver()

    # Print results in a structured JSON format
    print(json.dumps(results, indent=2))

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
{
  "LinearSolver": {
    "variables": {
      "LaminateProduction": "40000.0 (weekly sq ft produced for laminate planks)",
      "CarpetProduction": "20000.0 (weekly sq ft produced for carpets)"
    },
    "objective": 150000.0
  }
}
'''

'''Expected Output:
Expected solution

: {'variables': {'LaminateProduction': 40000.0, 'CarpetProduction': 20000.0}, 'objective': 150000.0}'''

