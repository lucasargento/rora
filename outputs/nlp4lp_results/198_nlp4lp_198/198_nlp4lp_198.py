# Problem Description:
'''Problem description: A concert organizer has to transport equipment using carts or trolleys. Carts can transport 5 kg/min of equipment and requires 2 workers. Trolleys can transport 7 kg/min of equipment and requires 4 workers. There must be at least 12 trolleys to be used. Additionally, only a maximum of 40% of the transportation can be using trolleys. The organizer has to deliver at a rate of 100 kg/min of equipment. How many of each transportation method should be used to minimize the total number of workers?

Expected Output Schema:
{
  "variables": {
    "NumberOfCarts": "float",
    "NumberOfTrolleys": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- M: set of transportation methods = {Cart, Trolley}

Parameters:
- capacity_cart = 5        // Equipment delivered per cart in kg per minute
- capacity_trolley = 7     // Equipment delivered per trolley in kg per minute
- workers_cart = 2         // Workers required per cart
- workers_trolley = 4      // Workers required per trolley
- required_delivery = 100  // Total required delivery rate in kg per minute
- min_trolleys = 12        // At least 12 trolleys must be used
- max_trolley_share = 0.4  // Maximum share (40%) of total delivery that can come from trolleys

Variables:
- NumberOfCarts, representing the number of carts used [decision variable, continuous (or integer if enforced) and ≥ 0]
- NumberOfTrolleys, representing the number of trolleys used [decision variable, continuous (or integer if enforced) and ≥ 0]

Objective:
- Minimize total workers required = workers_cart * NumberOfCarts + workers_trolley * NumberOfTrolleys

Constraints:
1. Delivery Requirement: 
   capacity_cart * NumberOfCarts + capacity_trolley * NumberOfTrolleys ≥ required_delivery
   (i.e., 5 * NumberOfCarts + 7 * NumberOfTrolleys ≥ 100)

2. Minimum Trolley Usage:
   NumberOfTrolleys ≥ min_trolleys
   (i.e., NumberOfTrolleys ≥ 12)

3. Trolley Share Limitation:
   The equipment delivered by trolleys may not exceed max_trolley_share of the total equipment delivered. That is,
   capacity_trolley * NumberOfTrolleys ≤ max_trolley_share * (capacity_cart * NumberOfCarts + capacity_trolley * NumberOfTrolleys)
   (i.e., 7 * NumberOfTrolleys ≤ 0.4 * (5 * NumberOfCarts + 7 * NumberOfTrolleys))

Comments:
- All rates and capacities are given in kg per minute and workers per vehicle.
- Although the decision variables could be naturally integer, the output schema indicates their type as "float". Adjust integrality constraints as needed in implementation.
- The third constraint ensures that at most 40% of the total transportation (by kg/min) is provided by trolleys.

Expected Output Schema:
{
  "variables": {
    "NumberOfCarts": "float",
    "NumberOfTrolleys": "float"
  },
  "objective": "float"
}'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_continuous():
    # Create the solver using the GLOP (continuous) backend.
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Could not create solver for continuous model.")
        return None

    # Parameters
    capacity_cart = 5
    capacity_trolley = 7
    workers_cart = 2
    workers_trolley = 4
    required_delivery = 100
    min_trolleys = 12
    max_trolley_share = 0.4  # The share limit for trolley equipment

    # Decision Variables (Continuous)
    # Although naturally integers, we allow continuous per problem statement output schema.
    NumberOfCarts = solver.NumVar(0.0, solver.infinity(), 'NumberOfCarts')
    NumberOfTrolleys = solver.NumVar(0.0, solver.infinity(), 'NumberOfTrolleys')

    # Constraints

    # 1. Delivery requirement: 5 * C + 7 * T >= 100
    solver.Add(capacity_cart * NumberOfCarts + capacity_trolley * NumberOfTrolleys >= required_delivery)

    # 2. Minimum trolley usage: T >= 12
    solver.Add(NumberOfTrolleys >= min_trolleys)

    # 3. Trolley share limitation:
    #    7 * T <= 0.4 * (5 * C + 7 * T)
    #    Rearranged: 7T - 2.8T <= 2C  => 4.2T <= 2C  => T <= (2/4.2)*C
    solver.Add(NumberOfTrolleys <= (2.0/4.2) * NumberOfCarts)

    # Objective: Minimize total workers = 2 * C + 4 * T
    objective = solver.Objective()
    objective.SetCoefficient(NumberOfCarts, workers_cart)
    objective.SetCoefficient(NumberOfTrolleys, workers_trolley)
    objective.SetMinimization()

    # Solve the model.
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "variables": {
                "NumberOfCarts": NumberOfCarts.solution_value(),
                "NumberOfTrolleys": NumberOfTrolleys.solution_value()
            },
            "objective": objective.Value()
        }
        return result
    else:
        print("The continuous model does not have an optimal solution.")
        return None

def solve_integer():
    # Create the solver using the CBC_MIXED_INTEGER_PROGRAMMING backend for integer variables
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Could not create solver for integer model.")
        return None

    # Parameters
    capacity_cart = 5
    capacity_trolley = 7
    workers_cart = 2
    workers_trolley = 4
    required_delivery = 100
    min_trolleys = 12
    max_trolley_share = 0.4

    # Decision Variables (Integer)
    NumberOfCarts = solver.IntVar(0, solver.infinity(), 'NumberOfCarts')
    NumberOfTrolleys = solver.IntVar(0, solver.infinity(), 'NumberOfTrolleys')

    # Constraints

    # 1. Delivery requirement: 5 * C + 7 * T >= 100
    solver.Add(capacity_cart * NumberOfCarts + capacity_trolley * NumberOfTrolleys >= required_delivery)

    # 2. Minimum trolley usage: T >= 12
    solver.Add(NumberOfTrolleys >= min_trolleys)

    # 3. Trolley share limitation:
    #    7 * T <= 0.4 * (5 * C + 7 * T)
    #    Rearranged to: T <= (2/4.2)*C
    # Using float coefficient in constraint:
    solver.Add(NumberOfTrolleys <= (2.0/4.2) * NumberOfCarts)

    # Objective: Minimize total workers = 2 * C + 4 * T
    objective = solver.Objective()
    objective.SetCoefficient(NumberOfCarts, workers_cart)
    objective.SetCoefficient(NumberOfTrolleys, workers_trolley)
    objective.SetMinimization()

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "variables": {
                "NumberOfCarts": NumberOfCarts.solution_value(),
                "NumberOfTrolleys": NumberOfTrolleys.solution_value()
            },
            "objective": objective.Value()
        }
        return result
    else:
        print("The integer model does not have an optimal solution.")
        return None

def main():
    continuous_result = solve_continuous()
    integer_result = solve_integer()
    
    print("Continuous Model (variables as float):")
    if continuous_result:
        print(continuous_result)
    else:
        print("No optimal solution found for the continuous model.")
    
    print("\nInteger Model (variables as integer):")
    if integer_result:
        print(integer_result)
    else:
        print("No optimal solution found for the integer model.")

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Continuous Model (variables as float):
{'variables': {'NumberOfCarts': 25.200000000000003, 'NumberOfTrolleys': 12.0}, 'objective': 98.4}

Integer Model (variables as integer):
{'variables': {'NumberOfCarts': 26.0, 'NumberOfTrolleys': 12.0}, 'objective': 100.0}
'''

'''Expected Output:
Expected solution

: {'variables': {'NumberOfCarts': 4.0, 'NumberOfTrolleys': 12.0}, 'objective': 56.0}'''

