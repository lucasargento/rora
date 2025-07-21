# Problem Description:
'''Problem description: An accounting firm employs part time workers and full time workers. Full time workers work 8 hours per shift while part time workers work 4 hours per shift. In addition, full time workers are paid $300 per shift while part time workers are paid $100 per shift. Currently, the accounting firm has a project requiring 500 hours of labor. If the firm has a budget of $15000, how many of each type of worker should be scheduled to minimize the total number of workers.

Expected Output Schema:
{
  "variables": {
    "NumFullTimeWorkers": "float",
    "NumPartTimeWorkers": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- WorkerTypes = {FullTime, PartTime}

Parameters:
- FullTimeShiftHours = 8  // hours of work per full-time worker shift
- PartTimeShiftHours = 4  // hours of work per part-time worker shift
- FullTimeCost = 300  // cost per full-time worker shift in USD
- PartTimeCost = 100  // cost per part-time worker shift in USD
- RequiredLaborHours = 500  // total labor hours needed for the project
- AvailableBudget = 15000  // total available budget in USD

Variables:
- NumFullTimeWorkers: number of full-time workers scheduled (integer, ≥ 0)
- NumPartTimeWorkers: number of part-time workers scheduled (integer, ≥ 0)

Objective:
- Minimize total number of workers = NumFullTimeWorkers + NumPartTimeWorkers

Constraints:
1. Labor Hours Constraint:
  FullTimeShiftHours * NumFullTimeWorkers + PartTimeShiftHours * NumPartTimeWorkers ≥ RequiredLaborHours
  → 8 * NumFullTimeWorkers + 4 * NumPartTimeWorkers ≥ 500

2. Budget Constraint:
  FullTimeCost * NumFullTimeWorkers + PartTimeCost * NumPartTimeWorkers ≤ AvailableBudget
  → 300 * NumFullTimeWorkers + 100 * NumPartTimeWorkers ≤ 15000

----------------------------------

Following the Expected Output Schema, the key decision variables and the objective are represented as:

{
  "variables": {
    "NumFullTimeWorkers": "float", 
    "NumPartTimeWorkers": "float"
  },
  "objective": "float"
}'''

# Generated Code:
from ortools.linear_solver import pywraplp

def solve_model():
    # Create the linear solver with the CBC backend.
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        return None, "Solver not created."

    # Data parameters
    full_time_hours = 8     # hours per full-time worker shift
    part_time_hours = 4     # hours per part-time worker shift
    full_time_cost = 300    # cost per full-time worker shift in USD
    part_time_cost = 100    # cost per part-time worker shift in USD
    required_labor = 500    # required total labor hours
    available_budget = 15000  # available budget in USD

    # Decision variables
    # They are integers, but represented as float in output schema.
    num_full_time = solver.IntVar(0, solver.infinity(), 'NumFullTimeWorkers')
    num_part_time = solver.IntVar(0, solver.infinity(), 'NumPartTimeWorkers')

    # Objective: minimize total number of workers = num_full_time + num_part_time
    solver.Minimize(num_full_time + num_part_time)

    # Constraint 1: Labor hours: 8 * num_full_time + 4 * num_part_time >= 500
    solver.Add(full_time_hours * num_full_time + part_time_hours * num_part_time >= required_labor)

    # Constraint 2: Budget: 300 * num_full_time + 100 * num_part_time <= 15000
    solver.Add(full_time_cost * num_full_time + part_time_cost * num_part_time <= available_budget)

    # Solve the model.
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        # Return the results in a structured dictionary.
        result = {
            "NumFullTimeWorkers": num_full_time.solution_value(),
            "NumPartTimeWorkers": num_part_time.solution_value(),
            "objective": solver.Objective().Value()
        }
        return result, None
    elif status == pywraplp.Solver.FEASIBLE:
        return None, "A feasible solution was found, but it may not be optimal."
    else:
        return None, "The solver could not find a feasible solution."

def main():
    # Since only one valid formulation is provided, we call only one model.
    result, error = solve_model()
    
    print("========== Optimization Results ==========")
    if result:
        print("Optimal Solution Found:")
        print(f" - Number of Full-Time Workers: {result['NumFullTimeWorkers']}")
        print(f" - Number of Part-Time Workers: {result['NumPartTimeWorkers']}")
        print(f" - Total Number of Workers (Objective Value): {result['objective']}")
    else:
        print(f"Solver Status Issue: {error}")

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
========== Optimization Results ==========
Optimal Solution Found:
 - Number of Full-Time Workers: 25.0
 - Number of Part-Time Workers: 75.0
 - Total Number of Workers (Objective Value): 100.0
'''

'''Expected Output:
Expected solution

: {'variables': {'NumFullTimeWorkers': 25.0, 'NumPartTimeWorkers': 75.0}, 'objective': 100.0}'''

