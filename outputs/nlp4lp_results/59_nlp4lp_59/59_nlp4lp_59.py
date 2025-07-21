# Problem Description:
'''Problem description: A tea estate has available 500 acres of land and they need to pick the tea leaves either using a traditional machine or modern machine. For each acre of land, the traditional machine can pick 30 kg of tea leaves, creates 10 kg of waste, and requires 20 liters of fuel. For each acre of land, the modern machine can pick 40 kg of tea leaves, creates 15 kg of waste, and requires 15 liters of fuel. The estate has available 9000 liters of fuel can handle at most 6000 kg of waste. For how many acres should each machine be used to maximize the amount of tea leaves that can be picked?

Expected Output Schema:
{
  "variables": {
    "AcresUsed": [
      "float"
    ]
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- M: set of machine types = {Traditional, Modern}

Parameters:
- acres_total: total available land in acres = 500 acres
- fuel_available: total available fuel = 9000 liters
- waste_capacity: maximum allowable waste = 6000 kg
- tea_yield[m]: tea leaves picked per acre for machine m (kg)
   - tea_yield[Traditional] = 30 kg/acre
   - tea_yield[Modern] = 40 kg/acre
- waste[m]: waste produced per acre for machine m (kg)
   - waste[Traditional] = 10 kg/acre
   - waste[Modern] = 15 kg/acre
- fuel[m]: fuel required per acre for machine m (liters)
   - fuel[Traditional] = 20 liters/acre
   - fuel[Modern] = 15 liters/acre

Variables:
- x[m] for m in M: acres of land allocated to machine m (continuous, in acres, >= 0)

Objective:
- Maximize total tea leaves picked = tea_yield[Traditional] * x[Traditional] + tea_yield[Modern] * x[Modern]

Constraints:
1. Land constraint: x[Traditional] + x[Modern] <= acres_total 
2. Fuel constraint: fuel[Traditional] * x[Traditional] + fuel[Modern] * x[Modern] <= fuel_available
3. Waste constraint: waste[Traditional] * x[Traditional] + waste[Modern] * x[Modern] <= waste_capacity

-----------------------------------------------------
This model assumes that acres can be fractionally allocated. If integer allocations (i.e., whole acres) are required, the variable x[m] should be defined as integer.'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_continuous():
    # Continuous model using Linear Programming (LP)
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Continuous solver not available.")
        return None

    # Parameters
    acres_total = 500
    fuel_available = 9000
    waste_capacity = 6000

    # Per-acre parameters for each machine type
    tea_yield = {'Traditional': 30, 'Modern': 40}
    waste = {'Traditional': 10, 'Modern': 15}
    fuel = {'Traditional': 20, 'Modern': 15}

    # Variables: Acres allocated to each machine (continuous)
    x_traditional = solver.NumVar(0.0, solver.infinity(), 'x_traditional')
    x_modern = solver.NumVar(0.0, solver.infinity(), 'x_modern')

    # Constraints
    # 1. Land constraint
    solver.Add(x_traditional + x_modern <= acres_total)
    # 2. Fuel constraint
    solver.Add(fuel['Traditional'] * x_traditional + fuel['Modern'] * x_modern <= fuel_available)
    # 3. Waste constraint
    solver.Add(waste['Traditional'] * x_traditional + waste['Modern'] * x_modern <= waste_capacity)

    # Objective: maximize total tea leaves picked
    objective = solver.Objective()
    objective.SetCoefficient(x_traditional, tea_yield['Traditional'])
    objective.SetCoefficient(x_modern, tea_yield['Modern'])
    objective.SetMaximization()

    status = solver.Solve()

    result = {"model": "Continuous LP"}
    if status == pywraplp.Solver.OPTIMAL:
        result["AcresUsed"] = {
            "Traditional": x_traditional.solution_value(),
            "Modern": x_modern.solution_value()
        }
        result["objective"] = objective.Value()
    else:
        result["error"] = "No optimal solution found or problem infeasible."
    return result

def solve_integer():
    # Integer model using Mixed Integer Programming (MIP)
    # Here, acres are assumed to be integer values.
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Integer solver not available.")
        return None

    # Parameters (same as continuous model)
    acres_total = 500
    fuel_available = 9000
    waste_capacity = 6000

    tea_yield = {'Traditional': 30, 'Modern': 40}
    waste = {'Traditional': 10, 'Modern': 15}
    fuel = {'Traditional': 20, 'Modern': 15}

    # Variables: Acres allocated to each machine (integer)
    x_traditional = solver.IntVar(0, acres_total, 'x_traditional')
    x_modern = solver.IntVar(0, acres_total, 'x_modern')

    # Constraints
    solver.Add(x_traditional + x_modern <= acres_total)
    solver.Add(fuel['Traditional'] * x_traditional + fuel['Modern'] * x_modern <= fuel_available)
    solver.Add(waste['Traditional'] * x_traditional + waste['Modern'] * x_modern <= waste_capacity)

    # Objective: maximize total tea leaves picked
    objective = solver.Objective()
    objective.SetCoefficient(x_traditional, tea_yield['Traditional'])
    objective.SetCoefficient(x_modern, tea_yield['Modern'])
    objective.SetMaximization()

    status = solver.Solve()

    result = {"model": "Integer MIP"}
    if status == pywraplp.Solver.OPTIMAL:
        result["AcresUsed"] = {
            "Traditional": x_traditional.solution_value(),
            "Modern": x_modern.solution_value()
        }
        result["objective"] = objective.Value()
    else:
        result["error"] = "No optimal solution found or problem infeasible."
    return result

def main():
    print("Optimization Results:")
    # Solve Continuous LP model
    continuous_result = solve_continuous()
    if continuous_result:
        print("\nContinuous LP Model:")
        if "error" in continuous_result:
            print("Error:", continuous_result["error"])
        else:
            print("Acres Used:", continuous_result["AcresUsed"])
            print("Objective (Total Tea Leaves Picked):", continuous_result["objective"])
    else:
        print("Continuous model could not be solved.")

    # Solve Integer MIP model
    integer_result = solve_integer()
    if integer_result:
        print("\nInteger MIP Model:")
        if "error" in integer_result:
            print("Error:", integer_result["error"])
        else:
            print("Acres Used:", integer_result["AcresUsed"])
            print("Objective (Total Tea Leaves Picked):", integer_result["objective"])
    else:
        print("Integer model could not be solved.")

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Optimization Results:

Continuous LP Model:
Acres Used: {'Traditional': 300.0000000000001, 'Modern': 199.9999999999999}
Objective (Total Tea Leaves Picked): 17000.0

Integer MIP Model:
Acres Used: {'Traditional': 300.0, 'Modern': 200.0}
Objective (Total Tea Leaves Picked): 17000.0
'''

'''Expected Output:
Expected solution

: {'variables': {'AcresUsed': [300.0, 200.0]}, 'objective': 17000.0}'''

