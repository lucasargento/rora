# Problem Description:
'''Problem description: A patient can be hooked up to two machines to have medicine delivered, machine 1 and machine 2. Machine 1 delivers 0.5 units of medicine to the heart per minute and 0.8 units of medicine per minute to the brain. Machine 2 delivers 0.3 units of medicine per minute to the heart and 1 unit of medicine per minute to the brain. In addition however, machine 1 creates 0.3 units of waste per minute while machine 2 creates 0.5 units of waste per minute. If at most 8 units of medicine can be received by the heart and at least 4 units of medicine should be received by the brain, how many minutes should each machine be used to minimize the total amount of waste produced?

Expected Output Schema:
{
  "variables": {
    "Machine1OperatingTime": "float",
    "Machine2OperatingTime": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- M: set of machines = {Machine1, Machine2}

Parameters:
- heart_rate[m]: amount of medicine delivered to the heart per minute by machine m [units/minute]
   • For Machine1: heart_rate[Machine1] = 0.5
   • For Machine2: heart_rate[Machine2] = 0.3
- brain_rate[m]: amount of medicine delivered to the brain per minute by machine m [units/minute]
   • For Machine1: brain_rate[Machine1] = 0.8
   • For Machine2: brain_rate[Machine2] = 1.0
- waste_rate[m]: amount of waste produced by machine m per minute [units/minute]
   • For Machine1: waste_rate[Machine1] = 0.3
   • For Machine2: waste_rate[Machine2] = 0.5
- max_heart: maximum total units of medicine allowed to be delivered to the heart [units] = 8
- min_brain: minimum total units of medicine required to be delivered to the brain [units] = 4

Variables:
- t[m]: operating time for machine m [continuous, minutes, t ≥ 0]
   • t[Machine1] = minutes Machine1 is used
   • t[Machine2] = minutes Machine2 is used

Objective:
- Minimize total waste = sum over m in M of (waste_rate[m] * t[m])
  (Units: waste units produced over the treatment duration)

Constraints:
- Heart medicine constraint: heart_rate[Machine1] * t[Machine1] + heart_rate[Machine2] * t[Machine2] ≤ max_heart
- Brain medicine constraint: brain_rate[Machine1] * t[Machine1] + brain_rate[Machine2] * t[Machine2] ≥ min_brain

Comments:
- All rates and limits are assumed to have consistent units (medicine in units, waste in units, time in minutes).
- The decision variables t[m] are continuous and represent the duration (in minutes) for which each machine is used.
- The formulation minimizes the total waste while ensuring the heart does not receive more than 8 units of medicine and the brain receives at least 4 units.'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_linear_model():
    # Create the linear solver with the GLOP backend for continuous problems.
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Could not create solver.")
        return None

    # Decision Variables: Operating times in minutes (continuous, >= 0)
    t1 = solver.NumVar(0.0, solver.infinity(), 'Machine1OperatingTime')
    t2 = solver.NumVar(0.0, solver.infinity(), 'Machine2OperatingTime')
    
    # Parameters (rates)
    heart_rate_m1 = 0.5   # Machine 1 heart medicine rate [units/min]
    heart_rate_m2 = 0.3   # Machine 2 heart medicine rate [units/min]
    brain_rate_m1 = 0.8   # Machine 1 brain medicine rate [units/min]
    brain_rate_m2 = 1.0   # Machine 2 brain medicine rate [units/min]
    waste_rate_m1 = 0.3   # Machine 1 waste rate [units/min]
    waste_rate_m2 = 0.5   # Machine 2 waste rate [units/min]
    
    # Constraints limits
    max_heart = 8.0  # maximum heart medicine [units]
    min_brain = 4.0  # minimum brain medicine [units]
    
    # Constraints
    # Heart medicine constraint: 0.5 * t1 + 0.3 * t2 <= 8
    solver.Add(heart_rate_m1 * t1 + heart_rate_m2 * t2 <= max_heart)
    
    # Brain medicine constraint: 0.8 * t1 + 1.0 * t2 >= 4
    solver.Add(brain_rate_m1 * t1 + brain_rate_m2 * t2 >= min_brain)
    
    # Objective: minimize total waste: 0.3 * t1 + 0.5 * t2
    objective = solver.Objective()
    objective.SetCoefficient(t1, waste_rate_m1)
    objective.SetCoefficient(t2, waste_rate_m2)
    objective.SetMinimization()
    
    # Solve the problem and return the results
    result_status = solver.Solve()
    
    if result_status == pywraplp.Solver.OPTIMAL:
        solution = {
            "variables": {
                "Machine1OperatingTime": t1.solution_value(),
                "Machine2OperatingTime": t2.solution_value(),
            },
            "objective": objective.Value()
        }
        return solution
    else:
        print("The problem does not have an optimal solution.")
        return None

def main():
    # Since the mathematical formulation leads to a unique model,
    # we implement the problem using a single version.
    # If there were multiple formulations, we would implement them as separate models.
    
    # Solve the linear model using ortools linear solver.
    linear_solution = solve_linear_model()
    
    # Print solutions in a structured output format.
    print("Linear Model Solution:")
    if linear_solution:
        print(linear_solution)
    else:
        print("No feasible solution found for the linear model.")

if __name__ == "__main__":
    main()

'''Execution Results:
SUCCESS:
Linear Model Solution:
{'variables': {'Machine1OperatingTime': 4.999999999999999, 'Machine2OperatingTime': 0.0}, 'objective': 1.4999999999999998}
'''

'''Expected Output:
Expected solution

: {'variables': {'Machine1OperatingTime': 5.0, 'Machine2OperatingTime': 0.0}, 'objective': 1.5}'''

