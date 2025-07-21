# Problem Description:
'''Problem description: A city employs seasonal and permanent snow removers. A seasonal snow remover works 6 hours per shift and gets paid $120. A permanent snow remover works 10 hours per shift and gets paid $250. Currently the city needs 300 hours of snow remover labor after a heavy snowfall. If the city has a budget of $6500, how many of each type of worker should be hired to minimize the total number of snow removers?

Expected Output Schema:
{
  "variables": {
    "NumberSeasonal": "float",
    "NumberPermanent": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- W: set of worker types = {Seasonal, Permanent}

Parameters:
- HoursPerShift_Seasonal = 6 (hours per shift for a seasonal snow remover)
- HoursPerShift_Permanent = 10 (hours per shift for a permanent snow remover)
- CostPerShift_Seasonal = 120 (USD per seasonal snow remover shift)
- CostPerShift_Permanent = 250 (USD per permanent snow remover shift)
- RequiredLaborHours = 300 (total snow removal labor hours needed)
- TotalBudget = 6500 (USD available for payment)

Variables:
- NumberSeasonal: number of seasonal snow removers hired (float ≥ 0; in practice, an integer count)
- NumberPermanent: number of permanent snow removers hired (float ≥ 0; in practice, an integer count)

Objective:
- Minimize TotalWorkers = NumberSeasonal + NumberPermanent

Constraints:
1. Labor Hours Constraint: 
   HoursPerShift_Seasonal * NumberSeasonal + HoursPerShift_Permanent * NumberPermanent ≥ RequiredLaborHours
   (i.e., 6 * NumberSeasonal + 10 * NumberPermanent ≥ 300)

2. Budget Constraint:
   CostPerShift_Seasonal * NumberSeasonal + CostPerShift_Permanent * NumberPermanent ≤ TotalBudget
   (i.e., 120 * NumberSeasonal + 250 * NumberPermanent ≤ 6500)

----------------------------
Expected Output Schema:
{
  "variables": {
    "NumberSeasonal": "float",
    "NumberPermanent": "float"
  },
  "objective": "float"
}'''

# Generated Code:
#!/usr/bin/env python3
"""
This script implements two versions of the optimization problem using Google OR-Tools.
Version 1: Uses ortools.linear_solver (continuous relaxation, i.e. real variables)
Version 2: Uses ortools.sat.python.cp_model (integer variables)
Both models solve the following problem:

    Minimize the total number of snow removers:
      NumberSeasonal + NumberPermanent

    Subject to:
      6 * NumberSeasonal + 10 * NumberPermanent >= 300      (labor hours constraint)
      120 * NumberSeasonal + 250 * NumberPermanent <= 6500     (budget constraint)
      
Execute the main() function to run both implementations and to print the results.
"""

from ortools.linear_solver import pywraplp
from ortools.sat.python import cp_model

def solve_linear_continuous():
    """Solves the problem using the linear solver with continuous variables."""
    # Create the solver with the GLOP backend.
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        return None

    # Define variables: in our model, these are continuous (although in practice they are integers)
    NumberSeasonal = solver.NumVar(0.0, solver.infinity(), 'NumberSeasonal')
    NumberPermanent = solver.NumVar(0.0, solver.infinity(), 'NumberPermanent')

    # Define constraints:
    # Labor Hours Constraint: 6*NumberSeasonal + 10*NumberPermanent >= 300
    solver.Add(6 * NumberSeasonal + 10 * NumberPermanent >= 300)
    # Budget Constraint: 120*NumberSeasonal + 250*NumberPermanent <= 6500
    solver.Add(120 * NumberSeasonal + 250 * NumberPermanent <= 6500)

    # Define the objective: Minimize NumberSeasonal + NumberPermanent
    objective = solver.Objective()
    objective.SetCoefficient(NumberSeasonal, 1)
    objective.SetCoefficient(NumberPermanent, 1)
    objective.SetMinimization()

    status = solver.Solve()

    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "variables": {
                "NumberSeasonal": NumberSeasonal.solution_value(),
                "NumberPermanent": NumberPermanent.solution_value()
            },
            "objective": objective.Value()
        }
    else:
        result = {"error": "No optimal solution found for the continuous model."}
    
    return result

def solve_cp_integer():
    """Solves the problem using the CP-SAT model with integer variables."""
    model = cp_model.CpModel()
    # Define variables: using integer domains, since they represent count of workers.
    # Since budget maximum is 6500, we can set an upper bound that is safe.
    # For NumberSeasonal, max could be 6500/120 = ~54.  For NumberPermanent, max could be 6500/250 = 26.
    # To be safe, we set bounds a bit higher.
    max_seasonal = 100
    max_permanent = 100
    
    NumberSeasonal = model.NewIntVar(0, max_seasonal, 'NumberSeasonal')
    NumberPermanent = model.NewIntVar(0, max_permanent, 'NumberPermanent')

    # Add constraints.
    # Labor Hours Constraint: 6 * NumberSeasonal + 10 * NumberPermanent >= 300
    model.Add(6 * NumberSeasonal + 10 * NumberPermanent >= 300)
    # Budget Constraint: 120 * NumberSeasonal + 250 * NumberPermanent <= 6500
    model.Add(120 * NumberSeasonal + 250 * NumberPermanent <= 6500)

    # Define objective: Minimize NumberSeasonal + NumberPermanent
    objective_var = model.NewIntVar(0, max_seasonal + max_permanent, 'total_workers')
    model.Add(objective_var == NumberSeasonal + NumberPermanent)
    model.Minimize(objective_var)

    # Solve the model.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    result = {}
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        result = {
            "variables": {
                "NumberSeasonal": solver.Value(NumberSeasonal),
                "NumberPermanent": solver.Value(NumberPermanent)
            },
            "objective": solver.Value(objective_var)
        }
    else:
        result = {"error": "No optimal solution found for the integer CP-SAT model."}
    
    return result

def main():
    # Solve using continuous linear solver
    continuous_result = solve_linear_continuous()
    # Solve using integer CP-SAT model
    integer_result = solve_cp_integer()

    # Print the results in a structured way.
    print("Continuous (Linear Solver) Model Result:")
    if "error" in continuous_result:
        print(continuous_result["error"])
    else:
        print(continuous_result)
    
    print("\nInteger (CP-SAT) Model Result:")
    if "error" in integer_result:
        print(integer_result["error"])
    else:
        print(integer_result)

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Continuous (Linear Solver) Model Result:
{'variables': {'NumberSeasonal': 33.33333333333333, 'NumberPermanent': 10.0}, 'objective': 43.33333333333333}

Integer (CP-SAT) Model Result:
{'variables': {'NumberSeasonal': 35, 'NumberPermanent': 9}, 'objective': 44}
'''

'''Expected Output:
Expected solution

: {'variables': {'NumberSeasonal': 35.0, 'NumberPermanent': 9.0}, 'objective': 44.0}'''

