# Problem Description:
'''Problem description: A factory provides rides for its employees in either taxis or company cars. Each taxi ride can take 2 employees while each company car ride can take 3 employees. Since buying and maintaining cars is expensive, at most 60% of the rides can be company car rides. However, there has to be at least 30 company car rides. If the company needs to transport at least 500 employees, how many rides of each should be done to minimize the total number of taxi rides.

Expected Output Schema:
{
  "variables": {
    "NumberOfTaxiRides": "float",
    "NumberOfCompanyCarRides": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- Rides = {Taxi, CompanyCar}

Parameters:
- taxi_capacity: number of employees per taxi ride, equals 2 [employees/ride]
- company_capacity: number of employees per company car ride, equals 3 [employees/ride]
- min_employees: minimum number of employees to be transported, equals 500 [employees]
- min_company_rides: minimum required company car rides, equals 30 [rides]
- max_company_ratio: maximum allowed ratio of company car rides among all rides, equals 0.60 [dimensionless]

Variables:
- taxi_rides: number of taxi rides to be provided, an integer ≥ 0 [rides]
- company_car_rides: number of company car rides to be provided, an integer ≥ 0 [rides]

Objective:
- Minimize the number of taxi rides, i.e., minimize taxi_rides

Constraints:
1. Employee Transportation Constraint:
   taxi_capacity * taxi_rides + company_capacity * company_car_rides ≥ min_employees
   
2. Minimum Company Rides Constraint:
   company_car_rides ≥ min_company_rides

3. Company Car Ride Ratio Constraint:
   company_car_rides ≤ max_company_ratio * (taxi_rides + company_car_rides)

Comments:
- The units are consistent: capacities are given in number of employees per ride while the total is in employees.
- Both taxi_rides and company_car_rides are assumed to be integer values since partial rides are not practical.
- The ratio constraint ensures that no more than 60% of all rides are company car rides.
- The objective is to minimize taxi_rides, which may motivate using as many company_car_rides as possible while still satisfying the ratio limit and other constraints.

This model faithfully represents the real-world problem using the five-element framework.'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_with_linear_solver():
    # Create the mip solver with the CBC backend.
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Solver not created.")
        return None

    # Parameters
    taxi_capacity = 2
    company_capacity = 3
    min_employees = 500
    min_company_rides = 30
    max_company_ratio = 0.60

    # Variables: integer variables for number of rides
    taxi_rides = solver.IntVar(0, solver.infinity(), 'taxi_rides')
    company_car_rides = solver.IntVar(0, solver.infinity(), 'company_car_rides')

    # Constraint 1: Employee Transportation Constraint
    # 2 * taxi_rides + 3 * company_car_rides >= 500
    solver.Add(taxi_capacity * taxi_rides + company_capacity * company_car_rides >= min_employees)

    # Constraint 2: Minimum Company Rides Constraint
    solver.Add(company_car_rides >= min_company_rides)

    # Constraint 3: Company Car Ride Ratio Constraint:
    # company_car_rides <= 0.60 * (taxi_rides + company_car_rides)
    # Rearranging:
    # company_car_rides - 0.60*company_car_rides <= 0.60*taxi_rides  =>  0.40*company_car_rides <= 0.60*taxi_rides
    # which is equivalent to: company_car_rides <= (0.60/0.40) * taxi_rides = 1.5 * taxi_rides
    solver.Add(company_car_rides <= 1.5 * taxi_rides)

    # Objective: Minimize the number of taxi rides
    objective = solver.Objective()
    objective.SetCoefficient(taxi_rides, 1)
    objective.SetMinimization()

    status = solver.Solve()

    result = {}

    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "variables": {
                "NumberOfTaxiRides": taxi_rides.solution_value(),
                "NumberOfCompanyCarRides": company_car_rides.solution_value()
            },
            "objective": objective.Value()
        }
        print("Linear Solver Model (MIP) optimal solution:")
        print("  Number of Taxi Rides = {}".format(taxi_rides.solution_value()))
        print("  Number of Company Car Rides = {}".format(company_car_rides.solution_value()))
        print("  Objective (Minimized Taxi Rides) = {}".format(objective.Value()))
    elif status == pywraplp.Solver.FEASIBLE:
        print("A feasible solution was found, but it may not be optimal.")
    else:
        print("The problem does not have an optimal solution.")

    return result

def main():
    results = {}

    # Only one formulation is provided, so we run this single model.
    results["LinearSolverModel"] = solve_with_linear_solver()

    # Print results in a structured way.
    print("\nFinal Results:")
    print(results)

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Linear Solver Model (MIP) optimal solution:
  Number of Taxi Rides = 78.0
  Number of Company Car Rides = 115.0
  Objective (Minimized Taxi Rides) = 78.0

Final Results:
{'LinearSolverModel': {'variables': {'NumberOfTaxiRides': 78.0, 'NumberOfCompanyCarRides': 115.0}, 'objective': 78.0}}
'''

'''Expected Output:
Expected solution

: {'variables': {'NumberOfTaxiRides': 0.0, 'NumberOfCompanyCarRides': 2000000000.0}, 'objective': 0.0}'''

