# Problem Description:
'''Problem description: An ice cream store can buy two machines, a counter-top sized one and a fridge sized one, to make ice cream. The counter-top sized one can produce 80 cones worth of ice cream every day while the fridge sizes one can produce 150 cones worth of ice cream every day. The counter-top sized machine outputs 50 units of heat while the fridge sized one outputs 70 units of heat. The ice cream store can output at most 500 units of heat per day and must produce at least 1000 cones worth of ice cream. How many of each machine should they buy to minimize the total number of machines needed?

Expected Output Schema:
{
  "variables": {
    "MachinesCounterTop": "float",
    "MachinesFridge": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- M: set of machine types = {CounterTop, Fridge}

Parameters:
- cones_per_machine:
   - For CounterTop machine: 80 cones/day produced.
   - For Fridge machine: 150 cones/day produced.
- heat_per_machine:
   - For CounterTop machine: 50 heat units/day generated.
   - For Fridge machine: 70 heat units/day generated.
- required_cones: 1000 cones (minimum ice cream production per day).
- max_heat: 500 heat units (maximum allowable daily heat output).

Variables:
- MachinesCounterTop: number of counter-top machines to buy (float; expected to be a whole number, units: machines).
- MachinesFridge: number of fridge machines to buy (float; expected to be a whole number, units: machines).

Objective:
- Minimize total number of machines purchased = MachinesCounterTop + MachinesFridge.

Constraints:
1. Production Constraint (Cones Requirement):
   80 * MachinesCounterTop + 150 * MachinesFridge >= required_cones
   (ensures that at least 1000 cones are produced per day).

2. Heat Constraint:
   50 * MachinesCounterTop + 70 * MachinesFridge <= max_heat
   (ensures that the total heat generated does not exceed 500 heat units per day).

Notes:
- Although the decision variables are defined as floats in the expected schema, in practical implementation they should represent integer values since machines cannot be divided.
- All units are consistent: cones per day for production and heat units per day for heat output.'''

# Generated Code:
#!/usr/bin/env python3
"""
This script implements the optimization problem for the ice cream store using two separate formulations:
1. A Mixed Integer Programming (MIP) formulation using ortools.linear_solver.
2. A CP-SAT formulation using ortools.sat.python.cp_model.

Both formulations are kept completely separate and are called from the main() function.
"""

from ortools.linear_solver import pywraplp
from ortools.sat.python import cp_model

def solve_with_linear_solver():
    # Create the mixed integer programming solver using CBC.
    solver = pywraplp.Solver.CreateSolver('CBC_MIXED_INTEGER_PROGRAMMING')
    if not solver:
        print("Linear solver not available.")
        return None

    # Parameters
    cones_required = 1000
    max_heat = 500

    # Production and heat per machine for both types
    cones_counter_top = 80
    cones_fridge = 150
    heat_counter_top = 50
    heat_fridge = 70

    # Decision variables: integer variables for number of machines.
    MachinesCounterTop = solver.IntVar(0, solver.infinity(), 'MachinesCounterTop')
    MachinesFridge = solver.IntVar(0, solver.infinity(), 'MachinesFridge')

    # Objective: minimize total number of machines.
    solver.Minimize(MachinesCounterTop + MachinesFridge)

    # Constraint 1: Production Constraint
    solver.Add(cones_counter_top * MachinesCounterTop + cones_fridge * MachinesFridge >= cones_required)

    # Constraint 2: Heat Constraint
    solver.Add(heat_counter_top * MachinesCounterTop + heat_fridge * MachinesFridge <= max_heat)

    status = solver.Solve()

    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result["MachinesCounterTop"] = MachinesCounterTop.solution_value()
        result["MachinesFridge"] = MachinesFridge.solution_value()
        result["objective"] = solver.Objective().Value()
    else:
        result["status"] = "infeasible or no optimal solution found."
    
    return result

def solve_with_cp_model():
    # Create CP-SAT model.
    model = cp_model.CpModel()

    # Parameters
    cones_required = 1000
    max_heat = 500
    cones_counter_top = 80
    cones_fridge = 150
    heat_counter_top = 50
    heat_fridge = 70

    # Decision variables: Integer variables.
    MachinesCounterTop = model.NewIntVar(0, 1000, 'MachinesCounterTop')
    MachinesFridge = model.NewIntVar(0, 1000, 'MachinesFridge')

    # Objective: minimize the sum of the machines.
    model.Minimize(MachinesCounterTop + MachinesFridge)

    # Constraint 1: Production Constraint (at least 1000 cones)
    model.Add(cones_counter_top * MachinesCounterTop + cones_fridge * MachinesFridge >= cones_required)

    # Constraint 2: Heat Constraint (no more than 500 heat units)
    model.Add(heat_counter_top * MachinesCounterTop + heat_fridge * MachinesFridge <= max_heat)

    # Solve the model.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    result = {}
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        result["MachinesCounterTop"] = solver.Value(MachinesCounterTop)
        result["MachinesFridge"] = solver.Value(MachinesFridge)
        result["objective"] = solver.ObjectiveValue()
    else:
        result["status"] = "infeasible or no optimal solution found."

    return result

def main():
    print("Solution using OR-Tools Linear Solver (MIP formulation):")
    linear_result = solve_with_linear_solver()
    if "status" in linear_result:
        print("Linear Solver Result: ", linear_result["status"])
    else:
        print("MachinesCounterTop: ", linear_result["MachinesCounterTop"])
        print("MachinesFridge: ", linear_result["MachinesFridge"])
        print("Objective (Total Machines): ", linear_result["objective"])
    
    print("\nSolution using OR-Tools CP-SAT model:")
    cp_result = solve_with_cp_model()
    if "status" in cp_result:
        print("CP-SAT Result: ", cp_result["status"])
    else:
        print("MachinesCounterTop: ", cp_result["MachinesCounterTop"])
        print("MachinesFridge: ", cp_result["MachinesFridge"])
        print("Objective (Total Machines): ", cp_result["objective"])

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Solution using OR-Tools Linear Solver (MIP formulation):
MachinesCounterTop:  0.0
MachinesFridge:  7.0
Objective (Total Machines):  7.0

Solution using OR-Tools CP-SAT model:
MachinesCounterTop:  0
MachinesFridge:  7
Objective (Total Machines):  7.0
'''

'''Expected Output:
Expected solution

: {'variables': {'MachinesCounterTop': 0.0, 'MachinesFridge': 7.0}, 'objective': 7.0}'''

