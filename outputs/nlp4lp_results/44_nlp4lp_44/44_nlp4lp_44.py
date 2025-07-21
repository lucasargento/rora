# Problem Description:
'''Problem description: An amusement park is installing ticket machines, both cash-based and card-only machines. A cash-based machine can process 20 people per hour while a card-only machine can process 30 people per hour. The cash-based machine needs 4 rolls of paper per hour while the card-only machine requires 5 rolls of paper per hour. The amusement park needs to be able to process at least 500 people per hour but can use at most 90 rolls of paper per hour. Since most people prefer to pay by cash, the number of card-only machines must not exceed the number of cash-based machines. How many of each machine should be bought to minimize the total number of machines in the park?

Expected Output Schema:
{
  "variables": {
    "NumCashMachines": "float",
    "NumCardMachines": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- M: set of machine types = {Cash, Card}

Parameters:
- capacity_Cash: processing capacity of one cash-based machine [persons per hour] = 20
- capacity_Card: processing capacity of one card-only machine [persons per hour] = 30
- paper_Cash: paper usage of one cash-based machine [rolls per hour] = 4
- paper_Card: paper usage of one card-only machine [rolls per hour] = 5
- min_persons: minimum processing requirement [persons per hour] = 500
- max_rolls: maximum available paper rolls per hour = 90

Variables:
- NumCashMachines: number of cash-based ticket machines, integer ≥ 0 [units]
- NumCardMachines: number of card-only ticket machines, integer ≥ 0 [units]

Objective:
- Minimize TotalMachines = NumCashMachines + NumCardMachines
  (This minimizes the total number of machines installed.)

Constraints:
1. Processing capacity constraint:
   20 * NumCashMachines + 30 * NumCardMachines ≥ 500
   (Ensures that at least 500 persons can be processed per hour.)
2. Paper usage constraint:
   4 * NumCashMachines + 5 * NumCardMachines ≤ 90
   (Ensures that the park does not use more than 90 rolls of paper per hour.)
3. Machine preference constraint:
   NumCardMachines ≤ NumCashMachines
   (Since most people prefer to pay by cash, there cannot be more card-only machines than cash-based ones.)'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_linear_model():
    # Create the linear solver with SCIP.
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        print("Solver not created.")
        return None

    # Variables: Number of Cash Machines and Card Machines (non-negative integers)
    num_cash = solver.IntVar(0, solver.infinity(), 'NumCashMachines')
    num_card = solver.IntVar(0, solver.infinity(), 'NumCardMachines')

    # Constraints:
    # 1. Processing capacity: 20*num_cash + 30*num_card >= 500
    solver.Add(20 * num_cash + 30 * num_card >= 500)

    # 2. Paper usage: 4*num_cash + 5*num_card <= 90
    solver.Add(4 * num_cash + 5 * num_card <= 90)

    # 3. Machine preference: num_card <= num_cash
    solver.Add(num_card <= num_cash)

    # Objective: minimize total machines (num_cash + num_card)
    objective = solver.Objective()
    objective.SetCoefficient(num_cash, 1)
    objective.SetCoefficient(num_card, 1)
    objective.SetMinimization()

    status = solver.Solve()

    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result['variables'] = {
            'NumCashMachines': num_cash.solution_value(),
            'NumCardMachines': num_card.solution_value()
        }
        result['objective'] = objective.Value()
    elif status == pywraplp.Solver.INFEASIBLE:
        result['error'] = "No feasible solution exists."
    else:
        result['error'] = "Solver ended with non-optimal status."

    return result

def main():
    results = {}
    # Only one formulation has been implemented (linear programming model).
    results['Implementation_1'] = solve_linear_model()
    
    # Print the outputs for all implementations in a structured way.
    print("Results from both implementations:")
    for key, res in results.items():
        print(f"{key}: {res}")

if __name__ == "__main__":
    main()

'''Execution Results:
SUCCESS:
Results from both implementations:
Implementation_1: {'variables': {'NumCashMachines': 10.0, 'NumCardMachines': 10.0}, 'objective': 20.0}
'''

'''Expected Output:
Expected solution

: {'variables': {'NumCashMachines': 10.0, 'NumCardMachines': 10.0}, 'objective': 20.0}'''

