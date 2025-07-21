# Problem Description:
'''Problem description: An oil and gas company is sending their oil to the port using containers and trucks. A container can hold 30 units of oil while a truck can hold 40 units of oil. Due to government restrictions, the number of trucks used has to at most half the number of containers used. If at least 2000 units of oil need to be sent to the port and at least 15 containers need to be used, minimize the total number of containers and trucks needed.

Expected Output Schema:
{
  "variables": {
    "NumContainers": "float",
    "NumTrucks": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Below is the five‐element structured model for the oil and gas container and truck transportation problem.

--------------------------------------------------
Sets:
- V = {Containers, Trucks}  
  (Note: Although there are only two decision types, we list them to show that our decisions pertain to the two vehicle types.)

--------------------------------------------------
Parameters:
- container_capacity = 30   (units of oil per container)
- truck_capacity = 40       (units of oil per truck)
- min_oil = 2000            (minimum total oil to be transported, in oil units)
- min_containers = 15       (minimum number of containers required)
- max_truck_ratio = 0.5     (government restriction: the number of trucks must be at most half the number of containers)

--------------------------------------------------
Variables:
- NumContainers: Number of containers used (integer, ≥ 0) [units: container count]
- NumTrucks: Number of trucks used (integer, ≥ 0) [units: truck count]

--------------------------------------------------
Objective:
- Minimize Total_Vehicles = NumContainers + NumTrucks  
  (This represents the minimization of the total number of containers and trucks used.)

--------------------------------------------------
Constraints:
1. Oil Capacity Requirement:
   container_capacity * NumContainers + truck_capacity * NumTrucks ≥ min_oil  
   [The combined capacity of the containers and trucks must be at least 2000 units.]

2. Minimum Container Requirement:
   NumContainers ≥ min_containers  
   [At least 15 containers must be used.]

3. Truck-to-Container Ratio (Government Restriction):
   NumTrucks ≤ max_truck_ratio * NumContainers  
   [The number of trucks used must be no more than half the number of containers.]

--------------------------------------------------
Additional Comments:
- All parameters are assumed to be in consistent units (oil in "units" and vehicles as counts). 
- Although the expected output schema lists decision variables as floats, here the variables are defined as integers to reflect that the number of containers and trucks must be whole numbers.
  
--------------------------------------------------
Expected Output Schema Example for Reference:
{
  "variables": {
    "NumContainers": "float",
    "NumTrucks": "float"
  },
  "objective": "float"
}

This complete and self-contained model can directly guide a working implementation in Python or OR-Tools.'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp
from ortools.sat.python import cp_model

def solve_with_linear_solver():
    # Create the MIP solver with SCIP backend.
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        print("Error: SCIP solver unavailable.")
        return None

    # Sets and Parameters
    container_capacity = 30
    truck_capacity = 40
    min_oil = 2000
    min_containers = 15
    max_truck_ratio = 0.5  # trucks <= 0.5 * containers

    # Variables: Using integer variables.
    # Even though output schema mentions float, the decision counts must be integer.
    NumContainers = solver.IntVar(min_containers, solver.infinity(), 'NumContainers')
    NumTrucks = solver.IntVar(0, solver.infinity(), 'NumTrucks')

    # Constraints
    # 1. Oil Capacity Requirement:
    #    container_capacity * NumContainers + truck_capacity * NumTrucks >= min_oil
    solver.Add(container_capacity * NumContainers + truck_capacity * NumTrucks >= min_oil)

    # 2. Minimum Container Requirement is already enforced by lower bound.
    # 3. Truck-to-Container Ratio:
    #    NumTrucks <= max_truck_ratio * NumContainers
    # This is equivalent to: 2 * NumTrucks - NumContainers <= 0.
    solver.Add(NumTrucks <= max_truck_ratio * NumContainers)

    # Objective: Minimize Total Vehicles = NumContainers + NumTrucks.
    solver.Minimize(NumContainers + NumTrucks)

    # Solve the model.
    status = solver.Solve()

    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "variables": {
                "NumContainers": NumContainers.solution_value(),
                "NumTrucks": NumTrucks.solution_value()
            },
            "objective": solver.Objective().Value()
        }
    else:
        result = {"message": "The linear solver could not find an optimal solution."}
    return result

def solve_with_cp_model():
    # Create the CP-SAT model.
    model = cp_model.CpModel()

    # Sets and Parameters
    container_capacity = 30
    truck_capacity = 40
    min_oil = 2000
    min_containers = 15
    max_truck_ratio = 0.5  # trucks <= 0.5 * containers
    # For CP-SAT, we transform trucks <= 0.5 * containers to an equivalent integer constraint:
    # Multiply both sides by 2: 2 * trucks <= containers.
    
    # Variables: we set a reasonable upper bound.
    # Upper bounds chosen arbitrarily high enough.
    max_bound = 10000  
    NumContainers = model.NewIntVar(min_containers, max_bound, 'NumContainers')
    NumTrucks = model.NewIntVar(0, max_bound, 'NumTrucks')

    # Constraints
    # 1. Oil Capacity Requirement:
    #    container_capacity * NumContainers + truck_capacity * NumTrucks >= min_oil
    model.Add(container_capacity * NumContainers + truck_capacity * NumTrucks >= min_oil)

    # 2. Minimum Container Requirement is inherently enforced by variable lower bound.
    # 3. Truck to Container Ratio:
    #    NumTrucks <= max_truck_ratio * NumContainers becomes 2 * NumTrucks <= NumContainers.
    model.Add(2 * NumTrucks <= NumContainers)

    # Objective: Minimize Total Vehicles = NumContainers + NumTrucks.
    objective_var = model.NewIntVar(0, max_bound, 'TotalVehicles')
    model.Add(objective_var == NumContainers + NumTrucks)
    model.Minimize(objective_var)

    # Solve the CP-SAT model.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    result = {}
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        result = {
            "variables": {
                "NumContainers": solver.Value(NumContainers),
                "NumTrucks": solver.Value(NumTrucks)
            },
            "objective": solver.Value(objective_var)
        }
    else:
        result = {"message": "The CP-SAT solver could not find an optimal solution."}
    return result

def main():
    print("Solution from Linear Solver (MIP):")
    linear_result = solve_with_linear_solver()
    print(linear_result)
    
    print("\nSolution from CP-SAT Model:")
    cp_result = solve_with_cp_model()
    print(cp_result)

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Solution from Linear Solver (MIP):
{'variables': {'NumContainers': 40.0, 'NumTrucks': 20.0}, 'objective': 60.000000000000014}

Solution from CP-SAT Model:
{'variables': {'NumContainers': 40, 'NumTrucks': 20}, 'objective': 60}
'''

'''Expected Output:
Expected solution

: {'variables': {'NumContainers': 40.0, 'NumTrucks': 20.0}, 'objective': 60.0}'''

