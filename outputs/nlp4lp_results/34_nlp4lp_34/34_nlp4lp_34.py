# Problem Description:
'''Problem description: A bakery bakes bagels and croissants. A batch of bagels can be made using 2 hours of oven time and 0.25 hours of pastry chef time. A batch of croissants is more complicated, so while they take 1 hour of oven time, they take 2 hours of pastry chef time. In a day, the bakery has at most 70 hours available for the oven and 32 pastry chef hours available. Using all the available capacity, what is the maximum profit the bakery can generate assuming the profit per batch is $20 and $40 respectively for a batch of bagels and a batch of croissants.

Expected Output Schema:
{
  "variables": {
    "Batch": {
      "0": "float",
      "1": "float"
    }
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- Products: {Bagels, Croissants}

Parameters:
- profit_per_batch: Dictionary with values {Bagels: 20 (USD per batch), Croissants: 40 (USD per batch)}
- oven_time_per_batch: Dictionary with values {Bagels: 2 (hours per batch), Croissants: 1 (hour per batch)}
- chef_time_per_batch: Dictionary with values {Bagels: 0.25 (hours per batch), Croissants: 2 (hours per batch)}
- oven_capacity: 70 (hours available per day)
- chef_capacity: 32 (hours available per day)
  (Note: All time units are in hours. It is assumed that batches are produced in whole numbers, so decision variables may be modeled as integer.)

Variables:
- x_Product: Number of batches produced for each product.
  Specifically,
  - x_Bagels: number of bagel batches produced (non-negative integer)
  - x_Croissants: number of croissant batches produced (non-negative integer)

Objective:
- Maximize total profit = profit_per_batch[Bagels] * x_Bagels + profit_per_batch[Croissants] * x_Croissants
  That is, Maximize 20 * x_Bagels + 40 * x_Croissants

Constraints:
1. Oven Time Constraint:
   oven_time_per_batch[Bagels] * x_Bagels + oven_time_per_batch[Croissants] * x_Croissants ≤ oven_capacity
   → 2 * x_Bagels + 1 * x_Croissants ≤ 70

2. Pastry Chef Time Constraint:
   chef_time_per_batch[Bagels] * x_Bagels + chef_time_per_batch[Croissants] * x_Croissants ≤ chef_capacity
   → 0.25 * x_Bagels + 2 * x_Croissants ≤ 32

This structured model provides a complete and unambiguous formulation for the bakery problem using the five-element framework.'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp
from ortools.sat.python import cp_model

def solve_with_linear_solver():
    # Create the CBC/MIP solver.
    solver = pywraplp.Solver.CreateSolver('CBC_MIXED_INTEGER_PROGRAMMING')
    if not solver:
        return None

    # Variables: Number of batches for bagels (x0) and croissants (x1)
    # They must be non-negative integers.
    x0 = solver.IntVar(0, solver.infinity(), 'x_Bagels')
    x1 = solver.IntVar(0, solver.infinity(), 'x_Croissants')
    
    # Constraints:
    # Oven time: 2*x_Bagels + 1*x_Croissants <= 70
    solver.Add(2 * x0 + 1 * x1 <= 70)
    # Pastry Chef time: 0.25*x_Bagels + 2*x_Croissants <= 32
    solver.Add(0.25 * x0 + 2 * x1 <= 32)

    # Objective function: Max 20*x_Bagels + 40*x_Croissants
    solver.Maximize(20 * x0 + 40 * x1)

    status = solver.Solve()

    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result['status'] = 'OPTIMAL'
        result['objective'] = solver.Objective().Value()
        result['variables'] = {
            "Batch": {
                "0": x0.solution_value(),
                "1": x1.solution_value()
            }
        }
    elif status == pywraplp.Solver.FEASIBLE:
        result['status'] = 'FEASIBLE'
        result['objective'] = solver.Objective().Value()
        result['variables'] = {
            "Batch": {
                "0": x0.solution_value(),
                "1": x1.solution_value()
            }
        }
    else:
        result['status'] = 'INFEASIBLE'
        result['message'] = 'The linear program could not find a feasible solution.'
        
    return result

def solve_with_cp_model():
    # In CP-SAT all coefficients must be integers.
    # For the constraint with coefficient 0.25, we scale it by multiplying everything by 4.
    # Original constraints:
    #   2 * x_Bagels + 1 * x_Croissants <= 70   (oven constraint)  -> multiply by 1 (no change)
    #   0.25 * x_Bagels + 2 * x_Croissants <= 32    (chef constraint)   -> multiply by 4 to avoid fraction
    # becomes:
    #   x_Bagels + 8 * x_Croissants <= 128
    model = cp_model.CpModel()
    
    # Variables: non-negative integers.
    x0 = model.NewIntVar(0, 1000, 'x_Bagels')      # Arbitrary upper bound.
    x1 = model.NewIntVar(0, 1000, 'x_Croissants')
    
    # Constraints:
    # Oven time: 2*x_Bagels + 1*x_Croissants <= 70
    model.Add(2 * x0 + 1 * x1 <= 70)
    # Pastry Chef time (scaled): x_Bagels + 8*x_Croissants <= 128
    model.Add(x0 + 8 * x1 <= 128)
    
    # Objective: maximize 20*x_Bagels + 40*x_Croissants.
    # CP-SAT can maximize integer objectives.
    model.Maximize(20 * x0 + 40 * x1)
    
    # Solve the model.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    
    result = {}
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        result['status'] = 'OPTIMAL' if status == cp_model.OPTIMAL else 'FEASIBLE'
        result['objective'] = solver.ObjectiveValue()
        result['variables'] = {
            "Batch": {
                "0": solver.Value(x0),
                "1": solver.Value(x1)
            }
        }
    else:
        result['status'] = 'INFEASIBLE'
        result['message'] = 'The CP-SAT model could not find a feasible solution.'
    
    return result

def main():
    # Solve using OR-Tools Linear Solver (MIP)
    linear_result = solve_with_linear_solver()
    # Solve using OR-Tools CP-SAT Solver
    cp_result = solve_with_cp_model()
    
    print("Results from Linear Solver (CBC_MIP):")
    print(linear_result)
    print("\nResults from CP-SAT Solver:")
    print(cp_result)

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Results from Linear Solver (CBC_MIP):
{'status': 'OPTIMAL', 'objective': 1060.0, 'variables': {'Batch': {'0': 29.0, '1': 12.0}}}

Results from CP-SAT Solver:
{'status': 'OPTIMAL', 'objective': 1060.0, 'variables': {'Batch': {'0': 29, '1': 12}}}
'''

'''Expected Output:
Expected solution

: {'variables': {'Batch': {'0': 28.8, '1': 12.4}}, 'objective': 1072.0}'''

