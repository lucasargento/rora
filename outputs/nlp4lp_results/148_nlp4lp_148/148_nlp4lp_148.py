# Problem Description:
'''Problem description: A chicken farmer has sold his chicken and they need to be transported either by bus or by car. A bus can take 100 chicken and takes 2 hours per trip. A car can take 40 chicken and takes 1.5 hours per trip. There can be at most 10 bus trips and at least 60% of the trips must be by car. If the farmer needs to transport 1200 chicken, how many trips of each should be done to minimize the total time needed to transport the chicken?

Expected Output Schema:
{
  "variables": {
    "NumberOfBusTrips": "float",
    "NumberOfCarTrips": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- TransportModes = {bus, car}

Parameters:
- BusCapacity: number of chickens transported per bus trip (100 chickens per trip)
- CarCapacity: number of chickens transported per car trip (40 chickens per trip)
- BusDuration: time required per bus trip (2 hours per trip)
- CarDuration: time required per car trip (1.5 hours per trip)
- TotalChickens: total number of chickens to transport (1200 chickens)
- MaxBusTrips: maximum number of bus trips allowed (10 trips)
- MinCarTripRatio: minimum ratio of car trips to total trips (0.6, meaning at least 60% of trips must be by car)

Variables:
- NumberOfBusTrips: number of bus trips to schedule (integer ≥ 0)
- NumberOfCarTrips: number of car trips to schedule (integer ≥ 0)

Objective:
- Minimize TotalTime = (BusDuration * NumberOfBusTrips) + (CarDuration * NumberOfCarTrips)

Constraints:
1. Chicken transportation constraint:
   (BusCapacity * NumberOfBusTrips) + (CarCapacity * NumberOfCarTrips) = TotalChickens
   (This constraint ensures that exactly 1200 chickens are transported.)
2. Bus trips limit:
   NumberOfBusTrips ≤ MaxBusTrips
3. Car trips ratio constraint (at least 60% of trips must be by car):
   NumberOfCarTrips ≥ MinCarTripRatio * (NumberOfBusTrips + NumberOfCarTrips)
   (This can be equivalently rearranged to: NumberOfCarTrips ≥ 1.5 * NumberOfBusTrips)
4. Non-negativity and integrality:
   NumberOfBusTrips and NumberOfCarTrips are nonnegative integers

Final Output Schema (as required):
{
  "variables": {
    "NumberOfBusTrips": "integer >= 0",
    "NumberOfCarTrips": "integer >= 0"
  },
  "objective": "Minimize TotalTime = 2 * NumberOfBusTrips + 1.5 * NumberOfCarTrips"
}'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_with_linear_solver():
    # Create the MIP solver with CBC backend.
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Solver not created successfully.")
        return None

    # Parameters
    bus_capacity = 100      # chickens per bus trip
    car_capacity = 40       # chickens per car trip
    bus_duration = 2.0      # hours per bus trip
    car_duration = 1.5      # hours per car trip
    total_chickens = 1200   # total chickens to transport
    max_bus_trips = 10
    # Car trip ratio: at least 60% of trips by car means carTrips >= 1.5 * busTrips
    # To avoid floating point inaccuracies in integer programming, we multiply by 2:
    # i.e., 2*carTrips >= 3*busTrips

    # Decision Variables: Integers >= 0.
    bus_trips = solver.IntVar(0, solver.infinity(), 'NumberOfBusTrips')
    car_trips = solver.IntVar(0, solver.infinity(), 'NumberOfCarTrips')

    # Constraints

    # 1. Chicken transportation constraint:
    #    bus_capacity * bus_trips + car_capacity * car_trips == total_chickens
    solver.Add(bus_capacity * bus_trips + car_capacity * car_trips == total_chickens)

    # 2. Bus trips limit:
    solver.Add(bus_trips <= max_bus_trips)

    # 3. Car trips ratio constraint: car_trips >= 1.5 * bus_trips
    #    Multiply by 2 to avoid fractions: 2 * car_trips >= 3 * bus_trips
    solver.Add(2 * car_trips >= 3 * bus_trips)

    # Objective: Minimize TotalTime = bus_duration * bus_trips + car_duration * car_trips
    objective = solver.Objective()
    objective.SetCoefficient(bus_trips, bus_duration)
    objective.SetCoefficient(car_trips, car_duration)
    objective.SetMinimization()

    status = solver.Solve()

    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        bus_val = bus_trips.solution_value()
        car_val = car_trips.solution_value()
        obj_val = objective.Value()
        result = {
            "variables": {
                "NumberOfBusTrips": int(round(bus_val)),
                "NumberOfCarTrips": int(round(car_val))
            },
            "objective": obj_val
        }
    else:
        result = {"error": "The problem does not have an optimal solution."}
    return result

def main():
    # We have one formulation provided. We call only one implementation.
    linear_result = solve_with_linear_solver()
    
    # Prepare the structured output for the implemented approach.
    final_output = {
        "LinearSolver_Model": linear_result
    }
    print(final_output)

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
{'LinearSolver_Model': {'variables': {'NumberOfBusTrips': 6, 'NumberOfCarTrips': 15}, 'objective': 34.5}}
'''

'''Expected Output:
Expected solution

: {'variables': {'NumberOfBusTrips': 7.0, 'NumberOfCarTrips': 13.0}, 'objective': 33.5}'''

