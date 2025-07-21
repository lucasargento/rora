# Problem Description:
'''Problem description: A volunteer organization transports voters to the polls on Election Day either by vans or cars. They have vans which can carry 6 people and cars which can carry 3 people.  They need to transport at least 200 voters to the polls. In addition, at most 30% of the vehicles can be vans. How many of each vehicle should be used to minimize the total number of cars used?

Expected Output Schema:
{
  "variables": {
    "NumberOfVans": "float",
    "NumberOfCars": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- V: set of vehicle types = {van, car}

Parameters:
- capacity_van: capacity per van [voters per van] = 6
- capacity_car: capacity per car [voters per car] = 3
- min_voters: minimum number of voters to transport [voters] = 200
- max_fraction_vans: maximum allowed fraction of vans in the fleet [unitless] = 0.30

Variables:
- NumberOfVans: number of vans used [integer ≥ 0]
- NumberOfCars: number of cars used [integer ≥ 0]

Objective:
- Minimize the total number of cars used, i.e., Minimize NumberOfCars

Constraints:
1. Voter Transport Constraint: 
   6 * NumberOfVans + 3 * NumberOfCars ≥ min_voters

2. Vehicle Composition Constraint (at most 30% vans):
   NumberOfVans ≤ max_fraction_vans * (NumberOfVans + NumberOfCars)
   (Alternatively, this constraint can be rearranged as 7 * NumberOfVans ≤ 3 * NumberOfCars.)

Comments:
- All vehicle counts are assumed to be integers. If fractional values are acceptable in a relaxed model, the variables may be considered as nonnegative floats.
- Capacity units are expressed in voters per vehicle.
- The reformulated vehicle composition constraint ensures that vans do not exceed 30% of the total vehicles.

Output as JSON following the expected output schema:
{
  "variables": {
    "NumberOfVans": "float",
    "NumberOfCars": "float"
  },
  "objective": "float"
}'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_model1():
    # Model 1: Using the vehicle composition constraint in its original form:
    # NumberOfVans <= max_fraction_vans * (NumberOfVans + NumberOfCars)
    # with max_fraction_vans = 0.30.
    
    # Create solver instance (CBC Mixed Integer Programming)
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        return None

    # Parameters
    capacity_van = 6
    capacity_car = 3
    min_voters = 200
    max_fraction_vans = 0.30

    # Variables: Non-negative integer variables
    NumberOfVans = solver.IntVar(0, solver.infinity(), 'NumberOfVans')
    NumberOfCars = solver.IntVar(0, solver.infinity(), 'NumberOfCars')

    # Constraint 1: Voter transport constraint
    # 6 * NumberOfVans + 3 * NumberOfCars >= 200
    solver.Add(capacity_van * NumberOfVans + capacity_car * NumberOfCars >= min_voters)

    # Constraint 2: Vehicle Composition Constraint (at most 30% vans)
    # Original formulation: NumberOfVans <= max_fraction_vans * (NumberOfVans + NumberOfCars)
    # This is equivalent to: NumberOfVans - 0.30*NumberOfVans - 0.30*NumberOfCars <= 0  => 0.70*NumberOfVans - 0.30*NumberOfCars <= 0.
    # Add the constraint in a way that avoids fractions:
    # Multiply both sides by 10: 7*NumberOfVans - 3*NumberOfCars <= 0.
    # However, for Model 1 we will add the constraint in its original fractional form.
    solver.Add(NumberOfVans <= max_fraction_vans * (NumberOfVans + NumberOfCars))

    # Objective: Minimize the number of cars used.
    objective = solver.Objective()
    objective.SetCoefficient(NumberOfCars, 1)
    objective.SetMinimization()

    # Solve the optimization problem.
    status = solver.Solve()
    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "NumberOfVans": NumberOfVans.solution_value(),
            "NumberOfCars": NumberOfCars.solution_value(),
            "objective": objective.Value()
        }
    else:
        result = {"error": "The problem does not have an optimal solution."}
    return result

def solve_model2():
    # Model 2: Using the alternative rearranged vehicle composition constraint:
    # 7 * NumberOfVans <= 3 * NumberOfCars
    # which is equivalent to the original constraint.
    
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        return None

    # Parameters
    capacity_van = 6
    capacity_car = 3
    min_voters = 200

    # Variables: Non-negative integer variables
    NumberOfVans = solver.IntVar(0, solver.infinity(), 'NumberOfVans')
    NumberOfCars = solver.IntVar(0, solver.infinity(), 'NumberOfCars')

    # Constraint 1: Voter transport constraint: 6 * NumberOfVans + 3 * NumberOfCars >= 200
    solver.Add(capacity_van * NumberOfVans + capacity_car * NumberOfCars >= min_voters)

    # Constraint 2: Alternative vehicle composition constraint: 7 * NumberOfVans <= 3 * NumberOfCars
    solver.Add(7 * NumberOfVans <= 3 * NumberOfCars)

    # Objective: Minimize the number of cars used.
    objective = solver.Objective()
    objective.SetCoefficient(NumberOfCars, 1)
    objective.SetMinimization()

    # Solve the optimization problem.
    status = solver.Solve()
    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "NumberOfVans": NumberOfVans.solution_value(),
            "NumberOfCars": NumberOfCars.solution_value(),
            "objective": objective.Value()
        }
    else:
        result = {"error": "The problem does not have an optimal solution."}
    return result

def main():
    results = {}
    
    # Solve using Model 1
    model1_result = solve_model1()
    results['Model1'] = model1_result
    
    # Solve using Model 2
    model2_result = solve_model2()
    results['Model2'] = model2_result
    
    # Print the results in a structured way
    import json
    print(json.dumps(results, indent=2))

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
{
  "Model1": {
    "NumberOfVans": 15.0,
    "NumberOfCars": 37.0,
    "objective": 37.0
  },
  "Model2": {
    "NumberOfVans": 15.0,
    "NumberOfCars": 37.0,
    "objective": 37.0
  }
}
'''

'''Expected Output:
Expected solution

: {'variables': {'NumberOfVans': 2000000000.0, 'NumberOfCars': 0.0}, 'objective': 0.0}'''

