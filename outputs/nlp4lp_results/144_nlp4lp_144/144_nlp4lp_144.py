# Problem Description:
'''Problem description: A theme park transports its visitors around the park either by scooter or rickshaw. A scooter can carry 2 people while a rickshaw can carry 3 people. To avoid excessive pollution, at most 40% of the vehicles used can be rickshaws. If the park needs to transport at least 300 visitors, minimize the total number of scooters used.

Expected Output Schema:
{
  "variables": {
    "NumScooters": "float",
    "NumRickshaws": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- V: set of vehicle types = {Scooter, Rickshaw}  
  (Note: Though vehicles have different capacities, we separate them by type.)

Parameters:
- capacity_Scooter: passenger capacity of one scooter = 2 visitors per scooter  
- capacity_Rickshaw: passenger capacity of one rickshaw = 3 visitors per rickshaw  
- min_passengers: minimum number of visitors to transport = 300 visitors  
- max_rickshaw_fraction: maximum fraction of vehicles that can be rickshaws = 0.40 (or 40%)

Variables:
- NumScooters: number of scooters to deploy [continuous integer variable; units: vehicles]  
- NumRickshaws: number of rickshaws to deploy [continuous integer variable; units: vehicles]

Objective:
- Minimize NumScooters  
  (Interpretation: The goal is to reduce the number of scooters used while still transporting at least 300 visitors and observing the pollution constraint on rickshaws.)

Constraints:
1. Passenger Capacity Constraint:  
   (capacity_Scooter * NumScooters) + (capacity_Rickshaw * NumRickshaws) ≥ min_passengers  
   (Ensures that at least 300 visitors are transported.)

2. Rickshaw Ratio Constraint:  
   NumRickshaws ≤ max_rickshaw_fraction * (NumScooters + NumRickshaws)  
   (Ensures that at most 40% of all vehicles are rickshaws.)

Comments:
- All units are assumed consistent in visitors per vehicle and vehicles count.  
- Decision variables are assumed to be integers. If fractional vehicles are not allowed in implementation, the variable type should be set to integer.  
- The objective solely minimizes the number of scooters used, which indirectly encourages maximizing the use of rickshaws without breaching the rickshaw fraction limit.'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_model():
    # Create the MIP solver with the CBC backend.
    solver = pywraplp.Solver.CreateSolver('CBC_MIXED_INTEGER_PROGRAMMING')
    if not solver:
        print("Solver not created.")
        return None

    # Problem Parameters
    capacity_scooter = 2      # capacity of one scooter
    capacity_rickshaw = 3     # capacity of one rickshaw
    min_passengers = 300      # minimum visitors to transport
    # max_rickshaw_fraction: at most 40% of total vehicles can be rickshaws
    # This constraint: NumRickshaws <= 0.4*(NumScooters + NumRickshaws)
    # is equivalent to: 3 * NumRickshaws <= 2 * NumScooters

    # Decision Variables: these are integer variables representing number of vehicles.
    NumScooters = solver.IntVar(0, solver.infinity(), 'NumScooters')
    NumRickshaws = solver.IntVar(0, solver.infinity(), 'NumRickshaws')

    # Constraint 1: Passenger Capacity Constraint
    # (capacity_scooter * NumScooters) + (capacity_rickshaw * NumRickshaws) >= min_passengers
    solver.Add(capacity_scooter * NumScooters + capacity_rickshaw * NumRickshaws >= min_passengers)

    # Constraint 2: Rickshaw Ratio Constraint
    # Transform: NumRickshaws <= 0.4*(NumScooters + NumRickshaws)
    # which simplifies to: 0.6*NumRickshaws <= 0.4*NumScooters
    # Multiply by 5 to avoid fractions: 3*NumRickshaws <= 2*NumScooters
    solver.Add(3 * NumRickshaws <= 2 * NumScooters)

    # Objective: Minimize the number of scooters
    objective = solver.Objective()
    objective.SetCoefficient(NumScooters, 1)
    objective.SetMinimization()

    # Solve the model
    status = solver.Solve()

    # Prepare output in the desired schema.
    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result["variables"] = {
            "NumScooters": NumScooters.solution_value(),
            "NumRickshaws": NumRickshaws.solution_value()
        }
        result["objective"] = objective.Value()
    elif status == pywraplp.Solver.FEASIBLE:
        result["message"] = "A feasible solution was found, but it may not be optimal."
        result["variables"] = {
            "NumScooters": NumScooters.solution_value(),
            "NumRickshaws": NumRickshaws.solution_value()
        }
        result["objective"] = objective.Value()
    else:
        result["message"] = "The problem does not have a feasible solution."

    return result

def main():
    # Since only one formulation is given, we implement the single model.
    result_model_1 = solve_model()
    
    # Print the results for the model in a structured way.
    print("Results for Model 1 (Linear/MIP formulation):")
    if result_model_1 is not None:
        for key, value in result_model_1.items():
            print(f"{key}: {value}")
    else:
        print("No result returned from the model.")

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Results for Model 1 (Linear/MIP formulation):
variables: {'NumScooters': 75.0, 'NumRickshaws': 50.0}
objective: 75.0
'''

'''Expected Output:
Expected solution

: {'variables': {'NumScooters': 0.0, 'NumRickshaws': 2000000000.0}, 'objective': 0.0}'''

