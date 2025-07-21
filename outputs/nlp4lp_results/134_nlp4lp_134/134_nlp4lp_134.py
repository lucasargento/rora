# Problem Description:
'''Problem description: A school is organizing a field trip to a science center and wants to hire small buses and large buses. A small bus can carry 20 students while a large bus can carry 50 students.  The school needs to provide transportation for at least 500 students.  In addition, since the parking lot is rather small, a maximum of 20% of the buses can be large buses. How many of each type of bus should be hired to minimize the total number of buses?

Expected Output Schema:
{
  "variables": {
    "NumberSmallBuses": "float",
    "NumberLargeBuses": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Below is the complete five‐element formulation for the bus hiring problem.

------------------------------------------------------------
Sets:
- BusTypes = {Small, Large}
  (This set represents the two types of buses available for hire)

------------------------------------------------------------
Parameters:
- Capacity_Small = 20 
  (Number of students that can be transported by one small bus)
- Capacity_Large = 50 
  (Number of students that can be transported by one large bus)
- Minimum_Students = 500 
  (The minimum number of students that must be transported)
- MaxFraction_Large = 0.2 
  (Maximum allowable fraction of large buses among all hired buses)

------------------------------------------------------------
Variables:
- NumberSmallBuses: integer ≥ 0 
  (The number of small buses to hire)
- NumberLargeBuses: integer ≥ 0 
  (The number of large buses to hire)

------------------------------------------------------------
Objective:
- Minimize TotalBuses, where 
  TotalBuses = NumberSmallBuses + NumberLargeBuses 
  (The goal is to minimize the total number of buses hired)

------------------------------------------------------------
Constraints:
1. Student Capacity Constraint:
   Capacity_Small * NumberSmallBuses + Capacity_Large * NumberLargeBuses ≥ Minimum_Students
   (This ensures that the hired buses can carry at least 500 students.)

2. Parking Lot (Large Bus) Constraint:
   NumberLargeBuses ≤ MaxFraction_Large * (NumberSmallBuses + NumberLargeBuses)
   (This ensures that no more than 20% of the total buses are large buses.)
   Alternatively, this constraint can be algebraically rearranged to:
   NumberSmallBuses ≥ 4 * NumberLargeBuses
   (This alternate form can sometimes simplify implementation.)

------------------------------------------------------------
For reference, the expected output schema in JSON is provided below:

{
  "variables": {
    "NumberSmallBuses": "integer (≥ 0)",
    "NumberLargeBuses": "integer (≥ 0)"
  },
  "objective": "Minimize (NumberSmallBuses + NumberLargeBuses)"
}

This complete model is self-contained and can be directly translated into implementation code.'''

# Generated Code:
from ortools.linear_solver import pywraplp

def solve_model1():
    """Model 1: Uses the parking lot constraint in its original formulation:
       NumberLargeBuses <= 0.2*(NumberSmallBuses + NumberLargeBuses)
       We reformulate it by multiplying both sides by 5:
           5 * NumberLargeBuses <= NumberSmallBuses + NumberLargeBuses  =>
           NumberSmallBuses >= 4 * NumberLargeBuses
       This implementation uses that derived linear constraint.
    """
    # Create the MIP solver using SCIP.
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        print("Solver not created for model 1.")
        return None

    # Define the integer variables for the number of buses.
    number_small = solver.IntVar(0, solver.infinity(), "NumberSmallBuses")
    number_large = solver.IntVar(0, solver.infinity(), "NumberLargeBuses")

    # Constraint 1: Student Capacity Constraint.
    # 20 * NumberSmallBuses + 50 * NumberLargeBuses >= 500
    solver.Add(20 * number_small + 50 * number_large >= 500)

    # Constraint 2: Parking lot (Large Bus) Constraint (derived version).
    # From: NumberLargeBuses <= 0.2*(NumberSmallBuses + NumberLargeBuses)
    # Multiply both sides by 5 to get: 5*NumberLargeBuses <= NumberSmallBuses + NumberLargeBuses,
    # which simplifies to: NumberSmallBuses >= 4 * NumberLargeBuses.
    solver.Add(number_small >= 4 * number_large)

    # Objective: Minimize the total number of buses hired.
    solver.Minimize(number_small + number_large)

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        solution = {
            "NumberSmallBuses": int(number_small.solution_value()),
            "NumberLargeBuses": int(number_large.solution_value()),
            "objective": int(number_small.solution_value() + number_large.solution_value())
        }
        return solution
    else:
        return {"message": "No optimal solution found in model 1."}


def solve_model2():
    """Model 2: Uses the alternate direct formulation of the parking constraint:
       NumberSmallBuses >= 4 * NumberLargeBuses
       This version explicitly adds that constraint.
    """
    # Create the MIP solver using SCIP.
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        print("Solver not created for model 2.")
        return None

    # Define the integer variables for the number of buses.
    number_small = solver.IntVar(0, solver.infinity(), "NumberSmallBuses")
    number_large = solver.IntVar(0, solver.infinity(), "NumberLargeBuses")

    # Constraint 1: Student Capacity Constraint.
    # 20 * NumberSmallBuses + 50 * NumberLargeBuses >= 500
    solver.Add(20 * number_small + 50 * number_large >= 500)

    # Constraint 2: Parking lot (Large Bus) Constraint (alternate form).
    # Directly add: NumberSmallBuses >= 4 * NumberLargeBuses.
    solver.Add(number_small >= 4 * number_large)

    # Objective: Minimize the total number of buses hired.
    solver.Minimize(number_small + number_large)

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        solution = {
            "NumberSmallBuses": int(number_small.solution_value()),
            "NumberLargeBuses": int(number_large.solution_value()),
            "objective": int(number_small.solution_value() + number_large.solution_value())
        }
        return solution
    else:
        return {"message": "No optimal solution found in model 2."}


def main():
    # Solve using Model 1
    sol1 = solve_model1()

    # Solve using Model 2
    sol2 = solve_model2()

    # Print results in a structured way.
    print("Model 1 (Constraint: NumberLargeBuses <= 0.2*(Total Buses)) solution:")
    print(sol1)
    print("\nModel 2 (Constraint: NumberSmallBuses >= 4*NumberLargeBuses) solution:")
    print(sol2)


if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Model 1 (Constraint: NumberLargeBuses <= 0.2*(Total Buses)) solution:
{'NumberSmallBuses': 16, 'NumberLargeBuses': 4, 'objective': 20}

Model 2 (Constraint: NumberSmallBuses >= 4*NumberLargeBuses) solution:
{'NumberSmallBuses': 16, 'NumberLargeBuses': 4, 'objective': 20}
'''

'''Expected Output:
Expected solution

: {'variables': {'NumberSmallBuses': 16.0, 'NumberLargeBuses': 4.0}, 'objective': 20.0}'''

