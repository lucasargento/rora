# Problem Description:
'''Problem description: A toy store sells plush toys and dolls. Each plush toy costs the store $3 and each doll costs the store $2. The store owner can spend at most $700 on inventory. Each plush toy is then sold for a profit of $4 while each doll is sold for a profit of $2. The owner estimates that at least 90 plush toys but at most 190 plush toys are sold each month. He also estimates that the number of dolls sold is at most twice the amount of plush toys sold. How many of each should be bought and sold to maximize profit?

Expected Output Schema:
{
  "variables": {
    "NumberPlushToys": "float",
    "NumberDolls": "float",
    "NumberPlushToysSold": "float",
    "NumberDollsSold": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Below is one clear formulation of the problem using the five‐element framework. Note that we distinguish between the quantity bought (the inventory decision) and the quantity sold (the sales decision). In an optimal solution (without further market considerations such as unsold inventory costs apart from the purchase cost) the purchased quantities would typically equal the sold quantities. However, the model below leaves open the possibility that not all purchased items are sold, by explicitly linking sales to available inventory.

-----------------------------------------------------------
Sets:
• Types = {PlushToys, Dolls}

-----------------------------------------------------------
Parameters:
• cost_Plush = 3 (US Dollars per plush toy purchased)
• cost_Doll = 2 (US Dollars per doll purchased)
• profit_Plush = 4 (US Dollars profit per plush toy sold)
• profit_Doll = 2 (US Dollars profit per doll sold)
• inventory_budget = 700 (US Dollars available for purchasing inventory)
• plush_sales_lower = 90 (minimum number of plush toys sold per month)
• plush_sales_upper = 190 (maximum number of plush toys sold per month)
• doll_to_plush_ratio = 2 (the number of dolls sold is at most twice the plush toys sold)

-----------------------------------------------------------
Variables (all decision variables are assumed to be nonnegative integers):
• NumberPlushToys: number of plush toys bought [units]
• NumberDolls: number of dolls bought [units]
• NumberPlushToysSold: number of plush toys sold [units]
• NumberDollsSold: number of dolls sold [units]

-----------------------------------------------------------
Objective:
Maximize total net profit given by:
  Total Profit = (profit_Plush × NumberPlushToysSold) + (profit_Doll × NumberDollsSold)

That is, maximize: 4 × NumberPlushToysSold + 2 × NumberDollsSold

-----------------------------------------------------------
Constraints:
1. Inventory Budget Constraint:
  (cost_Plush × NumberPlushToys) + (cost_Doll × NumberDolls) ≤ inventory_budget
  That is, 3 × NumberPlushToys + 2 × NumberDolls ≤ 700

2. Sales Cannot Exceed Inventory (feasibility constraints):
  NumberPlushToysSold ≤ NumberPlushToys 
  NumberDollsSold ≤ NumberDolls

3. Demand Range for Plush Toys:
  plush_sales_lower ≤ NumberPlushToysSold ≤ plush_sales_upper 
  That is, 90 ≤ NumberPlushToysSold ≤ 190

4. Sales Ratio Constraint for Dolls:
  NumberDollsSold ≤ doll_to_plush_ratio × NumberPlushToysSold 
  That is, NumberDollsSold ≤ 2 × NumberPlushToysSold

-----------------------------------------------------------
Additional Comments:
• The economic interpretation is that the store must decide how many plush toys and dolls to purchase under a limited inventory budget, and then how many of these to sell in order to maximize profit. The profit is computed only on sold items.
• It is assumed that unsold inventory does not generate profit and that additional costs (e.g., storage, spoilage) are not considered.
• All monetary parameters are expressed in US Dollars per unit, and all quantities are expressed in number of units.
• If desired, one could enforce that the sales variables equal the purchase variables. Here, we allow the possibility of having extra purchased units that are not sold, by ensuring only that sales do not exceed purchases.

-----------------------------------------------------------
Expected Output Schema (as expressed in a JSON-like structure):

{
  "variables": {
    "NumberPlushToys": "integer, nonnegative, number of plush toys bought [units]",
    "NumberDolls": "integer, nonnegative, number of dolls bought [units]",
    "NumberPlushToysSold": "integer, nonnegative, number of plush toys sold [units]",
    "NumberDollsSold": "integer, nonnegative, number of dolls sold [units]"
  },
  "objective": "4 * NumberPlushToysSold + 2 * NumberDollsSold (maximize total profit in US Dollars)"
}

This structured model fully describes the original real-world problem in a way that can be directly mapped to implementations in Python, OR-Tools, or similar optimization frameworks.'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_model_version1():
    """Version 1: Inventory and Sales decisions are modeled separately."""
    # Create the solver using CBC backend
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Solver not created.")
        return None

    # Decision variables: nonnegative integers
    NumberPlushToys = solver.IntVar(0.0, solver.infinity(), 'NumberPlushToys')      # plush toys bought
    NumberDolls = solver.IntVar(0.0, solver.infinity(), 'NumberDolls')              # dolls bought
    NumberPlushToysSold = solver.IntVar(0.0, solver.infinity(), 'NumberPlushToysSold')  # plush toys sold
    NumberDollsSold = solver.IntVar(0.0, solver.infinity(), 'NumberDollsSold')           # dolls sold

    # Data parameters
    cost_Plush = 3
    cost_Doll = 2
    profit_Plush = 4
    profit_Doll = 2
    inventory_budget = 700
    plush_sales_lower = 90
    plush_sales_upper = 190
    doll_to_plush_ratio = 2

    # Constraint 1: Inventory Budget Constraint (cost constraint)
    solver.Add(cost_Plush * NumberPlushToys + cost_Doll * NumberDolls <= inventory_budget)

    # Constraint 2: Sales cannot exceed inventory
    solver.Add(NumberPlushToysSold <= NumberPlushToys)
    solver.Add(NumberDollsSold <= NumberDolls)

    # Constraint 3: Plush toys sales limits
    solver.Add(NumberPlushToysSold >= plush_sales_lower)
    solver.Add(NumberPlushToysSold <= plush_sales_upper)

    # Constraint 4: Dolls sales limit relative to plush toys sold
    solver.Add(NumberDollsSold <= doll_to_plush_ratio * NumberPlushToysSold)

    # Objective: maximize profit from sold items
    objective = solver.Objective()
    objective.SetCoefficient(NumberPlushToysSold, profit_Plush)
    objective.SetCoefficient(NumberDollsSold, profit_Doll)
    objective.SetMaximization()

    status = solver.Solve()

    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "model": "Version 1 (Separate Inventory and Sales Decisions)",
            "variables": {
                "NumberPlushToys": NumberPlushToys.solution_value(),
                "NumberDolls": NumberDolls.solution_value(),
                "NumberPlushToysSold": NumberPlushToysSold.solution_value(),
                "NumberDollsSold": NumberDollsSold.solution_value()
            },
            "objective": objective.Value()
        }
    else:
        result = {
            "model": "Version 1 (Separate Inventory and Sales Decisions)",
            "status": "No optimal solution found."
        }
    return result

def solve_model_version2():
    """Version 2: Enforce that all purchased units are sold (inventory equals sales)."""
    # Create the solver using CBC backend
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Solver not created.")
        return None

    # Decision variables: nonnegative integers
    # In this version, we force the sales variables to equal the purchase variables.
    NumberPlushToys = solver.IntVar(0.0, solver.infinity(), 'NumberPlushToys')  # plush toys bought and sold
    NumberDolls = solver.IntVar(0.0, solver.infinity(), 'NumberDolls')          # dolls bought and sold

    # Data parameters
    cost_Plush = 3
    cost_Doll = 2
    profit_Plush = 4
    profit_Doll = 2
    inventory_budget = 700
    plush_sales_lower = 90
    plush_sales_upper = 190
    doll_to_plush_ratio = 2

    # Constraint 1: Inventory Budget Constraint
    solver.Add(cost_Plush * NumberPlushToys + cost_Doll * NumberDolls <= inventory_budget)

    # Since sales equal purchase, add additional sales/demand constraints:
    # Plush toys sales limits directly on purchased units.
    solver.Add(NumberPlushToys >= plush_sales_lower)
    solver.Add(NumberPlushToys <= plush_sales_upper)

    # Dolls sales constraint: the number of dolls sold (i.e., purchased) is at most twice the number of plush toys sold.
    solver.Add(NumberDolls <= doll_to_plush_ratio * NumberPlushToys)

    # Objective: maximize profit (all purchased units are sold)
    objective = solver.Objective()
    objective.SetCoefficient(NumberPlushToys, profit_Plush)
    objective.SetCoefficient(NumberDolls, profit_Doll)
    objective.SetMaximization()

    status = solver.Solve()

    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "model": "Version 2 (Purchase equals Sales)",
            "variables": {
                "NumberPlushToys": NumberPlushToys.solution_value(),
                "NumberDolls": NumberDolls.solution_value(),
                "NumberPlushToysSold": NumberPlushToys.solution_value(),  # same as purchased
                "NumberDollsSold": NumberDolls.solution_value()           # same as purchased
            },
            "objective": objective.Value()
        }
    else:
        result = {
            "model": "Version 2 (Purchase equals Sales)",
            "status": "No optimal solution found."
        }
    return result

def main():
    print("Solving both model versions...\n")
    results = []
    res1 = solve_model_version1()
    res2 = solve_model_version2()
    results.append(res1)
    results.append(res2)

    # Pretty print the results
    for res in results:
        print("Model:", res.get("model", ""))
        if "status" in res:
            print("Status:", res["status"])
        else:
            print("Optimal Variables:")
            for var, value in res["variables"].items():
                print("  ", var, "=", value)
            print("Optimal Objective Value:", res["objective"])
        print("-" * 50)

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Solving both model versions...

Model: Version 1 (Separate Inventory and Sales Decisions)
Optimal Variables:
   NumberPlushToys = 190.0
   NumberDolls = 65.0
   NumberPlushToysSold = 190.0
   NumberDollsSold = 65.0
Optimal Objective Value: 890.0
--------------------------------------------------
Model: Version 2 (Purchase equals Sales)
Optimal Variables:
   NumberPlushToys = 190.0
   NumberDolls = 65.0
   NumberPlushToysSold = 190.0
   NumberDollsSold = 65.0
Optimal Objective Value: 890.0
--------------------------------------------------
'''

'''Expected Output:
Expected solution

: {'variables': {'NumberPlushToys': 190.0, 'NumberDolls': 65.0, 'NumberPlushToysSold': 190.0, 'NumberDollsSold': 65.0}, 'objective': 890.0}'''

