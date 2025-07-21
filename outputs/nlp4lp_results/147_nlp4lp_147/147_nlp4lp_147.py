# Problem Description:
'''Problem description: A mail delivery service in an island village delivers mail by regular and speed boats. A regular boat can carry 20 pieces of mail per trip and uses 10 liters of gas. A speed boat can carry 30 pieces of mail per trip and uses 20 liters of gas. There can be at most 20 regular boat trips. Since customers want their mail as fast as possible, at least 50% of the trips must be made by speed boats. If the service needs to deliver 1000 pieces of mail, how many trips of each should be made to minimize the total amount of gas consumed?

Expected Output Schema:
{
  "variables": {
    "RegularBoatTrips": "float",
    "SpeedBoatTrips": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- BoatTypes: {Regular, Speed}

Parameters:
- mailCapacity_Regular: Number of mail pieces that a regular boat carries per trip = 20 [pieces per trip]
- mailCapacity_Speed: Number of mail pieces that a speed boat carries per trip = 30 [pieces per trip]
- gasConsumption_Regular: Gas used by a regular boat per trip = 10 [liters per trip]
- gasConsumption_Speed: Gas used by a speed boat per trip = 20 [liters per trip]
- maxRegularTrips: Maximum allowable trips using a regular boat = 20 [trips]
- totalMailRequired: Total mail pieces to be delivered = 1000 [pieces]
- minSpeedTripsFraction: Minimum fraction of trips that must be done by speed boats = 0.5 [fraction]

Variables:
- RegularBoatTrips: Number of trips made by regular boats, defined as a nonnegative integer [trips]
- SpeedBoatTrips: Number of trips made by speed boats, defined as a nonnegative integer [trips]

Objective:
- Minimize total gas consumption = (gasConsumption_Regular * RegularBoatTrips) + (gasConsumption_Speed * SpeedBoatTrips)  
  (Units: liters)

Constraints:
1. Mail delivery requirement:
   (mailCapacity_Regular * RegularBoatTrips) + (mailCapacity_Speed * SpeedBoatTrips) >= totalMailRequired

2. Regular boat trip limit:
   RegularBoatTrips <= maxRegularTrips

3. Minimum speed boat trips requirement:
   SpeedBoatTrips >= minSpeedTripsFraction * (RegularBoatTrips + SpeedBoatTrips)
   (This can be rearranged to: SpeedBoatTrips >= RegularBoatTrips)

4. Domain restrictions:
   RegularBoatTrips >= 0 and integer  
   SpeedBoatTrips >= 0 and integer

---------------------------
Expected Output Schema:
{
  "variables": {
    "RegularBoatTrips": "integer (>= 0)",
    "SpeedBoatTrips": "integer (>= 0)"
  },
  "objective": "Minimize total gas consumption in liters = 10 * RegularBoatTrips + 20 * SpeedBoatTrips"
}'''

# Generated Code:
from ortools.linear_solver import pywraplp

def solve_model_formulation():
    # Create the mip solver with the SCIP backend.
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        print("Solver not created.")
        return {}

    # Parameters
    mailCapacity_Regular = 20    # pieces per trip
    mailCapacity_Speed = 30      # pieces per trip
    gasConsumption_Regular = 10  # liters per trip
    gasConsumption_Speed = 20    # liters per trip
    maxRegularTrips = 20         # trips
    totalMailRequired = 1000     # pieces
    # Since at least 50% of the trips must be speed boat trips,
    # the math reformulation SpeedBoatTrips >= 0.5*(RegularBoatTrips + SpeedBoatTrips)
    # is equivalent to: SpeedBoatTrips >= RegularBoatTrips

    # Variables:
    # RegularBoatTrips: integer >= 0 (with an upper bound per regular trips limit)
    # SpeedBoatTrips: integer >= 0
    RegularBoatTrips = solver.IntVar(0, maxRegularTrips, 'RegularBoatTrips')
    SpeedBoatTrips = solver.IntVar(0, solver.infinity(), 'SpeedBoatTrips')

    # Constraint 1: Mail delivery requirement.
    solver.Add(mailCapacity_Regular * RegularBoatTrips + mailCapacity_Speed * SpeedBoatTrips >= totalMailRequired)

    # Constraint 2: Regular boat trip limit is implicitly enforced by variable domain (<= maxRegularTrips).

    # Constraint 3: At least 50% of all trips must be done by speed boats, reformulated as:
    solver.Add(SpeedBoatTrips >= RegularBoatTrips)

    # Objective: Minimize total gas consumption.
    objective = solver.Objective()
    objective.SetCoefficient(RegularBoatTrips, gasConsumption_Regular)
    objective.SetCoefficient(SpeedBoatTrips, gasConsumption_Speed)
    objective.SetMinimization()

    result_status = solver.Solve()

    result = {}
    if result_status == pywraplp.Solver.OPTIMAL:
        result["RegularBoatTrips"] = int(RegularBoatTrips.solution_value())
        result["SpeedBoatTrips"] = int(SpeedBoatTrips.solution_value())
        result["objective"] = objective.Value()
        print("Optimal solution using formulation:")
        print("RegularBoatTrips =", result["RegularBoatTrips"])
        print("SpeedBoatTrips =", result["SpeedBoatTrips"])
        print("Total gas consumption (liters) =", result["objective"])
    else:
        print("The problem does not have an optimal solution.")

    return result

def main():
    # Since the formulation provided is unique, we use one model implementation.
    formulation_result = solve_model_formulation()
    # You could add more formulations here if required by the problem statement.
    # Here we print the results in a structured manner.
    if formulation_result:
        print("\nStructured Output:")
        print({
            "variables": {
                "RegularBoatTrips": "integer (>= 0)",
                "SpeedBoatTrips": "integer (>= 0)"
            },
            "objective": "Minimize total gas consumption in liters = 10 * RegularBoatTrips + 20 * SpeedBoatTrips"
        })

if __name__ == "__main__":
    main()

'''Execution Results:
SUCCESS:
Optimal solution using formulation:
RegularBoatTrips = 20
SpeedBoatTrips = 20
Total gas consumption (liters) = 600.0

Structured Output:
{'variables': {'RegularBoatTrips': 'integer (>= 0)', 'SpeedBoatTrips': 'integer (>= 0)'}, 'objective': 'Minimize total gas consumption in liters = 10 * RegularBoatTrips + 20 * SpeedBoatTrips'}
'''

'''Expected Output:
Expected solution

: {'variables': {'RegularBoatTrips': 20.0, 'SpeedBoatTrips': 20.0}, 'objective': 600.0}'''

