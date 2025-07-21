# Problem Description:
'''Problem description: A zoo needs to transport their monkeys to the vet either by bus or by car. A bus can transport 20 monkeys per trip and takes 30 minutes. A car can transport 6 monkeys per trip and takes 15 minutes. There can be at most 10 bus trips. In addition, since the monkeys get aggressive when there are too many in one place at least 60% of the trips should be by car. If the zoo needs to transport 300 monkeys, how many trips of each should be done to minimize the total time required to transport the monkeys?

Expected Output Schema:
{
  "variables": {
    "BusTrips": "float",
    "CarTrips": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- TransportModes: set = {Bus, Car}

Parameters:
- capacity_Bus: number of monkeys per bus trip = 20 monkeys/trip
- capacity_Car: number of monkeys per car trip = 6 monkeys/trip
- time_Bus: travel time per bus trip = 30 minutes/trip
- time_Car: travel time per car trip = 15 minutes/trip
- max_bus_trips: maximum number of bus trips = 10 trips
- total_monkeys: total monkeys that need to be transported = 300 monkeys
- car_share_minimum: minimum fraction of trips that must be by car = 60% (i.e., 0.60)

Variables:
- BusTrips: number of bus trips (nonnegative integer)
- CarTrips: number of car trips (nonnegative integer)

Objective:
- Minimize the total transport time (minutes), given by:
  TotalTime = time_Bus * BusTrips + time_Car * CarTrips

Constraints:
1. Capacity constraint (ensure enough monkeys are transported):
   capacity_Bus * BusTrips + capacity_Car * CarTrips >= total_monkeys
2. Maximum bus trips constraint:
   BusTrips <= max_bus_trips
3. Car trip share constraint (at least 60% of the trips are by car):
   CarTrips >= car_share_minimum * (BusTrips + CarTrips)
   (This can be rearranged to: CarTrips >= (car_share_minimum / (1 - car_share_minimum)) * BusTrips, i.e., CarTrips >= 1.5 * BusTrips)

Note:
- The units are consistent: monkeys per trip combined with trips yield the total monkeys, and time units (minutes) multiplied by number of trips yield total time.
- Although trips are typically integer decisions, the variable type can be specified as integer if required by the implementation.

Expected Output Schema:
{
  "variables": {
    "BusTrips": "float",
    "CarTrips": "float"
  },
  "objective": "float"
}'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp
from ortools.sat.python import cp_model

def solve_with_linear_solver():
    # Create the MIP solver using CBC backend.
    solver = pywraplp.Solver.CreateSolver('CBC_MIXED_INTEGER_PROGRAMMING')
    if not solver:
        print("Linear solver not available.")
        return None

    # Parameters
    capacity_bus = 20
    capacity_car = 6
    time_bus = 30
    time_car = 15
    max_bus_trips = 10
    total_monkeys = 300
    car_share_minimum = 0.60  # 60%

    # Variables (we use integer variables)
    BusTrips = solver.IntVar(0, max_bus_trips, 'BusTrips')
    # Set an upper bound for CarTrips sufficiently large (e.g., total_monkeys)
    CarTrips = solver.IntVar(0, total_monkeys, 'CarTrips')

    # Constraint 1: Capacity constraint
    solver.Add(capacity_bus * BusTrips + capacity_car * CarTrips >= total_monkeys)

    # Constraint 2: Maximum bus trips
    solver.Add(BusTrips <= max_bus_trips)

    # Constraint 3: Car trip share constraint
    # At least 60% of the trips must be by car:
    # CarTrips >= 0.6 * (BusTrips + CarTrips)  ->  CarTrips >= (0.6/(1-0.6))*BusTrips = 1.5 * BusTrips
    # Multiply by 10 to avoid floating issues: 10 * CarTrips >= 15 * BusTrips
    solver.Add(10 * CarTrips >= 15 * BusTrips)

    # Objective: minimize total time = time_bus * BusTrips + time_car * CarTrips
    objective = solver.Objective()
    objective.SetCoefficient(BusTrips, time_bus)
    objective.SetCoefficient(CarTrips, time_car)
    objective.SetMinimization()

    status = solver.Solve()

    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result['BusTrips'] = BusTrips.solution_value()
        result['CarTrips'] = CarTrips.solution_value()
        result['objective'] = objective.Value()
    else:
        result['error'] = 'No optimal solution found using the Linear Solver.'
    return result

def solve_with_cp_model():
    # Create the CP model.
    model = cp_model.CpModel()

    # Parameters (same as before)
    capacity_bus = 20
    capacity_car = 6
    time_bus = 30
    time_car = 15
    max_bus_trips = 10
    total_monkeys = 300
    car_share_minimum = 0.60  # 60%

    # Variables: define integer variables.
    BusTrips = model.NewIntVar(0, max_bus_trips, 'BusTrips')
    CarTrips = model.NewIntVar(0, total_monkeys, 'CarTrips')

    # Constraint 1: Capacity constraint
    model.Add(capacity_bus * BusTrips + capacity_car * CarTrips >= total_monkeys)

    # Constraint 2: Maximum bus trips constraint is inherent in variable domain.

    # Constraint 3: Car trip share constraint.
    # Original constraint: CarTrips >= 1.5 * BusTrips.
    # To avoid fractional coefficients, multiply both sides by 2: 2 * CarTrips >= 3 * BusTrips
    model.Add(2 * CarTrips >= 3 * BusTrips)

    # Define the objective: minimize total time = time_bus * BusTrips + time_car * CarTrips.
    # In CP-SAT, we use AddMinimize.
    total_time = time_bus * BusTrips + time_car * CarTrips
    model.Minimize(total_time)

    # Create solver and solve.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    result = {}
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        result['BusTrips'] = solver.Value(BusTrips)
        result['CarTrips'] = solver.Value(CarTrips)
        result['objective'] = solver.ObjectiveValue()
    else:
        result['error'] = 'No solution found using CP-SAT model.'
    return result

def main():
    print("Solving with Linear Solver (MIP):")
    lin_result = solve_with_linear_solver()
    if lin_result is not None:
        if 'error' in lin_result:
            print(lin_result['error'])
        else:
            print({
              "variables": {
                "BusTrips": lin_result['BusTrips'],
                "CarTrips": lin_result['CarTrips']
              },
              "objective": lin_result['objective']
            })

    print("\nSolving with CP-SAT Model:")
    cp_result = solve_with_cp_model()
    if cp_result is not None:
        if 'error' in cp_result:
            print(cp_result['error'])
        else:
            print({
              "variables": {
                "BusTrips": cp_result['BusTrips'],
                "CarTrips": cp_result['CarTrips']
              },
              "objective": cp_result['objective']
            })

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Solving with Linear Solver (MIP):
{'variables': {'BusTrips': 10.0, 'CarTrips': 17.0}, 'objective': 555.0}

Solving with CP-SAT Model:
{'variables': {'BusTrips': 10, 'CarTrips': 17}, 'objective': 555.0}
'''

'''Expected Output:
Expected solution

: {'variables': {'BusTrips': 9.0, 'CarTrips': 20.0}, 'objective': 570.0}'''

