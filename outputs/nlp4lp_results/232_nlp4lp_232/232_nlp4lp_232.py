# Problem Description:
'''Problem description: A handmade sports equipment manufacturing company makes basketballs and footballs. Basketballs require 5 units of materials and 1 hour to make whereas footballs require 3 units of materials and 2 hours to make. The manufacturing company has available 1500 units of materials and their workers working at max capacity can work for at most 750 hours. Since basketballs sell better, there must be at least three times as many basketballs as footballs but the manufacturing company would like at least 50 footballs. How many of each should the manufacturing company make to maximize the total number of sports equipment produced?

Expected Output Schema:
{
  "variables": {
    "ProductionQuantity": {
      "0": "float",
      "1": "float"
    },
    "ProductionQuantityBasketballs": "float",
    "ProductionQuantityFootballs": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Below is the formulation of the problem using the five-element framework.

-----------------------------------------------------
Sets:
- E: set of equipment types = {basketball, football}

-----------------------------------------------------
Parameters:
- material_per_basketball = 5 units per basketball (material consumption per unit)
- material_per_football = 3 units per football (material consumption per unit)
- labor_per_basketball = 1 hour per basketball (labor consumption per unit)
- labor_per_football = 2 hours per football (labor consumption per unit)
- max_material = 1500 units (total available material)
- max_labor = 750 hours (total available worker hours)
- min_football = 50 (minimum number of footballs to produce)
- basketball_to_football_ratio = 3 (minimum factor such that number of basketballs is at least three times number of footballs)

-----------------------------------------------------
Variables:
- ProductionQuantityBasketballs: number of basketballs produced (non-negative integer)
- ProductionQuantityFootballs: number of footballs produced (non-negative integer)

For ease of notation, one can also define a helper vector variable:
- ProductionQuantity: where ProductionQuantity[0] = ProductionQuantityBasketballs and ProductionQuantity[1] = ProductionQuantityFootballs

-----------------------------------------------------
Objective:
Maximize total production of sports equipment, which is defined as:
TotalProduction = ProductionQuantityBasketballs + ProductionQuantityFootballs

-----------------------------------------------------
Constraints:
1. Material Constraint:
   5 * ProductionQuantityBasketballs + 3 * ProductionQuantityFootballs <= 1500
   (The total material used for both products must not exceed the 1500 available units.)

2. Labor Constraint:
   1 * ProductionQuantityBasketballs + 2 * ProductionQuantityFootballs <= 750
   (The total labor hours required for production cannot exceed the 750 available hours.)

3. Ratio Constraint (Basketball preference):
   ProductionQuantityBasketballs >= 3 * ProductionQuantityFootballs
   (At least three times as many basketballs must be produced as footballs.)

4. Minimum Football Production Constraint:
   ProductionQuantityFootballs >= 50
   (At least 50 footballs must be produced.)

-----------------------------------------------------

Expected Output Schema:
{
  "variables": {
    "ProductionQuantity": {
      "0": "float",
      "1": "float"
    },
    "ProductionQuantityBasketballs": "float",
    "ProductionQuantityFootballs": "float"
  },
  "objective": "float"
}

This completes the structured mathematical model for the manufacturing problem.'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_integer_model():
    # Create the linear solver with SCIP backend (for integer variables)
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        print("Integer model: Could not create solver.")
        return None

    # Variables: non-negative integers
    # ProductionQuantityBasketballs: variable for basketballs (non-negative integer)
    # ProductionQuantityFootballs: variable for footballs (non-negative integer)
    pb = solver.IntVar(0, solver.infinity(), 'ProductionQuantityBasketballs')
    pf = solver.IntVar(0, solver.infinity(), 'ProductionQuantityFootballs')

    # For easier printing, also define a helper vector variable ProductionQuantity:
    # ProductionQuantity[0] = pb, ProductionQuantity[1] = pf

    # Constraints:
    # 1. Material Constraint: 5*pb + 3*pf <= 1500
    solver.Add(5 * pb + 3 * pf <= 1500)

    # 2. Labor Constraint: 1*pb + 2*pf <= 750
    solver.Add(pb + 2 * pf <= 750)

    # 3. Ratio Constraint: pb >= 3*pf
    solver.Add(pb >= 3 * pf)

    # 4. Minimum Football Production Constraint: pf >= 50
    solver.Add(pf >= 50)

    # Objective: maximize total production: pb + pf
    objective = solver.Objective()
    objective.SetCoefficient(pb, 1)
    objective.SetCoefficient(pf, 1)
    objective.SetMaximization()

    status = solver.Solve()

    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "variables": {
                "ProductionQuantity": {
                    "0": pb.solution_value(),
                    "1": pf.solution_value()
                },
                "ProductionQuantityBasketballs": pb.solution_value(),
                "ProductionQuantityFootballs": pf.solution_value()
            },
            "objective": objective.Value()
        }
    else:
        result = {"error": "No optimal solution found for the integer model."}
    return result

def solve_continuous_model():
    # Create the linear solver with GLOP backend (for continuous variables)
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Continuous model: Could not create solver.")
        return None

    # Variables: non-negative continuous
    # Although the problem was formulated as integer, here we allow floats.
    pb = solver.NumVar(0.0, solver.infinity(), 'ProductionQuantityBasketballs')
    pf = solver.NumVar(0.0, solver.infinity(), 'ProductionQuantityFootballs')

    # Constraints:
    # 1. Material Constraint: 5*pb + 3*pf <= 1500
    solver.Add(5 * pb + 3 * pf <= 1500)

    # 2. Labor Constraint: pb + 2*pf <= 750
    solver.Add(pb + 2 * pf <= 750)

    # 3. Ratio Constraint: pb >= 3*pf
    solver.Add(pb >= 3 * pf)

    # 4. Minimum Football Production Constraint: pf >= 50
    solver.Add(pf >= 50)

    # Objective: maximize total production: pb + pf
    objective = solver.Objective()
    objective.SetCoefficient(pb, 1)
    objective.SetCoefficient(pf, 1)
    objective.SetMaximization()

    status = solver.Solve()

    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "variables": {
                "ProductionQuantity": {
                    "0": pb.solution_value(),
                    "1": pf.solution_value()
                },
                "ProductionQuantityBasketballs": pb.solution_value(),
                "ProductionQuantityFootballs": pf.solution_value()
            },
            "objective": objective.Value()
        }
    else:
        result = {"error": "No optimal solution found for the continuous model."}
    return result

def main():
    # Solve the integer (MIP) model
    integer_solution = solve_integer_model()
    # Solve the continuous (LP) model
    continuous_solution = solve_continuous_model()

    # Print results in a structured way
    print("Integer Model (MIP) Solution:")
    if "error" in integer_solution:
        print(integer_solution["error"])
    else:
        print(integer_solution)

    print("\nContinuous Model (LP) Solution:")
    if "error" in continuous_solution:
        print(continuous_solution["error"])
    else:
        print(continuous_solution)

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Integer Model (MIP) Solution:
{'variables': {'ProductionQuantity': {'0': 250.0, '1': 83.0}, 'ProductionQuantityBasketballs': 250.0, 'ProductionQuantityFootballs': 83.0}, 'objective': 333.0}

Continuous Model (LP) Solution:
{'variables': {'ProductionQuantity': {'0': 250.0, '1': 83.33333333333333}, 'ProductionQuantityBasketballs': 250.0, 'ProductionQuantityFootballs': 83.33333333333333}, 'objective': 333.3333333333333}
'''

'''Expected Output:
Expected solution

: {'variables': {'ProductionQuantity': {'0': 107.14285714285714, '1': 321.42857142857144}, 'ProductionQuantityBasketballs': 150.0, 'ProductionQuantityFootballs': 50.0}, 'objective': 428.57142857142856}'''

