# Problem Description:
'''Problem description: A popup clinic is doing virus testing with either spit tests or swabs. A spit test takes 10 minutes to administer while a  swab takes 15 minutes to administer. Since the spit test is more accurate, at least twice as many spit tests should be given as  swabs. However, at least 20  swabs must be administers. If the popup clinic operates for 8000 minutes, maximize the number of tests that can be administered.

Expected Output Schema:
{
  "variables": {
    "NumberOfSpitTests": "float",
    "NumberOfSwabTests": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- T: set of test types = {Spit, Swab}

Parameters:
- time_Spit: time to administer one spit test = 10 (minutes per test)
- time_Swab: time to administer one swab test = 15 (minutes per test)
- total_operating_time: available clinic operating time = 8000 (minutes)
- min_swab_tests: minimum number of swab tests = 20 (tests)
- spit_swab_ratio: minimum ratio of spit tests to swab tests = 2 (i.e., number of spit tests must be ≥ 2 × number of swab tests)

Variables:
- NumberOfSpitTests: number of spit tests administered [float, nonnegative]
- NumberOfSwabTests: number of swab tests administered [float, nonnegative]

Objective:
- Maximize total tests administered = NumberOfSpitTests + NumberOfSwabTests

Constraints:
1. Time constraint: (time_Spit × NumberOfSpitTests) + (time_Swab × NumberOfSwabTests) ≤ total_operating_time
2. Accuracy constraint: NumberOfSpitTests ≥ spit_swab_ratio × NumberOfSwabTests
3. Minimum swab tests: NumberOfSwabTests ≥ min_swab_tests

Comments:
- All time units are in minutes.
- Although tests are countable items and typically should be integers, the variable type is specified as float per the expected output schema.
- The objective is to maximize the total number of administered tests under the available operating time and quality constraints.'''

# Generated Code:
from ortools.linear_solver import pywraplp
from ortools.sat.python import cp_model

def solve_using_linear_solver():
    # Create the linear solver with the GLOP backend.
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Linear solver not available.")
        return None

    # Parameters
    time_spit = 10.0
    time_swab = 15.0
    total_operating_time = 8000.0
    min_swab_tests = 20.0
    spit_swab_ratio = 2.0

    # Variables: Using continuous (float) variables
    NumberOfSpitTests = solver.NumVar(0.0, solver.infinity(), 'NumberOfSpitTests')
    NumberOfSwabTests = solver.NumVar(0.0, solver.infinity(), 'NumberOfSwabTests')

    # Constraints
    # 1. Time constraint: 10*spit + 15*swab <= 8000
    solver.Add(time_spit * NumberOfSpitTests + time_swab * NumberOfSwabTests <= total_operating_time)
    # 2. Accuracy constraint: spit >= 2 * swab
    solver.Add(NumberOfSpitTests >= spit_swab_ratio * NumberOfSwabTests)
    # 3. Minimum swab tests: swab >= 20
    solver.Add(NumberOfSwabTests >= min_swab_tests)

    # Objective: Maximize total tests = spit + swab
    solver.Maximize(NumberOfSpitTests + NumberOfSwabTests)

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "variables": {
                "NumberOfSpitTests": NumberOfSpitTests.solution_value(),
                "NumberOfSwabTests": NumberOfSwabTests.solution_value()
            },
            "objective": NumberOfSpitTests.solution_value() + NumberOfSwabTests.solution_value()
        }
    else:
        result = None
    return result

def solve_using_cp_model():
    # CP-SAT model: We will use integer variables as CP-SAT does not support continuous domains.
    # Given tests are countable, integer solution is acceptable.
    model = cp_model.CpModel()

    # Parameters
    time_spit = 10
    time_swab = 15
    total_operating_time = 8000
    min_swab_tests = 20
    spit_swab_ratio = 2

    # Define a reasonable upper bound for the tests; we can use the scenario that all time is spent on the faster test.
    # Maximum spit tests possible = total_operating_time/time_spit = 8000/10 = 800.
    upper_bound_spit = 8000 // time_spit
    # Similarly, upper bound for swab tests:
    upper_bound_swab = 8000 // time_swab

    NumberOfSpitTests = model.NewIntVar(0, upper_bound_spit, 'NumberOfSpitTests')
    NumberOfSwabTests = model.NewIntVar(min_swab_tests, upper_bound_swab, 'NumberOfSwabTests')

    # Constraints:
    # 1. Time constraint: 10*spit + 15*swab <= 8000
    model.Add(time_spit * NumberOfSpitTests + time_swab * NumberOfSwabTests <= total_operating_time)
    # 2. Accuracy constraint: spit >= 2 * swab
    model.Add(NumberOfSpitTests >= spit_swab_ratio * NumberOfSwabTests)

    # Objective: maximize total tests = spit + swab
    model.Maximize(NumberOfSpitTests + NumberOfSwabTests)

    # Solve the model.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        result = {
            "variables": {
                "NumberOfSpitTests": float(solver.Value(NumberOfSpitTests)),
                "NumberOfSwabTests": float(solver.Value(NumberOfSwabTests))
            },
            "objective": float(solver.ObjectiveValue())
        }
    else:
        result = None
    return result

def main():
    linear_solution = solve_using_linear_solver()
    cp_solution = solve_using_cp_model()

    print("Linear Solver Model Solution:")
    if linear_solution:
        print(linear_solution)
    else:
        print("No solution found using the linear solver.")

    print("\nCP-SAT Model Solution:")
    if cp_solution:
        print(cp_solution)
    else:
        print("No solution found using the CP-SAT solver.")

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Linear Solver Model Solution:
{'variables': {'NumberOfSpitTests': 770.0, 'NumberOfSwabTests': 20.0}, 'objective': 790.0}

CP-SAT Model Solution:
{'variables': {'NumberOfSpitTests': 770.0, 'NumberOfSwabTests': 20.0}, 'objective': 790.0}
'''

'''Expected Output:
Expected solution

: {'variables': {'NumberOfSpitTests': 770.0, 'NumberOfSwabTests': 20.0}, 'objective': 790.0}'''

