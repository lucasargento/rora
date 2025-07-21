# Problem Description:
'''Problem description: Sleep inducing medicine and anti-inflammatory medicine is found in two pills, pill A and pill B. One pill A contains 3 units of sleep inducing medicine and 5 units of anti-inflammatory medicine. One pill B contains 6 units of sleep-inducing medicine and 1 unit of anti-inflammatory medicine. The cost per pill for pill A is $4 and the cost per pill for pill B is $5. A patient must consume these two pills to get at least 40 units of sleep-inducing medicine and 50 units of anti-inflammatory medicine. Formulate a LP to minimize the cost for the patient.

Expected Output Schema:
{
  "variables": {
    "PillsSelected": {
      "0": "float",
      "1": "float"
    }
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''{
  "Sets": {
    "Pills": ["A", "B"]
  },
  "Parameters": {
    "sleepContent": {
      "A": 3,    /* units of sleep inducing medicine per pill A */
      "B": 6     /* units of sleep inducing medicine per pill B */
    },
    "antiContent": {
      "A": 5,    /* units of anti-inflammatory medicine per pill A */
      "B": 1     /* units of anti-inflammatory medicine per pill B */
    },
    "pillCost": {
      "A": 4,    /* cost in USD per pill A */
      "B": 5     /* cost in USD per pill B */
    },
    "minSleepRequired": 40,        /* minimum required units of sleep inducing medicine */
    "minAntiRequired": 50          /* minimum required units of anti-inflammatory medicine */
  },
  "Variables": {
    "x": {
      "description": "Number of each pill selected (non-negative integer)",
      "A": "integer >= 0",
      "B": "integer >= 0"
    }
  },
  "Objective": "Minimize total cost = pillCost[A]*x[A] + pillCost[B]*x[B]",
  "Constraints": [
    {
      "name": "Sleep Medicine Constraint",
      "expression": "sleepContent[A]*x[A] + sleepContent[B]*x[B] >= minSleepRequired",
      "comment": "Ensures at least 40 units of sleep inducing medicine are obtained"
    },
    {
      "name": "Anti-inflammatory Medicine Constraint",
      "expression": "antiContent[A]*x[A] + antiContent[B]*x[B] >= minAntiRequired",
      "comment": "Ensures at least 50 units of anti-inflammatory medicine are obtained"
    }
  ]
}'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_formulation_version1():
    # Create the solver using CBC for mixed integer programming.
    solver = pywraplp.Solver.CreateSolver('CBC_MIXED_INTEGER_PROGRAMMING')
    if not solver:
        print("Solver not created.")
        return None

    # Variables: number of pill A and pill B, integer non-negative.
    xA = solver.IntVar(0, solver.infinity(), 'xA')  # Pill A
    xB = solver.IntVar(0, solver.infinity(), 'xB')  # Pill B

    # Parameters for the problem.
    sleepContent = {'A': 3, 'B': 6}
    antiContent = {'A': 5, 'B': 1}
    pillCost = {'A': 4, 'B': 5}
    minSleepRequired = 40
    minAntiRequired = 50

    # Constraints.
    # Sleep Medicine Constraint: 3*xA + 6*xB >= 40.
    solver.Add(sleepContent['A'] * xA + sleepContent['B'] * xB >= minSleepRequired)

    # Anti-inflammatory Medicine Constraint: 5*xA + 1*xB >= 50.
    solver.Add(antiContent['A'] * xA + antiContent['B'] * xB >= minAntiRequired)

    # Objective: minimize total cost = 4*xA + 5*xB.
    solver.Minimize(pillCost['A'] * xA + pillCost['B'] * xB)

    # Solve the problem.
    status = solver.Solve()
    
    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        solution = {
            "PillsSelected": {
                "0": xA.solution_value(),  # Pill A
                "1": xB.solution_value()   # Pill B
            }
        }
        objective = solver.Objective().Value()
        result = {"Version": "Formulation_Version1", "solution": solution, "objective": objective}
    else:
        result = {"Version": "Formulation_Version1", "message": "No optimal solution found. Problem infeasible or unbounded."}
    return result

def main():
    # Only one formulation version provided.
    results = []
    result_v1 = solve_formulation_version1()
    results.append(result_v1)
    
    # Print the results in a structured way.
    print("Optimization Results:")
    for res in results:
        print("------------------------------------------------")
        print("Model Version: {}".format(res.get("Version", "Unknown")))
        if "solution" in res:
            sol = res["solution"]
            print("Pill A (index 0): {}".format(sol["PillsSelected"]["0"]))
            print("Pill B (index 1): {}".format(sol["PillsSelected"]["1"]))
            print("Objective Value (Total Cost): {}".format(res["objective"]))
        else:
            print("Message: {}".format(res.get("message", "No solution information available.")))
    print("------------------------------------------------")

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Optimization Results:
------------------------------------------------
Model Version: Formulation_Version1
Pill A (index 0): 10.0
Pill B (index 1): 2.0
Objective Value (Total Cost): 50.0
------------------------------------------------
'''

'''Expected Output:
Expected solution

: {'variables': {'PillsSelected': {'0': 9.62962962962963, '1': 1.8518518518518519}}, 'objective': 47.77777777777778}'''

