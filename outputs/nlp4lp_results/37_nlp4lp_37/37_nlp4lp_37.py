# Problem Description:
'''Problem description: A school employs staff and substitute teachers. Per shift, staff teachers work 6 hours and get paid $300. Per shift, substitute teachers work 3 hours and get paid $100. For the summer term, the school requires 1000 hours of teaching availability. If the school has a budget of $40000, how many of each teacher should be hired to minimize the total number of teachers?

Expected Output Schema:
{
  "variables": {
    "NumStaffShifts": "float",
    "NumSubstituteShifts": "float",
    "NumStaffTeachers": "float",
    "NumSubstituteTeachers": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Below is one valid formulation using the five‐element framework. Note that in this formulation we represent separately the number of shifts that are “covered” (by hiring a teacher for that particular shift) and the number of teachers hired. We assume that a teacher may cover at most one shift during the summer (so the number of teachers hired must be at least the number of shifts that occur for that teacher type). All numeric values are in the units stated in the problem (hours, USD, teacher/shifts).

--------------------------------------------------------------
Sets:
• TeacherType = {Staff, Substitute}

--------------------------------------------------------------
Parameters:
• Hours_per_Shift(Staff) = 6     [hours per staff shift]
• Hours_per_Shift(Substitute) = 3  [hours per substitute shift]
• Cost_per_Shift(Staff) = 300   [USD per staff shift]
• Cost_per_Shift(Substitute) = 100  [USD per substitute shift]
• Required_Teaching_Hours = 1000  [total available teaching hours required for summer]
• Budget = 40000        [total available budget in USD]

--------------------------------------------------------------
Variables (all decision variables are assumed to be nonnegative; they may be defined as continuous but in an integer implementation they should be integers):
• NumStaffShifts: number of staff shifts assigned [number of shifts]
• NumSubstituteShifts: number of substitute shifts assigned [number of shifts]
• NumStaffTeachers: number of staff teachers hired [number of teachers]
• NumSubstituteTeachers: number of substitute teachers hired [number of teachers]

--------------------------------------------------------------
Objective:
• Minimize total teachers hired = NumStaffTeachers + NumSubstituteTeachers

--------------------------------------------------------------
Constraints:
1. Teaching Availability (Cover required hours):
  ( Hours_per_Shift(Staff) * NumStaffShifts ) + ( Hours_per_Shift(Substitute) * NumSubstituteShifts ) ≥ Required_Teaching_Hours
  i.e., 6 * NumStaffShifts + 3 * NumSubstituteShifts ≥ 1000

2. Budget Constraint:
  ( Cost_per_Shift(Staff) * NumStaffShifts ) + ( Cost_per_Shift(Substitute) * NumSubstituteShifts ) ≤ Budget
  i.e., 300 * NumStaffShifts + 100 * NumSubstituteShifts ≤ 40000

3. Teacher-to-Shift Assignment:
  Because each teacher can cover at most one shift in the summer term:
  – NumStaffTeachers ≥ NumStaffShifts
  – NumSubstituteTeachers ≥ NumSubstituteShifts

--------------------------------------------------------------
Comments:
• This model uses two sets of decision variables. The “shifts” (NumStaffShifts and NumSubstituteShifts) determine the total cost and total teaching hours provided. The “teachers” (NumStaffTeachers and NumSubstituteTeachers) count the number of individuals hired. Since each teacher covers one shift at most, we require that for each teacher type the number of teachers is at least as high as the number of shifts.
• All cost and hour parameters are used consistently with the problem statement.
• The objective of minimizing total teachers is equivalent to minimizing (NumStaffTeachers + NumSubstituteTeachers).

Expected Output Schema:
{
  "variables": {
    "NumStaffShifts": "float",
    "NumSubstituteShifts": "float",
    "NumStaffTeachers": "float",
    "NumSubstituteTeachers": "float"
  },
  "objective": "float"
}

This formulation is complete and faithful to the original problem while remaining clear and unambiguous for subsequent implementation in Python or OR-Tools.'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_teacher_hiring_model():
    # Create the solver using CBC (Mixed Integer Programming)
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Solver not created.")
        return None

    # Parameters
    hours_staff = 6         # hours per staff shift
    hours_substitute = 3    # hours per substitute shift
    cost_staff = 300        # cost per staff shift in USD
    cost_substitute = 100   # cost per substitute shift in USD
    required_hours = 1000   # required total teaching hours
    budget = 40000          # total budget in USD

    # Create decision variables
    # Number of shifts must be integer.
    staff_shifts = solver.IntVar(0, solver.infinity(), "NumStaffShifts")
    substitute_shifts = solver.IntVar(0, solver.infinity(), "NumSubstituteShifts")
    # Number of teachers hired (each teacher can cover at most one shift)
    staff_teachers = solver.IntVar(0, solver.infinity(), "NumStaffTeachers")
    substitute_teachers = solver.IntVar(0, solver.infinity(), "NumSubstituteTeachers")

    # Constraints

    # 1. Teaching Availability: total teaching hours provided must be at least 1000
    solver.Add(hours_staff * staff_shifts + hours_substitute * substitute_shifts >= required_hours)

    # 2. Budget Constraint: total cost must not exceed $40000
    solver.Add(cost_staff * staff_shifts + cost_substitute * substitute_shifts <= budget)

    # 3. Teacher-to-Shift Assignment constraints (each teacher can cover at most one shift)
    solver.Add(staff_teachers >= staff_shifts)
    solver.Add(substitute_teachers >= substitute_shifts)

    # Objective: Minimize total number of teachers hired
    objective = solver.Objective()
    objective.SetCoefficient(staff_teachers, 1)
    objective.SetCoefficient(substitute_teachers, 1)
    objective.SetMinimization()

    # Solve the problem.
    status = solver.Solve()

    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result["NumStaffShifts"] = staff_shifts.solution_value()
        result["NumSubstituteShifts"] = substitute_shifts.solution_value()
        result["NumStaffTeachers"] = staff_teachers.solution_value()
        result["NumSubstituteTeachers"] = substitute_teachers.solution_value()
        result["objective"] = objective.Value()
    else:
        result = None
    return result

def main():
    # Since there is one formulation provided, we implement it as Implementation 1.
    results = {}
    impl1_solution = solve_teacher_hiring_model()
    if impl1_solution is not None:
        results["Implementation_1"] = impl1_solution
    else:
        results["Implementation_1"] = "Infeasible or no solution found."

    # Print the results in a structured way
    print("Optimal Solutions for the Teacher Hiring Problem:")
    for impl, sol in results.items():
        print("\n" + impl + ":")
        if isinstance(sol, dict):
            print("Variables:")
            print(f"  NumStaffShifts: {sol['NumStaffShifts']}")
            print(f"  NumSubstituteShifts: {sol['NumSubstituteShifts']}")
            print(f"  NumStaffTeachers: {sol['NumStaffTeachers']}")
            print(f"  NumSubstituteTeachers: {sol['NumSubstituteTeachers']}")
            print(f"Objective (Total teachers): {sol['objective']}")
        else:
            print(sol)

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Optimal Solutions for the Teacher Hiring Problem:

Implementation_1:
Variables:
  NumStaffShifts: 66.0
  NumSubstituteShifts: 202.0
  NumStaffTeachers: 66.0
  NumSubstituteTeachers: 202.0
Objective (Total teachers): 268.0
'''

'''Expected Output:
Expected solution

: {'variables': 
{'NumStaffShifts': 0.0, 
'NumSubstituteShifts': 400.0, 
'NumStaffTeachers': -0.0, 
'NumSubstituteTeachers': -0.0}, 'objective': 0.0}'''

