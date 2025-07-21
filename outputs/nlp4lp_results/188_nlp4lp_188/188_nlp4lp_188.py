# Problem Description:
'''Problem description: A small bakery has 20000 grams of batter and 14000 grams of milk to make their crepe cakes, sponge cakes, and birthday cakes. A crepe cake needs 400 grams of batter and 200 grams of milk. A sponge cake requires 500 grams of batter and 300 grams of milk. A birthday cake requires 450 grams of batter and 350 grams of milk. If the profit per crepe cake is $12, the profit per sponge cake is $10, and the profit per birthday cake is $15, how many of each should the bakery make to maximize their profit?

Expected Output Schema:
{
  "variables": {
    "UnitsToProduce": {
      "0": "float",
      "1": "float",
      "2": "float"
    }
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Below is the complete structured mathematical model using the five-element framework.

–––––––––––––––––––––––––––––––––––
Sets:
• CakeTypes = {Crepe, Sponge, Birthday}
  (Each element represents a cake type produced by the bakery.)

Parameters:
• available_batter = 20000 grams  
  (Total available batter in grams.)
• available_milk = 14000 grams  
  (Total available milk in grams.)
• batter_required:
  – batter_required[Crepe] = 400 grams per crepe cake  
  – batter_required[Sponge] = 500 grams per sponge cake  
  – batter_required[Birthday] = 450 grams per birthday cake  
  (Batter needed for one unit of each cake type.)
• milk_required:
  – milk_required[Crepe] = 200 grams per crepe cake  
  – milk_required[Sponge] = 300 grams per sponge cake  
  – milk_required[Birthday] = 350 grams per birthday cake  
  (Milk needed for one unit of each cake type.)
• profit_per_cake:
  – profit_per_cake[Crepe] = 12 USD per crepe cake  
  – profit_per_cake[Sponge] = 10 USD per sponge cake  
  – profit_per_cake[Birthday] = 15 USD per birthday cake  
  (Profit earned for each cake type produced.)

Variables:
• x[c] for c in CakeTypes  
  (Number of cake type c produced; decision variables.)
  – Domain: integer, x[c] ≥ 0  
  (Assuming the bakery produces whole cakes.)

Objective:
• Maximize Total_Profit = sum for each c in CakeTypes of (profit_per_cake[c] * x[c])  
  (Total profit from all produced cakes in USD.)

Constraints:
1. Batter Constraint:
  Sum for each c in CakeTypes of (batter_required[c] * x[c]) ≤ available_batter  
   (a total batter usage within 20000 grams.)
2. Milk Constraint:
  Sum for each c in CakeTypes of (milk_required[c] * x[c]) ≤ available_milk  
   (a total milk usage within 14000 grams.)

–––––––––––––––––––––––––––––––––––
For clarity, here is a mapping of the cake types to indices if needed for a programming language implementation:
• Index 0: Crepe cake  
• Index 1: Sponge cake  
• Index 2: Birthday cake

Using the expected output schema, an equivalent representation for the decision variables and objective is:

{
  "variables": {
    "UnitsToProduce": {
      "0": "float",  // corresponds to x[Crepe]
      "1": "float",  // corresponds to x[Sponge]
      "2": "float"   // corresponds to x[Birthday]
    }
  },
  "objective": "float"  // represents Total_Profit = 12*x[Crepe] + 10*x[Sponge] + 15*x[Birthday]"
}

This complete model is self-contained and directly translatable into a working optimization implementation.'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_with_linear_solver():
    # Create the linear solver with the CBC backend.
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Solver not created successfully.")
        return None

    # Cake type indices:
    # 0: Crepe cake, 1: Sponge cake, 2: Birthday cake

    # Parameters
    available_batter = 20000  # grams
    available_milk = 14000    # grams

    batter_required = [400, 500, 450]  # grams per cake type [Crepe, Sponge, Birthday]
    milk_required = [200, 300, 350]    # grams per cake type [Crepe, Sponge, Birthday]
    profit = [12, 10, 15]              # profit per cake [Crepe, Sponge, Birthday]

    # Decision variables: x[i] for number of cakes produced for cake type i.
    # Variables are integer and non-negative.
    x = {}
    for i in range(3):
        # Using integer variables because we assume whole cakes are produced.
        x[i] = solver.IntVar(0, solver.infinity(), f"x[{i}]")

    # Objective: Maximize total profit
    objective = solver.Objective()
    for i in range(3):
        objective.SetCoefficient(x[i], profit[i])
    objective.SetMaximization()

    # Constraint 1: Batter constraint
    batter_constraint = solver.RowConstraint(0, available_batter, "BatterConstraint")
    for i in range(3):
        batter_constraint.SetCoefficient(x[i], batter_required[i])

    # Constraint 2: Milk constraint
    milk_constraint = solver.RowConstraint(0, available_milk, "MilkConstraint")
    for i in range(3):
        milk_constraint.SetCoefficient(x[i], milk_required[i])

    # Solve the model.
    status = solver.Solve()

    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result["model"] = "ORTools Linear Solver (CBC)"
        result["objective"] = objective.Value()
        result["variables"] = {"UnitsToProduce": {
            "0": x[0].solution_value(),
            "1": x[1].solution_value(),
            "2": x[2].solution_value()
        }}
    else:
        result["model"] = "ORTools Linear Solver (CBC)"
        result["message"] = "The problem does not have an optimal solution."

    return result

def main():
    # Only one implementation based on the described mathematical model.
    model1_result = solve_with_linear_solver()
    
    # Print results in a structured way.
    print("=== Optimization Results ===\n")
    if model1_result is not None:
        print("Model: ", model1_result.get("model", "No model information"))
        if "objective" in model1_result:
            print("Optimal Total Profit: {:.2f}".format(model1_result["objective"]))
            print("Decision Variables (UnitsToProduce):")
            for key, value in model1_result["variables"]["UnitsToProduce"].items():
                print("  Cake type {}: {}".format(key, int(value)))
        else:
            print(model1_result.get("message", "No solution found."))
    else:
        print("No results obtained from the model.")

if __name__ == "__main__":
    main()

'''Execution Results:
SUCCESS:
=== Optimization Results ===

Model:  ORTools Linear Solver (CBC)
Optimal Total Profit: 648.00
Decision Variables (UnitsToProduce):
  Cake type 0: 14
  Cake type 1: 0
  Cake type 2: 32
'''

'''Expected Output:
Expected solution

: {'variables': {'UnitsToProduce': {'0': 14.0, '1': 0.0, '2': 32.0}}, 'objective': 648.0}'''

