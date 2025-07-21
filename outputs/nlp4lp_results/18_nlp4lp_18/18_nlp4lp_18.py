# Problem Description:
'''Problem description: A suspicious factory has 100 sq. feet of space. It makes bootleg phones and laptops. Phones require 2 hours of labor and cost $12 for each sq. foot of space allocated for phone production (cost of electricity and equipment). Laptops require 3 hours of labor and cost $15 for each sq. foot of space allocated for laptop production. Phones produce a net revenue of $50 per sq. foot while laptops produce a net revenue of $70 per sq. foot. The factory wants to spend at most $5000 and 2000 hours of labor. What is the optimal factory layout to maximize revenue?

Expected Output Schema:
{
  "variables": {
    "AllocatedSpace": {
      "0": "float",
      "1": "float"
    }
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Below is one complete formulation of the factory layout problem using the five-element framework.

--------------------------------------------------

Sets:
- P: set of products = {Phone, Laptop}

Parameters:
- total_space: total available factory floor space [sq. feet] = 100
- cost_per_sqft:
  • phone: cost per square foot for phone production [USD/sq.ft] = 12
  • laptop: cost per square foot for laptop production [USD/sq.ft] = 15
- net_revenue_per_sqft:
  • phone: net revenue per square foot for phone production [USD/sq.ft] = 50
  • laptop: net revenue per square foot for laptop production [USD/sq.ft] = 70
- labor_required:
  • phone: labor hours required per square foot for phone production [hours/sq.ft] = 2
  • laptop: labor hours required per square foot for laptop production [hours/sq.ft] = 3
- cost_limit: maximum spending for production inputs [USD] = 5000
- labor_limit: maximum labor hours available [hours] = 2000

Variables:
- x_p: allocated space for product p ∈ P in square feet (continuous variable, ≥ 0)
  • x_phone corresponds to space for phone production
  • x_laptop corresponds to space for laptop production

Objective:
- Maximize total net revenue = (net_revenue_per_sqft[phone] * x_phone) + (net_revenue_per_sqft[laptop] * x_laptop)
  (Note: The term “net revenue” already represents revenue in excess of other variable production costs. The production costs appear only as constraints through the spending limit.)

Constraints:
1. Space constraint:
   - x_phone + x_laptop ≤ total_space
2. Cost constraint:
   - (cost_per_sqft[phone] * x_phone) + (cost_per_sqft[laptop] * x_laptop) ≤ cost_limit
3. Labor constraint:
   - (labor_required[phone] * x_phone) + (labor_required[laptop] * x_laptop) ≤ labor_limit
4. Non-negativity:
   - For each p in P, x_p ≥ 0

--------------------------------------------------

Comments:
- All parameters are expressed with consistent units: space in square feet, cost and revenue in US dollars per square foot, and labor in hours per square foot.
- The decision variables (x_phone and x_laptop) represent how many square feet of the available 100 sq. feet are allocated to each product.
- The objective maximizes total net revenue subject to physical (space) and operational (labor and expenditure) constraints.

--------------------------------------------------

Alternative modeling note:
If one instead prefers to separately account for revenue and the cost of space allocation (i.e., treating revenue and cost as separate expressions), an alternative formulation would be:
  • Total revenue = (50 * x_phone) + (70 * x_laptop)
  • Total cost = (12 * x_phone) + (15 * x_laptop)
  • Then the net objective would be: maximize (Total revenue – Total cost)
In that case, the cost constraint (Total cost ≤ 5000) would still be enforced, and the objective would explicitly subtract total cost from total revenue. However, based on the phrase “net revenue” in the problem statement, the first formulation is the direct translation.'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_model_version1():
    # Model Version 1:
    # Formulation:
    #   Maximize: 50*x_phone + 70*x_laptop
    #   Subject to:
    #       x_phone + x_laptop <= 100
    #       12*x_phone + 15*x_laptop <= 5000
    #       2*x_phone + 3*x_laptop <= 2000
    #       x_phone, x_laptop >= 0

    # Create the linear solver with the GLOP backend.
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        return None, None

    # Decision variables
    x_phone = solver.NumVar(0.0, solver.infinity(), 'x_phone')
    x_laptop = solver.NumVar(0.0, solver.infinity(), 'x_laptop')

    # Constraints
    # Space constraint
    solver.Add(x_phone + x_laptop <= 100)
    # Cost constraint
    solver.Add(12 * x_phone + 15 * x_laptop <= 5000)
    # Labor constraint
    solver.Add(2 * x_phone + 3 * x_laptop <= 2000)

    # Objective: maximize net revenue (as provided)
    objective = solver.Objective()
    objective.SetCoefficient(x_phone, 50)
    objective.SetCoefficient(x_laptop, 70)
    objective.SetMaximization()

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL:
        solution = {
            "AllocatedSpace": {
                "0": x_phone.solution_value(),
                "1": x_laptop.solution_value()
            }
        }
        objective_value = objective.Value()
        return solution, objective_value
    else:
        return None, None

def solve_model_version2():
    # Model Version 2:
    # Alternative formulation where:
    #   Total revenue = 50*x_phone + 70*x_laptop
    #   Total cost = 12*x_phone + 15*x_laptop
    #   Net objective = Total revenue - Total cost = 38*x_phone + 55*x_laptop
    # Subject to same constraints:
    #       x_phone + x_laptop <= 100
    #       12*x_phone + 15*x_laptop <= 5000
    #       2*x_phone + 3*x_laptop <= 2000
    #       x_phone, x_laptop >= 0

    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        return None, None

    # Decision variables
    x_phone = solver.NumVar(0.0, solver.infinity(), 'x_phone')
    x_laptop = solver.NumVar(0.0, solver.infinity(), 'x_laptop')

    # Constraints
    solver.Add(x_phone + x_laptop <= 100)                        # Space constraint
    solver.Add(12 * x_phone + 15 * x_laptop <= 5000)               # Cost constraint
    solver.Add(2 * x_phone + 3 * x_laptop <= 2000)                 # Labor constraint

    # Objective: maximize net objective computed as (Total revenue - Total cost)
    # which simplifies to: maximize 38*x_phone + 55*x_laptop.
    objective = solver.Objective()
    objective.SetCoefficient(x_phone, 38)
    objective.SetCoefficient(x_laptop, 55)
    objective.SetMaximization()

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL:
        solution = {
            "AllocatedSpace": {
                "0": x_phone.solution_value(),
                "1": x_laptop.solution_value()
            }
        }
        objective_value = objective.Value()
        return solution, objective_value
    else:
        return None, None

def main():
    print("Optimization Results for Factory Layout Problem")
    print("--------------------------------------------------")

    # Solve the first formulation
    sol1, obj1 = solve_model_version1()
    if sol1 is not None:
        print("Model Version 1 (Maximize net revenue):")
        print("Solution:", sol1)
        print("Objective Value (Total Net Revenue):", obj1)
    else:
        print("Model Version 1: No optimal solution found.")

    print("\n--------------------------------------------------")

    # Solve the alternative formulation
    sol2, obj2 = solve_model_version2()
    if sol2 is not None:
        print("Model Version 2 (Maximize Total Revenue - Total Cost):")
        print("Solution:", sol2)
        print("Objective Value (Net Objective):", obj2)
    else:
        print("Model Version 2: No optimal solution found.")

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Optimization Results for Factory Layout Problem
--------------------------------------------------
Model Version 1 (Maximize net revenue):
Solution: {'AllocatedSpace': {'0': 0.0, '1': 100.0}}
Objective Value (Total Net Revenue): 7000.0

--------------------------------------------------
Model Version 2 (Maximize Total Revenue - Total Cost):
Solution: {'AllocatedSpace': {'0': 0.0, '1': 100.0}}
Objective Value (Net Objective): 5500.0
'''

'''Expected Output:
Expected solution

: {'variables': {'AllocatedSpace': {'0': 0.0, '1': 100.0}}, 'objective': 7000.0}'''

