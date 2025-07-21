# Problem Description:
'''Problem description: A railway company is planning the infrastructure for the city and is considering two types of transportation, trains and trams. Each train can transport 120 people per hour comfortably and each tram can transport 30 people per hour comfortably. Since trains take longer to build, the number of trams must be at least twice the number of trains. If the railway company wants to transport at least 600 people per hour, minimize the total number of transportation units required.

Expected Output Schema:
{
  "variables": {
    "NumberOfTrams": "float",
    "NumberOfTrains": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- Modes: set of transportation modes = {Train, Tram}

Parameters:
- train_capacity: capacity per train [people per hour] = 120
- tram_capacity: capacity per tram [people per hour] = 30
- min_required_capacity: minimum total capacity required [people per hour] = 600

Variables:
- NumberOfTrains: number of trains to build [nonnegative integer] (can be modeled as float if relaxed)
- NumberOfTrams: number of trams to build [nonnegative integer] (can be modeled as float if relaxed)

Objective:
- Minimize total_units = NumberOfTrains + NumberOfTrams

Constraints:
1. Capacity Constraint: (train_capacity * NumberOfTrains) + (tram_capacity * NumberOfTrams) ≥ min_required_capacity  
   Meaning: 120 * NumberOfTrains + 30 * NumberOfTrams ≥ 600
2. Ratio Constraint: NumberOfTrams ≥ 2 * NumberOfTrains  
   Meaning: there are at least twice as many trams as trains

--------------------------------------------------

Expected Output Schema:
{
  "variables": {
    "NumberOfTrams": "float",
    "NumberOfTrains": "float"
  },
  "objective": "float"
}

Comments:
- All units (people per hour) are consistent.
- Although the decision variables are naturally integers, they can be treated as floats in a relaxed model.
- The model minimizes the total number of units while ensuring the capacity and ratio constraints required for the transportation infrastructure are met.'''

# Generated Code:
from ortools.linear_solver import pywraplp

def solve_linear_program():
    # Create the linear solver with the GLOP backend for continuous LP.
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Solver not created successfully.")
        return None

    # Decision Variables:
    # Even though they represent integer units, they are treated as floats (relaxed model)
    NumberOfTrains = solver.NumVar(0, solver.infinity(), 'NumberOfTrains')
    NumberOfTrams = solver.NumVar(0, solver.infinity(), 'NumberOfTrams')

    # Parameters
    train_capacity = 120
    tram_capacity = 30
    min_required_capacity = 600

    # Constraints:
    # 1. Capacity Constraint: 120 * NumberOfTrains + 30 * NumberOfTrams >= 600
    solver.Add(train_capacity * NumberOfTrains + tram_capacity * NumberOfTrams >= min_required_capacity)

    # 2. Ratio Constraint: NumberOfTrams >= 2 * NumberOfTrains
    solver.Add(NumberOfTrams >= 2 * NumberOfTrains)

    # Objective: Minimize the total number of units (trains + trams)
    objective = solver.Objective()
    objective.SetCoefficient(NumberOfTrains, 1)
    objective.SetCoefficient(NumberOfTrams, 1)
    objective.SetMinimization()

    # Solve the problem
    result_status = solver.Solve()

    # Check the result status and return solution details
    if result_status == pywraplp.Solver.OPTIMAL:
        solution = {
            "variables": {
                "NumberOfTrams": NumberOfTrams.solution_value(),
                "NumberOfTrains": NumberOfTrains.solution_value()
            },
            "objective": objective.Value()
        }
        return solution
    else:
        print("The problem does not have an optimal solution.")
        return None

def main():
    # Since only one formulation is provided, we execute a single implementation.
    print("Solution using Linear Programming (ortools.linear_solver):")
    solution = solve_linear_program()
    if solution:
        print(solution)
    else:
        print("No optimal solution found.")

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Solution using Linear Programming (ortools.linear_solver):
{'variables': {'NumberOfTrams': 6.666666666666666, 'NumberOfTrains': 3.3333333333333335}, 'objective': 10.0}
'''

'''Expected Output:
Expected solution

: {'variables': {'NumberOfTrams': 8.0, 'NumberOfTrains': 3.0}, 'objective': 11.0}'''

