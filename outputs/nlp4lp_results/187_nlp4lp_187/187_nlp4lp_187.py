# Problem Description:
'''Problem description: A repairman fixes washing machines and freezers. Each washing machine takes 30 minutes of inspection and 90 minutes of fixing time. Each freezer takes 20 minutes of inspection and 125 minutes of fixing time. The repairman has 5000 minutes available for inspection and 20000 minutes available in his schedule. If each washing machine repaired earns him $250 and each freezer repaired earns his $375, how many of each appliance should he fix to maximize his earnings?

Expected Output Schema:
{
  "variables": {
    "WashingMachinesInspected": "float",
    "FreezersInspected": "float",
    "WashingMachinesRepaired": "float",
    "FreezersRepaired": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- A: set of appliance types = {WashingMachine, Freezer}

Parameters:
- inspection_time_WM: inspection time per washing machine [minutes] = 30
- repair_time_WM: repair time per washing machine [minutes] = 90
- inspection_time_FR: inspection time per freezer [minutes] = 20
- repair_time_FR: repair time per freezer [minutes] = 125
- revenue_WM: revenue per washing machine repaired [USD] = 250
- revenue_FR: revenue per freezer repaired [USD] = 375
- max_inspection_time: total available inspection time [minutes] = 5000
- max_repair_time: total available repair time [minutes] = 20000

Variables:
- WashingMachinesInspected: number of washing machines inspected [nonnegative integer]
- WashingMachinesRepaired: number of washing machines repaired [nonnegative integer]
- FreezersInspected: number of freezers inspected [nonnegative integer]
- FreezersRepaired: number of freezers repaired [nonnegative integer]
  (Note: In this model it is assumed that an appliance must be inspected before it is repaired. Therefore, each washing machine (or freezer) that is repaired is also inspected.)

Objective:
- Maximize total revenue = (revenue_WM * WashingMachinesRepaired) + (revenue_FR * FreezersRepaired)

Constraints:
1. Inspection time constraint:
   30 * WashingMachinesInspected + 20 * FreezersInspected ≤ max_inspection_time

2. Repair time constraint:
   90 * WashingMachinesRepaired + 125 * FreezersRepaired ≤ max_repair_time

3. Synchronization constraints (inspection precedes repair):
   WashingMachinesInspected = WashingMachinesRepaired
   FreezersInspected = FreezersRepaired

Comments:
- All time parameters are in minutes and all revenue parameters are in US dollars per repaired appliance.
- The synchronization constraints reflect the assumption that each appliance fixed must be inspected first. If however the inspection process can extend to appliances that are not fixed, then these two pairs of variables might be decoupled and additional modeling of inspection-to-repair conversion would be required.
- The decision variables are modeled as nonnegative integers, though they are declared as floats in the expected schema; in an integer programming implementation, they would be integer-valued.

This complete model adheres to the five-element structure and is directly mappable to a working implementation in Python or OR-Tools.'''

# Generated Code:
#!/usr/bin/env python3
"""
This script implements two formulations of the repairman problem using Google OR-Tools.
Formulation 1 (Strict Synchronization): 
  WashingMachinesInspected == WashingMachinesRepaired and FreezersInspected == FreezersRepaired.
Formulation 2 (Decoupled Inspection & Repair):
  WashingMachinesInspected >= WashingMachinesRepaired and FreezersInspected >= FreezersRepaired.
Both models maximize revenue subject to inspection and repair time constraints.
"""

from ortools.linear_solver import pywraplp

def solve_strict_synchronization():
    # Create the solver using CBC backend.
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Solver not created!")
        return None

    # Parameters
    max_inspection_time = 5000
    max_repair_time = 20000
    # Washing Machines
    inspection_time_WM = 30
    repair_time_WM = 90
    revenue_WM = 250
    # Freezers
    inspection_time_FR = 20
    repair_time_FR = 125
    revenue_FR = 375

    # Decision Variables: non-negative integers
    WashingMachinesInspected = solver.IntVar(0, solver.infinity(), 'WashingMachinesInspected')
    WashingMachinesRepaired  = solver.IntVar(0, solver.infinity(), 'WashingMachinesRepaired')
    FreezersInspected       = solver.IntVar(0, solver.infinity(), 'FreezersInspected')
    FreezersRepaired        = solver.IntVar(0, solver.infinity(), 'FreezersRepaired')

    # Objective: maximize revenue
    objective = solver.Objective()
    objective.SetCoefficient(WashingMachinesRepaired, revenue_WM)
    objective.SetCoefficient(FreezersRepaired, revenue_FR)
    objective.SetMaximization()

    # Constraints
    # Inspection time constraint
    solver.Add(inspection_time_WM * WashingMachinesInspected + inspection_time_FR * FreezersInspected <= max_inspection_time)
    # Repair time constraint
    solver.Add(repair_time_WM * WashingMachinesRepaired + repair_time_FR * FreezersRepaired <= max_repair_time)
    # Synchronization constraints: each repaired appliance has been inspected (strict equalities)
    solver.Add(WashingMachinesInspected == WashingMachinesRepaired)
    solver.Add(FreezersInspected == FreezersRepaired)

    # Solve model
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        solution = {
            "WashingMachinesInspected": WashingMachinesInspected.solution_value(),
            "WashingMachinesRepaired":  WashingMachinesRepaired.solution_value(),
            "FreezersInspected":       FreezersInspected.solution_value(),
            "FreezersRepaired":        FreezersRepaired.solution_value(),
            "objective": objective.Value()
        }
    else:
        solution = None
    return solution

def solve_decoupled_inspection_repair():
    # Create the solver using CBC backend.
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Solver not created!")
        return None

    # Parameters
    max_inspection_time = 5000
    max_repair_time = 20000
    # Washing Machines
    inspection_time_WM = 30
    repair_time_WM = 90
    revenue_WM = 250
    # Freezers
    inspection_time_FR = 20
    repair_time_FR = 125
    revenue_FR = 375

    # Decision Variables: non-negative integers
    WashingMachinesInspected = solver.IntVar(0, solver.infinity(), 'WashingMachinesInspected')
    WashingMachinesRepaired  = solver.IntVar(0, solver.infinity(), 'WashingMachinesRepaired')
    FreezersInspected       = solver.IntVar(0, solver.infinity(), 'FreezersInspected')
    FreezersRepaired        = solver.IntVar(0, solver.infinity(), 'FreezersRepaired')

    # Objective: maximize revenue (only repair yields revenue)
    objective = solver.Objective()
    objective.SetCoefficient(WashingMachinesRepaired, revenue_WM)
    objective.SetCoefficient(FreezersRepaired, revenue_FR)
    objective.SetMaximization()

    # Constraints
    # Inspection time constraint
    solver.Add(inspection_time_WM * WashingMachinesInspected + inspection_time_FR * FreezersInspected <= max_inspection_time)
    # Repair time constraint
    solver.Add(repair_time_WM * WashingMachinesRepaired + repair_time_FR * FreezersRepaired <= max_repair_time)
    # Synchronization constraints: each repaired appliance must be inspected (inspection can be more)
    solver.Add(WashingMachinesInspected >= WashingMachinesRepaired)
    solver.Add(FreezersInspected >= FreezersRepaired)

    # Solve model
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        solution = {
            "WashingMachinesInspected": WashingMachinesInspected.solution_value(),
            "WashingMachinesRepaired":  WashingMachinesRepaired.solution_value(),
            "FreezersInspected":       FreezersInspected.solution_value(),
            "FreezersRepaired":        FreezersRepaired.solution_value(),
            "objective": objective.Value()
        }
    else:
        solution = None
    return solution

def main():
    result_strict = solve_strict_synchronization()
    result_decoupled = solve_decoupled_inspection_repair()

    print("Results for Formulation 1 (Strict Synchronization):")
    if result_strict is not None:
        print(result_strict)
    else:
        print("The problem is infeasible or an error occurred.")

    print("\nResults for Formulation 2 (Decoupled Inspection & Repair):")
    if result_decoupled is not None:
        print(result_decoupled)
    else:
        print("The problem is infeasible or an error occurred.")

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Results for Formulation 1 (Strict Synchronization):
{'WashingMachinesInspected': 0.0, 'WashingMachinesRepaired': 0.0, 'FreezersInspected': 160.0, 'FreezersRepaired': 160.0, 'objective': 60000.0}

Results for Formulation 2 (Decoupled Inspection & Repair):
{'WashingMachinesInspected': 60.0, 'WashingMachinesRepaired': 0.0, 'FreezersInspected': 160.0, 'FreezersRepaired': 160.0, 'objective': 60000.0}
'''

'''Expected Output:
Expected solution

: {'variables': {'WashingMachinesInspected': 0.0, 'FreezersInspected': 0.0, 'WashingMachinesRepaired': -0.0, 'FreezersRepaired': 160.0}, 'objective': 60000.0}'''

