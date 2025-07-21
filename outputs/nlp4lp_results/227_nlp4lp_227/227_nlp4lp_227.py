# Problem Description:
'''Problem description: Due to an accident, at least 550 locals must be moved across a lake. They can either be transported over the lake by a kayak or a motorboat. Kayaks can transport 4 people every trip and motorboats can transport 5 people every trip. Kayaks take 5 minutes per trip whereas motorboats take 3 minutes per trip. Due to the limited number of motorboats available to the locals, there can be at most 25 motorboat trips and at least 75% of the trips should be by kayak. How many of each transportation method should be used to minimize the total amount of time needed to transport all the locals?

Expected Output Schema:
{
  "variables": {
    "KayakTrips": "float",
    "MotorboatTrips": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- T: set of transportation modes = {Kayak, Motorboat}

Parameters:
- PeoplePerKayak: number of people transported per kayak trip = 4 [people/trip]
- PeoplePerMotorboat: number of people transported per motorboat trip = 5 [people/trip]
- TimePerKayak: time taken per kayak trip = 5 [minutes/trip]
- TimePerMotorboat: time taken per motorboat trip = 3 [minutes/trip]
- MinimumLocals: total locals to be transported = 550 [people]
- MaxMotorboatTrips: maximum allowed motorboat trips = 25 [trips]
- MinKayakTripFraction: minimum fraction of trips that must be by kayak = 0.75 [fraction]

Variables:
- KayakTrips: number of kayak trips to operate (integer, nonnegative) [trips]
- MotorboatTrips: number of motorboat trips to operate (integer, nonnegative) [trips]

Objective:
- Minimize TotalTime = (TimePerKayak * KayakTrips) + (TimePerMotorboat * MotorboatTrips) [minutes]

Constraints:
1. Transportation Capacity Constraint:
   (PeoplePerKayak * KayakTrips) + (PeoplePerMotorboat * MotorboatTrips) >= MinimumLocals
   (Ensures that at least 550 locals are moved across the lake.)
2. Motorboat Availability Constraint:
   MotorboatTrips <= MaxMotorboatTrips
   (Due to the limited number of motorboats available.)
3. Kayak Trip Fraction Constraint:
   KayakTrips >= MinKayakTripFraction * (KayakTrips + MotorboatTrips)
   (Ensures that at least 75% of all trips are made by kayak.)

Comments:
- All time units are in minutes, capacities in people per trip, and trip counts are assumed to be integer values.
- The decision variables represent the number of trips to schedule for each transportation mode.
- The Kayak Trip Fraction Constraint can also be algebraically rearranged as KayakTrips >= 3 * MotorboatTrips.
  
This completes the structured mathematical model using the five-element framework.'''

# Generated Code:
from ortools.linear_solver import pywraplp

def solve_model_version1():
    """Model Version 1: Uses the fractional constraint formulation.
    Constraint: KayakTrips >= 0.75 * (KayakTrips + MotorboatTrips)
    """
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Solver not created.")
        return None

    # Decision Variables (integer, non-negative)
    kayak_trips = solver.IntVar(0, solver.infinity(), 'KayakTrips')
    motorboat_trips = solver.IntVar(0, solver.infinity(), 'MotorboatTrips')

    # Parameters
    people_per_kayak = 4
    people_per_motorboat = 5
    time_per_kayak = 5
    time_per_motorboat = 3
    minimum_locals = 550
    max_motorboat_trips = 25

    # Constraints
    # 1. Transportation Capacity Constraint:
    #    4 * KayakTrips + 5 * MotorboatTrips >= 550
    solver.Add(people_per_kayak * kayak_trips + people_per_motorboat * motorboat_trips >= minimum_locals)

    # 2. Motorboat Availability Constraint:
    #    MotorboatTrips <= 25
    solver.Add(motorboat_trips <= max_motorboat_trips)

    # 3. Kayak Trip Fraction Constraint (fraction version):
    #    KayakTrips >= 0.75 * (KayakTrips + MotorboatTrips)
    solver.Add(kayak_trips >= 0.75 * (kayak_trips + motorboat_trips))

    # Objective: Minimize total time = 5 * KayakTrips + 3 * MotorboatTrips
    solver.Minimize(time_per_kayak * kayak_trips + time_per_motorboat * motorboat_trips)

    # Solve model
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "KayakTrips": kayak_trips.solution_value(),
            "MotorboatTrips": motorboat_trips.solution_value(),
            "objective": solver.Objective().Value()
        }
        print("Version 1 (Fractional Constraint) Optimal Solution:")
        print(result)
        return result
    else:
        print("Version 1: No optimal solution found.")
        return None

def solve_model_version2():
    """Model Version 2: Uses the equivalent algebraic constraint.
    Constraint: KayakTrips >= 3 * MotorboatTrips (derived from the fractional version)
    """
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Solver not created.")
        return None

    # Decision Variables (integer, non-negative)
    kayak_trips = solver.IntVar(0, solver.infinity(), 'KayakTrips')
    motorboat_trips = solver.IntVar(0, solver.infinity(), 'MotorboatTrips')

    # Parameters
    people_per_kayak = 4
    people_per_motorboat = 5
    time_per_kayak = 5
    time_per_motorboat = 3
    minimum_locals = 550
    max_motorboat_trips = 25

    # Constraints
    # 1. Transportation Capacity Constraint:
    solver.Add(people_per_kayak * kayak_trips + people_per_motorboat * motorboat_trips >= minimum_locals)

    # 2. Motorboat Availability Constraint:
    solver.Add(motorboat_trips <= max_motorboat_trips)

    # 3. Kayak Trip Fraction Constraint (algebraic version):
    #    KayakTrips >= 3 * MotorboatTrips
    solver.Add(kayak_trips >= 3 * motorboat_trips)

    # Objective: Minimize total time = 5 * KayakTrips + 3 * MotorboatTrips
    solver.Minimize(time_per_kayak * kayak_trips + time_per_motorboat * motorboat_trips)

    # Solve model
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "KayakTrips": kayak_trips.solution_value(),
            "MotorboatTrips": motorboat_trips.solution_value(),
            "objective": solver.Objective().Value()
        }
        print("Version 2 (Algebraic Constraint) Optimal Solution:")
        print(result)
        return result
    else:
        print("Version 2: No optimal solution found.")
        return None

def main():
    print("Running Model Version 1 (Fractional Constraint)...")
    result_v1 = solve_model_version1()
    print("\nRunning Model Version 2 (Algebraic Constraint)...")
    result_v2 = solve_model_version2()

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Running Model Version 1 (Fractional Constraint)...
Version 1 (Fractional Constraint) Optimal Solution:
{'KayakTrips': 107.0, 'MotorboatTrips': 25.0, 'objective': 610.0}

Running Model Version 2 (Algebraic Constraint)...
Version 2 (Algebraic Constraint) Optimal Solution:
{'KayakTrips': 107.0, 'MotorboatTrips': 25.0, 'objective': 610.0}
'''

'''Expected Output:
Expected solution

: {'variables': {'KayakTrips': 107.0, 'MotorboatTrips': 25.0}, 'objective': 610.0}'''

