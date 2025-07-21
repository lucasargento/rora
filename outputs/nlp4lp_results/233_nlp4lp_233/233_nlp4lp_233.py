# Problem Description:
'''Problem description: A researcher must perform two types of experiments, in-vivo and ex-vivo. In-vivo experiments requires 30 minutes to prepare and 60 minutes to execute. Ex-vivo experiments require 45 minutes to prepare and 30 minutes to execute. In addition, in-vivo experiments gives the researcher 2 units of radiation while ex-vivo experiments give the researcher 3 unites of radiation. At most 400 minutes can be used for preparation and 500 minutes for execution of the experiment. How many of each experiment should be scheduled by the researcher to minimize the total radiation received by the researcher?

Expected Output Schema:
{
  "variables": {
    "NumberOfInVivoExperiments": "float",
    "NumberOfExVivoExperiments": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- E: set of experiment types = {in_vivo, ex_vivo}

Parameters:
- prep_time_e: preparation time required per experiment of type e [minutes]
  • in_vivo: 30
  • ex_vivo: 45
- exec_time_e: execution time required per experiment of type e [minutes]
  • in_vivo: 60
  • ex_vivo: 30
- radiation_e: radiation unit produced per experiment of type e [units]
  • in_vivo: 2
  • ex_vivo: 3
- max_prep_time: maximum available preparation time [minutes] = 400
- max_exec_time: maximum available execution time [minutes] = 500

Variables:
- x_e: number of experiments of type e to schedule [nonnegative real, ideally integer]
  • x_in_vivo corresponds to in_vivo experiments
  • x_ex_vivo corresponds to ex_vivo experiments

Objective:
- Minimize total radiation received, calculated as:
  Total Radiation = (radiation_in_vivo * x_in_vivo) + (radiation_ex_vivo * x_ex_vivo)
  Which numerically is: 2 * x_in_vivo + 3 * x_ex_vivo

Constraints:
1. Preparation time constraint:
   (prep_time_in_vivo * x_in_vivo) + (prep_time_ex_vivo * x_ex_vivo) ≤ max_prep_time
   That is: 30 * x_in_vivo + 45 * x_ex_vivo ≤ 400

2. Execution time constraint:
   (exec_time_in_vivo * x_in_vivo) + (exec_time_ex_vivo * x_ex_vivo) ≤ max_exec_time
   That is: 60 * x_in_vivo + 30 * x_ex_vivo ≤ 500

Comments:
- All time-related parameters are given in minutes.
- Decision variables represent the count of experiments and ideally should be integer values, though they are defined as nonnegative real numbers in this basic formulation.
- The objective is to minimize radiation exposure for the researcher while not exceeding the given preparation and execution time limits.

Expected Output Schema:
{
  "variables": {
    "NumberOfInVivoExperiments": "float",
    "NumberOfExVivoExperiments": "float"
  },
  "objective": "float"
}'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp
from ortools.sat.python import cp_model

def solve_lp():
    # Create the linear solver with GLOP backend.
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("LP solver not available.")
        return None

    # Variables (continuous LP relaxation)
    x_in_vivo = solver.NumVar(0.0, solver.infinity(), 'x_in_vivo')
    x_ex_vivo = solver.NumVar(0.0, solver.infinity(), 'x_ex_vivo')

    # Constraints:
    # 30*x_in_vivo + 45*x_ex_vivo <= 400 (preparation time)
    solver.Add(30 * x_in_vivo + 45 * x_ex_vivo <= 400)
    # 60*x_in_vivo + 30*x_ex_vivo <= 500 (execution time)
    solver.Add(60 * x_in_vivo + 30 * x_ex_vivo <= 500)

    # Objective: minimize total radiation = 2*x_in_vivo + 3*x_ex_vivo
    solver.Minimize(2 * x_in_vivo + 3 * x_ex_vivo)

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "variables": {
                "NumberOfInVivoExperiments": x_in_vivo.solution_value(),
                "NumberOfExVivoExperiments": x_ex_vivo.solution_value()
            },
            "objective": solver.Objective().Value()
        }
        return result
    else:
        print("The LP problem does not have an optimal solution.")
        return None


def solve_cp_sat():
    # Create CP-SAT model.
    model = cp_model.CpModel()
    
    # We create integer (non-negative) variables.
    # We assume a reasonable upper bound; given the constraints, an experiment count will not exceed 1000.
    ub = 1000
    x_in_vivo = model.NewIntVar(0, ub, 'x_in_vivo')
    x_ex_vivo = model.NewIntVar(0, ub, 'x_ex_vivo')

    # Constraints:
    # 30*x_in_vivo + 45*x_ex_vivo <= 400
    model.Add(30 * x_in_vivo + 45 * x_ex_vivo <= 400)
    # 60*x_in_vivo + 30*x_ex_vivo <= 500
    model.Add(60 * x_in_vivo + 30 * x_ex_vivo <= 500)
    
    # Objective: minimize total radiation = 2*x_in_vivo + 3*x_ex_vivo
    objective_var = model.NewIntVar(0, 10000, 'total_radiation')
    model.Add(objective_var == 2 * x_in_vivo + 3 * x_ex_vivo)
    model.Minimize(objective_var)

    # Solve using the CP-SAT solver.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        result = {
            "variables": {
                "NumberOfInVivoExperiments": solver.Value(x_in_vivo),
                "NumberOfExVivoExperiments": solver.Value(x_ex_vivo)
            },
            "objective": solver.Value(objective_var)
        }
        return result
    else:
        print("The CP-SAT problem does not have an optimal solution.")
        return None


def main():
    results = {}

    # Solve using LP (continuous relaxation)
    lp_result = solve_lp()
    if lp_result is not None:
        results['LP_Model'] = lp_result
    else:
        results['LP_Model'] = "Infeasible or no optimal solution."

    # Solve using CP-SAT (integer formulation)
    cpsat_result = solve_cp_sat()
    if cpsat_result is not None:
        results['CP_SAT_Model'] = cpsat_result
    else:
        results['CP_SAT_Model'] = "Infeasible or no optimal solution."

    # Print results in a structured way (JSON-like)
    print(results)


if __name__ == "__main__":
    main()

'''Execution Results:
SUCCESS:
{'LP_Model': {'variables': {'NumberOfInVivoExperiments': 0.0, 'NumberOfExVivoExperiments': 0.0}, 'objective': 0.0}, 'CP_SAT_Model': {'variables': {'NumberOfInVivoExperiments': 0, 'NumberOfExVivoExperiments': 0}, 'objective': 0}}
'''

'''Expected Output:
Expected solution

: {'variables': {'NumberOfInVivoExperiments': 0.0, 'NumberOfExVivoExperiments': -0.0}, 'objective': 0.0}'''

