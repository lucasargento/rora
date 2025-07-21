# Problem Description:
'''Problem description: A factory has two machines, A and B. Each day, machine A can make 30 items and consumes 100 kWh. Machine B can make 50 items and consumes 120 kWh per day. The factory must produce at least 1000 items per day and has 3000 kWh of electricity available per day. Since there are not many workers that can operate both machines, at most 30% of the machines must be of type B. Further, at least 5 machines of type A should be used. How many of each machine should be used to minimize the total number of machines?

Expected Output Schema:
{
  "variables": {
    "NumberA": "float",
    "NumberB": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- Machines: set of machine types = {A, B}

Parameters:
- Production_A: number of items produced per machine A per day = 30 items/day
- Production_B: number of items produced per machine B per day = 50 items/day
- Energy_A: electricity consumed by one machine A per day = 100 kWh/day
- Energy_B: electricity consumed by one machine B per day = 120 kWh/day
- Demand: minimum required items per day = 1000 items/day
- Energy_limit: maximum available electricity per day = 3000 kWh/day
- B_ratio_limit: maximum allowed proportion of type B machines = 0.3 (i.e., at most 30% of all machines)
- Min_A: minimum number of machine A = 5

Variables:
- NumberA: number of machine A used [integer, lower bound 5]
- NumberB: number of machine B used [integer, lower bound 0]

Objective:
- Minimize total machines = NumberA + NumberB

Constraints:
1. Production constraint: (Production_A * NumberA) + (Production_B * NumberB) >= Demand  
   (i.e., 30*NumberA + 50*NumberB >= 1000)

2. Electricity constraint: (Energy_A * NumberA) + (Energy_B * NumberB) <= Energy_limit  
   (i.e., 100*NumberA + 120*NumberB <= 3000)

3. Machine type ratio constraint: NumberB <= B_ratio_limit * (NumberA + NumberB)  
   This can be rearranged as: (NumberA + NumberB) >= (NumberB / 0.3) or equivalently 0.7*NumberB <= 0.3*NumberA

4. Minimum machine A constraint: NumberA >= Min_A

---------------------------
Expected Output Schema:
{
  "variables": {
    "NumberA": "integer (>=5)",
    "NumberB": "integer (>=0)"
  },
  "objective": "Minimize total machines = NumberA + NumberB"
}'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp
from ortools.sat.python import cp_model

def solve_with_linear_solver():
    # Create the MIP solver with SCIP backend.
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        return None, None, "Solver not created."
    
    # Parameters
    production_A = 30
    production_B = 50
    energy_A = 100
    energy_B = 120
    demand = 1000
    energy_limit = 3000
    min_A = 5

    # Variables
    NumberA = solver.IntVar(min_A, solver.infinity(), 'NumberA')
    NumberB = solver.IntVar(0, solver.infinity(), 'NumberB')

    # Constraint 1: Production constraint
    solver.Add(production_A * NumberA + production_B * NumberB >= demand)

    # Constraint 2: Electricity constraint
    solver.Add(energy_A * NumberA + energy_B * NumberB <= energy_limit)

    # Constraint 3: Machine type ratio: 7*NumberB <= 3*NumberA  (derived from 0.7 * NumberB <= 0.3*NumberA)
    solver.Add(7 * NumberB <= 3 * NumberA)

    # Objective: Minimize total machines = NumberA + NumberB
    solver.Minimize(NumberA + NumberB)

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        solution = {
            "NumberA": int(NumberA.solution_value()),
            "NumberB": int(NumberB.solution_value())
        }
        objective_value = NumberA.solution_value() + NumberB.solution_value()
        return solution, objective_value, None
    elif status == pywraplp.Solver.FEASIBLE:
        return None, None, "A feasible solution was found, but it might not be optimal."
    else:
        return None, None, "No solution found."

def solve_with_cp_model():
    # Create the CP-SAT model.
    model = cp_model.CpModel()

    # Parameters
    production_A = 30
    production_B = 50
    energy_A = 100
    energy_B = 120
    demand = 1000
    energy_limit = 3000
    min_A = 5

    # Define a reasonable upper bound for machines.
    # Upper bound can be estimated by ignoring other constraints.
    ub_A = energy_limit // energy_A  # worst-case for A only
    ub_B = energy_limit // energy_B  # worst-case for B only

    # Variables: using cp_model.IntVar(lower, upper, name)
    NumberA = model.NewIntVar(min_A, ub_A, 'NumberA')
    NumberB = model.NewIntVar(0, ub_B, 'NumberB')

    # Constraint 1: Production constraint: 30*NumberA + 50*NumberB >= 1000
    model.Add(production_A * NumberA + production_B * NumberB >= demand)

    # Constraint 2: Electricity constraint: 100*NumberA + 120*NumberB <= 3000
    model.Add(energy_A * NumberA + energy_B * NumberB <= energy_limit)

    # Constraint 3: Machine ratio constraint: 7*NumberB <= 3*NumberA
    model.Add(7 * NumberB <= 3 * NumberA)

    # Objective: Minimize total machines = NumberA + NumberB
    total_machines = model.NewIntVar(min_A, ub_A + ub_B, 'total_machines')
    model.Add(total_machines == NumberA + NumberB)
    model.Minimize(total_machines)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        solution = {
            "NumberA": solver.Value(NumberA),
            "NumberB": solver.Value(NumberB)
        }
        objective_value = solver.Value(total_machines)
        return solution, objective_value, None
    else:
        return None, None, "No solution found."

def main():
    results = {}

    # Solve using Linear Solver (MIP approach)
    lin_sol, lin_obj, lin_error = solve_with_linear_solver()
    if lin_error:
        results["LinearSolver"] = {"error": lin_error}
    else:
        results["LinearSolver"] = {"variables": lin_sol, "objective": lin_obj}
    
    # Solve using CP-SAT Model
    cp_sol, cp_obj, cp_error = solve_with_cp_model()
    if cp_error:
        results["CPSAT"] = {"error": cp_error}
    else:
        results["CPSAT"] = {"variables": cp_sol, "objective": cp_obj}
    
    # Print results in a structured way.
    print("Results:")
    for method, res in results.items():
        print("-" * 40)
        print(f"Method: {method}")
        if "error" in res:
            print(f"Error: {res['error']}")
        else:
            print(f"Optimal Variables: {res['variables']}")
            print(f"Objective Value: {res['objective']}")
    print("-" * 40)

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Results:
----------------------------------------
Method: LinearSolver
Optimal Variables: {'NumberA': 20, 'NumberB': 8}
Objective Value: 28.0
----------------------------------------
Method: CPSAT
Optimal Variables: {'NumberA': 20, 'NumberB': 8}
Objective Value: 28
----------------------------------------
'''

'''Expected Output:
Expected solution

: {'variables': {'NumberA': 20.0, 'NumberB': 8.0}, 'objective': 28.0}'''

