# Problem Description:
'''Problem description: A village delivers mail to nearby villages either by runners or canoers. Runners can carry three bags of mail each time and takes 4 hours. Canoers can carry ten bags of mail each time and takes 2 hours. At most 33% of deliveries can be by canoe. Additionally, the village can spare at most 200 total hours and at least 4 runners must be used. How many of each way to deliver must be used to maximize the total amount of mail that can be delivered?

Expected Output Schema:
{
  "variables": {
    "NumRunnerTrips": "float",
    "NumCanoeTrips": "float",
    "NumberOfRunners": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Below is one complete formulation that faithfully translates the problem into a structured five‐element model.

--------------------------------------------------

Sets:
• DeliveryModes = {Runner, Canoe}
  (This set distinguishes the two types of delivery methods.)

Parameters:
• bag_capacity_runner = 3                [mail bags per runner trip]
• bag_capacity_canoe = 10                [mail bags per canoe trip]
• time_runner_trip = 4                   [hours per runner trip]
• time_canoe_trip = 2                    [hours per canoe trip]
• max_total_time = 200                   [total available delivery hours]
• max_canoe_fraction = 0.33              [maximum fraction of trips that may be by canoe]
• min_runners = 4                        [minimum number of distinct runners required]
• Note: We assume that each runner makes a single trip. (Alternatively, if runners can make multiple trips then a linking constraint between trips and number of runners would be needed. For this model we assume one trip per runner so that NumberOfRunners equals the number of runner trips.)

Variables:
• NumRunnerTrips: integer ≥ 0  
  (Number of trips made on foot by runners)
• NumCanoeTrips: integer ≥ 0  
  (Number of trips made by canoe)
• NumberOfRunners: integer ≥ 0  
  (Number of distinct runners employed; will be forced to be at least min_runners)

Objective:
• Maximize TotalMailDelivered = bag_capacity_runner * NumRunnerTrips + bag_capacity_canoe * NumCanoeTrips  
  [mail bags delivered]

Constraints:
1. Total time available:
   time_runner_trip * NumRunnerTrips + time_canoe_trip * NumCanoeTrips ≤ max_total_time

2. Canoe delivery fraction:
   NumCanoeTrips ≤ max_canoe_fraction * (NumRunnerTrips + NumCanoeTrips)
   (This ensures that at most 33% of all deliveries are by canoe.)

3. Minimum number of runners:
   NumberOfRunners ≥ min_runners

4. Linking runners and runner trips (based on the assumption that each runner can only make one trip):
   NumRunnerTrips ≤ NumberOfRunners
   (If, in another formulation, runners can make multiple trips then a different linking constraint would be required.)

--------------------------------------------------

The expected output schema (using the variable names defined above) is:

{
  "variables": {
    "NumRunnerTrips": "integer, number of trips by runners",
    "NumCanoeTrips": "integer, number of trips by canoe",
    "NumberOfRunners": "integer, number of distinct runners used (must be at least 4)"
  },
  "objective": "Maximize TotalMailDelivered = 3 * NumRunnerTrips + 10 * NumCanoeTrips"
}

This structured model is self-contained and can be implemented in a working optimization code.'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_model_single_trip_per_runner():
    """Model 1: Each runner makes exactly one trip.
    Here we force NumberOfRunners == NumRunnerTrips.
    """
    # Create solver
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        return None

    # Parameters
    bag_capacity_runner = 3
    bag_capacity_canoe = 10
    time_runner_trip = 4
    time_canoe_trip = 2
    max_total_time = 200
    max_canoe_fraction = 0.33
    min_runners = 4

    # Decision variables:
    # NumRunnerTrips: integer ≥ 0
    runner_trips = solver.IntVar(0, solver.infinity(), 'NumRunnerTrips')
    # NumCanoeTrips: integer ≥ 0
    canoe_trips = solver.IntVar(0, solver.infinity(), 'NumCanoeTrips')
    # NumberOfRunners: integer ≥ 0
    num_runners = solver.IntVar(0, solver.infinity(), 'NumberOfRunners')

    # Constraint 1: Total time available.
    solver.Add(time_runner_trip * runner_trips + time_canoe_trip * canoe_trips <= max_total_time)

    # Constraint 2: Canoe delivery fraction.
    # To model: canoe_trips <= max_canoe_fraction * (runner_trips + canoe_trips)
    # Rearranged: canoe_trips - max_canoe_fraction*(runner_trips + canoe_trips) <= 0
    # => canoe_trips*(1 - max_canoe_fraction) - max_canoe_fraction*runner_trips <= 0
    solver.Add((1 - max_canoe_fraction)*canoe_trips - max_canoe_fraction * runner_trips <= 0)

    # Constraint 3: Minimum number of runners.
    solver.Add(num_runners >= min_runners)

    # Constraint 4: Linking constraint (single trip per runner):
    # Force NumberOfRunners to equal the number of runner trips.
    solver.Add(num_runners == runner_trips)

    # Objective: Maximize total mail delivered.
    # TotalMailDelivered = 3*NumRunnerTrips + 10*NumCanoeTrips
    objective = solver.Objective()
    objective.SetCoefficient(runner_trips, bag_capacity_runner)
    objective.SetCoefficient(canoe_trips, bag_capacity_canoe)
    objective.SetMaximization()

    status = solver.Solve()

    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result['model'] = 'Single Trip per Runner'
        result['objective'] = objective.Value()
        result['variables'] = {
            'NumRunnerTrips': runner_trips.solution_value(),
            'NumCanoeTrips': canoe_trips.solution_value(),
            'NumberOfRunners': num_runners.solution_value()
        }
    else:
        result['model'] = 'Single Trip per Runner'
        result['status'] = 'No optimal solution found.'
    return result

def solve_model_multiple_trips_per_runner():
    """Model 2: Runners can make multiple trips.
    Here NumberOfRunners is independent (except for the minimum requirement) and
    we add a linking constraint forcing that the total runner trips do not
    exceed the capacity of the hired runners. We assume a maximum trips per runner.
    """
    # Create solver
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        return None

    # Parameters
    bag_capacity_runner = 3
    bag_capacity_canoe = 10
    time_runner_trip = 4
    time_canoe_trip = 2
    max_total_time = 200
    max_canoe_fraction = 0.33
    min_runners = 4
    # Assume a runner can work at most this many trips
    max_trips_per_runner = 50  # since 200/4 = 50, a runner working alone can run 50 trips

    # Decision variables:
    # NumRunnerTrips: integer ≥ 0
    runner_trips = solver.IntVar(0, solver.infinity(), 'NumRunnerTrips')
    # NumCanoeTrips: integer ≥ 0
    canoe_trips = solver.IntVar(0, solver.infinity(), 'NumCanoeTrips')
    # NumberOfRunners: integer ≥ 0
    num_runners = solver.IntVar(0, solver.infinity(), 'NumberOfRunners')

    # Constraint 1: Total time available.
    solver.Add(time_runner_trip * runner_trips + time_canoe_trip * canoe_trips <= max_total_time)

    # Constraint 2: Canoe delivery fraction.
    # canoe_trips <= max_canoe_fraction*(runner_trips+canoe_trips)
    solver.Add((1 - max_canoe_fraction)*canoe_trips - max_canoe_fraction * runner_trips <= 0)

    # Constraint 3: Minimum number of runners.
    solver.Add(num_runners >= min_runners)

    # Constraint 4: Linking runners and runner trips in a multiple-trip setting.
    # A hired runner can make at most max_trips_per_runner trips.
    solver.Add(runner_trips <= num_runners * max_trips_per_runner)

    # Objective: Maximize total mail delivered.
    objective = solver.Objective()
    objective.SetCoefficient(runner_trips, bag_capacity_runner)
    objective.SetCoefficient(canoe_trips, bag_capacity_canoe)
    objective.SetMaximization()

    status = solver.Solve()

    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result['model'] = 'Multiple Trips per Runner'
        result['objective'] = objective.Value()
        result['variables'] = {
            'NumRunnerTrips': runner_trips.solution_value(),
            'NumCanoeTrips': canoe_trips.solution_value(),
            'NumberOfRunners': num_runners.solution_value()
        }
    else:
        result['model'] = 'Multiple Trips per Runner'
        result['status'] = 'No optimal solution found.'
    return result

def main():
    # Solve the two models and print results in a structured way
    results = []
    
    result1 = solve_model_single_trip_per_runner()
    if result1:
        results.append(result1)
    result2 = solve_model_multiple_trips_per_runner()
    if result2:
        results.append(result2)
    
    # Print results
    print("Optimization Results:")
    for res in results:
        print("\nModel: {}".format(res.get('model', '')))
        if 'status' in res:
            print("Status: {}".format(res['status']))
        else:
            print("Objective Value: {}".format(res['objective']))
            print("Variables:")
            for var, val in res['variables'].items():
                print("  {} = {}".format(var, val))

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Optimization Results:

Model: Single Trip per Runner
Objective Value: 310.0
Variables:
  NumRunnerTrips = 40.0
  NumCanoeTrips = 19.0
  NumberOfRunners = 40.0

Model: Multiple Trips per Runner
Objective Value: 310.0
Variables:
  NumRunnerTrips = 40.0
  NumCanoeTrips = 19.0
  NumberOfRunners = 4.0
'''

'''Expected Output:
Expected solution

: {'variables': {'NumRunnerTrips': 47.0, 'NumCanoeTrips': 6.0, 'NumberOfRunners': 4.0}, 'objective': 201.0}'''

