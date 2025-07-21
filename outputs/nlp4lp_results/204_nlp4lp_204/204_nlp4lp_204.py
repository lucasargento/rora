# Problem Description:
'''Problem description: An oil and gas company has two types of pipes, a high-volume and a low-volume one. Every day, the high-volume pipe allows 10000 US gallons and it is recommended that 12 technicians closely monitor the pipes to ensure that it is functioning properly. Each day, the low-volume pipe allows 5000 US gallons and 5 technicians should closely monitor for safety reasons. Every day, the oil and gas company needs to meet the demands of at least 150000 US gallons of gas and they have 160 technicians that are on their staff. Since the high-volume pipe has a higher risk of environmental damage, at most 35 percent of the pipes can be high-volume ones. Additionally, there must be a minimum of 8 low-volume pipes. How many of each pipe types should be used to reduce the total number of pipes required?

Expected Output Schema:
{
  "variables": {
    "HighVolumePipes": "float",
    "LowVolumePipes": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- PIPETYPE: set of pipe types = {HighVolume, LowVolume}

Parameters:
- high_flow: gallons of gas per high-volume pipe per day = 10000 (US gallons)
- low_flow: gallons of gas per low-volume pipe per day = 5000 (US gallons)
- high_tech_required: technicians required per high-volume pipe per day = 12 (technicians)
- low_tech_required: technicians required per low-volume pipe per day = 5 (technicians)
- min_total_flow: minimum gas flow required per day = 150000 (US gallons)
- available_techs: total technicians available per day = 160 (technicians)
- max_high_percentage: maximum fraction of high-volume pipes allowed = 0.35 (35 percent)
- min_low_pipes: minimum number of low-volume pipes required = 8 (pipes)

Variables:
- HighVolumePipes: number of high-volume pipes to use (integer, ≥ 0)
- LowVolumePipes: number of low-volume pipes to use (integer, ≥ 0)

Objective:
- Minimize total number of pipes = HighVolumePipes + LowVolumePipes

Constraints:
1. Gas Flow Constraint:
   - high_flow * HighVolumePipes + low_flow * LowVolumePipes ≥ min_total_flow
   - Meaning: 10000 * HighVolumePipes + 5000 * LowVolumePipes ≥ 150000

2. Technician Constraint:
   - high_tech_required * HighVolumePipes + low_tech_required * LowVolumePipes ≤ available_techs
   - Meaning: 12 * HighVolumePipes + 5 * LowVolumePipes ≤ 160

3. High-Volume Pipe Percentage Constraint:
   - HighVolumePipes ≤ max_high_percentage * (HighVolumePipes + LowVolumePipes)
   - Meaning: HighVolumePipes ≤ 0.35 * (HighVolumePipes + LowVolumePipes)

4. Low-Volume Pipes Minimum Constraint:
   - LowVolumePipes ≥ min_low_pipes
   - Meaning: LowVolumePipes ≥ 8

---

Note:
- All units are assumed consistent. Gallons refer to US gallons and technician counts are per day.
- The decision variables are integers. In some implementations, you might relax integrality if pipes can be considered in continuous approximation, but here pipes are discrete items.
- The model minimizes the total number of pipes while ensuring the gas flow demand is met, technician availability is not exceeded, and safety/environmental policies are observed.

Expected Output Schema:
{
  "variables": {
    "HighVolumePipes": "integer ≥ 0",
    "LowVolumePipes": "integer ≥ 0"
  },
  "objective": "minimize HighVolumePipes + LowVolumePipes"
}'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_with_linear_solver():
    # Create the linear solver with the CBC backend.
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Solver not created.")
        return None

    # Parameters
    high_flow = 10000         # US gallons per high-volume pipe per day
    low_flow = 5000           # US gallons per low-volume pipe per day
    high_tech_required = 12   # Technicians per high-volume pipe per day
    low_tech_required = 5     # Technicians per low-volume pipe per day
    min_total_flow = 150000   # Minimum required gas flow per day
    available_techs = 160     # Total available technicians per day
    max_high_percentage = 0.35  # Maximum fraction of pipes allowed to be high-volume
    min_low_pipes = 8         # Minimum required low-volume pipes

    # Decision variables (non-negative integers)
    HighVolumePipes = solver.IntVar(0, solver.infinity(), 'HighVolumePipes')
    LowVolumePipes = solver.IntVar(0, solver.infinity(), 'LowVolumePipes')

    # Objective: Minimize total number of pipes
    solver.Minimize(HighVolumePipes + LowVolumePipes)

    # Constraint 1: Gas flow constraint
    solver.Add(high_flow * HighVolumePipes + low_flow * LowVolumePipes >= min_total_flow)

    # Constraint 2: Technician constraint
    solver.Add(high_tech_required * HighVolumePipes + low_tech_required * LowVolumePipes <= available_techs)

    # Constraint 3: High-volume pipe percentage constraint
    # H <= 0.35 * (H + L)  <=>  13*H <= 7*L  [after multiplying both sides by 20]
    solver.Add(13 * HighVolumePipes - 7 * LowVolumePipes <= 0)

    # Constraint 4: Minimum low-volume pipes
    solver.Add(LowVolumePipes >= min_low_pipes)

    # Solve the problem and return results
    status = solver.Solve()
    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result['HighVolumePipes'] = int(HighVolumePipes.solution_value())
        result['LowVolumePipes'] = int(LowVolumePipes.solution_value())
        result['objective'] = HighVolumePipes.solution_value() + LowVolumePipes.solution_value()
    else:
        result['message'] = "The problem does not have an optimal solution."
    return result

def main():
    results = {}
    
    # Model implementation using ortools.linear_solver
    linear_solver_result = solve_with_linear_solver()
    results['LinearSolverImplementation'] = linear_solver_result

    # Output the solutions in a structured format.
    print("Optimization Results:")
    for model_name, result in results.items():
        print(f"--- {model_name} ---")
        if 'message' in result:
            print(result['message'])
        else:
            print("HighVolumePipes:", result['HighVolumePipes'])
            print("LowVolumePipes:", result['LowVolumePipes'])
            print("Total Pipes (Objective Value):", result['objective'])
        print()

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Optimization Results:
--- LinearSolverImplementation ---
HighVolumePipes: 5
LowVolumePipes: 20
Total Pipes (Objective Value): 25.0

'''

'''Expected Output:
Expected solution

: {'variables': {'HighVolumePipes': 5.0, 'LowVolumePipes': 20.0}, 'objective': 25.0}'''

