# Problem Description:
'''Problem description: A candle-making company can move their inventory of candles using freight and air. Freight can transport 5 tons per trip while using air can transport 3 tons per trip. Since freight take longer, the cost for each freight trip is $300 while the cost over air for each trip is $550. The company needs to transport at least 200 tons of candles and they have a budget of $20000. Additionally, due to some urgent orders, at least 30% of tons of candles must be transported through air. There must also be at least 5 trips through freight. How many of trip by each should be scheduled to minimize the total number of trips?

Expected Output Schema:
{
  "variables": {
    "FreightTrips": "float",
    "AirTrips": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Below is a complete formulation of the problem using the five‐element structure.

------------------------------------------------------------
Sets:
- TransportModes: the set of transportation modes = {Freight, Air}

------------------------------------------------------------
Parameters:
- freightCapacity = 5   (tons per freight trip)
- airCapacity = 3       (tons per air trip)
- freightCost = 300     (dollars per freight trip)
- airCost = 550         (dollars per air trip)
- requiredTons = 200    (minimum total tons to transport)
- budget = 20000        (maximum total dollars available for transportation)
- airPercentage = 0.30  (minimum fraction of total tons that must be transported by air)
- minFreightTrips = 5   (minimum number of freight trips to schedule)

------------------------------------------------------------
Variables:
- FreightTrips: number of trips scheduled by freight (integer ≥ 0)
- AirTrips: number of trips scheduled by air (integer ≥ 0)

------------------------------------------------------------
Objective:
Minimize totalTrips = FreightTrips + AirTrips  
(The aim is to minimize the total number of trips scheduled)

------------------------------------------------------------
Constraints:
1. Inventory Transport Constraint (tons requirement):
   (freightCapacity * FreightTrips) + (airCapacity * AirTrips) ≥ requiredTons  
   i.e., 5*FreightTrips + 3*AirTrips ≥ 200

2. Budget Constraint:
   (freightCost * FreightTrips) + (airCost * AirTrips) ≤ budget  
   i.e., 300*FreightTrips + 550*AirTrips ≤ 20000

3. Air Transportation Minimum Percentage Constraint:
   Tons transported by air must be at least airPercentage of total transport:
   airCapacity * AirTrips ≥ airPercentage * [(freightCapacity * FreightTrips) + (airCapacity * AirTrips)]
   i.e., 3*AirTrips ≥ 0.30*(5*FreightTrips + 3*AirTrips)
   (This can be rearranged if needed for implementation.)

4. Minimum Freight Trips Constraint:
   FreightTrips ≥ minFreightTrips  
   i.e., FreightTrips ≥ 5

------------------------------------------------------------
Note:
- All units are consistent: tons for capacity, dollars for cost, and trips (assumed integer) for number of trips.
- Decision variables are integers since the number of trips cannot be fractional.
- In the air percentage constraint, we compare the tons moved by air (3 tons each trip) with 30% of total tons moved by both modes.
 
------------------------------------------------------------
Expected Output Schema:
{
  "variables": {
    "FreightTrips": "integer >= 0",
    "AirTrips": "integer >= 0"
  },
  "objective": "Minimize totalTrips, where totalTrips = FreightTrips + AirTrips"
}'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_linear_model():
    # Create the MIP solver using CBC backend.
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Could not create solver CBC.")
        return None

    # Decision Variables
    FreightTrips = solver.IntVar(0, solver.infinity(), 'FreightTrips')
    AirTrips = solver.IntVar(0, solver.infinity(), 'AirTrips')

    # Parameters
    freightCapacity = 5    # tons per freight trip
    airCapacity = 3        # tons per air trip
    freightCost = 300      # dollars per freight trip
    airCost = 550          # dollars per air trip
    requiredTons = 200     # minimum tons of candles to transport
    budget = 20000         # max dollars available
    airPercentage = 0.30   # minimum fraction of tons by air
    minFreightTrips = 5    # minimum number of freight trips

    # Constraints
    # 1. Inventory Transport Constraint: 5*FreightTrips + 3*AirTrips >= 200
    solver.Add(freightCapacity * FreightTrips + airCapacity * AirTrips >= requiredTons)

    # 2. Budget Constraint: 300*FreightTrips + 550*AirTrips <= 20000
    solver.Add(freightCost * FreightTrips + airCost * AirTrips <= budget)

    # 3. Air Transportation Minimum Percentage:
    #    3*AirTrips >= 0.30 * (5*FreightTrips + 3*AirTrips)
    # Rearranging: 3*AirTrips - 0.30*(3*AirTrips) >= 0.30*5*FreightTrips 
    #             (3 - 0.9)*AirTrips >= 1.5*FreightTrips 
    #             2.1*AirTrips >= 1.5*FreightTrips
    # But we can add the constraint in the original form:
    solver.Add(airCapacity * AirTrips >= airPercentage * (freightCapacity * FreightTrips + airCapacity * AirTrips))
    
    # 4. Minimum Freight Trips: FreightTrips >= 5
    solver.Add(FreightTrips >= minFreightTrips)

    # Objective: Minimize total trips = FreightTrips + AirTrips
    solver.Minimize(FreightTrips + AirTrips)

    # Solve model
    status = solver.Solve()

    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "FreightTrips": FreightTrips.solution_value(),
            "AirTrips": AirTrips.solution_value(),
            "Objective": (FreightTrips.solution_value() + AirTrips.solution_value())
        }
    elif status == pywraplp.Solver.FEASIBLE:
        print("A solution was found, but it might not be optimal.")
        result = {
            "FreightTrips": FreightTrips.solution_value(),
            "AirTrips": AirTrips.solution_value(),
            "Objective": (FreightTrips.solution_value() + AirTrips.solution_value())
        }
    else:
        print("The problem does not have an optimal solution.")
        result = None

    return result

def main():
    results = {}
    
    # Since the problem formulation is unambiguous and only one model is provided,
    # we create one implementation (using the linear solver).
    linear_solution = solve_linear_model()
    
    results["LinearSolverSolution"] = linear_solution
    
    # Print results in structured format.
    if linear_solution:
        print("Linear Solver Optimal Solution:")
        print("FreightTrips =", linear_solution["FreightTrips"])
        print("AirTrips =", linear_solution["AirTrips"])
        print("Total Trips (Objective) =", linear_solution["Objective"])
    else:
        print("No optimal solution found for the linear solver model.")

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Linear Solver Optimal Solution:
FreightTrips = 28.0
AirTrips = 20.0
Total Trips (Objective) = 48.0
'''

'''Expected Output:
Expected solution

: {'variables': {'FreightTrips': 28.0, 'AirTrips': 20.0}, 'objective': 48.0}'''

