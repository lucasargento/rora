# Problem Description:
'''Problem description: A research group is making fabric and plastic using two methods, method A and method B. Method A produces 25 units of fabric and 14 units of plastic per hour. Method B produces 45 units of fabric and 25 units of plastic per hour. Method A requires 60 units of a special element while method B requires 65 units of the same special element. The research group has available 3500 units of the special element and must make at least 1400 units of fabric and 1000 units of plastic. How many of each method should be executed to minimize the total time needed?

Expected Output Schema:
{
  "variables": {
    "OperationTime": {
      "0": "float",
      "1": "float"
    },
    "TotalTime": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''{
  "Sets": {
    "Methods": ["A", "B"]
  },
  "Parameters": {
    "fabricPerHour": {
      "A": 25,          // fabric units produced per hour by Method A (units/hour)
      "B": 45           // fabric units produced per hour by Method B (units/hour)
    },
    "plasticPerHour": {
      "A": 14,          // plastic units produced per hour by Method A (units/hour)
      "B": 25           // plastic units produced per hour by Method B (units/hour)
    },
    "elementUsagePerHour": {
      "A": 60,          // special element units consumed per hour by Method A (units/hour)
      "B": 65           // special element units consumed per hour by Method B (units/hour)
    },
    "totalElementAvailable": 3500,  // total available special element units
    "requiredFabric": 1400,         // minimum required fabric units
    "requiredPlastic": 1000         // minimum required plastic units
  },
  "Variables": {
    "OperationTime": {
      "A": "float >= 0",   // hours to run Method A
      "B": "float >= 0"    // hours to run Method B
    },
    "TotalTime": "float"     // total operating time (hours), defined as OperationTime[A] + OperationTime[B]
  },
  "Objective": "Minimize TotalTime = OperationTime[A] + OperationTime[B]",
  "Constraints": [
    "Fabric production: fabricPerHour[A] * OperationTime[A] + fabricPerHour[B] * OperationTime[B] >= requiredFabric",
    "Plastic production: plasticPerHour[A] * OperationTime[A] + plasticPerHour[B] * OperationTime[B] >= requiredPlastic",
    "Special element usage: elementUsagePerHour[A] * OperationTime[A] + elementUsagePerHour[B] * OperationTime[B] <= totalElementAvailable"
  ]
}'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_with_linear_solver():
    # Create the linear solver with the CBC backend.
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Failed to create solver.")
        return None

    # Parameters.
    fabric_per_hour = {'A': 25, 'B': 45}
    plastic_per_hour = {'A': 14, 'B': 25}
    element_usage_per_hour = {'A': 60, 'B': 65}
    total_element_available = 3500
    required_fabric = 1400
    required_plastic = 1000

    # Decision variables: Operation time for method A and B (continuous, non-negative).
    op_time_A = solver.NumVar(0, solver.infinity(), 'OperationTime_A')
    op_time_B = solver.NumVar(0, solver.infinity(), 'OperationTime_B')

    # Total operating time is defined as the sum of operation times.
    total_time = solver.Sum([op_time_A, op_time_B])

    # Constraint: Fabric production must be at least required_fabric.
    solver.Add(fabric_per_hour['A'] * op_time_A + fabric_per_hour['B'] * op_time_B >= required_fabric)

    # Constraint: Plastic production must be at least required_plastic.
    solver.Add(plastic_per_hour['A'] * op_time_A + plastic_per_hour['B'] * op_time_B >= required_plastic)

    # Constraint: Special element usage must not exceed available amount.
    solver.Add(element_usage_per_hour['A'] * op_time_A + element_usage_per_hour['B'] * op_time_B <= total_element_available)

    # Objective: Minimize the total operating time.
    solver.Minimize(total_time)

    # Solve the model.
    solution_status = solver.Solve()

    result = {}
    if solution_status == pywraplp.Solver.OPTIMAL or solution_status == pywraplp.Solver.FEASIBLE:
        result = {
            "variables": {
                "OperationTime": {
                    "A": op_time_A.solution_value(),
                    "B": op_time_B.solution_value()
                },
                "TotalTime": total_time.solution_value()
            },
            "objective": total_time.solution_value()
        }
    else:
        result = {"message": "The problem does not have a feasible solution."}

    return result

def main():
    # Since there is only one valid formulation for this problem,
    # we are implementing it using a linear programming model.
    result_linear = solve_with_linear_solver()
    
    # Print results in a structured way.
    print("----- Linear Solver (OR-Tools Linear) Results -----")
    if "message" in result_linear:
        print(result_linear["message"])
    else:
        print("Optimal Variables:")
        print("  OperationTime:")
        print("    Method A:", result_linear["variables"]["OperationTime"]["A"])
        print("    Method B:", result_linear["variables"]["OperationTime"]["B"])
        print("  Total Time:", result_linear["variables"]["TotalTime"])
        print("Optimal Objective (TotalTime):", result_linear["objective"])

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
----- Linear Solver (OR-Tools Linear) Results -----
Optimal Variables:
  OperationTime:
    Method A: 0.0
    Method B: 40.0
  Total Time: 40.0
Optimal Objective (TotalTime): 40.0
'''

'''Expected Output:
Expected solution

: {'variables': {'OperationTime': {'0': 0.0, '1': 53.84615384615385}, 'TotalTime': 0.0}, 'objective': 0.0}'''

