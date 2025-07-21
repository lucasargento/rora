# Problem Description:
'''Problem description: A science show preforms two different demonstrations, demonstration 1 and demonstration 2. In demonstration 1, 10 units of mint and 20 units of the active ingredient is used to make 25 units of minty foam. In demonstration 2, 12 units of mint and 15 units of the active ingredient is used to make 18 units of minty foam. In addition, demonstration 1 creates 5 units of black tar while demonstration 2 creates 3 units of black tar. The show has available 120 units of mint and 100 units of active ingredients. If at most 50 units of black tar can be produced, how many of each demonstration should be done to maximize the amount of minty foam produced?

Expected Output Schema:
{
  "variables": {
    "DemonstrationUsed": [
      "float"
    ]
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- Demos: set of demonstrations = {1, 2}

Parameters:
- mint_required_d: mint used per demonstration d (units)
  • For demo 1: 10
  • For demo 2: 12
- active_required_d: active ingredient used per demonstration d (units)
  • For demo 1: 20
  • For demo 2: 15
- foam_produced_d: minty foam produced per demonstration d (units)
  • For demo 1: 25
  • For demo 2: 18
- tar_produced_d: black tar produced per demonstration d (units)
  • For demo 1: 5
  • For demo 2: 3
- available_mint: total available mint (units) = 120
- available_active: total available active ingredient (units) = 100
- max_tar: maximum allowable black tar produced (units) = 50

Variables:
- x_d: number of times demonstration d is performed, for all d in Demos (nonnegative float; note: while the decision logically pertains to countable demonstrations, the expected output schema permits float)

Objective:
- Maximize total minty foam produced = foam_produced_1 * x_1 + foam_produced_2 * x_2

Constraints:
1. Mint constraint: mint_required_1 * x_1 + mint_required_2 * x_2 ≤ available_mint
2. Active ingredient constraint: active_required_1 * x_1 + active_required_2 * x_2 ≤ available_active
3. Black tar constraint: tar_produced_1 * x_1 + tar_produced_2 * x_2 ≤ max_tar

Comments:
- All units are assumed to be consistent (units for mint, active ingredient, foam, and tar are all as stated in the problem description).
- Although demonstrations are inherently discrete events, the expected schema defines decision variables as float so x_d is modeled as continuous.
- This structured model precisely represents the original optimization problem.'''

# Generated Code:
from ortools.linear_solver import pywraplp

def solve_with_linear_solver():
    # Create the linear solver using the GLOP backend.
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Solver not created.")
        return None

    # Parameters
    available_mint = 120
    available_active = 100
    max_tar = 50

    # Parameters for each demonstration:
    # demo 1
    mint_required_1 = 10
    active_required_1 = 20
    foam_produced_1 = 25
    tar_produced_1 = 5
    # demo 2
    mint_required_2 = 12
    active_required_2 = 15
    foam_produced_2 = 18
    tar_produced_2 = 3

    # Decision variables: number of times each demonstration is performed (continuous as per expected schema)
    x1 = solver.NumVar(0.0, solver.infinity(), 'x1')  # demonstration 1
    x2 = solver.NumVar(0.0, solver.infinity(), 'x2')  # demonstration 2

    # Constraints
    # Mint constraint: 10 * x1 + 12 * x2 <= 120
    solver.Add(mint_required_1 * x1 + mint_required_2 * x2 <= available_mint)
    # Active ingredient constraint: 20 * x1 + 15 * x2 <= 100
    solver.Add(active_required_1 * x1 + active_required_2 * x2 <= available_active)
    # Black tar constraint: 5 * x1 + 3 * x2 <= 50
    solver.Add(tar_produced_1 * x1 + tar_produced_2 * x2 <= max_tar)

    # Objective: maximize total minty foam produced = 25*x1 + 18*x2
    objective = solver.Objective()
    objective.SetCoefficient(x1, foam_produced_1)
    objective.SetCoefficient(x2, foam_produced_2)
    objective.SetMaximization()

    # Solve the problem
    result_status = solver.Solve()

    # Check the result status.
    solution = {}
    if result_status == pywraplp.Solver.OPTIMAL:
        solution['variables'] = {
            "DemonstrationUsed": [x1.solution_value(), x2.solution_value()]
        }
        solution['objective'] = objective.Value()
    else:
        solution['message'] = "No optimal solution found. The problem might be infeasible."

    return solution

def main():
    # Since only a single formulation is provided, we only call one model implementation.
    solution_linear = solve_with_linear_solver()

    print("Results for the Linear Programming Model using ortools.linear_solver:")
    if 'message' in solution_linear:
        print(solution_linear['message'])
    else:
        print("Demonstrations (Demo 1, Demo 2):", solution_linear['variables']["DemonstrationUsed"])
        print("Total Minty Foam Produced =", solution_linear['objective'])

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Results for the Linear Programming Model using ortools.linear_solver:
Demonstrations (Demo 1, Demo 2): [5.000000000000001, 0.0]
Total Minty Foam Produced = 125.00000000000003
'''

'''Expected Output:
Expected solution

: {'variables': {'DemonstrationUsed': [5.0, 0.0]}, 'objective': 125.0}'''

