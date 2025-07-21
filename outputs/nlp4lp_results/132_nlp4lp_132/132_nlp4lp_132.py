# Problem Description:
'''Problem description: A shoe company supplies shoes to stores via vans and trucks. A van can transport 50 pairs of shoes while a truck can transport 100 pairs of shoes. The company must supply a minimum of 2000 pairs of shoes around the city. Since most stores are small, the number of trucks used cannot exceed the number of vans used.  Find the minimum number of vans that can be used?

Expected Output Schema:
{
  "variables": {
    "NumberOfVans": "float",
    "NumberOfTrucks": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- VehicleTypes: set of vehicle types = {Van, Truck}

Parameters:
- van_capacity: capacity of a van in pairs of shoes = 50 pairs
- truck_capacity: capacity of a truck in pairs of shoes = 100 pairs
- minimum_supply: minimum number of pairs of shoes that must be supplied = 2000 pairs

Variables:
- NumberOfVans: number of vans used [integer, ≥ 0]
- NumberOfTrucks: number of trucks used [integer, ≥ 0]

Objective:
- Minimize NumberOfVans  
  (The goal is to use as few vans as possible while meeting the supply requirement.)

Constraints:
1. Supply Constraint:  
   van_capacity * NumberOfVans + truck_capacity * NumberOfTrucks ≥ minimum_supply  
   (This ensures the total number of shoes transported meets or exceeds 2000 pairs.)
2. Vehicle Balance Constraint:  
   NumberOfTrucks ≤ NumberOfVans  
   (This ensures that the number of trucks used does not exceed the number of vans used.)'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp
from ortools.sat.python import cp_model

def solve_with_linear_solver():
    # Create linear solver instance using CBC backend for mixed integer programming.
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Solver not found.")
        return None

    # Parameters
    van_capacity = 50
    truck_capacity = 100
    minimum_supply = 2000

    # Variables: integers >= 0
    NumberOfVans = solver.IntVar(0, solver.infinity(), 'NumberOfVans')
    NumberOfTrucks = solver.IntVar(0, solver.infinity(), 'NumberOfTrucks')

    # Constraints:
    # 1. Supply constraint: 50 * vans + 100 * trucks >= 2000
    solver.Add(van_capacity * NumberOfVans + truck_capacity * NumberOfTrucks >= minimum_supply)
    # 2. Vehicle balance constraint: trucks <= vans
    solver.Add(NumberOfTrucks <= NumberOfVans)

    # Objective: Minimize NumberOfVans
    objective = solver.Objective()
    objective.SetCoefficient(NumberOfVans, 1)
    objective.SetMinimization()

    # Solve
    status = solver.Solve()

    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result['NumberOfVans'] = NumberOfVans.solution_value()
        result['NumberOfTrucks'] = NumberOfTrucks.solution_value()
        result['objective'] = NumberOfVans.solution_value()
    else:
        result['error'] = "No optimal solution found using linear solver."
    return result

def solve_with_cp_model():
    # Create the CP-SAT model.
    model = cp_model.CpModel()

    # Parameters
    van_capacity = 50
    truck_capacity = 100
    minimum_supply = 2000

    # Variables:
    # CP-SAT requires bounds, we set an arbitrary high upper bound
    max_vehicles = 1000  # arbitrary high bound, sufficient for this problem
    NumberOfVans = model.NewIntVar(0, max_vehicles, 'NumberOfVans')
    NumberOfTrucks = model.NewIntVar(0, max_vehicles, 'NumberOfTrucks')

    # Constraints:
    # 1. Supply constraint: 50 * vans + 100 * trucks >= 2000
    model.Add(van_capacity * NumberOfVans + truck_capacity * NumberOfTrucks >= minimum_supply)
    # 2. Vehicle balance constraint: trucks <= vans
    model.Add(NumberOfTrucks <= NumberOfVans)

    # Objective: Minimize NumberOfVans
    model.Minimize(NumberOfVans)

    # Solve the model.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    result = {}
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        result['NumberOfVans'] = solver.Value(NumberOfVans)
        result['NumberOfTrucks'] = solver.Value(NumberOfTrucks)
        result['objective'] = solver.Value(NumberOfVans)
    else:
        result['error'] = "No optimal solution found using CP-SAT model."
    return result

def main():
    # Solve using linear solver implementation
    linear_result = solve_with_linear_solver()
    
    # Solve using CP-SAT model implementation
    cp_model_result = solve_with_cp_model()
    
    # Print results in a structured way:
    print("Results using OR-Tools Linear Solver:")
    if linear_result and not linear_result.get('error'):
        print("  NumberOfVans: ", linear_result['NumberOfVans'])
        print("  NumberOfTrucks: ", linear_result['NumberOfTrucks'])
        print("  Objective (Min NumberOfVans): ", linear_result['objective'])
    else:
        print("  ", linear_result.get('error', 'Unknown error.'))
    
    print("\nResults using OR-Tools CP-SAT Model:")
    if cp_model_result and not cp_model_result.get('error'):
        print("  NumberOfVans: ", cp_model_result['NumberOfVans'])
        print("  NumberOfTrucks: ", cp_model_result['NumberOfTrucks'])
        print("  Objective (Min NumberOfVans): ", cp_model_result['objective'])
    else:
        print("  ", cp_model_result.get('error', 'Unknown error.'))

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Results using OR-Tools Linear Solver:
  NumberOfVans:  14.0
  NumberOfTrucks:  13.0
  Objective (Min NumberOfVans):  14.0

Results using OR-Tools CP-SAT Model:
  NumberOfVans:  14
  NumberOfTrucks:  13
  Objective (Min NumberOfVans):  14
'''

'''Expected Output:
Expected solution

: {'variables': {'NumberOfVans': 14.0, 'NumberOfTrucks': 14.0}, 'objective': 14.0}'''

