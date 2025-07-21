# Problem Description:
'''Problem description: A large fishing boat sends fish back to shore either by small canoes or smaller diesel boats. A canoe can carry back 10 fish while a small diesel boat can carry back 15 fish. In order to follow environmental rules, the number of small canoes used has to be at least 3 times as many as the number of diesel boats uses. If  at least 1000 fish need to be transported to shore, minimize the total number of canoes and diesel boats needed.

Expected Output Schema:
{
  "variables": {
    "NumberOfCanoes": "float",
    "NumberOfDieselBoats": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- V: set of vessel types = {Canoe, DieselBoat}

Parameters:
- capacity_Canoe: 10 fish per canoe
- capacity_DieselBoat: 15 fish per diesel boat
- fishRequirement: 1000 fish (minimum fish to be transported)

Variables:
- NumberOfCanoes: number of canoes to be used (nonnegative, decision variable; assumed to be an integer)
- NumberOfDieselBoats: number of diesel boats to be used (nonnegative, decision variable; assumed to be an integer)

Objective:
- Minimize totalVehicles = NumberOfCanoes + NumberOfDieselBoats

Constraints:
1. Fish Transportation Constraint:
   (capacity_Canoe * NumberOfCanoes) + (capacity_DieselBoat * NumberOfDieselBoats) ≥ fishRequirement
   (This means that the total number of fish carried by all vessels must be at least 1000 fish)

2. Environmental Regulation Constraint:
   NumberOfCanoes ≥ 3 * NumberOfDieselBoats
   (The number of canoes must be at least three times the number of diesel boats)

Output Schema Example:
{
  "variables": {
    "NumberOfCanoes": "float",
    "NumberOfDieselBoats": "float"
  },
  "objective": "float"
}'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp
from ortools.sat.python import cp_model

def solve_with_linear_solver():
    # Create the linear solver with the CBC backend.
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Linear Solver not found.")
        return None

    # Define decision variables (nonnegative integers).
    NumberOfCanoes = solver.IntVar(0, solver.infinity(), 'NumberOfCanoes')
    NumberOfDieselBoats = solver.IntVar(0, solver.infinity(), 'NumberOfDieselBoats')

    # Parameters.
    capacity_Canoe = 10
    capacity_DieselBoat = 15
    fishRequirement = 1000

    # Constraint 1: Fish Transportation Constraint.
    solver.Add(capacity_Canoe * NumberOfCanoes + capacity_DieselBoat * NumberOfDieselBoats >= fishRequirement)

    # Constraint 2: Environmental Regulation Constraint.
    solver.Add(NumberOfCanoes >= 3 * NumberOfDieselBoats)

    # Objective: Minimize the total number of vessels.
    solver.Minimize(NumberOfCanoes + NumberOfDieselBoats)

    # Solve the problem.
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "variables": {
                "NumberOfCanoes": NumberOfCanoes.solution_value(),
                "NumberOfDieselBoats": NumberOfDieselBoats.solution_value()
            },
            "objective": NumberOfCanoes.solution_value() + NumberOfDieselBoats.solution_value()
        }
    else:
        result = {"message": "No optimal solution found with linear solver."}

    return result

def solve_with_cp_model():
    # Create the CP-SAT model.
    model = cp_model.CpModel()

    # Define decision variables.
    NumberOfCanoes = model.NewIntVar(0, 10000, 'NumberOfCanoes')
    NumberOfDieselBoats = model.NewIntVar(0, 10000, 'NumberOfDieselBoats')

    # Parameters.
    capacity_Canoe = 10
    capacity_DieselBoat = 15
    fishRequirement = 1000

    # Constraint 1: Fish Transportation Constraint.
    model.Add(capacity_Canoe * NumberOfCanoes + capacity_DieselBoat * NumberOfDieselBoats >= fishRequirement)

    # Constraint 2: Environmental Regulation Constraint.
    model.Add(NumberOfCanoes >= 3 * NumberOfDieselBoats)

    # Objective: Minimize the total number of vessels.
    total_vehicles = model.NewIntVar(0, 10000, 'total_vehicles')
    model.Add(total_vehicles == NumberOfCanoes + NumberOfDieselBoats)
    model.Minimize(total_vehicles)

    # Solve the problem.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        result = {
            "variables": {
                "NumberOfCanoes": solver.Value(NumberOfCanoes),
                "NumberOfDieselBoats": solver.Value(NumberOfDieselBoats)
            },
            "objective": solver.Value(total_vehicles)
        }
    else:
        result = {"message": "No optimal solution found with CP-SAT model."}

    return result

def main():
    print("Results from Linear Solver (MIP):")
    linear_result = solve_with_linear_solver()
    print(linear_result)
    print("\nResults from CP-SAT Model:")
    cp_result = solve_with_cp_model()
    print(cp_result)

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Results from Linear Solver (MIP):
{'variables': {'NumberOfCanoes': 67.0, 'NumberOfDieselBoats': 22.0}, 'objective': 89.0}

Results from CP-SAT Model:
{'variables': {'NumberOfCanoes': 67, 'NumberOfDieselBoats': 22}, 'objective': 89}
'''

'''Expected Output:
Expected solution

: {'variables': {'NumberOfCanoes': 67.0, 'NumberOfDieselBoats': 22.0}, 'objective': 89.0}'''

