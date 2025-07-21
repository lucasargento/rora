# Problem Description:
'''Problem description: An airport can either install escalators or elevators. Escalators can transport 20 people every minute whereas elevators can transport 8 people every minute. Escalators take up 5 units of space while elevators take 2 units of space. The airport needs to have enough capacity to transport at least 400 people every minute. Additionally, there must be at least three times more escalators than elevators and at least 2 elevators must be used. How many of each type should the airport install to minimize the total units of space taken?

Expected Output Schema:
{
  "variables": {
    "NumberEscalators": "float",
    "NumberElevators": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- DeviceType: set = {Escalator, Elevator}

Parameters:
- CapacityPerEscalator: 20 people per minute (transport capacity of one escalator)
- CapacityPerElevator: 8 people per minute (transport capacity of one elevator)
- SpaceEscalator: 5 units (space consumed by one escalator)
- SpaceElevator: 2 units (space consumed by one elevator)
- RequiredCapacity: 400 people per minute (minimum transport capacity)
- RatioFactor: 3 (the number of escalators must be at least three times the number of elevators)
- MinElevators: 2 (at least two elevators must be installed)

Variables:
- NumberEscalators: integer, ≥ 0 (number of escalators to install)
- NumberElevators: integer, ≥ 0 (number of elevators to install)

Objective:
Minimize TotalSpace = (SpaceEscalator * NumberEscalators) + (SpaceElevator * NumberElevators)
  (This represents the total units of space taken by the installed devices.)

Constraints:
1. Capacity Constraint:
   (CapacityPerEscalator * NumberEscalators) + (CapacityPerElevator * NumberElevators) ≥ RequiredCapacity
   (The combined capacity of escalators and elevators must transport at least 400 people per minute.)
   
2. Ratio Constraint:
   NumberEscalators ≥ RatioFactor * NumberElevators
   (There must be at least three times more escalators than elevators.)
   
3. Minimum Elevators Constraint:
   NumberElevators ≥ MinElevators
   (At least 2 elevators must be installed.)'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_linear_model():
    # Create the linear solver using the CBC backend.
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        return None, "Solver not created."

    # Variables: numbers of escalators and elevators (integer, nonnegative)
    num_escalators = solver.IntVar(0.0, solver.infinity(), 'NumberEscalators')
    num_elevators = solver.IntVar(0.0, solver.infinity(), 'NumberElevators')

    # Parameters
    capacity_per_escalator = 20
    capacity_per_elevator = 8
    space_escalator = 5
    space_elevator = 2
    required_capacity = 400
    ratio_factor = 3
    min_elevators = 2

    # Constraints:
    # 1. Capacity Constraint:
    #    20 * NumberEscalators + 8 * NumberElevators >= 400
    capacity_constraint = solver.Constraint(required_capacity, solver.infinity())
    capacity_constraint.SetCoefficient(num_escalators, capacity_per_escalator)
    capacity_constraint.SetCoefficient(num_elevators, capacity_per_elevator)

    # 2. Ratio Constraint:
    #    NumberEscalators >= 3 * NumberElevators
    ratio_constraint = solver.Constraint(0, solver.infinity())
    ratio_constraint.SetCoefficient(num_escalators, 1)
    ratio_constraint.SetCoefficient(num_elevators, -ratio_factor)

    # 3. Minimum Elevators Constraint:
    #    NumberElevators >= 2
    min_elevator_constraint = solver.Constraint(min_elevators, solver.infinity())
    min_elevator_constraint.SetCoefficient(num_elevators, 1)

    # Objective: Minimize total space = 5 * NumberEscalators + 2 * NumberElevators
    objective = solver.Objective()
    objective.SetCoefficient(num_escalators, space_escalator)
    objective.SetCoefficient(num_elevators, space_elevator)
    objective.SetMinimization()

    # Solve the model.
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "variables": {
                "NumberEscalators": num_escalators.solution_value(),
                "NumberElevators": num_elevators.solution_value()
            },
            "objective": objective.Value()
        }
    else:
        result = {
            "message": "No optimal solution found. The problem might be infeasible."
        }
    return result, None

def main():
    # We'll implement one formulation from the provided description.
    results = {}

    # Implementation 1: Linear programming formulation with ortools.linear_solver
    result_lp, error_lp = solve_linear_model()
    if error_lp:
        results["LinearModel"] = {"error": error_lp}
    else:
        results["LinearModel"] = result_lp

    # Print structured results for each implementation.
    print("Results:")
    for impl, res in results.items():
        print(f"{impl}: {res}")

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Results:
LinearModel: {'variables': {'NumberEscalators': 18.0, 'NumberElevators': 5.0}, 'objective': 100.0}
'''

'''Expected Output:
Expected solution

: {'variables': {'NumberEscalators': 18.0, 'NumberElevators': 5.0}, 'objective': 100.0}'''

