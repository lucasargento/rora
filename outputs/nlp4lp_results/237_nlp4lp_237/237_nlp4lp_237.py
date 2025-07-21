# Problem Description:
'''Problem description: A company in the desert can transport goods to rural cities either by camel caravans or desert trucks. A camel caravan can deliver 50 units of goods per trip and takes 12 hours. A desert truck can deliver 150 units of goods per trip and takes 5 hours. However, due to the cost of fuel, the company prefers to have more camel caravans than desert trucks.  If the company needs to deliver 1500 units of goods, how many of each method of transportation should the company organize to minimize the total number of hours required?

Expected Output Schema:
{
  "variables": {
    "NumberCamelCaravans": "float",
    "NumberDesertTrucks": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- TransportationMethods: set of methods = {CamelCaravan, DesertTruck}

Parameters:
- CamelCaravan_capacity = 50 units per trip
- DesertTruck_capacity = 150 units per trip
- CamelCaravan_time = 12 hours per trip
- DesertTruck_time = 5 hours per trip
- Demand = 1500 units (total goods to be delivered)
- Note: The company’s policy implies a preference constraint: the number of CamelCaravan trips should be at least as many as DesertTruck trips.

Variables:
- NumberCamelCaravans: number of camel caravan trips (decision variable, assumed nonnegative; can be modeled as continuous or integer)
- NumberDesertTrucks: number of desert truck trips (decision variable, assumed nonnegative; can be modeled as continuous or integer)

Objective:
- Minimize TotalHours = (CamelCaravan_time * NumberCamelCaravans) + (DesertTruck_time * NumberDesertTrucks)

Constraints:
1. Demand constraint:
   (CamelCaravan_capacity * NumberCamelCaravans) + (DesertTruck_capacity * NumberDesertTrucks) >= Demand
2. Preference constraint:
   NumberCamelCaravans >= NumberDesertTrucks

Expected Output Schema:
{
  "variables": {
    "NumberCamelCaravans": "float",
    "NumberDesertTrucks": "float"
  },
  "objective": "float"
}'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_continuous_model():
    # Create the solver with the GLOP backend.
    solver = pywraplp.Solver.CreateSolver("GLOP")
    if not solver:
        print("Solver not created.")
        return None

    # Parameters
    camel_capacity = 50
    truck_capacity = 150
    camel_time = 12
    truck_time = 5
    demand = 1500

    # Decision Variables: continuous nonnegative
    NumberCamelCaravans = solver.NumVar(0.0, solver.infinity(), 'NumberCamelCaravans')
    NumberDesertTrucks = solver.NumVar(0.0, solver.infinity(), 'NumberDesertTrucks')

    # Constraints:
    # Demand constraint: 50 * NumberCamelCaravans + 150 * NumberDesertTrucks >= 1500
    solver.Add(camel_capacity * NumberCamelCaravans + truck_capacity * NumberDesertTrucks >= demand)
    # Preference constraint: NumberCamelCaravans >= NumberDesertTrucks
    solver.Add(NumberCamelCaravans - NumberDesertTrucks >= 0)

    # Objective: Minimize total hours = 12 * NumberCamelCaravans + 5 * NumberDesertTrucks
    objective = solver.Objective()
    objective.SetCoefficient(NumberCamelCaravans, camel_time)
    objective.SetCoefficient(NumberDesertTrucks, truck_time)
    objective.SetMinimization()

    # Solve the model.
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "variables": {
                "NumberCamelCaravans": NumberCamelCaravans.solution_value(),
                "NumberDesertTrucks": NumberDesertTrucks.solution_value()
            },
            "objective": objective.Value()
        }
        return result
    else:
        print("No optimal solution found for the continuous model.")
        return None

def solve_integer_model():
    # Create the solver with the CBC backend.
    solver = pywraplp.Solver.CreateSolver("CBC")
    if not solver:
        print("Solver not created.")
        return None

    # Parameters
    camel_capacity = 50
    truck_capacity = 150
    camel_time = 12
    truck_time = 5
    demand = 1500

    # Decision Variables: integer nonnegative
    NumberCamelCaravans = solver.IntVar(0, solver.infinity(), 'NumberCamelCaravans')
    NumberDesertTrucks = solver.IntVar(0, solver.infinity(), 'NumberDesertTrucks')

    # Constraints:
    # Demand constraint: 50 * NumberCamelCaravans + 150 * NumberDesertTrucks >= 1500
    solver.Add(camel_capacity * NumberCamelCaravans + truck_capacity * NumberDesertTrucks >= demand)
    # Preference constraint: NumberCamelCaravans >= NumberDesertTrucks
    solver.Add(NumberCamelCaravans - NumberDesertTrucks >= 0)

    # Objective: Minimize total hours = 12 * NumberCamelCaravans + 5 * NumberDesertTrucks
    objective = solver.Objective()
    objective.SetCoefficient(NumberCamelCaravans, camel_time)
    objective.SetCoefficient(NumberDesertTrucks, truck_time)
    objective.SetMinimization()

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "variables": {
                "NumberCamelCaravans": NumberCamelCaravans.solution_value(),
                "NumberDesertTrucks": NumberDesertTrucks.solution_value()
            },
            "objective": objective.Value()
        }
        return result
    else:
        print("No optimal solution found for the integer model.")
        return None

def main():
    print("Continuous Model (Variables can be fractional):")
    continuous_result = solve_continuous_model()
    if continuous_result:
        print(continuous_result)

    print("\nInteger Model (Variables are integers):")
    integer_result = solve_integer_model()
    if integer_result:
        print(integer_result)

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Continuous Model (Variables can be fractional):
{'variables': {'NumberCamelCaravans': 7.5, 'NumberDesertTrucks': 7.5}, 'objective': 127.5}

Integer Model (Variables are integers):
{'variables': {'NumberCamelCaravans': 8.0, 'NumberDesertTrucks': 8.0}, 'objective': 136.0}
'''

'''Expected Output:
Expected solution

: {'variables': {'NumberCamelCaravans': -0.0, 'NumberDesertTrucks': 10.0}, 'objective': 50.0}'''

