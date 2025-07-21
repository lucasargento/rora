# Problem Description:
'''Problem description: A dessert shop is popular for their only two desserts - matcha ice cream and orange sorbet. Two units of flavouring and four units of ice cream is required to make one order of matcha ice cream. Four units of flavouring and three units of water is required to make an order of orange sorbet. The dessert shop has recently been getting more orders online for orange sorbet and therefore, there should be more orange sorbet made than matcha ice cream. However, at least fifteen percent of desserts made must be matcha ice cream. The dessert shop has available 600 units of ice cream and 550 units of water. How many of each dessert should the shop make to minimize the total amount of flavouring needed?

Expected Output Schema:
{
  "variables": {
    "MatchaIceCream": "float",
    "OrangeSorbet": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Below is one valid mathematical formulation using the five‐element framework. In this model we assume that the decision variables are continuous (although in practice they might be integer counts). Note that “more orange sorbet than matcha” is modeled by requiring that the number of orange sorbet orders is at least one unit higher than the number of matcha ice cream orders (i.e. OrangeSorbet ≥ MatchaIceCream + 1). An alternative formulation would simply require OrangeSorbet ≥ MatchaIceCream if a strict inequality cannot be modeled directly in linear programming.

────────────────────────────
Sets:
• DESSERTS = {MatchaIceCream, OrangeSorbet}

────────────────────────────
Parameters:
• For MatchaIceCream:
  - flavoring_per_order = 2 (flavouring units per order)
  - ice_cream_per_order = 4 (ice cream units per order)
• For OrangeSorbet:
  - flavoring_per_order = 4 (flavouring units per order)
  - water_per_order = 3 (water units per order)
• Available resources:
  - total_ice_cream = 600 units (available ice cream)
  - total_water = 550 units (available water)

  (Note: We assume that the available resources for ice cream and water are measured in consistent units matching the per order requirements.)

────────────────────────────
Variables:
• x_Matcha: Number of orders produced for MatchaIceCream (float, ≥ 0)
• x_Orange: Number of orders produced for OrangeSorbet (float, ≥ 0)

────────────────────────────
Objective:
Minimize total flavouring used:
  Minimize Flavoring = 2*x_Matcha + 4*x_Orange
(The unit is “flavouring units”.)

────────────────────────────
Constraints:
1. Ice Cream Resource Constraint:
   4*x_Matcha ≤ 600
   (Total ice cream used for matcha orders must not exceed available ice cream.)

2. Water Resource Constraint:
   3*x_Orange ≤ 550
   (Total water used for orange sorbet orders must not exceed available water.)

3. Dessert Preference Constraint (more orange sorbet than matcha):
   x_Orange ≥ x_Matcha + 1
   (At least one more order of orange sorbet than matcha is made.
    Alternative: x_Orange ≥ x_Matcha, if a strict inequality cannot be imposed.)

4. Matcha Minimum Proportion Constraint:
   x_Matcha ≥ 0.15*(x_Matcha + x_Orange)
   (At least fifteen percent of total desserts produced must be matcha ice cream.)

5. Nonnegativity Constraint:
   x_Matcha ≥ 0, x_Orange ≥ 0

────────────────────────────
Additional Comments:
• The constraint x_Matcha ≥ 0.15*(x_Matcha + x_Orange) can also be rearranged as 0.85*x_Matcha ≥ 0.15*x_Orange.
• If a linear programming formulation with continuous variables is used, the “+1” in Constraint 3 forces a minimum positive gap. In cases where decision variables must be integers, this ensures that x_Orange is strictly greater than x_Matcha.
• All units have been assumed consistent with the given per order resource requirements.

────────────────────────────
Expected Output Schema (example JSON):

{
  "variables": {
    "MatchaIceCream": "float",
    "OrangeSorbet": "float"
  },
  "objective": "2 * MatchaIceCream + 4 * OrangeSorbet"
}

This completes the structured formulation of the problem.'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_model1():
    """Model 1: Using strict dessert preference constraint x_Orange >= x_Matcha + 1."""
    # Create the linear solver using GLOP backend.
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        return None

    # Decision variables: Continuous nonnegative.
    x_Matcha = solver.NumVar(0.0, solver.infinity(), 'MatchaIceCream')
    x_Orange = solver.NumVar(0.0, solver.infinity(), 'OrangeSorbet')

    # Constraints:
    # 1. Ice Cream Resource Constraint: 4*x_Matcha <= 600.
    solver.Add(4 * x_Matcha <= 600)

    # 2. Water Resource Constraint: 3*x_Orange <= 550.
    solver.Add(3 * x_Orange <= 550)

    # 3. Dessert Preference Constraint: More orange than matcha: x_Orange >= x_Matcha + 1.
    solver.Add(x_Orange >= x_Matcha + 1)

    # 4. Matcha Minimum Proportion Constraint: x_Matcha >= 0.15*(x_Matcha + x_Orange).
    solver.Add(x_Matcha >= 0.15 * (x_Matcha + x_Orange))
    # Alternatively, this can be rearranged to: 0.85*x_Matcha >= 0.15*x_Orange.

    # Objective: Minimize total flavouring used: 2*x_Matcha + 4*x_Orange.
    objective = solver.Objective()
    objective.SetCoefficient(x_Matcha, 2)
    objective.SetCoefficient(x_Orange, 4)
    objective.SetMinimization()

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        solution = {
            "MatchaIceCream": x_Matcha.solution_value(),
            "OrangeSorbet": x_Orange.solution_value(),
            "objective": objective.Value()
        }
        return solution
    else:
        return {"message": "No optimal solution found."}

def solve_model2():
    """Model 2: Using alternative dessert preference constraint x_Orange >= x_Matcha."""
    # Create the linear solver using GLOP backend.
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        return None

    # Decision variables: Continuous nonnegative.
    x_Matcha = solver.NumVar(0.0, solver.infinity(), 'MatchaIceCream')
    x_Orange = solver.NumVar(0.0, solver.infinity(), 'OrangeSorbet')

    # Constraints:
    # 1. Ice Cream Resource Constraint: 4*x_Matcha <= 600.
    solver.Add(4 * x_Matcha <= 600)

    # 2. Water Resource Constraint: 3*x_Orange <= 550.
    solver.Add(3 * x_Orange <= 550)

    # 3. Dessert Preference Constraint: Alternative version (if strict inequality can't be modeled): x_Orange >= x_Matcha.
    solver.Add(x_Orange >= x_Matcha)

    # 4. Matcha Minimum Proportion Constraint: x_Matcha >= 0.15*(x_Matcha + x_Orange).
    solver.Add(x_Matcha >= 0.15 * (x_Matcha + x_Orange))
    # Alternatively: 0.85*x_Matcha >= 0.15*x_Orange.

    # Objective: Minimize total flavouring used: 2*x_Matcha + 4*x_Orange.
    objective = solver.Objective()
    objective.SetCoefficient(x_Matcha, 2)
    objective.SetCoefficient(x_Orange, 4)
    objective.SetMinimization()

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        solution = {
            "MatchaIceCream": x_Matcha.solution_value(),
            "OrangeSorbet": x_Orange.solution_value(),
            "objective": objective.Value()
        }
        return solution
    else:
        return {"message": "No optimal solution found."}

def main():
    results = {}

    # Solve and print results for Model 1.
    model1_result = solve_model1()
    results["Model1"] = {
        "description": "Dessert Preference Constraint: x_Orange >= x_Matcha + 1",
        "result": model1_result
    }

    # Solve and print results for Model 2.
    model2_result = solve_model2()
    results["Model2"] = {
        "description": "Dessert Preference Constraint: x_Orange >= x_Matcha",
        "result": model2_result
    }

    # Print the results in a structured way.
    import json
    print(json.dumps(results, indent=4))

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
{
    "Model1": {
        "description": "Dessert Preference Constraint: x_Orange >= x_Matcha + 1",
        "result": {
            "MatchaIceCream": 0.21428571428571433,
            "OrangeSorbet": 1.2142857142857144,
            "objective": 5.2857142857142865
        }
    },
    "Model2": {
        "description": "Dessert Preference Constraint: x_Orange >= x_Matcha",
        "result": {
            "MatchaIceCream": 0.0,
            "OrangeSorbet": 0.0,
            "objective": 0.0
        }
    }
}
'''

'''Expected Output:
Expected solution

: {'variables': {'MatchaIceCream': 0.0, 'OrangeSorbet': 0.0}, 'objective': 0.0}'''

