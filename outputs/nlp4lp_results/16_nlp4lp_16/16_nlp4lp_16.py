# Problem Description:
'''Problem description: An electronics store wants to optimize how many phones and laptops are enough to keep in inventory. A phone will earn the store $120 in profits, and a laptop will earn $40. A phone requires 1 sq ft of floor space, whereas a laptop requires 4 sq ft. In total, 400 sq ft of floor space is available. The store stocks only phones and laptops. Corporate has required that at least 80% of all appliances in stock be laptops. Finally, a phone costs $400 for the store, and a laptop, $100. The store wants to spend at most $6000. Formulate an LP that can be used to maximize the store's profit.

Expected Output Schema:
{
  "variables": {
    "NumberOfPhones": "float",
    "NumberOfLaptops": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- Items: set of inventory items = {Phone, Laptop}

Parameters:
- profit_item: profit earned per unit sold for each item (in USD per unit) with
  - profit_Phone = 120
  - profit_Laptop = 40
- space_item: floor space required per unit (in square feet per unit) with
  - space_Phone = 1
  - space_Laptop = 4
- total_floor_space: total available floor space = 400 (sq ft)
- cost_item: purchase cost per unit for each item (in USD per unit) with
  - cost_Phone = 400
  - cost_Laptop = 100
- max_total_cost: maximum spending allowed = 6000 (USD)
- laptop_ratio_min: minimum fraction of total appliances that must be laptops = 0.8

Variables:
- NumberOfPhones: number of phones to stock (continuous ≥ 0, units)
- NumberOfLaptops: number of laptops to stock (continuous ≥ 0, units)

Objective:
- Maximize total profit, where
  TotalProfit = (profit_Phone * NumberOfPhones) + (profit_Laptop * NumberOfLaptops)

Constraints:
1. Floor Space Constraint:
   (space_Phone * NumberOfPhones) + (space_Laptop * NumberOfLaptops) ≤ total_floor_space
   → (1 * NumberOfPhones) + (4 * NumberOfLaptops) ≤ 400

2. Cost Constraint:
   (cost_Phone * NumberOfPhones) + (cost_Laptop * NumberOfLaptops) ≤ max_total_cost
   → (400 * NumberOfPhones) + (100 * NumberOfLaptops) ≤ 6000

3. Laptop Inventory Ratio Constraint:
   Laptops must be at least 80% of the total stock
   → NumberOfLaptops ≥ laptop_ratio_min * (NumberOfPhones + NumberOfLaptops)
   (This can be rearranged as:  NumberOfLaptops - 0.8 * NumberOfLaptops ≥ 0.8 * NumberOfPhones, i.e., 0.2 * NumberOfLaptops ≥ 0.8 * NumberOfPhones, or equivalently NumberOfLaptops ≥ 4 * NumberOfPhones)

Model Comments:
- All units are consistent: profits and costs are in USD per unit, floor space is in square feet, and inventory counts are in units.
- Although inventory counts are naturally integers, they are defined as continuous (float) variables for LP relaxation, aligning with the schema requirements.
- The laptop ratio constraint ensures that at least 80% of all appliances in stock are laptops.

Overall Structured Model:
{
  "Sets": {
    "Items": ["Phone", "Laptop"]
  },
  "Parameters": {
    "profit_item": {"Phone": 120, "Laptop": 40},
    "space_item": {"Phone": 1, "Laptop": 4},
    "total_floor_space": 400,
    "cost_item": {"Phone": 400, "Laptop": 100},
    "max_total_cost": 6000,
    "laptop_ratio_min": 0.8
  },
  "Variables": {
    "NumberOfPhones": "float, >= 0",
    "NumberOfLaptops": "float, >= 0"
  },
  "Objective": "Maximize total profit = (120 * NumberOfPhones) + (40 * NumberOfLaptops)",
  "Constraints": [
    "Floor Space: (1 * NumberOfPhones) + (4 * NumberOfLaptops) <= 400",
    "Cost: (400 * NumberOfPhones) + (100 * NumberOfLaptops) <= 6000",
    "Laptop Ratio: NumberOfLaptops >= 0.8 * (NumberOfPhones + NumberOfLaptops)  [equivalently, NumberOfLaptops >= 4 * NumberOfPhones]"
  ]
}'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_model_version1():
    # Create the solver with GLOP backend.
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Solver not created.")
        return None

    # Define variables for model version 1.
    # x: NumberOfPhones, y: NumberOfLaptops.
    x = solver.NumVar(0.0, solver.infinity(), 'NumberOfPhones')
    y = solver.NumVar(0.0, solver.infinity(), 'NumberOfLaptops')

    # Constraint 1: Floor Space constraint: 1*x + 4*y <= 400.
    solver.Add(x + 4 * y <= 400)

    # Constraint 2: Cost constraint: 400*x + 100*y <= 6000.
    solver.Add(400 * x + 100 * y <= 6000)

    # Constraint 3: Laptop Inventory Ratio constraint (using original formulation):
    # y >= 0.8*(x + y)
    # This can be rearranged to: y >= 0.8*x + 0.8*y  --> 0.2*y >= 0.8*x  --> y >= 4*x.
    # However, for model version 1, we add it directly as provided.
    solver.Add(y >= 0.8 * (x + y))

    # Objective: maximize profit = 120*x + 40*y.
    solver.Maximize(120 * x + 40 * y)

    status = solver.Solve()

    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "NumberOfPhones": x.solution_value(),
            "NumberOfLaptops": y.solution_value(),
            "objective": solver.Objective().Value()
        }
    else:
        result = {"error": "The problem does not have an optimal solution."}

    return result

def solve_model_version2():
    # Create the solver with GLOP backend.
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Solver not created.")
        return None

    # Define variables for model version 2.
    # x: NumberOfPhones, y: NumberOfLaptops.
    x = solver.NumVar(0.0, solver.infinity(), 'NumberOfPhones')
    y = solver.NumVar(0.0, solver.infinity(), 'NumberOfLaptops')

    # Constraint 1: Floor Space constraint: 1*x + 4*y <= 400.
    solver.Add(x + 4 * y <= 400)

    # Constraint 2: Cost constraint: 400*x + 100*y <= 6000.
    solver.Add(400 * x + 100 * y <= 6000)

    # Constraint 3: Laptop Inventory Ratio constraint (using alternate reformulation):
    # y >= 4*x.
    solver.Add(y >= 4 * x)

    # Objective: maximize profit = 120*x + 40*y.
    solver.Maximize(120 * x + 40 * y)

    status = solver.Solve()

    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "NumberOfPhones": x.solution_value(),
            "NumberOfLaptops": y.solution_value(),
            "objective": solver.Objective().Value()
        }
    else:
        result = {"error": "The problem does not have an optimal solution."}

    return result

def main():
    # Solve using model version 1 (original laptop ratio formulation)
    result_v1 = solve_model_version1()
    # Solve using model version 2 (reformulated laptop ratio constraint)
    result_v2 = solve_model_version2()

    print("Results for Model Version 1 (using y >= 0.8*(x+y)):")
    if "error" in result_v1:
        print(result_v1["error"])
    else:
        print("NumberOfPhones:", result_v1["NumberOfPhones"])
        print("NumberOfLaptops:", result_v1["NumberOfLaptops"])
        print("Objective (Total Profit):", result_v1["objective"])

    print("\nResults for Model Version 2 (using y >= 4*x):")
    if "error" in result_v2:
        print(result_v2["error"])
    else:
        print("NumberOfPhones:", result_v2["NumberOfPhones"])
        print("NumberOfLaptops:", result_v2["NumberOfLaptops"])
        print("Objective (Total Profit):", result_v2["objective"])

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Results for Model Version 1 (using y >= 0.8*(x+y)):
NumberOfPhones: 0.0
NumberOfLaptops: 59.99999999999999
Objective (Total Profit): 2399.9999999999995

Results for Model Version 2 (using y >= 4*x):
NumberOfPhones: 0.0
NumberOfLaptops: 60.00000000000001
Objective (Total Profit): 2400.0000000000005
'''

'''Expected Output:
Expected solution

: {'variables': {'NumberOfPhones': 0.0, 'NumberOfLaptops': 60.0}, 'objective': 2400.0}'''

