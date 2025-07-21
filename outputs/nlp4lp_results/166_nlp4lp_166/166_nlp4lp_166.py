# Problem Description:
'''Problem description: Employees have the option of car-pooling to work or taking the company bus. A car can take 4 employees and produces 10 units of pollution, while a bus can take 20 employees and produces 30 units of pollution. At least 300 employees need to be transported and at most 4 buses can be used. How many of each type of transport should be taken to minimize the total pollution produced.

Expected Output Schema:
{
  "variables": {
    "xCars": "float",
    "xBuses": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- T: set of transport types = {Car, Bus}

Parameters:
- capacity_Car: number of employees that can be transported by one car = 4 [employees per car]
- capacity_Bus: number of employees that can be transported by one bus = 20 [employees per bus]
- pollution_Car: pollution produced by one car = 10 [pollution units per car]
- pollution_Bus: pollution produced by one bus = 30 [pollution units per bus]
- min_employees: minimum number of employees to transport = 300 [employees]
- max_buses: maximum number of buses allowed = 4 [buses]

Variables:
- xCars: number of cars to be used [integer, ≥ 0, units: vehicles]
- xBuses: number of buses to be used [integer, ≥ 0, units: vehicles]

Objective:
- Minimize total pollution = pollution_Car * xCars + pollution_Bus * xBuses

Constraints:
- Employee Transport Constraint: capacity_Car * xCars + capacity_Bus * xBuses ≥ min_employees  
  (This ensures that the total number of employees that can be transported meets or exceeds 300.)
- Bus Limit Constraint: xBuses ≤ max_buses  
  (This ensures that at most 4 buses are used.)'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_with_linear_solver():
    # Create the mip solver with SCIP backend.
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        return None, "Solver not created."

    # Parameters.
    capacity_Car = 4
    capacity_Bus = 20
    pollution_Car = 10
    pollution_Bus = 30
    min_employees = 300
    max_buses = 4

    # Variables.
    xCars = solver.IntVar(0, solver.infinity(), 'xCars')
    xBuses = solver.IntVar(0, max_buses, 'xBuses')  # xBuses is upper bounded by max_buses

    # Constraints.
    # Employee Transport Constraint: 4*xCars + 20*xBuses >= 300.
    solver.Add(capacity_Car * xCars + capacity_Bus * xBuses >= min_employees)

    # Note: The bus limit constraint is already enforced by the domain of xBuses (<= max_buses).

    # Objective: Minimize total pollution.
    objective = solver.Objective()
    objective.SetCoefficient(xCars, pollution_Car)
    objective.SetCoefficient(xBuses, pollution_Bus)
    objective.SetMinimization()

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "variables": {
                "xCars": xCars.solution_value(),
                "xBuses": xBuses.solution_value()
            },
            "objective": objective.Value()
        }
        return result, None
    elif status == pywraplp.Solver.INFEASIBLE:
        return None, "No feasible solution found."
    else:
        return None, "Solver ended with an unexpected status."

def main():
    # As only one formulation is provided, we only call one implementation.
    result, error = solve_with_linear_solver()
    if error:
        print("Error:", error)
    else:
        # Print the result in a structured way.
        print("Solution using ortools.linear_solver:")
        print(result)

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Solution using ortools.linear_solver:
{'variables': {'xCars': 55.0, 'xBuses': 4.0}, 'objective': 670.0}
'''

'''Expected Output:
Expected solution

: {'variables': {'xCars': 55.0, 'xBuses': 4.0}, 'objective': 670.0}'''

