# Problem Description:
'''Problem description: Both chemical A and chemical B need to be added to a mixer for making bread. One unit of chemical A takes 30 seconds to be effective while one unit of chemical B takes 45 seconds to be effective. Because chemical A can be dangerous, there has to be at most a third as much chemical A as chemical B in the mixer. If there has to be at least 300 units of chemical A in the mixer and at least 1500 units of total chemicals in the mixer, how many units of each should be added to minimize the total time it takes for the mixed bread to be ready?

Expected Output Schema:
{
  "variables": {
    "QuantityChemicalA": "float",
    "QuantityChemicalB": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- Chem: set of chemicals = {A, B}

Parameters:
- time_per_unit_A: Time required for one unit of chemical A to be effective [seconds per unit] = 30
- time_per_unit_B: Time required for one unit of chemical B to be effective [seconds per unit] = 45
- safe_ratio: Maximum allowed ratio of chemical A to chemical B [unitless] = 1/3  
  (Interpretation: The quantity of chemical A must be at most one third of the quantity of chemical B.)
- min_A: Minimum required units of chemical A [units] = 300
- min_total: Minimum required total units of chemicals A and B [units] = 1500

Variables:
- QuantityChemicalA: Number of units of chemical A to add [continuous, ≥ 0, units]
- QuantityChemicalB: Number of units of chemical B to add [continuous, ≥ 0, units]

Objective:
- Minimize total_mixing_time = (time_per_unit_A * QuantityChemicalA) + (time_per_unit_B * QuantityChemicalB)
  [Total mixing time in seconds]

Constraints:
1. Safety constraint: QuantityChemicalA ≤ safe_ratio * QuantityChemicalB
   (Ensures that chemical A does not exceed one third the amount of chemical B.)
2. Minimum chemical A requirement: QuantityChemicalA ≥ min_A
3. Total chemical requirement: QuantityChemicalA + QuantityChemicalB ≥ min_total

Comments:
- All units are assumed to be consistent (units for chemicals, seconds for time).  
- The objective is to reduce the overall mixing time while respecting safety and minimum quantity constraints.  
- Both decision variables are modeled as continuous, but if the application requires discrete units, they could be redefined as integers.'''

# Generated Code:
#!/usr/bin/env python3
"""
This script provides two separate implementations for the given optimization problem.
One uses the Google OR-Tools linear solver (LP formulation with continuous variables)
and the other uses the CP-SAT model (integer formulation). Both models are kept completely
separate and the results of both are printed at the end.
"""

from ortools.linear_solver import pywraplp
from ortools.sat.python import cp_model

def solve_with_linear_solver():
    # Create the linear solver with GLOP backend (for LP)
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        return {"error": "Linear solver not available."}

    # Parameters
    time_per_unit_A = 30
    time_per_unit_B = 45
    safe_ratio = 1.0/3.0  # A must be at most one-third of B.
    min_A = 300
    min_total = 1500

    # Variables: continuous
    # Lower bound is 0 by default, but we set the minimum for Chemical A as 300 later explicitly.
    QuantityChemicalA = solver.NumVar(0.0, solver.infinity(), 'QuantityChemicalA')
    QuantityChemicalB = solver.NumVar(0.0, solver.infinity(), 'QuantityChemicalB')

    # Add constraints:
    # 1. Safety constraint: QuantityChemicalA <= safe_ratio * QuantityChemicalB
    solver.Add(QuantityChemicalA <= safe_ratio * QuantityChemicalB)
    
    # 2. Minimum chemical A requirement: QuantityChemicalA >= min_A
    solver.Add(QuantityChemicalA >= min_A)
    
    # 3. Total chemical requirement: QuantityChemicalA + QuantityChemicalB >= min_total
    solver.Add(QuantityChemicalA + QuantityChemicalB >= min_total)

    # Objective: minimize total mixing time = 30*A + 45*B
    objective = solver.Objective()
    objective.SetCoefficient(QuantityChemicalA, time_per_unit_A)
    objective.SetCoefficient(QuantityChemicalB, time_per_unit_B)
    objective.SetMinimization()

    # Solve the problem
    result_status = solver.Solve()

    # Prepare output dictionary
    output = {}
    if result_status == pywraplp.Solver.OPTIMAL:
        output["variables"] = {
            "QuantityChemicalA": QuantityChemicalA.solution_value(),
            "QuantityChemicalB": QuantityChemicalB.solution_value()
        }
        output["objective"] = objective.Value()
    elif result_status == pywraplp.Solver.FEASIBLE:
        output["warning"] = "A feasible solution was found, but it may not be optimal."
        output["variables"] = {
            "QuantityChemicalA": QuantityChemicalA.solution_value(),
            "QuantityChemicalB": QuantityChemicalB.solution_value()
        }
        output["objective"] = objective.Value()
    else:
        output["error"] = "The problem does not have an optimal solution (or is infeasible)."
    
    return output

def solve_with_cp_model():
    # CP-SAT model works with integer variables, so we create an integer version of the problem.
    model = cp_model.CpModel()
    
    # Parameters
    time_per_unit_A = 30
    time_per_unit_B = 45
    safe_ratio = 1.0/3.0  # A must be at most one-third of B.
    # For CP-SAT integer formulation, we can restate the safety constraint as 3*A <= B (multiplying by 3).
    min_A = 300
    min_total = 1500

    # Set upper bounds for the decision variables.
    # We choose an arbitrary upper bound (e.g. 10000) that is sufficiently high.
    ub = 10000

    # Variables: integers
    A = model.NewIntVar(min_A, ub, 'QuantityChemicalA')
    # For B, the lower bound is 0; however, the total constraint A+B >= 1500 and A>=300 implies B >= 1200 at minimum.
    B = model.NewIntVar(0, ub, 'QuantityChemicalB')

    # Constraints:
    # 1. Safety constraint: A <= safe_ratio * B becomes 3*A <= B after multiplying both sides by 3.
    model.Add(3 * A <= B)
    
    # 2. Minimum total chemical requirement: A + B >= min_total
    model.Add(A + B >= min_total)

    # Objective: minimize total mixing time = 30*A + 45*B
    # CP-SAT allows linear objective functions.
    objective_var = model.NewIntVar(0, ub * (time_per_unit_A + time_per_unit_B), 'objective')
    # Instead of linking objective_var, we can just set the objective directly.
    model.Minimize(time_per_unit_A * A + time_per_unit_B * B)

    # Solve the model.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    # Prepare output dictionary.
    output = {}
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        output["variables"] = {
            "QuantityChemicalA": solver.Value(A),
            "QuantityChemicalB": solver.Value(B)
        }
        output["objective"] = solver.ObjectiveValue()
    else:
        output["error"] = "The problem does not have an optimal solution (or is infeasible)."
    
    return output

def main():
    print("----- Linear Solver (LP formulation) Solution -----")
    lp_solution = solve_with_linear_solver()
    print(lp_solution)
    
    print("\n----- CP-SAT Model (Integer formulation) Solution -----")
    cp_solution = solve_with_cp_model()
    print(cp_solution)

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
----- Linear Solver (LP formulation) Solution -----
{'variables': {'QuantityChemicalA': 375.0, 'QuantityChemicalB': 1125.0}, 'objective': 61875.0}

----- CP-SAT Model (Integer formulation) Solution -----
{'variables': {'QuantityChemicalA': 375, 'QuantityChemicalB': 1125}, 'objective': 61875.0}
'''

'''Expected Output:
Expected solution

: {'variables': {'QuantityChemicalA': 375.0, 'QuantityChemicalB': 1125.0}, 'objective': 61875.0}'''

