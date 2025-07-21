# Problem Description:
'''Problem description: A hobbyist makes model trains and planes using wood and paint. A model train requires 3 units of wood and 3 units of paint. A model plane requires 4 units of wood and 2 units of paint. The hobbyist has available 120 units of wood and 90 units of paint. If the profit per model train is $8 and the profit per model plane is $10, how many of each should be made to maximize his profit?

Expected Output Schema:
{
  "variables": {
    "NumberOfTrains": "float",
    "NumberOfPlanes": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- Products: {Train, Plane}

Parameters:
- profit_Product: profit per unit produced [USD per unit] where
  - profit_Train = 8
  - profit_Plane = 10
- woodRequired_Product: units of wood required per unit produced [wood units per unit] where
  - woodRequired_Train = 3
  - woodRequired_Plane = 4
- paintRequired_Product: units of paint required per unit produced [paint units per unit] where
  - paintRequired_Train = 3
  - paintRequired_Plane = 2
- availableWood: total available wood [wood units] = 120
- availablePaint: total available paint [paint units] = 90

Variables:
- NumberOfTrains: number of model trains to produce (decision variable, continuous nonnegative value; in practical implementation, you may require integer values)
- NumberOfPlanes: number of model planes to produce (decision variable, continuous nonnegative value; in practical implementation, you may require integer values)

Objective:
- Maximize total profit = (profit_Train * NumberOfTrains) + (profit_Plane * NumberOfPlanes)
  - This represents the total revenue from selling the produced models.

Constraints:
1. Wood constraint: (woodRequired_Train * NumberOfTrains) + (woodRequired_Plane * NumberOfPlanes) ≤ availableWood  
   i.e., 3*NumberOfTrains + 4*NumberOfPlanes ≤ 120
2. Paint constraint: (paintRequired_Train * NumberOfTrains) + (paintRequired_Plane * NumberOfPlanes) ≤ availablePaint  
   i.e., 3*NumberOfTrains + 2*NumberOfPlanes ≤ 90
3. Nonnegativity constraints:
   - NumberOfTrains ≥ 0
   - NumberOfPlanes ≥ 0

----------------------------------
Expected Output Schema (as required):
{
  "variables": {
    "NumberOfTrains": "float",
    "NumberOfPlanes": "float"
  },
  "objective": "float"
}'''

# Generated Code:
from ortools.linear_solver import pywraplp

def solve_model_linear():
    # Create the linear solver using the GLOP backend for linear programming.
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Solver not created.")
        return None

    # Define decision variables: continuous nonnegative variables.
    # In practice these might be integers, but here we follow the formulation as continuous.
    NumberOfTrains = solver.NumVar(0.0, solver.infinity(), "NumberOfTrains")
    NumberOfPlanes = solver.NumVar(0.0, solver.infinity(), "NumberOfPlanes")

    # Add constraints.
    # Wood constraint: 3*NumberOfTrains + 4*NumberOfPlanes <= 120
    solver.Add(3 * NumberOfTrains + 4 * NumberOfPlanes <= 120)
    # Paint constraint: 3*NumberOfTrains + 2*NumberOfPlanes <= 90
    solver.Add(3 * NumberOfTrains + 2 * NumberOfPlanes <= 90)

    # Set the objective function: Maximize total profit = 8*NumberOfTrains + 10*NumberOfPlanes.
    objective = solver.Objective()
    objective.SetCoefficient(NumberOfTrains, 8)
    objective.SetCoefficient(NumberOfPlanes, 10)
    objective.SetMaximization()

    # Solve the optimization problem.
    status = solver.Solve()

    # Check for optimal solution.
    if status != pywraplp.Solver.OPTIMAL:
        print("The problem does not have an optimal solution!")
        return None

    # Create a structured result as specified.
    result = {
        "variables": {
            "NumberOfTrains": NumberOfTrains.solution_value(),
            "NumberOfPlanes": NumberOfPlanes.solution_value()
        },
        "objective": objective.Value()
    }
    return result

def main():
    # Since only one formulation was provided, we call the linear model implementation.
    linear_solution = solve_model_linear()
    
    if linear_solution:
        print("Linear model solution:")
        print(linear_solution)
    else:
        print("No feasible solution found for the linear model.")

if __name__ == "__main__":
    main()

'''Execution Results:
SUCCESS:
Linear model solution:
{'variables': {'NumberOfTrains': 20.000000000000004, 'NumberOfPlanes': 14.999999999999993}, 'objective': 310.0}
'''

'''Expected Output:
Expected solution

: {'variables': {'NumberOfTrains': 20.0, 'NumberOfPlanes': 15.0}, 'objective': 310.0}'''

