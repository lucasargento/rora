# Problem Description:
'''Problem description: A singer has two types of concerts he can hold, pop and R&B. Each pop concert will bring in 100 audience members and take 2 days of practice. Every R&B concert brings in 240 audience members and takes 4 days of practice. The singer must bring in at least 10000 audience members and only has available 180 days for practice. If he can at most perform 40% of his concerts as R&B because he likes pop songs more, how many of each type of concert should be created to minimize the total number of concerts?

Expected Output Schema:
{
  "variables": {
    "NumPopConcerts": "float",
    "NumRnBConcerts": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- ConcertTypes = {Pop, RnB}

Parameters:
- AudiencePerPop = 100        // audience members attracted by one pop concert [audience members per concert]
- AudiencePerRnB = 240        // audience members attracted by one RnB concert [audience members per concert]
- PracticeDaysPop = 2         // practice days required for one pop concert [days per concert]
- PracticeDaysRnB = 4         // practice days required for one RnB concert [days per concert]
- MinAudience = 10000         // minimum total audience required [audience members]
- TotalPracticeDays = 180     // total available practice days [days]
- MaxFractionRnB = 0.4        // maximum allowed fraction of concerts that can be RnB

Variables:
- NumPopConcerts: integer, number of pop concerts to hold [concerts, integer ≥ 0]
- NumRnBConcerts: integer, number of RnB concerts to hold [concerts, integer ≥ 0]

Objective:
- Minimize TotalConcerts = NumPopConcerts + NumRnBConcerts
  (Minimizing the total number of concerts held)

Constraints:
1. Audience constraint:
   AudiencePerPop * NumPopConcerts + AudiencePerRnB * NumRnBConcerts ≥ MinAudience
   i.e., 100 * NumPopConcerts + 240 * NumRnBConcerts ≥ 10000

2. Practice time constraint:
   PracticeDaysPop * NumPopConcerts + PracticeDaysRnB * NumRnBConcerts ≤ TotalPracticeDays
   i.e., 2 * NumPopConcerts + 4 * NumRnBConcerts ≤ 180

3. RnB fraction constraint:
   NumRnBConcerts ≤ MaxFractionRnB * (NumPopConcerts + NumRnBConcerts)
   This can be rearranged as:
   NumRnBConcerts ≤ (2/3) * NumPopConcerts
   (Explanation: Starting from NumRnBConcerts ≤ 0.4*(NumPopConcerts + NumRnBConcerts), subtracting 0.4*NumRnBConcerts from both sides yields 0.6*NumRnBConcerts ≤ 0.4*NumPopConcerts, which simplifies to NumRnBConcerts ≤ (2/3)*NumPopConcerts.)

Expected Output Schema:
{
  "variables": {
    "NumPopConcerts": "integer ≥ 0",
    "NumRnBConcerts": "integer ≥ 0"
  },
  "objective": "Minimize TotalConcerts = NumPopConcerts + NumRnBConcerts"
}'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp
from ortools.sat.python import cp_model

def solve_with_linear_solver():
    # Create the linear solver with the CBC backend.
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Linear solver not available.")
        return None

    # Define variables: integer variables for number of concerts.
    num_pop = solver.IntVar(0, solver.infinity(), 'NumPopConcerts')
    num_rnb = solver.IntVar(0, solver.infinity(), 'NumRnBConcerts')

    # Constraint 1: Audience constraint
    # 100 * NumPopConcerts + 240 * NumRnBConcerts >= 10000
    solver.Add(100 * num_pop + 240 * num_rnb >= 10000)

    # Constraint 2: Practice time constraint
    # 2 * NumPopConcerts + 4 * NumRnBConcerts <= 180
    solver.Add(2 * num_pop + 4 * num_rnb <= 180)

    # Constraint 3: RnB fraction constraint
    # Original: NumRnBConcerts <= 0.4*(NumPopConcerts + NumRnBConcerts)
    # Rearranged: 0.6 NumRNBConcerts <= 0.4 NumPopConcerts  --> multiply both sides by 10:
    # 6 NumRNBConcerts <= 4 NumPopConcerts  --> simplify dividing by 2: 3 NumRNBConcerts <= 2 NumPopConcerts.
    solver.Add(3 * num_rnb <= 2 * num_pop)

    # Objective: minimize total concerts = NumPopConcerts + NumRnBConcerts
    objective = solver.Objective()
    objective.SetMinimization()
    objective.SetCoefficient(num_pop, 1)
    objective.SetCoefficient(num_rnb, 1)

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        result = {
            'NumPopConcerts': int(num_pop.solution_value()),
            'NumRnBConcerts': int(num_rnb.solution_value()),
            'ObjectiveValue': int(num_pop.solution_value() + num_rnb.solution_value())
        }
        return result
    else:
        print("The problem does not have an optimal solution (Linear Solver).")
        return None

def solve_with_cp_model():
    # Create the CP model.
    model = cp_model.CpModel()

    # Define decision variables.
    num_pop = model.NewIntVar(0, 10000, 'NumPopConcerts')  # upper bound chosen arbitrarily high
    num_rnb = model.NewIntVar(0, 10000, 'NumRnBConcerts')

    # Constraint 1: Audience constraint
    # 100 * NumPopConcerts + 240 * NumRnBConcerts >= 10000
    model.Add(100 * num_pop + 240 * num_rnb >= 10000)

    # Constraint 2: Practice time constraint
    # 2 * NumPopConcerts + 4 * NumRnBConcerts <= 180
    model.Add(2 * num_pop + 4 * num_rnb <= 180)

    # Constraint 3: RnB fraction constraint
    # 3 * NumRnBConcerts <= 2 * NumPopConcerts (derived from ratio requirement)
    model.Add(3 * num_rnb <= 2 * num_pop)

    # Objective: minimize total concerts = NumPopConcerts + NumRnBConcerts.
    total_concerts = model.NewIntVar(0, 10000, 'TotalConcerts')
    model.Add(total_concerts == num_pop + num_rnb)
    model.Minimize(total_concerts)

    # Solve the model using the CP-SAT solver.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        result = {
            'NumPopConcerts': solver.Value(num_pop),
            'NumRnBConcerts': solver.Value(num_rnb),
            'ObjectiveValue': solver.Value(total_concerts)
        }
        return result
    else:
        print("The problem does not have an optimal solution (CP Model).")
        return None

def main():
    print("Solution using OR-Tools Linear Solver:")
    linear_result = solve_with_linear_solver()
    if linear_result:
        print("NumPopConcerts:", linear_result['NumPopConcerts'])
        print("NumRnBConcerts:", linear_result['NumRnBConcerts'])
        print("TotalConcerts (Objective Value):", linear_result['ObjectiveValue'])
    print("\n" + "="*50 + "\n")
    print("Solution using OR-Tools CP Model:")
    cp_result = solve_with_cp_model()
    if cp_result:
        print("NumPopConcerts:", cp_result['NumPopConcerts'])
        print("NumRnBConcerts:", cp_result['NumRnBConcerts'])
        print("TotalConcerts (Objective Value):", cp_result['ObjectiveValue'])

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Solution using OR-Tools Linear Solver:
NumPopConcerts: 40
NumRnBConcerts: 25
TotalConcerts (Objective Value): 65

==================================================

Solution using OR-Tools CP Model:
NumPopConcerts: 40
NumRnBConcerts: 25
TotalConcerts (Objective Value): 65
'''

'''Expected Output:
Expected solution

: {'variables': {'NumPopConcerts': 40.0, 'NumRnBConcerts': 25.0}, 'objective': 65.0}'''

