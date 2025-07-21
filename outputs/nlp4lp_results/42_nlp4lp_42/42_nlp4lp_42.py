# Problem Description:
'''Problem description: A farmer has 200 acres of land on which he must process hay using either a windrower or hay harvester. For each acre of land, the windrower can process 10 kg of hay while the hay harvester can process 8 kg of hay. Per acre, the windrower produces 5 kg of methane gas and requires 2 kg of fuel. On the other hand, the hay harvester produces 3 kg of methane gas per acre and requires 1 kg of fuel. There are 300 kg of fuel available and the farmer can produce at most 800 kg of methane gas. For how many acres should each machine be used to maximize the amount of hay processed?

Expected Output Schema:
{
  "variables": {
    "AcresAllocated": [
      "float"
    ]
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- Machines: set of machine types = {Windrower, HayHarvester}

Parameters:
- available_acres: total acres available = 200 acres
- fuel_available: total fuel available = 300 kg
- methane_limit: maximum allowable methane gas produced = 800 kg
- hay_per_acre:
  - Windrower: 10 kg hay processed per acre
  - HayHarvester: 8 kg hay processed per acre
- fuel_req:
  - Windrower: 2 kg fuel required per acre
  - HayHarvester: 1 kg fuel required per acre
- methane_prod:
  - Windrower: 5 kg methane produced per acre
  - HayHarvester: 3 kg methane produced per acre

Variables:
- acres_allocated[m in Machines]: number of acres on which machine m is used [continuous, >= 0] (unit: acres)

Objective:
- Maximize total hay processed = (10 * acres_allocated[Windrower]) + (8 * acres_allocated[HayHarvester])
  (unit: kg hay)

Constraints:
1. Land constraint: acres_allocated[Windrower] + acres_allocated[HayHarvester] ≤ available_acres (200 acres)
2. Fuel constraint: (2 * acres_allocated[Windrower]) + (1 * acres_allocated[HayHarvester]) ≤ fuel_available (300 kg)
3. Methane constraint: (5 * acres_allocated[Windrower]) + (3 * acres_allocated[HayHarvester]) ≤ methane_limit (800 kg methane)

--------------------------------------------------
Output Schema (for reference):
{
  "variables": {
    "AcresAllocated": [
      "float"
    ]
  },
  "objective": "float"
}'''

# Generated Code:
#!/usr/bin/env python3
"""
This script implements the optimization problem using two distinct OR-Tools approaches.
One implementation uses the linear_solver (with continuous variables) and the other uses
the CP-SAT model (with integer variables). Both models solve the following problem:
 
  A farmer has 200 acres of land. For each acre:
    - Windrower processes 10 kg hay, produces 5 kg methane and requires 2 kg fuel.
    - Hay Harvester processes 8 kg hay, produces 3 kg methane and requires 1 kg fuel.
     
  Subject to:
    - Total acres used ≤ 200
    - Total fuel used (2*Windrower_acres + 1*HayHarvester_acres) ≤ 300 kg.
    - Total methane produced (5*Windrower_acres + 3*HayHarvester_acres) ≤ 800 kg.
    
  The objective is to maximize total hay processed.

Two formulations are provided:
1. Continuous model using ortools.linear_solver.
2. Integer model using ortools.sat.python.cp_model.

Both implementations are completely independent.
"""

from ortools.linear_solver import pywraplp
from ortools.sat.python import cp_model

def solve_with_linear_solver():
    # Create the linear solver with the GLOP backend.
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        return {"error": "Linear solver not created."}
    
    # Decision variables (continuous, acres can be fractional).
    windrower = solver.NumVar(0.0, solver.infinity(), 'Windrower_acres')
    hayharvester = solver.NumVar(0.0, solver.infinity(), 'HayHarvester_acres')
    
    # Constraints
    # 1. Land constraint: windrower + hayharvester <= 200
    solver.Add(windrower + hayharvester <= 200)
    
    # 2. Fuel constraint: 2*windrower + hayharvester <= 300 
    solver.Add(2 * windrower + hayharvester <= 300)
    
    # 3. Methane constraint: 5*windrower + 3*hayharvester <= 800 
    solver.Add(5 * windrower + 3 * hayharvester <= 800)
    
    # Objective: maximize hay processed = 10 * windrower + 8 * hayharvester
    objective = solver.Objective()
    objective.SetCoefficient(windrower, 10)
    objective.SetCoefficient(hayharvester, 8)
    objective.SetMaximization()
    
    # Solve the model.
    status = solver.Solve()
    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "model": "LinearSolver (Continuous)",
            "variables": {
                "AcresAllocated": [
                    {"machine": "Windrower", "value": windrower.solution_value()},
                    {"machine": "HayHarvester", "value": hayharvester.solution_value()}
                ]
            },
            "objective": objective.Value()
        }
    else:
        result = {
            "model": "LinearSolver (Continuous)",
            "error": "No optimal solution found."
        }
    return result

def solve_with_cp_sat():
    # Create the CP-SAT model.
    model = cp_model.CpModel()
    
    # In CP-SAT, variables must be integer.
    # We assume acres are integer-valued.
    max_acres = 200
    windrower = model.NewIntVar(0, max_acres, 'Windrower_acres')
    hayharvester = model.NewIntVar(0, max_acres, 'HayHarvester_acres')
    
    # Constraints
    # 1. Land constraint: windrower + hayharvester <= 200
    model.Add(windrower + hayharvester <= 200)
    
    # 2. Fuel constraint: 2*windrower + hayharvester <= 300
    model.Add(2 * windrower + hayharvester <= 300)
    
    # 3. Methane constraint: 5*windrower + 3*hayharvester <= 800
    model.Add(5 * windrower + 3 * hayharvester <= 800)
    
    # Objective: maximize hay processed = 10*windrower + 8*hayharvester.
    # CP-SAT optimizes integer linear objectives.
    model.Maximize(10 * windrower + 8 * hayharvester)
    
    # Solve the model.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    result = {}
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        result = {
            "model": "CP-SAT (Integer)",
            "variables": {
                "AcresAllocated": [
                    {"machine": "Windrower", "value": solver.Value(windrower)},
                    {"machine": "HayHarvester", "value": solver.Value(hayharvester)}
                ]
            },
            "objective": solver.ObjectiveValue()
        }
    else:
        result = {
            "model": "CP-SAT (Integer)",
            "error": "No optimal solution found."
        }
    return result

def main():
    # Solve using the linear solver.
    linear_result = solve_with_linear_solver()
    
    # Solve using the CP-SAT model.
    cp_sat_result = solve_with_cp_sat()
    
    # Print the results in a structured way.
    results = {
        "LinearSolver_Result": linear_result,
        "CP_SAT_Result": cp_sat_result
    }
    print(results)

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
{'LinearSolver_Result': {'model': 'LinearSolver (Continuous)', 'variables': {'AcresAllocated': [{'machine': 'Windrower', 'value': 100.00000000000001}, {'machine': 'HayHarvester', 'value': 99.99999999999997}]}, 'objective': 1800.0}, 'CP_SAT_Result': {'model': 'CP-SAT (Integer)', 'variables': {'AcresAllocated': [{'machine': 'Windrower', 'value': 100}, {'machine': 'HayHarvester', 'value': 100}]}, 'objective': 1800.0}}
'''

'''Expected Output:
Expected solution

: {'variables': {'AcresAllocated': [100.0, 100.0]}, 'objective': 1800.0}'''

