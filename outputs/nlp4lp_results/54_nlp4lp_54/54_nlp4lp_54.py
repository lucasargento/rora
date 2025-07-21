# Problem Description:
'''Problem description: A clinic employs nurses and pharmacists to deliver shots to patients. A nurse works 5 hours per shift while a pharmacist works 7 hours per shift. Nurses are paid $250 per shift while pharmacists are paid $300 per shift. Currently, the clinic needs 200 hours of healthcare labor to meet needs. If the firm has a budget of $9000, how many of each healthcare worker should be scheduled to minimize the total number of workers?

Expected Output Schema:
{
  "variables": {
    "NumberOfNurseShifts": "float",
    "NumberOfPharmacistShifts": "float",
    "NumberOfNurses": "float",
    "NumberOfPharmacists": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''{
  "Sets": {
    "WorkerTypes": ["Nurse", "Pharmacist"]
  },
  "Parameters": {
    "nurse_shift_hours": {
      "value": 5,
      "units": "hours per shift",
      "description": "Number of work hours provided by one nurse shift"
    },
    "pharmacist_shift_hours": {
      "value": 7,
      "units": "hours per shift",
      "description": "Number of work hours provided by one pharmacist shift"
    },
    "nurse_cost_per_shift": {
      "value": 250,
      "units": "USD per shift",
      "description": "Cost to employ a nurse for one shift"
    },
    "pharmacist_cost_per_shift": {
      "value": 300,
      "units": "USD per shift",
      "description": "Cost to employ a pharmacist for one shift"
    },
    "required_hours": {
      "value": 200,
      "units": "hours",
      "description": "Total required healthcare labor hours to be delivered"
    },
    "budget": {
      "value": 9000,
      "units": "USD",
      "description": "Total budget available to pay for the shifts"
    }
  },
  "Variables": {
    "NumberOfNurseShifts": {
      "type": "integer",
      "lower_bound": 0,
      "description": "Number of nurse shifts scheduled"
    },
    "NumberOfPharmacistShifts": {
      "type": "integer",
      "lower_bound": 0,
      "description": "Number of pharmacist shifts scheduled"
    },
    "NumberOfNurses": {
      "type": "integer",
      "lower_bound": 0,
      "description": "Number of nurses scheduled; assumed one shift corresponds to one nurse"
    },
    "NumberOfPharmacists": {
      "type": "integer",
      "lower_bound": 0,
      "description": "Number of pharmacists scheduled; assumed one shift corresponds to one pharmacist"
    }
  },
  "Objective": {
    "expression": "NumberOfNurseShifts + NumberOfPharmacistShifts",
    "sense": "minimize",
    "description": "Minimize the total number of healthcare workers scheduled"
  },
  "Constraints": {
    "HealthcareHoursConstraint": "5 * NumberOfNurseShifts + 7 * NumberOfPharmacistShifts >= 200",
    "BudgetConstraint": "250 * NumberOfNurseShifts + 300 * NumberOfPharmacistShifts <= 9000",
    "NurseShiftWorkerLink": "NumberOfNurseShifts == NumberOfNurses",
    "PharmacistShiftWorkerLink": "NumberOfPharmacistShifts == NumberOfPharmacists"
  }
}'''

# Generated Code:
#!/usr/bin/env python3
"""
This script solves the clinic scheduling problem using two separate implementations with OR-Tools.
Implementation 1 uses only the "shift" variables.
Implementation 2 uses four separate variables (nurse shifts, pharmacist shifts, and their worker equivalents)
with linking constraints.
Both models minimize the total number of workers (shifts) subject to:
  - Providing at least 200 healthcare hours.
  - Spending no more than 9000 USD on shifts.
"""

from ortools.linear_solver import pywraplp

def solve_model_version1():
    # Create the solver using CBC_MIXED_INTEGER_PROGRAMMING
    solver = pywraplp.Solver.CreateSolver('CBC_MIXED_INTEGER_PROGRAMMING')
    if not solver:
        print("Solver not found.")
        return None

    # Decision variables: Only shift variables
    nurse_shifts = solver.IntVar(0, solver.infinity(), 'NumberOfNurseShifts')
    pharmacist_shifts = solver.IntVar(0, solver.infinity(), 'NumberOfPharmacistShifts')
    # In this model, the number of workers equals the number of shifts.
    nurses = nurse_shifts
    pharmacists = pharmacist_shifts

    # Parameters
    nurse_shift_hours = 5
    pharmacist_shift_hours = 7
    nurse_cost = 250
    pharmacist_cost = 300
    required_hours = 200
    budget = 9000

    # Constraints:
    # Healthcare Hours Constraint: 5 * nurse_shifts + 7 * pharmacist_shifts >= 200
    solver.Add(nurse_shift_hours * nurse_shifts + pharmacist_shift_hours * pharmacist_shifts >= required_hours)

    # Budget Constraint: 250 * nurse_shifts + 300 * pharmacist_shifts <= 9000
    solver.Add(nurse_cost * nurse_shifts + pharmacist_cost * pharmacist_shifts <= budget)

    # Objective: Minimize the total number of healthcare workers scheduled
    objective = solver.Objective()
    objective.SetCoefficient(nurse_shifts, 1)
    objective.SetCoefficient(pharmacist_shifts, 1)
    objective.SetMinimization()

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "variables": {
                "NumberOfNurseShifts": nurse_shifts.solution_value(),
                "NumberOfPharmacistShifts": pharmacist_shifts.solution_value(),
                "NumberOfNurses": nurses.solution_value(),
                "NumberOfPharmacists": pharmacists.solution_value()
            },
            "objective": objective.Value()
        }
        return result
    else:
        return {"error": "No optimal solution found in Model Version 1."}

def solve_model_version2():
    # Create the solver using CBC_MIXED_INTEGER_PROGRAMMING
    solver = pywraplp.Solver.CreateSolver('CBC_MIXED_INTEGER_PROGRAMMING')
    if not solver:
        print("Solver not found.")
        return None

    # Decision variables: Separate variables for shifts and worker counts.
    nurse_shifts = solver.IntVar(0, solver.infinity(), 'NumberOfNurseShifts')
    pharmacist_shifts = solver.IntVar(0, solver.infinity(), 'NumberOfPharmacistShifts')
    nurses = solver.IntVar(0, solver.infinity(), 'NumberOfNurses')
    pharmacists = solver.IntVar(0, solver.infinity(), 'NumberOfPharmacists')

    # Parameters
    nurse_shift_hours = 5
    pharmacist_shift_hours = 7
    nurse_cost = 250
    pharmacist_cost = 300
    required_hours = 200
    budget = 9000

    # Constraints:
    # Healthcare Hours Constraint: 5 * nurse_shifts + 7 * pharmacist_shifts >= 200
    solver.Add(nurse_shift_hours * nurse_shifts + pharmacist_shift_hours * pharmacist_shifts >= required_hours)

    # Budget Constraint: 250 * nurse_shifts + 300 * pharmacist_shifts <= 9000
    solver.Add(nurse_cost * nurse_shifts + pharmacist_cost * pharmacist_shifts <= budget)

    # Linking constraints: number of shifts equals number of workers.
    solver.Add(nurse_shifts == nurses)
    solver.Add(pharmacist_shifts == pharmacists)

    # Objective: Minimize the total number of healthcare workers scheduled.
    objective = solver.Objective()
    objective.SetCoefficient(nurse_shifts, 1)
    objective.SetCoefficient(pharmacist_shifts, 1)
    objective.SetMinimization()

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "variables": {
                "NumberOfNurseShifts": nurse_shifts.solution_value(),
                "NumberOfPharmacistShifts": pharmacist_shifts.solution_value(),
                "NumberOfNurses": nurses.solution_value(),
                "NumberOfPharmacists": pharmacists.solution_value()
            },
            "objective": objective.Value()
        }
        return result
    else:
        return {"error": "No optimal solution found in Model Version 2."}

def main():
    print("Solving Model Version 1 (Using shift variables only):")
    result_v1 = solve_model_version1()
    print(result_v1)
    print("\nSolving Model Version 2 (Using separate shift and worker variables with linking constraints):")
    result_v2 = solve_model_version2()
    print(result_v2)

if __name__ == "__main__":
    main()

'''Execution Results:
SUCCESS:
Solving Model Version 1 (Using shift variables only):
{'variables': {'NumberOfNurseShifts': 0.0, 'NumberOfPharmacistShifts': 29.0, 'NumberOfNurses': 0.0, 'NumberOfPharmacists': 29.0}, 'objective': 29.0}

Solving Model Version 2 (Using separate shift and worker variables with linking constraints):
{'variables': {'NumberOfNurseShifts': 0.0, 'NumberOfPharmacistShifts': 29.0, 'NumberOfNurses': 0.0, 'NumberOfPharmacists': 29.0}, 'objective': 29.0}
'''

'''Expected Output:
Expected solution

: {'variables': {'NumberOfNurseShifts': 12.0, 'NumberOfPharmacistShifts': 20.0, 'NumberOfNurses': -0.0, 'NumberOfPharmacists': -0.0}, 'objective': 0.0}'''

