# Problem Description:
'''Problem description: The weather is freezing and the fish in the pond need to be transported either by helicopter or car. A helicopter can take 30 fish per trip and takes 40 minutes. A car can take 20 fish per trip and takes 30 minutes. Since helicopter trips are expensive, there can be at most 5 helicopter trips. In addition, at least 60% of the trips should be by car. If at least 300 fish need to transported, how many of each trip should be taken to minimize the total time needed?

Expected Output Schema:
{
  "variables": {
    "HelicopterTrips": "float",
    "CarTrips": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- Trips: the set of trip modes = {Helicopter, Car} (Note: each mode has its own characteristics)

Parameters:
- Helicopter_Capacity = 30 (fish per helicopter trip)
- Car_Capacity = 20 (fish per car trip)
- Helicopter_Time = 40 (minutes per helicopter trip)
- Car_Time = 30 (minutes per car trip)
- Max_Helicopter_Trips = 5 (maximum number of helicopter trips allowed)
- Min_Fish_Transport = 300 (minimum number of fish to transport)
- Min_Car_Trip_Fraction = 0.60 (at least 60% of total trips must be by car)

Variables:
- HelicopterTrips: number of helicopter trips (integer, ≥ 0)
- CarTrips: number of car trips (integer, ≥ 0)

Objective:
- Minimize Total_Time = Helicopter_Time * HelicopterTrips + Car_Time * CarTrips  
  (minutes; this represents the total transportation time)

Constraints:
1. Fish Transport Requirement:  
   Helicopter_Capacity * HelicopterTrips + Car_Capacity * CarTrips ≥ Min_Fish_Transport

2. Helicopter Trip Limit:  
   HelicopterTrips ≤ Max_Helicopter_Trips

3. Minimum Car Trip Proportion:  
   Since at least 60% of all trips must be by car, we require:  
   CarTrips ≥ Min_Car_Trip_Fraction * (HelicopterTrips + CarTrips)  
   This can be rearranged to: CarTrips ≥ 1.5 * HelicopterTrips

Notes:
- Units are consistent: fish counts for capacities and total fish, minutes for trip times.
- Although trips are typically integer quantities, they are defined here as integer decision variables.
- The reformulated constraint for car trips (CarTrips ≥ 1.5 * HelicopterTrips) ensures that the proportion of car trips is at least 60% of all trips.

Expected Output Schema:
{
  "variables": {
    "HelicopterTrips": "float",
    "CarTrips": "float"
  },
  "objective": "float"
}'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp
from ortools.sat.python import cp_model

def solve_with_linear_solver():
    # Create the MIP solver using SCIP backend.
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        print("Linear Solver not available.")
        return None

    # PARAMETERS
    Helicopter_Capacity = 30
    Car_Capacity = 20
    Helicopter_Time = 40
    Car_Time = 30
    Max_Helicopter_Trips = 5
    Min_Fish_Transport = 300
    Min_Car_Trip_Fraction = 0.60  # i.e., CarTrips >= 1.5 * HelicopterTrips

    infinity = solver.infinity()

    # VARIABLES: Integer trips, with HelicopterTrips bounded by the maximum allowed.
    HelicopterTrips = solver.IntVar(0, Max_Helicopter_Trips, 'HelicopterTrips')
    CarTrips = solver.IntVar(0, infinity, 'CarTrips')

    # CONSTRAINT 1: Fish Transport Requirement
    # 30*HelicopterTrips + 20*CarTrips >= 300
    solver.Add(Helicopter_Capacity * HelicopterTrips + Car_Capacity * CarTrips >= Min_Fish_Transport)

    # CONSTRAINT 2: Helicopter Trip Limit (already enforced by variable bound)

    # CONSTRAINT 3: Minimum Car Trip Proportion
    # CarTrips >= 1.5 * HelicopterTrips
    solver.Add(CarTrips >= 1.5 * HelicopterTrips)

    # OBJECTIVE: Minimize total time: 40*HelicopterTrips + 30*CarTrips
    solver.Minimize(Helicopter_Time * HelicopterTrips + Car_Time * CarTrips)

    status = solver.Solve()

    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "variables": {
                "HelicopterTrips": HelicopterTrips.solution_value(),
                "CarTrips": CarTrips.solution_value()
            },
            "objective": solver.Objective().Value()
        }
    else:
        result = {"error": "No optimal solution found using the linear solver."}
    return result

def solve_with_cp_model():
    # Create the CP-SAT model.
    model = cp_model.CpModel()

    # PARAMETERS
    Helicopter_Capacity = 30
    Car_Capacity = 20
    Helicopter_Time = 40
    Car_Time = 30
    Max_Helicopter_Trips = 5
    Min_Fish_Transport = 300
    # For CP-SAT, we eliminate fractional constraint by multiplying by 2:
    # Original: CarTrips >= 1.5 * HelicopterTrips  is equivalent to: 2*CarTrips >= 3*HelicopterTrips

    # VARIABLES: Using integer decision variables.
    HelicopterTrips = model.NewIntVar(0, Max_Helicopter_Trips, 'HelicopterTrips')
    # Reasonable upper bound for CarTrips can be computed from fish requirement: all by car => CarTrips = ceil(300/20)=15, plus a margin.
    CarTrips = model.NewIntVar(0, 1000, 'CarTrips')

    # CONSTRAINT 1: Fish Transport Requirement
    # 30*HelicopterTrips + 20*CarTrips >= 300
    model.Add(Helicopter_Capacity * HelicopterTrips + Car_Capacity * CarTrips >= Min_Fish_Transport)

    # CONSTRAINT 2: Helicopter Trip Limit is enforced on HelicopterTrips

    # CONSTRAINT 3: Minimum Car Trip Proportion rewritten as: 2*CarTrips >= 3*HelicopterTrips
    model.Add(2 * CarTrips >= 3 * HelicopterTrips)

    # OBJECTIVE: Minimize total time: 40*HelicopterTrips + 30*CarTrips
    objective_var = model.NewIntVar(0, 10000, 'total_time')
    model.Add(objective_var == Helicopter_Time * HelicopterTrips + Car_Time * CarTrips)
    model.Minimize(objective_var)

    # Solve the model.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    result = {}
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        result = {
            "variables": {
                "HelicopterTrips": solver.Value(HelicopterTrips),
                "CarTrips": solver.Value(CarTrips)
            },
            "objective": solver.Value(objective_var)
        }
    else:
        result = {"error": "No optimal solution found using the CP-SAT model."}
    return result

def main():
    # Solve using linear solver implementation.
    linear_result = solve_with_linear_solver()
    # Solve using CP-SAT model implementation.
    cp_result = solve_with_cp_model()

    # Present the results in a structured way.
    final_result = {
        "LinearSolver": linear_result,
        "CPSAT": cp_result
    }
    print(final_result)

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
{'LinearSolver': {'variables': {'HelicopterTrips': 4.0, 'CarTrips': 9.0}, 'objective': 430.0}, 'CPSAT': {'variables': {'HelicopterTrips': 4, 'CarTrips': 9}, 'objective': 430}}
'''

'''Expected Output:
Expected solution

: {'variables': {'HelicopterTrips': 4.0, 'CarTrips': 9.0}, 'objective': 430.0}'''

