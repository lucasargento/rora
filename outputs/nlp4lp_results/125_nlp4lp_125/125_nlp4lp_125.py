# Problem Description:
'''Problem description: A chocolate company can transport their boxes of chocolate either using their own vans or by renting trucks. Their vans can transport 50 boxes per trip while a truck can transport 80 boxes per trip. Since they own their vans, the cost per van trip is $30 while the cost per truck trip is $50. The company needs to transport at least 1500 boxes of chocolate and they have a budget of $1000. Since the vans also provide advertising, the number of trips by van must be larger than the number of trips by trucks. How many of trip by each should be done to minimize the total number of trips?

Expected Output Schema:
{
  "variables": {
    "VanTrips": "float",
    "TruckTrips": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- TransportModes: {Van, Truck}

Parameters:
- VanCapacity: number of boxes that can be transported per van trip (value = 50 boxes/trip)
- TruckCapacity: number of boxes that can be transported per truck trip (value = 80 boxes/trip)
- VanCost: cost per van trip (value = 30 dollars/trip)
- TruckCost: cost per truck trip (value = 50 dollars/trip)
- RequiredBoxes: minimum number of boxes to transport (value = 1500 boxes)
- Budget: maximum allowed transportation cost (value = 1000 dollars)

Variables:
- VanTrips: number of trips made with vans (decision variable, nonnegative integer; note that while the expected output schema indicates "float", conceptually this represents an integer number of trips)
- TruckTrips: number of trips made with trucks (decision variable, nonnegative integer)

Objective:
- Minimize total trips = VanTrips + TruckTrips

Constraints:
1. Capacity Constraint: (VanCapacity * VanTrips) + (TruckCapacity * TruckTrips) ≥ RequiredBoxes
   - That is: 50 * VanTrips + 80 * TruckTrips ≥ 1500

2. Budget Constraint: (VanCost * VanTrips) + (TruckCost * TruckTrips) ≤ Budget
   - That is: 30 * VanTrips + 50 * TruckTrips ≤ 1000

3. Advertising Constraint: VanTrips must be strictly greater than TruckTrips.
   - Since trips are integer quantities, enforce VanTrips ≥ TruckTrips + 1

// Note: All units are consistent with the problem statement (boxes, dollars, trips). The decision variables are defined as nonnegative; if fractional trips are allowed the variables could be continuous (float), but typically trips are integer values. The model above follows the five-element format as required.

Expected Output Schema:
{
  "variables": {
    "VanTrips": "float",
    "TruckTrips": "float"
  },
  "objective": "float"
}'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp
from ortools.sat.python import cp_model

def solve_with_linear_solver():
    # Create the MIP solver using CBC
    solver = pywraplp.Solver.CreateSolver('CBC_MIXED_INTEGER_PROGRAMMING')
    if not solver:
        return None, "Linear solver unavailable."
    
    # Parameters
    VanCapacity = 50
    TruckCapacity = 80
    VanCost = 30
    TruckCost = 50
    RequiredBoxes = 1500
    Budget = 1000

    # Decision Variables: Using integer values even though output is float.
    VanTrips = solver.IntVar(0, solver.infinity(), 'VanTrips')
    TruckTrips = solver.IntVar(0, solver.infinity(), 'TruckTrips')

    # Constraints
    # 1. Capacity Constraint: 50 * VanTrips + 80 * TruckTrips >= 1500
    solver.Add(VanCapacity * VanTrips + TruckCapacity * TruckTrips >= RequiredBoxes)
    # 2. Budget Constraint: 30 * VanTrips + 50 * TruckTrips <= 1000
    solver.Add(VanCost * VanTrips + TruckCost * TruckTrips <= Budget)
    # 3. Advertising Constraint: VanTrips >= TruckTrips + 1
    solver.Add(VanTrips >= TruckTrips + 1)

    # Objective: Minimize total trips = VanTrips + TruckTrips
    objective = solver.Objective()
    objective.SetCoefficient(VanTrips, 1)
    objective.SetCoefficient(TruckTrips, 1)
    objective.SetMinimization()

    # Solve
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        solution = {
            "variables": {
                "VanTrips": float(VanTrips.solution_value()),
                "TruckTrips": float(TruckTrips.solution_value())
            },
            "objective": float(objective.Value())
        }
        return solution, None
    elif status == pywraplp.Solver.INFEASIBLE:
        return None, "No feasible solution found (Linear Solver)."
    else:
        return None, "Solver ended with an unexpected status (Linear Solver)."

def solve_with_cp_model():
    # Create the CP-SAT model
    model = cp_model.CpModel()
    
    # Parameters
    VanCapacity = 50
    TruckCapacity = 80
    VanCost = 30
    TruckCost = 50
    RequiredBoxes = 1500
    Budget = 1000
    
    # Without knowing the exact upper bound, we set a reasonable maximum.
    # Budget alone gives an upper bound: For vans, 1000/30 ~33, for trucks: 1000/50 =20.
    # We'll use 100 as an upper bound for both to be safe.
    ub = 100
    VanTrips = model.NewIntVar(0, ub, 'VanTrips')
    TruckTrips = model.NewIntVar(0, ub, 'TruckTrips')

    # Constraints
    # 1. Capacity Constraint: 50 * VanTrips + 80 * TruckTrips >= 1500    
    model.Add(VanCapacity * VanTrips + TruckCapacity * TruckTrips >= RequiredBoxes)
    # 2. Budget Constraint: 30 * VanTrips + 50 * TruckTrips <= 1000
    model.Add(VanCost * VanTrips + TruckCost * TruckTrips <= Budget)
    # 3. Advertising Constraint: VanTrips >= TruckTrips + 1
    model.Add(VanTrips >= TruckTrips + 1)

    # Objective: Minimize total trips = VanTrips + TruckTrips
    objective_var = model.NewIntVar(0, 2*ub, 'TotalTrips')
    model.Add(objective_var == VanTrips + TruckTrips)
    model.Minimize(objective_var)
    
    # Solve the model
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
        solution = {
            "variables": {
                "VanTrips": float(solver.Value(VanTrips)),
                "TruckTrips": float(solver.Value(TruckTrips))
            },
            "objective": float(solver.Value(objective_var))
        }
        return solution, None
    else:
        return None, "No feasible solution found (CP-SAT Solver)."

def main():
    results = {}

    # Solve using the linear solver implementation
    lin_solution, lin_error = solve_with_linear_solver()
    if lin_error:
        results["LinearSolver"] = {"error": lin_error}
    else:
        results["LinearSolver"] = lin_solution

    # Solve using the CP-SAT model implementation
    cp_solution, cp_error = solve_with_cp_model()
    if cp_error:
        results["CpSatSolver"] = {"error": cp_error}
    else:
        results["CpSatSolver"] = cp_solution

    # Print the results in a structured manner
    print("Optimal Solutions:")
    print(results)

if __name__ == "__main__":
    main()

'''Execution Results:
SUCCESS:
Optimal Solutions:
{'LinearSolver': {'variables': {'VanTrips': 14.0, 'TruckTrips': 10.0}, 'objective': 24.0}, 'CpSatSolver': {'variables': {'VanTrips': 13.0, 'TruckTrips': 11.0}, 'objective': 24.0}}
'''

'''Expected Output:
Expected solution

: {'variables': {'VanTrips': 13.0, 'TruckTrips': 11.0}, 'objective': 24.0}'''

