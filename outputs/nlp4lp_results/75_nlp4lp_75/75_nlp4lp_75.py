# Problem Description:
'''Problem description: A mining company has available a total of 100 square miles of mining sites and considering the use of two mining techniques: heap leaching and vat leaching. For each square mile of land, heap leaching technique can have a daily production of 3 tons of rare earth oxide per square miles but it also creates 8 tons of polluted wastewater and requires 10 extraction machines. On the other hand, vat leaching technique produces 5 tons of rare earth oxide per square miles per day while creating 17 tons of polluted wastewater and requiring 20 extraction machines. There are 100 machines available and due to environmental regulations, the amount of polluted wastewater must be at most 90 tons daily. Find the proportion of lands that use each mining technique in order to maximize the daily production of rare earth oxide.

Expected Output Schema:
{
  "variables": {
    "LandAllocated": {
      "0": "float",
      "1": "float"
    }
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Below is the five‐element mathematical formulation for the mining problem.

--------------------------------------------------
Sets:
- T: set of mining techniques = {heap, vat}

--------------------------------------------------
Parameters:
- TotalLand: total available mining sites [square miles] = 100
- production_rate[t]:
  • heap: tons of rare earth oxide produced per square mile per day = 3
  • vat: tons of rare earth oxide produced per square mile per day = 5
- wastewater_rate[t]:
  • heap: tons of polluted wastewater generated per square mile per day = 8
  • vat: tons of polluted wastewater generated per square mile per day = 17
- machine_req[t]:
  • heap: extraction machines required per square mile = 10
  • vat: extraction machines required per square mile = 20
- maxMachines: total available extraction machines = 100
- maxWastewater: maximum allowed polluted wastewater per day [tons] = 90

--------------------------------------------------
Variables:
- LandAllocated[t] for t in T (continuous, unit: square miles, ≥ 0)
  • LandAllocated[heap]: area allocated to heap leaching
  • LandAllocated[vat]: area allocated to vat leaching

--------------------------------------------------
Objective:
Maximize total daily production of rare earth oxide:
  Maximize TotalProduction = production_rate[heap]*LandAllocated[heap] + production_rate[vat]*LandAllocated[vat]
  (Unit: tons per day)

--------------------------------------------------
Constraints:
1. Land availability constraint:
  LandAllocated[heap] + LandAllocated[vat] ≤ TotalLand

2. Machine availability constraint:
  machine_req[heap]*LandAllocated[heap] + machine_req[vat]*LandAllocated[vat] ≤ maxMachines

3. Wastewater regulation constraint:
  wastewater_rate[heap]*LandAllocated[heap] + wastewater_rate[vat]*LandAllocated[vat] ≤ maxWastewater

--------------------------------------------------
Below is the corresponding JSON structure (as expected):

{
  "variables": {
    "LandAllocated": {
      "0": "float",    // corresponds to LandAllocated[heap]
      "1": "float"     // corresponds to LandAllocated[vat]
    }
  },
  "objective": "float"   // TotalProduction = 3*LandAllocated[heap] + 5*LandAllocated[vat]"
}'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_mining_problem_linear():
    # Create the linear solver with the GLOP backend.
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Solver not created.")
        return None

    # Sets/Indices:
    # t=0 corresponds to heap leaching; t=1 corresponds to vat leaching.

    # Parameters
    TotalLand = 100                 # total available mining sites (square miles)
    production_rate = [3, 5]        # tons of rare earth oxide produced per square mile per day for heap and vat, respectively.
    wastewater_rate = [8, 17]       # tons of polluted wastewater per square mile per day.
    machine_req = [10, 20]          # extraction machines required per square mile.
    maxMachines = 100               # total available extraction machines.
    maxWastewater = 90              # maximum allowed polluted wastewater per day (tons).

    # Variables: LandAllocated[t] for each mining technique (continuous variables and ≥ 0)
    land_allocated_heap = solver.NumVar(0.0, solver.infinity(), 'LandAllocated_heap')
    land_allocated_vat = solver.NumVar(0.0, solver.infinity(), 'LandAllocated_vat')

    # Constraint 1: Land availability constraint.
    # LandAllocated[heap] + LandAllocated[vat] <= TotalLand
    solver.Add(land_allocated_heap + land_allocated_vat <= TotalLand)

    # Constraint 2: Machine availability constraint.
    # machine_req[heap]*LandAllocated[heap] + machine_req[vat]*LandAllocated[vat] <= maxMachines
    solver.Add(machine_req[0] * land_allocated_heap + machine_req[1] * land_allocated_vat <= maxMachines)

    # Constraint 3: Wastewater regulation constraint.
    # wastewater_rate[heap]*LandAllocated[heap] + wastewater_rate[vat]*LandAllocated[vat] <= maxWastewater
    solver.Add(wastewater_rate[0] * land_allocated_heap + wastewater_rate[1] * land_allocated_vat <= maxWastewater)

    # Objective: Maximize total daily production of rare earth oxide.
    # Maximize  production_rate[heap]*LandAllocated[heap] + production_rate[vat]*LandAllocated[vat]
    objective = solver.Objective()
    objective.SetCoefficient(land_allocated_heap, production_rate[0])
    objective.SetCoefficient(land_allocated_vat, production_rate[1])
    objective.SetMaximization()

    status = solver.Solve()

    solution = {}
    if status == pywraplp.Solver.OPTIMAL:
        solution = {
            "variables": {
                "LandAllocated": {
                    "0": land_allocated_heap.solution_value(),  # heap leaching allocation (square miles)
                    "1": land_allocated_vat.solution_value()     # vat leaching allocation (square miles)
                }
            },
            "objective": objective.Value()  # total production (tons per day)
        }
    else:
        print("The solver did not find an optimal solution.")
    return solution

def main():
    # Since the problem formulation is unambiguous, we only use the linear solver based model.
    result_linear = solve_mining_problem_linear()

    print("----- Linear Solver (ORTools) Results -----")
    if result_linear:
        print(result_linear)
    else:
        print("No solution found.")

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
----- Linear Solver (ORTools) Results -----
{'variables': {'LandAllocated': {'0': 10.000000000000002, '1': 0.0}}, 'objective': 30.000000000000007}
'''

'''Expected Output:
Expected solution

: {'variables': {'LandAllocated': {'0': 10.0, '1': 0.0}}, 'objective': 30.0}'''

