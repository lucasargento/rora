# Problem Description:
'''Problem description: A clinic is conducting a throat or nasal swabs on each patient. A throat swab takes 5 minutes while a nasal swab takes 3 minutes. The clinic must administer at least 30 nasal swabs. Since the nasal swab is more uncomfortable, at least 4 times as many throat swabs must be done as nasal swabs. If the clinic is only operational for 20000 minutes, how many of each swab should be done to maximize the number of patients seen?

Expected Output Schema:
{
  "variables": {
    "NumThroatSwab": "float",
    "NumNasalSwab": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- S: set of swab types = {Throat, Nasal}

Parameters:
- time_Throat: time required for one throat swab [minutes] = 5
- time_Nasal: time required for one nasal swab [minutes] = 3
- min_nasal: minimum number of nasal swabs [swabs] = 30
- throat_ratio: minimum ratio of throat to nasal swabs = 4  (i.e., at least 4 times as many throat swabs as nasal swabs)
- max_operational_time: total available operating time [minutes] = 20000

Variables:
- NumThroatSwab: number of throat swabs to be administered [integer ≥ 0] 
- NumNasalSwab: number of nasal swabs to be administered [integer ≥ 0]

Objective:
- Maximize total number of patients served = NumThroatSwab + NumNasalSwab

Constraints:
1. Time constraint: 5 * NumThroatSwab + 3 * NumNasalSwab ≤ 20000
2. Minimum nasal swabs constraint: NumNasalSwab ≥ 30
3. Throat swab ratio constraint: NumThroatSwab ≥ 4 * NumNasalSwab

Note:
- Each patient receives exactly one swab.
- Although the expected output schema lists the decision variables as floats, these represent counts and are naturally modeled as integers.
- All time units are in minutes and the total available time is 20000 minutes.'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_linear_model():
    # Create the linear solver with the CBC backend.
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        return {"error": "Solver not created."}
    
    # Parameters
    time_throat = 5         # minutes required for one throat swab
    time_nasal = 3          # minutes required for one nasal swab
    min_nasal = 30          # minimum nasal swabs
    throat_ratio = 4        # NumThroatSwab must be at least 4 times NumNasalSwab
    max_operational_time = 20000  # total available time in minutes

    # Decision Variables:
    # Even though expected schema indicates float, these represent counts so we use integer variables.
    num_throat_swab = solver.IntVar(0, solver.infinity(), 'NumThroatSwab')
    num_nasal_swab = solver.IntVar(0, solver.infinity(), 'NumNasalSwab')

    # Constraints:
    # 1. Time constraint: 5 * NumThroatSwab + 3 * NumNasalSwab <= 20000
    solver.Add(time_throat * num_throat_swab + time_nasal * num_nasal_swab <= max_operational_time)
    
    # 2. Minimum nasal swabs: NumNasalSwab >= 30
    solver.Add(num_nasal_swab >= min_nasal)
    
    # 3. Throat swab ratio constraint: NumThroatSwab >= 4 * NumNasalSwab
    solver.Add(num_throat_swab >= throat_ratio * num_nasal_swab)
    
    # Objective: Maximize the total number of patients served = NumThroatSwab + NumNasalSwab
    objective = solver.Objective()
    objective.SetCoefficient(num_throat_swab, 1)
    objective.SetCoefficient(num_nasal_swab, 1)
    objective.SetMaximization()

    # Solve the model.
    status = solver.Solve()

    if status != pywraplp.Solver.OPTIMAL:
        return {"error": "The model does not have an optimal solution."}
    
    # Prepare the solution output as required.
    solution = {
        "variables": {
            "NumThroatSwab": num_throat_swab.solution_value(),
            "NumNasalSwab": num_nasal_swab.solution_value()
        },
        "objective": objective.Value()
    }
    return solution

def main():
    solutions = {}

    # Implementation 1: Linear MIP model with ortools.linear_solver.
    sol_linear = solve_linear_model()
    solutions["LinearModel"] = sol_linear

    # There is only one formulation provided; if additional formulations existed,
    # they would be implemented here in a separate function and added under a different key.

    # Print the structured results.
    print(solutions)

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
{'LinearModel': {'variables': {'NumThroatSwab': 3478.0, 'NumNasalSwab': 869.0}, 'objective': 4347.0}}
'''

'''Expected Output:
Expected solution

: {'variables': {'NumThroatSwab': 3479.0, 'NumNasalSwab': 868.0}, 'objective': 4347.0}'''

