# Problem Description:
'''Problem description: A clinic makes batches of vitamin shots and pills. Each batch of vitamin shots requires 30 units of vitamin C and 40 units of vitamin D. Each batch of vitamin pills requires 50 units of vitamin C and 30 units of vitamin D. Since pills are more popular, the number of batches of vitamin pills must be larger than the number of batches of vitamin shots. Further, the clinic can make at most 10 batches of vitamin shots. The clinic has available 1200 units of vitamin C and 1500 units of vitamin D. If each batch of vitamin shots can supply 10 people and each batch of vitamin pills can supply 7 people, how many batches of each should be made to maximize the number of people that can be supplied?

Expected Output Schema:
{
  "variables": {
    "BatchesShots": "float",
    "BatchesPills": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
  - ProductTypes = {Shots, Pills}

Parameters:
  - vitaminC_shots = 30 units per batch (Vitamin C required for one batch of vitamin shots)
  - vitaminD_shots = 40 units per batch (Vitamin D required for one batch of vitamin shots)
  - vitaminC_pills = 50 units per batch (Vitamin C required for one batch of vitamin pills)
  - vitaminD_pills = 30 units per batch (Vitamin D required for one batch of vitamin pills)
  - supply_per_shot = 10 people per batch (Number of people supplied per batch of vitamin shots)
  - supply_per_pill = 7 people per batch (Number of people supplied per batch of vitamin pills)
  - available_vitaminC = 1200 units (Total Vitamin C available)
  - available_vitaminD = 1500 units (Total Vitamin D available)
  - max_batches_shots = 10 (Maximum allowed batches of vitamin shots)

Variables:
  - BatchesShots: integer, number of batches of vitamin shots to produce (>= 0)
  - BatchesPills: integer, number of batches of vitamin pills to produce (>= 0)

Objective:
  - Maximize TotalPeopleSupplied = (supply_per_shot * BatchesShots) + (supply_per_pill * BatchesPills)
    (Maximize the number of people supplied with vitamin shots and pills)

Constraints:
  - Vitamin C constraint: 
      (vitaminC_shots * BatchesShots) + (vitaminC_pills * BatchesPills) <= available_vitaminC
      i.e., 30 * BatchesShots + 50 * BatchesPills <= 1200
  - Vitamin D constraint:
      (vitaminD_shots * BatchesShots) + (vitaminD_pills * BatchesPills) <= available_vitaminD
      i.e., 40 * BatchesShots + 30 * BatchesPills <= 1500
  - Production limit for shots:
      BatchesShots <= max_batches_shots
      i.e., BatchesShots <= 10
  - Popularity constraint (batches of pills must be larger than batches of shots): 
      BatchesPills >= BatchesShots + 1
      (This enforces that the number of vitamin pill batches is strictly greater than the number of vitamin shot batches)'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp
from ortools.sat.python import cp_model

def solve_with_linear_solver():
    # Create the mip solver with the CBC backend.
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Linear solver not available.")
        return None

    # Parameters
    vitaminC_shots = 30
    vitaminD_shots = 40
    vitaminC_pills = 50
    vitaminD_pills = 30
    supply_per_shot = 10
    supply_per_pill = 7
    available_vitaminC = 1200
    available_vitaminD = 1500
    max_batches_shots = 10

    # Decision Variables: integer variables >= 0
    BatchesShots = solver.IntVar(0, max_batches_shots, 'BatchesShots')
    # Assuming no explicit upper bound for pills aside from resource constraints,
    # set a high upper bound.
    BatchesPills = solver.IntVar(0, solver.infinity(), 'BatchesPills')

    # Constraints
    # 1. Vitamin C constraint: 30 * BatchesShots + 50 * BatchesPills <= 1200
    solver.Add(vitaminC_shots * BatchesShots + vitaminC_pills * BatchesPills <= available_vitaminC)

    # 2. Vitamin D constraint: 40 * BatchesShots + 30 * BatchesPills <= 1500
    solver.Add(vitaminD_shots * BatchesShots + vitaminD_pills * BatchesPills <= available_vitaminD)

    # 3. Production limit for shots: BatchesShots <= 10 (already set by variable bounds)

    # 4. Popularity constraint: BatchesPills >= BatchesShots + 1
    solver.Add(BatchesPills >= BatchesShots + 1)

    # Objective: Maximize total people supplied = 10*BatchesShots + 7*BatchesPills
    objective = solver.Objective()
    objective.SetCoefficient(BatchesShots, supply_per_shot)
    objective.SetCoefficient(BatchesPills, supply_per_pill)
    objective.SetMaximization()

    status = solver.Solve()
    solution = {}
    if status == pywraplp.Solver.OPTIMAL:
        solution['BatchesShots'] = BatchesShots.solution_value()
        solution['BatchesPills'] = BatchesPills.solution_value()
        solution['objective'] = objective.Value()
    else:
        print("The linear solver did not find an optimal solution.")
        return None

    return solution

def solve_with_cp_model():
    # Create the CP-SAT model.
    model = cp_model.CpModel()

    # Parameters (same as before)
    vitaminC_shots = 30
    vitaminD_shots = 40
    vitaminC_pills = 50
    vitaminD_pills = 30
    supply_per_shot = 10
    supply_per_pill = 7
    available_vitaminC = 1200
    available_vitaminD = 1500
    max_batches_shots = 10

    # Decision Variables: integer variables; we use cp_model.INT_VAR_MIN and cp_model.INT_VAR_MAX.
    BatchesShots = model.NewIntVar(0, max_batches_shots, 'BatchesShots')
    # For BatchesPills, set an upper bound. Here, using 1000 as a safe upper bound.
    BatchesPills = model.NewIntVar(0, 1000, 'BatchesPills')

    # Constraints
    model.Add(vitaminC_shots * BatchesShots + vitaminC_pills * BatchesPills <= available_vitaminC)
    model.Add(vitaminD_shots * BatchesShots + vitaminD_pills * BatchesPills <= available_vitaminD)
    # Popularity constraint: BatchesPills >= BatchesShots + 1
    model.Add(BatchesPills >= BatchesShots + 1)

    # Objective: Maximize total people supplied = 10 * BatchesShots + 7 * BatchesPills
    total_people = supply_per_shot * BatchesShots + supply_per_pill * BatchesPills
    model.Maximize(total_people)

    # Solve the model.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    solution = {}
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        solution['BatchesShots'] = solver.Value(BatchesShots)
        solution['BatchesPills'] = solver.Value(BatchesPills)
        solution['objective'] = solver.ObjectiveValue()
    else:
        print("The CP-SAT model did not find an optimal solution.")
        return None

    return solution

def main():
    results = {}
    # Run linear solver model
    lin_solution = solve_with_linear_solver()
    if lin_solution:
        results['LinearSolver'] = lin_solution
    else:
        results['LinearSolver'] = "No optimal solution found."

    # Run CP-SAT model
    cp_solution = solve_with_cp_model()
    if cp_solution:
        results['CPSAT'] = cp_solution
    else:
        results['CPSAT'] = "No optimal solution found."

    # Print the results in a structured manner.
    print("Optimization Results:")
    for model_name, sol in results.items():
        print(f"\nModel: {model_name}")
        if isinstance(sol, dict):
            print(f"  BatchesShots: {sol['BatchesShots']}")
            print(f"  BatchesPills: {sol['BatchesPills']}")
            print(f"  Objective Value (Total People Supplied): {sol['objective']}")
        else:
            print("  " + sol)

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Optimization Results:

Model: LinearSolver
  BatchesShots: 10.0
  BatchesPills: 18.0
  Objective Value (Total People Supplied): 226.0

Model: CPSAT
  BatchesShots: 10
  BatchesPills: 18
  Objective Value (Total People Supplied): 226.0
'''

'''Expected Output:
Expected solution

: {'variables': {'BatchesShots': 10.0, 'BatchesPills': 18.0}, 'objective': 226.0}'''

