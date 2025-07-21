# Problem Description:
'''Problem description: A village hosts a banquet and provides bike and car transportation for everyone. A bike can take 3 people while a car can take 5 people. Since cars are more expensive, at most 40% of the vehicles can be cars. If the village needs to transport at least 500 people, how many of each vehicle should be used to minimize the total number of bikes needed?

Expected Output Schema:
{
  "variables": {
    "NumberOfBikes": "float",
    "NumberOfCars": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Below is the complete five‐element structured model that represents the problem exactly as described.

--------------------------------------------------

Sets:
- Vehicles = {Bike, Car}  
  (Note: Although only two types exist, we keep them separate for clarity.)

Parameters:
- capacity_Bike = 3   (number of people a bike can transport)
- capacity_Car = 5    (number of people a car can transport)
- min_people = 500    (minimum number of people to be transported)
- max_car_fraction = 0.4   (maximum allowed fraction of vehicles that can be cars)

Variables:
- NumberOfBikes: number of bikes used [nonnegative real number, assume integer in practical implementation]
- NumberOfCars: number of cars used [nonnegative real number, assume integer in practical implementation]

Objective:
- Minimize the total number of bikes, i.e., minimize NumberOfBikes  
  (Here, the assumption is that bikes are cheaper relative to limiting total vehicles but the goal is to reduce the deployed bike count.)

Constraints:
1. Transportation capacity constraint:  
   3 * NumberOfBikes + 5 * NumberOfCars >= 500  
   (This ensures that the combined capacity of bikes and cars covers at least 500 people.)

2. Car fraction constraint:  
   NumberOfCars <= 0.4 * (NumberOfBikes + NumberOfCars)  
   (This ensures that cars do not exceed 40% of the total vehicles used.)  

--------------------------------------------------

Additional Comments:
- Both NumberOfBikes and NumberOfCars are decision variables and although the expected output schema lists them as float, in practice they should be integers since you cannot use a fraction of a vehicle.
- All capacities and the minimum requirement are expressed in "people".
- The car fraction is expressed as a percentage (40%) in its decimal form (0.4) ensuring unit consistency with the overall count of vehicles.

This model is complete, self-contained, and logically consistent for implementing in any optimization solver such as OR-Tools or Python-based frameworks.'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_model1():
    # Model 1: Using the original car fraction constraint:
    #   3*bikes + 5*cars >= 500
    #   cars <= 0.4*(bikes + cars)
    #   Minimize bikes
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        return None

    # Define variables as non-negative integers
    bikes = solver.IntVar(0, solver.infinity(), 'NumberOfBikes')
    cars  = solver.IntVar(0, solver.infinity(), 'NumberOfCars')

    # Constraint 1: Transportation capacity
    solver.Add(3 * bikes + 5 * cars >= 500)

    # Constraint 2: Car fraction constraint
    #   cars <= 0.4*(bikes + cars)
    # To avoid fractional coefficients in integer programming, we can multiply by 10:
    #   10*cars <= 4*(bikes + cars)
    # Simplify: 10*cars <= 4*bikes + 4*cars   -->   6*cars <= 4*bikes   or   3*cars <= 2*bikes
    # However, here we keep the original constraint as provided, directly.
    # Using the fractional form:
    solver.Add(cars <= 0.4 * (bikes + cars))

    # Objective: Minimize number of bikes
    objective = solver.Objective()
    objective.SetCoefficient(bikes, 1)
    objective.SetMinimization()

    status = solver.Solve()

    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "NumberOfBikes": bikes.solution_value(),
            "NumberOfCars": cars.solution_value(),
            "objective": objective.Value()
        }
    else:
        result = {"error": "Model 1: No optimal solution found."}
    return result

def solve_model2():
    # Model 2: Using the simplified equivalent Constraint for the car fraction:
    #   From: cars <= 0.4*(bikes+cars) we derived: 3*cars <= 2*bikes
    # and the transportation constraint: 3*bikes + 5*cars >= 500
    # Objective remains: minimize bikes.
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        return None

    # Define variables as non-negative integers
    bikes = solver.IntVar(0, solver.infinity(), 'NumberOfBikes')
    cars  = solver.IntVar(0, solver.infinity(), 'NumberOfCars')

    # Constraint 1: Transportation capacity
    solver.Add(3 * bikes + 5 * cars >= 500)

    # Constraint 2: Simplified car fraction constraint: 3*cars <= 2*bikes
    solver.Add(3 * cars <= 2 * bikes)

    # Objective: Minimize number of bikes
    objective = solver.Objective()
    objective.SetCoefficient(bikes, 1)
    objective.SetMinimization()

    status = solver.Solve()

    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "NumberOfBikes": bikes.solution_value(),
            "NumberOfCars": cars.solution_value(),
            "objective": objective.Value()
        }
    else:
        result = {"error": "Model 2: No optimal solution found."}
    return result

def main():
    result1 = solve_model1()
    result2 = solve_model2()

    print("Results for Model 1 (Original constraint formulation):")
    if "error" in result1:
        print(result1["error"])
    else:
        print(result1)

    print("\nResults for Model 2 (Simplified constraint formulation):")
    if "error" in result2:
        print(result2["error"])
    else:
        print(result2)

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Results for Model 1 (Original constraint formulation):
{'NumberOfBikes': 80.0, 'NumberOfCars': 53.0, 'objective': 80.0}

Results for Model 2 (Simplified constraint formulation):
{'NumberOfBikes': 80.0, 'NumberOfCars': 53.0, 'objective': 80.0}
'''

'''Expected Output:
Expected solution

: {'variables': {'NumberOfBikes': 80.0, 'NumberOfCars': 53.0}, 'objective': 80.0}'''

