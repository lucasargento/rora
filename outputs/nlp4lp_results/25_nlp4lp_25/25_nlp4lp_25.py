# Problem Description:
'''Problem description: A food truck owner can spend at most $20000 on mangos and guavas. A mango costs the food truck owner $5 and a guava costs him $3. Spices are added and each mango is sold for a profit of $3 while each guava is sold for a profit of $4. The owner estimates that at least 100 mangos but at the most 150 are sold each month. He also estimates that the number of guavas sold is at most a third of the mangos sold. How many mangos and guavas should be sold in order to maximize the profit?

Expected Output Schema:
{
  "variables": {
    "QuantityMango": "float",
    "QuantityGuava": "float",
    "MangosSold": "float",
    "GuavasSold": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Below is a complete five‐element formulation that stays true to the problem details. Note that in this model we assume that the number of fruits purchased equals the number sold so that QuantityMango equals MangosSold and QuantityGuava equals GuavasSold. You can later choose to treat them as separate decisions if the problem’s business logic requires it.

-----------------------------------------------------------
Sets:
• Fruits = {Mango, Guava}

-----------------------------------------------------------
Parameters:
• max_budget = 20000  
  – The maximum dollars available to spend on fruits.
• cost_Mango = 5  
  – The cost in dollars per mango.
• cost_Guava = 3  
  – The cost in dollars per guava.
• profit_Mango = 3  
  – The profit in dollars earned from selling one mango.
• profit_Guava = 4  
  – The profit in dollars earned from selling one guava.
• min_mangos_sold = 100  
  – The minimum number of mangos that must be sold each month.
• max_mangos_sold = 150  
  – The maximum number of mangos that can be sold each month.
• guava_ratio = 1/3  
  – Guavas sold cannot exceed one third of the number of mangos sold.
   (Interpretation: GuavasSold ≤ (1/3) × MangosSold)

-----------------------------------------------------------
Variables:
• MangosSold  
  – Number of mangos sold [integer, units]  
• GuavasSold  
  – Number of guavas sold [integer, units]  
• QuantityMango  
  – Total number of mangos purchased [float]; in this model we set QuantityMango = MangosSold.
• QuantityGuava  
  – Total number of guavas purchased [float]; here QuantityGuava = GuavasSold.

-----------------------------------------------------------
Objective:
Maximize profit, defined as:
  Total Profit = profit_Mango × MangosSold + profit_Guava × GuavasSold  
  or equivalently, maximize 3 × MangosSold + 4 × GuavasSold.
  (This formulation assumes profit is calculated after accounting for the cost of spices; only the per-unit profits of fruits are used here as per the problem description.)

-----------------------------------------------------------
Constraints:
1. Budget Constraint:  
  cost_Mango × MangosSold + cost_Guava × GuavasSold ≤ max_budget  
  In expression form: 5 × MangosSold + 3 × GuavasSold ≤ 20000  
  (Unit: dollars)

2. Mango Sales Range:  
  min_mangos_sold ≤ MangosSold ≤ max_mangos_sold  
  That is, 100 ≤ MangosSold ≤ 150

3. Guava Sales Ratio Constraint:  
  GuavasSold ≤ guava_ratio × MangosSold  
  That is, GuavasSold ≤ (1/3) × MangosSold

-----------------------------------------------------------
Comments:
• All cost and profit parameters are in U.S. dollars per unit, and all sales numbers are expressed in units.  
• The assumption that QuantityMango equals MangosSold (and similarly for guavas) is made since the problem does not distinguish between purchase quantity and sold quantity.  
• Decision variables are assumed to be nonnegative integers, although they are marked as floats in the expected output schema. This choice can be adapted if fractional sales are acceptable in a relaxed model.

This structured model conforms to the five-element framework and is ready for implementation in OR-Tools or similar optimization libraries.

-----------------------------------------------------------

Expected Output Schema:
{
  "variables": {
    "QuantityMango": "float",
    "QuantityGuava": "float",
    "MangosSold": "float",
    "GuavasSold": "float"
  },
  "objective": "float"
}'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp
import json

def solve_model1():
    """Model 1: Single set of variables, where Quantity equals Sales.
    Variables:
        MangosSold (float, between 100 and 150)
        GuavasSold (float, >= 0)
    Constraints:
        5 * MangosSold + 3 * GuavasSold <= 20000    (Budget constraint)
        GuavasSold <= (1/3) * MangosSold              (Guava ratio)
    Objective:
        Maximize 3 * MangosSold + 4 * GuavasSold
    Note: Here QuantityMango = MangosSold and QuantityGuava = GuavasSold.
    """
    # Create a MIP solver using CBC
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Solver not available.")
        return None

    # Define variables. Although expected schema uses "float", we use non-negative variables.
    MangosSold = solver.NumVar(100.0, 150.0, 'MangosSold')  # Sales must be between 100 and 150.
    GuavasSold = solver.NumVar(0.0, solver.infinity(), 'GuavasSold')

    # Budget constraint: 5 * MangosSold + 3 * GuavasSold <= 20000
    solver.Add(5 * MangosSold + 3 * GuavasSold <= 20000)

    # Guava ratio constraint: GuavasSold <= (1/3) * MangosSold
    solver.Add(GuavasSold <= (1/3) * MangosSold)

    # Set the objective function: maximize 3*MangosSold + 4*GuavasSold
    objective = solver.Objective()
    objective.SetCoefficient(MangosSold, 3)
    objective.SetCoefficient(GuavasSold, 4)
    objective.SetMaximization()

    # Solve the problem.
    status = solver.Solve()

    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        # In model 1, Quantity variables equal the sales variables.
        result = {
            "variables": {
                "QuantityMango": MangosSold.solution_value(),
                "QuantityGuava": GuavasSold.solution_value(),
                "MangosSold": MangosSold.solution_value(),
                "GuavasSold": GuavasSold.solution_value()
            },
            "objective": objective.Value()
        }
    else:
        result = {"error": "The problem does not have an optimal solution."}
    return result

def solve_model2():
    """Model 2: Separate decisions for Purchase (Quantity) and Sales.
    Variables:
        Q_Mango: Quantity of mangos purchased (float, >=0)
        Q_Guava: Quantity of guavas purchased (float, >=0)
        S_Mango: Mangos sold (float, between 100 and 150)
        S_Guava: Guavas sold (float, >=0)
    Additional constraints:
        1. Budget: 5 * Q_Mango + 3 * Q_Guava <= 20000.
        2. Sales must not exceed purchases: S_Mango <= Q_Mango, S_Guava <= Q_Guava.
        3. Guava ratio: S_Guava <= (1/3) * S_Mango.
    Objective:
        Maximize profit = 3 * S_Mango + 4 * S_Guava.
    In an optimal solution, it is expected that Q_Mango = S_Mango and Q_Guava = S_Guava.
    """
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Solver not available.")
        return None

    # Purchase (Quantity) variables: They can be any nonnegative number.
    Q_Mango = solver.NumVar(0.0, solver.infinity(), 'QuantityMango')
    Q_Guava = solver.NumVar(0.0, solver.infinity(), 'QuantityGuava')

    # Sales variables:
    S_Mango = solver.NumVar(100.0, 150.0, 'MangosSold')
    S_Guava = solver.NumVar(0.0, solver.infinity(), 'GuavasSold')

    # Budget constraint on purchases: 5 * Q_Mango + 3 * Q_Guava <= 20000.
    solver.Add(5 * Q_Mango + 3 * Q_Guava <= 20000)

    # Sales cannot exceed what is purchased.
    solver.Add(S_Mango <= Q_Mango)
    solver.Add(S_Guava <= Q_Guava)

    # Guava sales ratio constraint: S_Guava <= (1/3) * S_Mango.
    solver.Add(S_Guava <= (1/3) * S_Mango)

    # Objective function: maximize profit from sold fruits = 3 * S_Mango + 4 * S_Guava.
    objective = solver.Objective()
    objective.SetCoefficient(S_Mango, 3)
    objective.SetCoefficient(S_Guava, 4)
    objective.SetMaximization()

    # Solve the model.
    status = solver.Solve()

    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        # In a realistic optimal solution, purchase equals sales.
        result = {
            "variables": {
                "QuantityMango": Q_Mango.solution_value(),
                "QuantityGuava": Q_Guava.solution_value(),
                "MangosSold": S_Mango.solution_value(),
                "GuavasSold": S_Guava.solution_value()
            },
            "objective": objective.Value()
        }
    else:
        result = {"error": "The problem does not have an optimal solution."}
    return result

def main():
    results = {}

    # Model 1: Combined Purchase and Sales.
    model1_result = solve_model1()
    results["Model_1"] = model1_result

    # Model 2: Separate Purchase and Sales decisions.
    model2_result = solve_model2()
    results["Model_2"] = model2_result

    # Print the structured results for each model.
    print(json.dumps(results, indent=4))

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
{
    "Model_1": {
        "variables": {
            "QuantityMango": 150.0,
            "QuantityGuava": 50.0,
            "MangosSold": 150.0,
            "GuavasSold": 50.0
        },
        "objective": 650.0
    },
    "Model_2": {
        "variables": {
            "QuantityMango": 3970.0,
            "QuantityGuava": 50.0,
            "MangosSold": 150.0,
            "GuavasSold": 50.0
        },
        "objective": 650.0
    }
}
'''

'''Expected Output:
Expected solution

: {'variables': {'QuantityMango': -0.0, 'QuantityGuava': -0.0, 'MangosSold': 150.0, 'GuavasSold': 50.0}, 'objective': 650.0}'''

