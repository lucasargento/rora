# Problem Description:
'''Problem description: A clinic administers two vaccines available for the public to take one at a time. One vaccine is taken as a pill and another is taken as a shot. The pill vaccine takes 10 minutes to administer while the shot takes 20 minutes to administer. Since the shot has been more thoroughly studied, the clinic must deliver at least 3 times as many shots as pill. In addition, the clinic must administer at least 30 pill vaccines. If the clinic only operates for 10000 minutes, maximize the number of patients that can be vaccinated.

Expected Output Schema:
{
  "variables": {
    "NumberOfPills": "float",
    "NumberOfShots": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- V: set of vaccine types = {pill, shot}

Parameters:
- time_pill: time required to administer a pill vaccine (minutes) = 10
- time_shot: time required to administer a shot vaccine (minutes) = 20
- min_pill: minimum number of pill vaccines to administer [units] = 30
- min_shot_factor: factor required such that number of shots ≥ min_shot_factor * number of pills = 3
- total_operating_time: total available operating time (minutes) = 10000

Variables:
- NumberOfPills: number of pill vaccines administered [integer ≥ 0] [units]
- NumberOfShots: number of shot vaccines administered [integer ≥ 0] [units]

Objective:
- Maximize total patients vaccinated = NumberOfPills + NumberOfShots

Constraints:
1. Time Constraint: (time_pill * NumberOfPills) + (time_shot * NumberOfShots) ≤ total_operating_time  
   (i.e., 10 * NumberOfPills + 20 * NumberOfShots ≤ 10000)
2. Shot-Pill Ratio Constraint: NumberOfShots ≥ min_shot_factor * NumberOfPills  
   (i.e., NumberOfShots ≥ 3 * NumberOfPills)
3. Minimum Pill Constraint: NumberOfPills ≥ min_pill  
   (i.e., NumberOfPills ≥ 30)

--------------------------------------------------

Expected Output Schema:
{
  "variables": {
    "NumberOfPills": "float",
    "NumberOfShots": "float"
  },
  "objective": "float"
}'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_with_linear_solver():
    # Create the CBC solver.
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Solver not created.")
        return None

    # Define variables.
    # NumberOfPills and NumberOfShots are non-negative integers.
    NumberOfPills = solver.IntVar(0, solver.infinity(), "NumberOfPills")
    NumberOfShots = solver.IntVar(0, solver.infinity(), "NumberOfShots")

    # Constraint 1: Minimum Pill Constraint: NumberOfPills >= 30
    solver.Add(NumberOfPills >= 30)

    # Constraint 2: Time Constraint: 10 * NumberOfPills + 20 * NumberOfShots <= 10000
    solver.Add(10 * NumberOfPills + 20 * NumberOfShots <= 10000)

    # Constraint 3: Shot-Pill Ratio Constraint: NumberOfShots >= 3 * NumberOfPills
    solver.Add(NumberOfShots >= 3 * NumberOfPills)

    # Objective: Maximize total patients vaccinated (NumberOfPills + NumberOfShots)
    objective = solver.Objective()
    objective.SetCoefficient(NumberOfPills, 1)
    objective.SetCoefficient(NumberOfShots, 1)
    objective.SetMaximization()

    # Solve the problem.
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        solution = {
            "NumberOfPills": NumberOfPills.solution_value(),
            "NumberOfShots": NumberOfShots.solution_value(),
            "objective": objective.Value()
        }
        return solution
    else:
        return None

def main():
    # Solve using the linear solver implementation.
    final_solution = solve_with_linear_solver()

    # Display the result in a structured way.
    if final_solution:
        print("Solution using Linear Solver:")
        print(final_solution)
    else:
        print("No optimal solution found or the model is infeasible.")

if __name__ == "__main__":
    main()

'''Execution Results:
SUCCESS:
Solution using Linear Solver:
{'NumberOfPills': 142.0, 'NumberOfShots': 429.0, 'objective': 571.0}
'''

'''Expected Output:
Expected solution

: {'variables': {'NumberOfPills': 142.0, 'NumberOfShots': 429.0}, 'objective': 571.0}'''

