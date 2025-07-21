# Problem Description:
'''Problem description: A teddy bear company produces three different colored bears: black, white, and brown. These bears are made in two different factories. Running factory 1 for 1 hour costs $300 and produces 5 black teddy bears, 6 white teddy bears, and 3 brown ones. Running factory 2 for 1 hour costs $600 and produces 10 black teddy bears and 10 white teddy bears. (but no brown ones). To meet children's demand, at least 20 black teddy bears, 5 white teddy bears, and 15 brown teddy bears must be made daily. Given this information, develop a linear programming problem assuming the teddy bear company wants to minimize the cost of production.

Expected Output Schema:
{
  "variables": {
    "RunningTime": {
      "0": "float",
      "1": "float"
    }
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Below is a precise formulation of the problem using the five-element structure:

------------------------------------------------------------
Sets:
- F: set of factories = {1, 2}
- B: set of bear colors = {black, white, brown}

------------------------------------------------------------
Parameters:
- cost[f]: production cost per hour for factory f (in USD/hour). Namely, cost[1] = 300, cost[2] = 600.
- prod[f, b]: number of bears of color b produced per hour in factory f.
  - For factory 1: prod[1, black] = 5, prod[1, white] = 6, prod[1, brown] = 3.
  - For factory 2: prod[2, black] = 10, prod[2, white] = 10, prod[2, brown] = 0.
- demand[b]: minimum number of bears that must be produced daily for each color.
  - demand[black] = 20, demand[white] = 5, demand[brown] = 15.

------------------------------------------------------------
Variables:
- x[f]: running time of factory f (in hours). Here x[1] and x[2] are continuous variables with x[f] >= 0.
  (The variable x[f] represents the number of hours factory f is operated.)

------------------------------------------------------------
Objective:
- Minimize total production cost.
  That is, minimize Z = sum over f in F of (cost[f] * x[f]).
  In this problem: Z = 300*x[1] + 600*x[2].

------------------------------------------------------------
Constraints:
For each bear color b in B, the total production from both factories must meet or exceed the daily demand.
- For black bears: prod[1, black]*x[1] + prod[2, black]*x[2] >= demand[black]
  which becomes: 5*x[1] + 10*x[2] >= 20.
- For white bears: prod[1, white]*x[1] + prod[2, white]*x[2] >= demand[white]
  which becomes: 6*x[1] + 10*x[2] >= 5.
- For brown bears: prod[1, brown]*x[1] + prod[2, brown]*x[2] >= demand[brown]
  which becomes: 3*x[1] + 0*x[2] >= 15.

------------------------------------------------------------
Additional Notes:
- All production rates and costs are given per hour, ensuring consistency in units.
- The decision variables (x[1] and x[2]) are continuous, assuming that fractional hours of operation are allowed.
- The model is linear and minimizes the total operational costs while satisfying the daily production requirements.
- In implementation, one could map the factories with indices 0 and 1 if required (e.g., RunningTime{0} corresponds to x[1] and RunningTime{1} corresponds to x[2]).

This completes the structured linear programming model for the teddy bear production problem.'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_model_version1():
    # Version 1: Variables are explicitly named x1 and x2
    # Production parameters
    cost = {1: 300, 2: 600}
    prod = {
        1: {"black": 5, "white": 6, "brown": 3},
        2: {"black": 10, "white": 10, "brown": 0}
    }
    demand = {"black": 20, "white": 5, "brown": 15}

    # Create solver using GLOP (linear programming solver)
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Solver not created.")
        return None

    # Define variables x1 and x2: running time for Factory 1 and Factory 2 respectively.
    x1 = solver.NumVar(0.0, solver.infinity(), 'x1')
    x2 = solver.NumVar(0.0, solver.infinity(), 'x2')

    # Objective: Minimize total production cost = 300*x1 + 600*x2
    objective = solver.Objective()
    objective.SetCoefficient(x1, cost[1])
    objective.SetCoefficient(x2, cost[2])
    objective.SetMinimization()

    # Constraints for each bear color:
    # Black bears: 5*x1 + 10*x2 >= 20
    black_constraint = solver.Constraint(demand["black"], solver.infinity())
    black_constraint.SetCoefficient(x1, prod[1]["black"])
    black_constraint.SetCoefficient(x2, prod[2]["black"])

    # White bears: 6*x1 + 10*x2 >= 5
    white_constraint = solver.Constraint(demand["white"], solver.infinity())
    white_constraint.SetCoefficient(x1, prod[1]["white"])
    white_constraint.SetCoefficient(x2, prod[2]["white"])

    # Brown bears: 3*x1 + 0*x2 >= 15
    brown_constraint = solver.Constraint(demand["brown"], solver.infinity())
    brown_constraint.SetCoefficient(x1, prod[1]["brown"])
    brown_constraint.SetCoefficient(x2, prod[2]["brown"])

    status = solver.Solve()

    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result['RunningTime'] = {"1": x1.solution_value(), "2": x2.solution_value()}
        result['objective'] = objective.Value()
    else:
        result['error'] = "No optimal solution found."
    return result

def solve_model_version2():
    # Version 2: Using list indexing with 0 corresponding to Factory 1 and 1 corresponding to Factory 2.
    # Production parameters (same as version 1, but index adjusted)
    cost = [300, 600]  # cost[0]=300 for factory1, cost[1]=600 for factory2
    # prod[f][bear] where f=0 (factory 1) and f=1 (factory 2)
    prod = [
        {"black": 5, "white": 6, "brown": 3},   # Factory 1
        {"black": 10, "white": 10, "brown": 0}    # Factory 2
    ]
    demand = {"black": 20, "white": 5, "brown": 15}

    # Create solver using GLOP (linear programming solver)
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Solver not created.")
        return None

    # Define variables: RunningTime[0] for Factory 1 and RunningTime[1] for Factory 2.
    RunningTime = []
    for i in range(2):
        var = solver.NumVar(0.0, solver.infinity(), f'RunningTime[{i}]')
        RunningTime.append(var)

    # Objective: Minimize total production cost = 300*RunningTime[0] + 600*RunningTime[1]
    objective = solver.Objective()
    for i in range(2):
        objective.SetCoefficient(RunningTime[i], cost[i])
    objective.SetMinimization()

    # Constraints for each bear color:
    # Black bears: 5*RunningTime[0] + 10*RunningTime[1] >= 20
    black_constraint = solver.Constraint(demand["black"], solver.infinity())
    black_constraint.SetCoefficient(RunningTime[0], prod[0]["black"])
    black_constraint.SetCoefficient(RunningTime[1], prod[1]["black"])

    # White bears: 6*RunningTime[0] + 10*RunningTime[1] >= 5
    white_constraint = solver.Constraint(demand["white"], solver.infinity())
    white_constraint.SetCoefficient(RunningTime[0], prod[0]["white"])
    white_constraint.SetCoefficient(RunningTime[1], prod[1]["white"])

    # Brown bears: 3*RunningTime[0] + 0*RunningTime[1] >= 15
    brown_constraint = solver.Constraint(demand["brown"], solver.infinity())
    brown_constraint.SetCoefficient(RunningTime[0], prod[0]["brown"])
    brown_constraint.SetCoefficient(RunningTime[1], prod[1]["brown"])

    status = solver.Solve()

    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        # Mapping to expected output schema keys: "0": value for factory1, "1": value for factory2.
        result['RunningTime'] = {"0": RunningTime[0].solution_value(), "1": RunningTime[1].solution_value()}
        result['objective'] = objective.Value()
    else:
        result['error'] = "No optimal solution found."
    return result

def main():
    results = {}
    # Solve version 1
    version1_result = solve_model_version1()
    results['Version1'] = version1_result

    # Solve version 2
    version2_result = solve_model_version2()
    results['Version2'] = version2_result

    # Print the results in a structured manner.
    print("Optimization Results:")
    for version, res in results.items():
        print(f"\n{version}:")
        if 'error' in res:
            print("  Error: " + res['error'])
        else:
            print("  Optimal RunningTimes:")
            for key, value in res['RunningTime'].items():
                print(f"    Factory {key}: {value}")
            print(f"  Objective Value: {res['objective']}")

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Optimization Results:

Version1:
  Optimal RunningTimes:
    Factory 1: 5.0
    Factory 2: 0.0
  Objective Value: 1500.0

Version2:
  Optimal RunningTimes:
    Factory 0: 5.0
    Factory 1: 0.0
  Objective Value: 1500.0
'''

'''Expected Output:
Expected solution

: {'variables': {'RunningTime': {'0': 5.0, '1': 0.0}}, 'objective': 1500.0}'''

