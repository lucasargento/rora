# Problem Description:
'''Problem description: A toy store decides to deliver gifts using two shipping companies, a new one and an old one. The new company can deliver 50 gifts per trip while the old company can deliver 70 gifts per trip. The new company uses 30 liters of diesel per trip while the old company uses 40 liters of diesel per trip. The toy store needs to deliver at least 1000 gifts. There can be at most 15 trips made by the new company. In order to make sure that the old company does not go out of business, at least 40% of all trips must be made by the old company. How many trips should each company make to minimize the total amount of diesel used?

Expected Output Schema:
{
  "variables": {
    "TripsNewCompany": "float",
    "TripsOldCompany": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- Companies: {New, Old}

Parameters:
- new_trip_capacity: Number of gifts delivered by the new company per trip (50 gifts per trip)
- old_trip_capacity: Number of gifts delivered by the old company per trip (70 gifts per trip)
- new_trip_diesel: Diesel consumption per trip for the new company (30 liters per trip)
- old_trip_diesel: Diesel consumption per trip for the old company (40 liters per trip)
- min_gifts: Minimum total number of gifts to deliver (1000 gifts)
- max_new_trips: Maximum number of trips allowed by the new company (15 trips)
- min_old_trip_ratio: Minimum fraction of total trips that must be made by the old company (0.40)

Variables:
- TripsNewCompany: Number of trips by the new company (integer, ≥ 0)
- TripsOldCompany: Number of trips by the old company (integer, ≥ 0)

Objective:
- Minimize total diesel usage = new_trip_diesel * TripsNewCompany + old_trip_diesel * TripsOldCompany

Constraints:
1. Gift Delivery Constraint:
   new_trip_capacity * TripsNewCompany + old_trip_capacity * TripsOldCompany ≥ min_gifts

2. New Company Trip Limit:
   TripsNewCompany ≤ max_new_trips

3. Minimum Old Company Trip Proportion:
   To ensure at least 40% of all trips are by the old company, the following must hold:
   TripsOldCompany ≥ min_old_trip_ratio * (TripsNewCompany + TripsOldCompany)
   This can be reformulated as:  TripsOldCompany - min_old_trip_ratio * (TripsNewCompany + TripsOldCompany) ≥ 0
   or equivalently:  (1 - min_old_trip_ratio)*TripsOldCompany - min_old_trip_ratio*TripsNewCompany ≥ 0
   With min_old_trip_ratio = 0.40, this becomes:
   0.60 * TripsOldCompany - 0.40 * TripsNewCompany ≥ 0
   which can also be written as:
   3 * TripsOldCompany - 2 * TripsNewCompany ≥ 0

Comments:
- All parameter units are consistent: capacities in gifts per trip, diesel usage in liters per trip, and the gift requirement in gifts.
- The decision variables are modeled as integers since trips are discrete counts.
- The model minimizes the total diesel consumption while ensuring sufficient delivery of gifts and the required distribution of trips between the companies.

Expected Output Schema:
{
  "variables": {
    "TripsNewCompany": "integer",
    "TripsOldCompany": "integer"
  },
  "objective": "Minimize total diesel usage = 30 * TripsNewCompany + 40 * TripsOldCompany"
}'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_model_version1():
    # Create the MIP solver with SCIP backend.
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        print("Solver not created.")
        return None

    # Parameters
    new_trip_capacity = 50         # gifts per trip by new company
    old_trip_capacity = 70         # gifts per trip by old company
    new_trip_diesel = 30           # liters per trip for new company
    old_trip_diesel = 40           # liters per trip for old company
    min_gifts = 1000               # minimum required gifts to deliver
    max_new_trips = 15             # maximum trips allowed for new company
    min_old_trip_ratio = 0.40      # minimum fraction of trips by old company

    # Decision Variables
    TripsNewCompany = solver.IntVar(0, max_new_trips, 'TripsNewCompany')
    TripsOldCompany = solver.IntVar(0, solver.infinity(), 'TripsOldCompany')

    # Constraints
    # 1. Gift Delivery Constraint: 50 * TripsNewCompany + 70 * TripsOldCompany ≥ 1000
    solver.Add(new_trip_capacity * TripsNewCompany + old_trip_capacity * TripsOldCompany >= min_gifts)
    
    # 2. New Company Trip Limit is already defined in variable upper bound (TripsNewCompany ≤ 15)

    # 3. Minimum Old Company Trip Proportion:
    # Formulation: TripsOldCompany ≥ 0.40 * (TripsNewCompany + TripsOldCompany)
    # Rearranging: TripsOldCompany - 0.40*(TripsNewCompany + TripsOldCompany) >= 0  ->  0.60*TripsOldCompany - 0.40*TripsNewCompany >= 0
    # We'll add the constraint as:
    solver.Add(0.60 * TripsOldCompany - 0.40 * TripsNewCompany >= 0)

    # Objective: Minimize total diesel consumption = 30 * TripsNewCompany + 40 * TripsOldCompany
    objective = solver.Objective()
    objective.SetCoefficient(TripsNewCompany, new_trip_diesel)
    objective.SetCoefficient(TripsOldCompany, old_trip_diesel)
    objective.SetMinimization()

    status = solver.Solve()

    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result['TripsNewCompany'] = int(TripsNewCompany.solution_value())
        result['TripsOldCompany'] = int(TripsOldCompany.solution_value())
        result['Objective'] = objective.Value()
    else:
        result['error'] = "No optimal solution found in Model Version 1."

    return result


def solve_model_version2():
    # Create the MIP solver with SCIP backend.
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        print("Solver not created.")
        return None

    # Parameters (same as before)
    new_trip_capacity = 50         # gifts per trip by new company
    old_trip_capacity = 70         # gifts per trip by old company
    new_trip_diesel = 30           # liters per trip for new company
    old_trip_diesel = 40           # liters per trip for old company
    min_gifts = 1000               # minimum required gifts to deliver
    max_new_trips = 15             # maximum trips allowed for new company
    # Instead of using the ratio directly, we reformulate:
    # Using the equivalent constraint: 3 * TripsOldCompany - 2 * TripsNewCompany ≥ 0

    # Decision Variables
    TripsNewCompany = solver.IntVar(0, max_new_trips, 'TripsNewCompany')
    TripsOldCompany = solver.IntVar(0, solver.infinity(), 'TripsOldCompany')

    # Constraints
    # 1. Gift Delivery Constraint: 50 * TripsNewCompany + 70 * TripsOldCompany ≥ 1000
    solver.Add(new_trip_capacity * TripsNewCompany + old_trip_capacity * TripsOldCompany >= min_gifts)
    
    # 2. New Company Trip Limit is already enforced in the variable domain (TripsNewCompany ≤ 15)

    # 3. Minimum Old Company Trip Proportion Reformulated:
    # 3 * TripsOldCompany - 2 * TripsNewCompany ≥ 0
    solver.Add(3 * TripsOldCompany - 2 * TripsNewCompany >= 0)

    # Objective: Minimize total diesel consumption = 30 * TripsNewCompany + 40 * TripsOldCompany
    objective = solver.Objective()
    objective.SetCoefficient(TripsNewCompany, new_trip_diesel)
    objective.SetCoefficient(TripsOldCompany, old_trip_diesel)
    objective.SetMinimization()

    status = solver.Solve()

    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result['TripsNewCompany'] = int(TripsNewCompany.solution_value())
        result['TripsOldCompany'] = int(TripsOldCompany.solution_value())
        result['Objective'] = objective.Value()
    else:
        result['error'] = "No optimal solution found in Model Version 2."

    return result


def main():
    results = {}
    
    # Solve using version 1 formulation (direct ratio formulation)
    res1 = solve_model_version1()
    results['Model_Version1'] = res1
    
    # Solve using version 2 formulation (reformulated constraint)
    res2 = solve_model_version2()
    results['Model_Version2'] = res2
    
    # Display the results in a structured way.
    print("Optimization Results:")
    for version, res in results.items():
        print(f"\n{version}:")
        if 'error' in res:
            print(res['error'])
        else:
            print(f"TripsNewCompany: {res['TripsNewCompany']}")
            print(f"TripsOldCompany: {res['TripsOldCompany']}")
            print(f"Total Diesel Consumption (Objective): {res['Objective']}")


if __name__ == "__main__":
    main()

'''Execution Results:
SUCCESS:
Optimization Results:

Model_Version1:
TripsNewCompany: 2
TripsOldCompany: 13
Total Diesel Consumption (Objective): 580.0

Model_Version2:
TripsNewCompany: 2
TripsOldCompany: 13
Total Diesel Consumption (Objective): 580.0
'''

'''Expected Output:
Expected solution

: {'variables': {'TripsNewCompany': 2.0, 'TripsOldCompany': 13.0}, 'objective': 580.0}'''

