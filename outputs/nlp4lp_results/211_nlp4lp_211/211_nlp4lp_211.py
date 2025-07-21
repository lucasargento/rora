# Problem Description:
'''Problem description: A dim sum restaurant can deliver their food by cart or by hand. Servers can deliver by cart and have 70 customer interactions and will have to refill food five times an hour. They can also deliver more food by hand, due to the increased mobility, and have 85 customer interactions while refilling food twenty times an hour. However, the customers get more options when delivering by cart, therefore at least 70% of delivery shifts must be by cart. There must be at least 3 servers delivering by hand for their direct customer service. If the restaurant wants to have 4000 customer interactions per hour, how many of each form of delivery should the dim sum restaurant schedule to minimize the total number of refills per hour?

Expected Output Schema:
{
  "variables": {
    "NumberOfCartDeliveryServers": "float",
    "NumberOfHandDeliveryServers": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- D: set of delivery modes = {Cart, Hand}

Parameters:
- interactions_Cart: number of customer interactions per hour for a cart server = 70 [interactions/server·hour]
- interactions_Hand: number of customer interactions per hour for a hand server = 85 [interactions/server·hour]
- refills_Cart: number of refills per hour for a cart server = 5 [refills/server·hour]
- refills_Hand: number of refills per hour for a hand server = 20 [refills/server·hour]
- required_interactions: required total customer interactions per hour = 4000 [interactions/hour]
- cart_shift_percentage: minimum percentage of shifts to be delivered by cart = 0.70 [unitless]
- min_hand_servers: minimum number of servers delivering by hand = 3 [servers]

Variables:
- x_Cart: number of cart delivery servers scheduled (continuous, nonnegative) [servers]
- x_Hand: number of hand delivery servers scheduled (continuous, nonnegative) [servers]

Objective:
- Minimize total refills per hour = (refills_Cart * x_Cart) + (refills_Hand * x_Hand)

Constraints:
1. Customer interaction constraint:
   interactions_Cart * x_Cart + interactions_Hand * x_Hand = required_interactions
   (i.e., 70 * x_Cart + 85 * x_Hand = 4000)

2. Delivery mode ratio (at least 70% by cart):
   x_Cart >= cart_shift_percentage * (x_Cart + x_Hand)
   (This is equivalent to x_Cart >= 0.7*(x_Cart + x_Hand))

3. Minimum hand delivery servers:
   x_Hand >= min_hand_servers

Comments:
- All parameters are expressed per hour.
- The decision variables x_Cart and x_Hand are modeled as continuous for scheduling purposes. If only integer numbers of servers can be scheduled, these should be declared as integers.
- The customer interaction constraint is set to equality to exactly meet the desired 4000 interactions per hour.
- The delivery mode ratio constraint can be algebraically rearranged (x_Cart >= (7/3)*x_Hand) if needed for simplification.'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp
from ortools.sat.python import cp_model

def solve_with_linear_solver():
    # Create linear solver with the GLOP backend (continuous LP)
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Linear solver not available.")
        return None

    # Parameters
    interactions_cart = 70
    interactions_hand = 85
    refills_cart = 5
    refills_hand = 20
    required_interactions = 4000
    cart_shift_percentage = 0.70
    min_hand_servers = 3

    # Variables (continuous)
    x_cart = solver.NumVar(0.0, solver.infinity(), 'x_cart')
    x_hand = solver.NumVar(0.0, solver.infinity(), 'x_hand')

    # Constraint 1: Customer interactions exactly equal 4000
    solver.Add(interactions_cart * x_cart + interactions_hand * x_hand == required_interactions)

    # Constraint 2: At least 70% of shifts by cart.
    # Original: x_cart >= 0.70*(x_cart + x_hand)
    # Rearranged: 0.3*x_cart - 0.7*x_hand >= 0
    solver.Add(0.3 * x_cart - 0.7 * x_hand >= 0)

    # Constraint 3: At least 3 hand delivery servers
    solver.Add(x_hand >= min_hand_servers)

    # Objective: Minimize total refills per hour.
    solver.Minimize(refills_cart * x_cart + refills_hand * x_hand)

    status = solver.Solve()

    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "NumberOfCartDeliveryServers": x_cart.solution_value(),
            "NumberOfHandDeliveryServers": x_hand.solution_value(),
            "objective": solver.Objective().Value()
        }
    else:
        print("The linear solver model did not find an optimal solution.")
    return result

def solve_with_cp_model():
    # In this version, we assume servers must be scheduled as integers.
    model = cp_model.CpModel()

    # Parameters
    interactions_cart = 70
    interactions_hand = 85
    refills_cart = 5
    refills_hand = 20
    required_interactions = 4000
    min_hand_servers = 3
    # For the ratio constraint:
    # Original: x_cart >= 0.70*(x_cart + x_hand)
    # Multiply both sides by 10 to eliminate decimals:
    # 10*x_cart >= 7*(x_cart + x_hand)
    # => 10*x_cart - 7*x_cart - 7*x_hand >= 0  => 3*x_cart >= 7*x_hand
    # We'll use this form: 3 * x_cart - 7 * x_hand >= 0

    # Upper bound guesses: assume maximum servers might be required.
    max_servers = 4000  # arbitrary large number to define domain

    # Variables (integer)
    x_cart = model.NewIntVar(0, max_servers, 'x_cart')
    x_hand = model.NewIntVar(0, max_servers, 'x_hand')

    # Constraint 1: Customer interactions exactly equal 4000
    # 70*x_cart + 85*x_hand == 4000
    model.Add(interactions_cart * x_cart + interactions_hand * x_hand == required_interactions)

    # Constraint 2: At least 70% of shifts by cart
    model.Add(3 * x_cart - 7 * x_hand >= 0)

    # Constraint 3: At least 3 hand delivery servers
    model.Add(x_hand >= min_hand_servers)

    # Objective: Minimize total refills per hour = 5*x_cart + 20*x_hand
    objective_var = model.NewIntVar(0, max_servers * max(refills_cart, refills_hand) * 10, 'objective')
    # Since we can set objective directly using linear expression in CpModel, we use:
    model.Minimize(refills_cart * x_cart + refills_hand * x_hand)

    # Solve model.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    result = {}
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        result = {
            "NumberOfCartDeliveryServers": solver.Value(x_cart),
            "NumberOfHandDeliveryServers": solver.Value(x_hand),
            "objective": solver.ObjectiveValue()
        }
    else:
        print("The CP-SAT model did not find a feasible solution.")
    return result

def main():
    print("Solution using Linear Solver (continuous variables):")
    linear_result = solve_with_linear_solver()
    if linear_result:
        print(linear_result)

    print("\nSolution using CP-SAT Model (integer variables):")
    cp_result = solve_with_cp_model()
    if cp_result:
        print(cp_result)

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Solution using Linear Solver (continuous variables):
{'NumberOfCartDeliveryServers': 53.5, 'NumberOfHandDeliveryServers': 3.0, 'objective': 327.5}

Solution using CP-SAT Model (integer variables):
{'NumberOfCartDeliveryServers': 45, 'NumberOfHandDeliveryServers': 10, 'objective': 425.0}
'''

'''Expected Output:
Expected solution

: {'variables': {'NumberOfCartDeliveryServers': 54.0, 'NumberOfHandDeliveryServers': 3.0}, 'objective': 330.0}'''

