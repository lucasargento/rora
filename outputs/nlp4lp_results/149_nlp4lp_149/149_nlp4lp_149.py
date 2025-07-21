# Problem Description:
'''Problem description: Children can go to school either by van or by minibus. A van can take 6 kids and produces 7 units of pollution. A minibus can take 10 kids and produced 10 units of pollution. There are at least 150 kids than need to go to school and at most 10 minibuses can be used. In addition, the number of vans used must exceed the number of minibuses. How many of each should be used to minimize the total amount of pollution produced?

Expected Output Schema:
{
  "variables": {
    "NumberOfVans": "float",
    "NumberOfMinibuses": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- Vehicles: {Van, Minibus}

Parameters:
- VanCapacity: 6 kids per van
- MinibusCapacity: 10 kids per minibus
- VanPollution: 7 pollution units per van
- MinibusPollution: 10 pollution units per minibus
- MinimumKids: 150 kids (total required)
- MaxMinibuses: 10 minibuses (upper limit)

Variables:
- NumberOfVans: integer ≥ 0 (number of vans used)
- NumberOfMinibuses: integer ≥ 0 (number of minibuses used)

Objective:
- Minimize TotalPollution = (VanPollution * NumberOfVans) + (MinibusPollution * NumberOfMinibuses)

Constraints:
1. Kid Transportation Coverage:
   - (VanCapacity * NumberOfVans) + (MinibusCapacity * NumberOfMinibuses) ≥ MinimumKids
2. Limit on Number of Minibuses:
   - NumberOfMinibuses ≤ MaxMinibuses
3. Van Usage Exceeds Minibus Usage:
   - NumberOfVans ≥ NumberOfMinibuses + 1
   
Note:
- The constraint "NumberOfVans ≥ NumberOfMinibuses + 1" replaces the strict inequality "NumberOfVans > NumberOfMinibuses" to ensure integer variable feasibility.
- All pollution and capacity parameters are assumed to be in consistent units (per vehicle).

For clarity, the expected output schema is:
{
  "variables": {
    "NumberOfVans": "integer ≥ 0",
    "NumberOfMinibuses": "integer ≥ 0"
  },
  "objective": "Minimize (7 * NumberOfVans) + (10 * NumberOfMinibuses)"
}'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp
from ortools.sat.python import cp_model

def solve_with_linear_solver():
    # Create the linear solver with CBC backend.
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        return None

    # Parameters
    van_capacity = 6
    minibus_capacity = 10
    van_pollution = 7
    minibus_pollution = 10
    min_kids = 150
    max_minibuses = 10

    # Decision variables: integer variables
    NumberOfVans = solver.IntVar(0, solver.infinity(), 'NumberOfVans')
    NumberOfMinibuses = solver.IntVar(0, max_minibuses, 'NumberOfMinibuses')  # upper bounded by max_minibuses

    # Constraints
    # 1. Transportation capacity: 6 * vans + 10 * minibuses >= 150
    solver.Add(van_capacity * NumberOfVans + minibus_capacity * NumberOfMinibuses >= min_kids)

    # 2. Limit on minibuses is already handled by upper bound, but we add constraint for clarity.
    solver.Add(NumberOfMinibuses <= max_minibuses)

    # 3. Number of vans must be at least one more than minibuses (ensures vans > minibuses)
    solver.Add(NumberOfVans >= NumberOfMinibuses + 1)

    # Objective: minimize pollution: 7 * vans + 10 * minibuses
    objective = solver.Objective()
    objective.SetCoefficient(NumberOfVans, van_pollution)
    objective.SetCoefficient(NumberOfMinibuses, minibus_pollution)
    objective.SetMinimization()

    status = solver.Solve()

    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result = {
            'NumberOfVans': int(NumberOfVans.solution_value()),
            'NumberOfMinibuses': int(NumberOfMinibuses.solution_value()),
            'objective': objective.Value()
        }
    else:
        result = {'message': 'The problem does not have an optimal solution using the linear solver.'}
    return result

def solve_with_cp_model():
    # Create the CP-SAT model.
    model = cp_model.CpModel()

    # Parameters
    van_capacity = 6
    minibus_capacity = 10
    van_pollution = 7
    minibus_pollution = 10
    min_kids = 150
    max_minibuses = 10

    # Decide safe upper bounds.
    # For minibuses, upper bound is max_minibuses.
    # For vans, because of capacity constraint: need enough vans if no minibuses used:
    # 6 * NumberOfVans >= 150  => NumberOfVans >= 25; to allow for margin, set upper bound to 100.
    max_vans = 100

    # Decision variables.
    NumberOfVans = model.NewIntVar(0, max_vans, 'NumberOfVans')
    NumberOfMinibuses = model.NewIntVar(0, max_minibuses, 'NumberOfMinibuses')

    # Constraints
    # 1. Capacity constraint: 6*vans + 10*minibuses >= 150
    model.Add(van_capacity * NumberOfVans + minibus_capacity * NumberOfMinibuses >= min_kids)
    
    # 2. Number of minibuses <= max_minibuses is implicit by domain, but re-assert for clarity.
    model.Add(NumberOfMinibuses <= max_minibuses)
    
    # 3. Vans exceed minibuses: NumberOfVans >= NumberOfMinibuses + 1.
    model.Add(NumberOfVans >= NumberOfMinibuses + 1)

    # Objective: minimize pollution = 7 * vans + 10 * minibuses.
    model.Minimize(van_pollution * NumberOfVans + minibus_pollution * NumberOfMinibuses)

    # Solve the model.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    result = {}
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        result = {
            'NumberOfVans': solver.Value(NumberOfVans),
            'NumberOfMinibuses': solver.Value(NumberOfMinibuses),
            'objective': solver.ObjectiveValue()
        }
    else:
        result = {'message': 'The problem does not have an optimal solution using CP-SAT.'}
    return result

def main():
    results = {}
    # Solve using OR-Tools Linear Solver.
    linear_result = solve_with_linear_solver()
    results['LinearSolver'] = linear_result

    # Solve using OR-Tools CP-SAT Model.
    cp_result = solve_with_cp_model()
    results['CPSAT'] = cp_result

    # Print the results in a structured way.
    print("Optimization Results:")
    for method, res in results.items():
        print(f"\nMethod: {method}")
        if 'message' in res:
            print(res['message'])
        else:
            print("NumberOfVans:", res['NumberOfVans'])
            print("NumberOfMinibuses:", res['NumberOfMinibuses'])
            print("Total Pollution:", res['objective'])

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Optimization Results:

Method: LinearSolver
NumberOfVans: 10
NumberOfMinibuses: 9
Total Pollution: 160.0

Method: CPSAT
NumberOfVans: 10
NumberOfMinibuses: 9
Total Pollution: 160.0
'''

'''Expected Output:
Expected solution

: {'variables': {'NumberOfVans': 10.0, 'NumberOfMinibuses': 9.0}, 'objective': 160.0}'''

