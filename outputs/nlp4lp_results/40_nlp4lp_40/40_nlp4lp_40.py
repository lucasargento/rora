# Problem Description:
'''Problem description: There are two processes, process A and process B, to plate a coin with gold. Process A requires 3 units of gold, 2 wires, and can plate 5 coins. Process B requires 5 units of gold, 3 wires, and can plate 7 coins. There are 500 units of gold and 300 wires available. How many processes of each type should be run to maximize the total number of coins that can be plated?

Expected Output Schema:
{
  "variables": {
    "ExecuteProcessA": "float",
    "ExecuteProcessB": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- P: set of processes = {ProcessA, ProcessB}

Parameters:
- goldRequired[ProcessA] = 3 (units of gold per execution of ProcessA)
- wireRequired[ProcessA] = 2 (units of wires per execution of ProcessA)
- coinsProduced[ProcessA] = 5 (coins plated per execution of ProcessA)
- goldRequired[ProcessB] = 5 (units of gold per execution of ProcessB)
- wireRequired[ProcessB] = 3 (units of wires per execution of ProcessB)
- coinsProduced[ProcessB] = 7 (coins plated per execution of ProcessB)
- totalGoldAvailable = 500 (total units of gold available)
- totalWiresAvailable = 300 (total units of wires available)
  
Variables:
- ExecuteProcessA: number of times ProcessA is executed (nonnegative, float; can be later restricted to integer if required)
- ExecuteProcessB: number of times ProcessB is executed (nonnegative, float; can be later restricted to integer if required)

Objective:
- Maximize total number of coins plated, defined as:
  TotalCoins = (coinsProduced[ProcessA] * ExecuteProcessA) + (coinsProduced[ProcessB] * ExecuteProcessB)

Constraints:
1. Gold constraint:
   (goldRequired[ProcessA] * ExecuteProcessA) + (goldRequired[ProcessB] * ExecuteProcessB) <= totalGoldAvailable

2. Wire constraint:
   (wireRequired[ProcessA] * ExecuteProcessA) + (wireRequired[ProcessB] * ExecuteProcessB) <= totalWiresAvailable

Model Comments:
- All units are assumed consistent: gold in units, wires in units, coins as output quantity.
- The decision variables represent the number of times each process is executed. Although defined as float here, if the process executions must be whole numbers, they can be required to be integers.
- The objective function focuses solely on maximizing the total coins plated and does not consider any cost since none were provided.

Expected Output Schema:
{
  "variables": {
    "ExecuteProcessA": "float",
    "ExecuteProcessB": "float"
  },
  "objective": "float"
}'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_continuous_model():
    # Create the solver using the GLOP back-end (for continuous LP)
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Solver not created for the continuous model.")
        return None

    # Decision Variables: continuous
    ExecuteProcessA = solver.NumVar(0.0, solver.infinity(), 'ExecuteProcessA')
    ExecuteProcessB = solver.NumVar(0.0, solver.infinity(), 'ExecuteProcessB')

    # Parameters (given data)
    goldRequiredA = 3
    wireRequiredA = 2
    coinsProducedA = 5
    goldRequiredB = 5
    wireRequiredB = 3
    coinsProducedB = 7
    totalGoldAvailable = 500
    totalWiresAvailable = 300

    # Constraints:
    # Gold constraint: 3 * ExecuteProcessA + 5 * ExecuteProcessB <= 500
    solver.Add(goldRequiredA * ExecuteProcessA + goldRequiredB * ExecuteProcessB <= totalGoldAvailable)
    # Wire constraint: 2 * ExecuteProcessA + 3 * ExecuteProcessB <= 300
    solver.Add(wireRequiredA * ExecuteProcessA + wireRequiredB * ExecuteProcessB <= totalWiresAvailable)

    # Objective: Maximize total coins produced
    objective = solver.Maximize(coinsProducedA * ExecuteProcessA + coinsProducedB * ExecuteProcessB)

    status = solver.Solve()

    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "model": "Continuous LP Model",
            "variables": {
                "ExecuteProcessA": ExecuteProcessA.solution_value(),
                "ExecuteProcessB": ExecuteProcessB.solution_value()
            },
            "objective": solver.Objective().Value()
        }
    else:
        result = {
            "model": "Continuous LP Model",
            "status": "No optimal solution found."
        }
    return result

def solve_integer_model():
    # Create the solver using the CBC_MIXED_INTEGER_PROGRAMMING back-end (for integer MIP)
    solver = pywraplp.Solver.CreateSolver('CBC_MIXED_INTEGER_PROGRAMMING')
    if not solver:
        print("Solver not created for the integer model.")
        return None

    # Decision Variables: integer (non-negative)
    ExecuteProcessA = solver.IntVar(0, solver.infinity(), 'ExecuteProcessA')
    ExecuteProcessB = solver.IntVar(0, solver.infinity(), 'ExecuteProcessB')

    # Parameters (given data)
    goldRequiredA = 3
    wireRequiredA = 2
    coinsProducedA = 5
    goldRequiredB = 5
    wireRequiredB = 3
    coinsProducedB = 7
    totalGoldAvailable = 500
    totalWiresAvailable = 300

    # Constraints:
    # Gold constraint: 3 * ExecuteProcessA + 5 * ExecuteProcessB <= 500
    solver.Add(goldRequiredA * ExecuteProcessA + goldRequiredB * ExecuteProcessB <= totalGoldAvailable)
    # Wire constraint: 2 * ExecuteProcessA + 3 * ExecuteProcessB <= 300
    solver.Add(wireRequiredA * ExecuteProcessA + wireRequiredB * ExecuteProcessB <= totalWiresAvailable)

    # Objective: Maximize total coins produced
    solver.Maximize(coinsProducedA * ExecuteProcessA + coinsProducedB * ExecuteProcessB)

    status = solver.Solve()

    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "model": "Integer MIP Model",
            "variables": {
                "ExecuteProcessA": ExecuteProcessA.solution_value(),
                "ExecuteProcessB": ExecuteProcessB.solution_value()
            },
            "objective": solver.Objective().Value()
        }
    else:
        result = {
            "model": "Integer MIP Model",
            "status": "No optimal solution found."
        }
    return result

def main():
    continuous_result = solve_continuous_model()
    integer_result = solve_integer_model()

    print("Optimization Results:")
    print("--------------------------------------------------")
    if continuous_result:
        print("Continuous LP Model Result:")
        for key, value in continuous_result.items():
            print(f"{key}: {value}")
    else:
        print("Continuous LP Model encountered an error.")
    print("--------------------------------------------------")
    if integer_result:
        print("Integer MIP Model Result:")
        for key, value in integer_result.items():
            print(f"{key}: {value}")
    else:
        print("Integer MIP Model encountered an error.")
        
if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Optimization Results:
--------------------------------------------------
Continuous LP Model Result:
model: Continuous LP Model
variables: {'ExecuteProcessA': 149.99999999999997, 'ExecuteProcessB': 0.0}
objective: 749.9999999999999
--------------------------------------------------
Integer MIP Model Result:
model: Integer MIP Model
variables: {'ExecuteProcessA': 150.0, 'ExecuteProcessB': 0.0}
objective: 750.0
'''

'''Expected Output:
Expected solution

: {'variables': {'ExecuteProcessA': 150.0, 'ExecuteProcessB': 0.0}, 'objective': 750.0}'''

