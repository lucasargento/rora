# Problem Description:
'''Problem description: A mall buys two types of hand sanitizer machines, a motion activated one and a manual one. The motion activated one can deliver 50 drops per minute and consumes 30 kWh. The manual one can deliver 75 drops per minute and consumes 20 kWh. Since the motion activated one is more hygienic, at most 40% of the machines can be manual. In addition, at least 3 should be motion activated. If the mall must be able to deliver at least 1000 drops per minute and can use at most 500 kWh per minute, how many of each machine should they buy to minimize the total number of machines?

Expected Output Schema:
{
  "variables": {
    "ManualMachines": "float",
    "MotionActivatedMachines": "float",
    "TotalMachines": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- M: set of machine types = {Manual, MotionActivated}

Parameters:
- drops_per_min_manual = 75 [drops per minute per manual machine]
- drops_per_min_motion = 50 [drops per minute per motion activated machine]
- energy_per_min_manual = 20 [kWh per minute per manual machine]
- energy_per_min_motion = 30 [kWh per minute per motion activated machine]
- min_total_drops = 1000 [drops per minute required]
- max_total_energy = 500 [kWh per minute allowed]
- max_manual_ratio = 0.4 [maximum allowed fraction of manual machines in the total fleet]
- min_motion_machines = 3 [minimum number of motion activated machines required]

Variables:
- ManualMachines: number of manual hand sanitizer machines [integer ≥ 0]
- MotionActivatedMachines: number of motion activated hand sanitizer machines [integer ≥ min_motion_machines]
- TotalMachines: total number of machines purchased, defined as ManualMachines + MotionActivatedMachines [integer]

Objective:
- Minimize TotalMachines = ManualMachines + MotionActivatedMachines

Constraints:
1. Hygiene Ratio Constraint:
   - The fraction of manual machines must be at most 40% of the total machines:
   - ManualMachines ≤ max_manual_ratio × (ManualMachines + MotionActivatedMachines)
   (This can be algebraically rearranged to the linear form: ManualMachines ≤ (2/3) × MotionActivatedMachines.)

2. Minimum Drops Delivery Constraint:
   - The combined drops per minute must be at least min_total_drops:
   - drops_per_min_motion × MotionActivatedMachines + drops_per_min_manual × ManualMachines ≥ min_total_drops

3. Maximum Energy Consumption Constraint:
   - The total energy consumption per minute cannot exceed max_total_energy:
   - energy_per_min_motion × MotionActivatedMachines + energy_per_min_manual × ManualMachines ≤ max_total_energy

4. Minimum Number of Motion Activated Machines:
   - MotionActivatedMachines ≥ min_motion_machines

Comments:
- All parameters are assumed to be given per minute as stated in the problem.
- Although the decision variables represent machine counts and thus are integer, the model focuses on the structure; an implementation may impose integrality explicitly.
- The hygiene ratio constraint has been reformulated into a linear constraint for ease of implementation.

This completes the structured mathematical model using the five-element framework.'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_version_a():
    # Create the solver using SCIP as the underlying MIP solver.
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        return None

    # Data / Parameters
    drops_per_min_manual = 75
    drops_per_min_motion = 50
    energy_per_min_manual = 20
    energy_per_min_motion = 30
    min_total_drops = 1000
    max_total_energy = 500
    max_manual_ratio = 0.4  # equivalent to ManualMachines <= (2/3)*MotionActivatedMachines
    min_motion_machines = 3

    # Decision variables: integers
    # ManualMachines >=0 and MotionActivatedMachines >= min_motion_machines.
    ManualMachines = solver.IntVar(0, solver.infinity(), 'ManualMachines')
    MotionActivatedMachines = solver.IntVar(min_motion_machines, solver.infinity(), 'MotionActivatedMachines')

    # Since TotalMachines = ManualMachines + MotionActivatedMachines, we don't define it as a separate variable for version A.
    # The objective is to minimize the total number of machines.
    solver.Minimize(ManualMachines + MotionActivatedMachines)

    # Constraint 1: Hygiene Ratio Constraint. 
    # Original constraint: ManualMachines <= max_manual_ratio*(ManualMachines + MotionActivatedMachines)
    # Algebraically: ManualMachines <= 0.4*(ManualMachines+MotionActivatedMachines)
    # Multiply both sides by 10 to avoid decimals:
    # 10 * ManualMachines <= 4*(ManualMachines+MotionActivatedMachines)
    # which simplifies to: 6*ManualMachines <= 4*MotionActivatedMachines
    solver.Add(6 * ManualMachines <= 4 * MotionActivatedMachines)

    # Constraint 2: Minimum Drops Delivery Constraint.
    solver.Add(drops_per_min_motion * MotionActivatedMachines + drops_per_min_manual * ManualMachines >= min_total_drops)

    # Constraint 3: Maximum Energy Consumption Constraint.
    solver.Add(energy_per_min_motion * MotionActivatedMachines + energy_per_min_manual * ManualMachines <= max_total_energy)

    # Solve the problem.
    status = solver.Solve()

    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        manual_val = ManualMachines.solution_value()
        motion_val = MotionActivatedMachines.solution_value()
        total_val = manual_val + motion_val
        objective = solver.Objective().Value()
        result = {
            "ManualMachines": manual_val,
            "MotionActivatedMachines": motion_val,
            "TotalMachines": total_val,
            "objective": objective
        }
    else:
        result = None
    return result

def solve_version_b():
    # Create a separate solver for version B.
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        return None

    # Data / Parameters
    drops_per_min_manual = 75
    drops_per_min_motion = 50
    energy_per_min_manual = 20
    energy_per_min_motion = 30
    min_total_drops = 1000
    max_total_energy = 500
    max_manual_ratio = 0.4  # original ratio constraint: ManualMachines <= 0.4*(ManualMachines+MotionActivatedMachines)
    min_motion_machines = 3

    # Decision variables: integers
    ManualMachines = solver.IntVar(0, solver.infinity(), 'ManualMachines')
    MotionActivatedMachines = solver.IntVar(min_motion_machines, solver.infinity(), 'MotionActivatedMachines')
    # Introduce TotalMachines as a separate variable to allow an explicit link.
    TotalMachines = solver.IntVar(0, solver.infinity(), 'TotalMachines')

    # Link TotalMachines with Manual and Motion activated machines.
    solver.Add(TotalMachines == ManualMachines + MotionActivatedMachines)

    # Objective: minimize the total number of machines.
    solver.Minimize(TotalMachines)

    # Constraint 1: Hygiene Ratio Constraint using the original formulation.
    solver.Add(ManualMachines <= max_manual_ratio * TotalMachines)

    # Constraint 2: Minimum Drops Delivery Constraint.
    solver.Add(drops_per_min_motion * MotionActivatedMachines + drops_per_min_manual * ManualMachines >= min_total_drops)

    # Constraint 3: Maximum Energy Consumption Constraint.
    solver.Add(energy_per_min_motion * MotionActivatedMachines + energy_per_min_manual * ManualMachines <= max_total_energy)

    # Constraint 4: Minimum Number of Motion Activated Machines is already ensured by variable bounds.
    # Solve the problem.
    status = solver.Solve()

    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        manual_val = ManualMachines.solution_value()
        motion_val = MotionActivatedMachines.solution_value()
        total_val = TotalMachines.solution_value()
        objective_val = solver.Objective().Value()
        result = {
            "ManualMachines": manual_val,
            "MotionActivatedMachines": motion_val,
            "TotalMachines": total_val,
            "objective": objective_val
        }
    else:
        result = None
    return result

def main():
    print("Version A: Using reformulated hygiene ratio constraint (6*M <= 4*MotionActivatedMachines)")
    result_a = solve_version_a()
    if result_a:
        print("Optimal solution found:")
        print("  ManualMachines         =", result_a["ManualMachines"])
        print("  MotionActivatedMachines=", result_a["MotionActivatedMachines"])
        print("  TotalMachines          =", result_a["TotalMachines"])
        print("  Objective (Total)      =", result_a["objective"])
    else:
        print("No optimal solution found for Version A.")

    print("\nVersion B: Using explicit TotalMachines variable and original hygiene ratio constraint (ManualMachines <= 0.4 * TotalMachines)")
    result_b = solve_version_b()
    if result_b:
        print("Optimal solution found:")
        print("  ManualMachines         =", result_b["ManualMachines"])
        print("  MotionActivatedMachines=", result_b["MotionActivatedMachines"])
        print("  TotalMachines          =", result_b["TotalMachines"])
        print("  Objective (Total)      =", result_b["objective"])
    else:
        print("No optimal solution found for Version B.")

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Version A: Using reformulated hygiene ratio constraint (6*M <= 4*MotionActivatedMachines)
Optimal solution found:
  ManualMachines         = 6.0
  MotionActivatedMachines= 11.0
  TotalMachines          = 17.0
  Objective (Total)      = 17.0

Version B: Using explicit TotalMachines variable and original hygiene ratio constraint (ManualMachines <= 0.4 * TotalMachines)
Optimal solution found:
  ManualMachines         = 6.0
  MotionActivatedMachines= 11.0
  TotalMachines          = 17.0
  Objective (Total)      = 17.0
'''

'''Expected Output:
Expected solution

: {'variables': {'ManualMachines': 6.0, 'MotionActivatedMachines': 11.0, 'TotalMachines': 17.0}, 'objective': 17.0}'''

