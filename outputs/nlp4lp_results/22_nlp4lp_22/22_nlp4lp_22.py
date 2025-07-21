# Problem Description:
'''Problem description: Ayse produces a plant growth compound by mixing two types of fertilizer: C and Y. This growth compound must contain at least 5 units of nitrous oxide and 8 units of vitamin mix. Fertilizer C and Y cost $2 and $3 per kg respectively. Fertilizer C contains 1.5 units of nitrous oxide per kg and 3 units of vitamin mix per kg. Fertilizer Y contains 5 units of nitrous oxide per kg and 1 unit of vitamin mix per kg. Determine the minimum cost of Ayse's compound.

Expected Output Schema:
{
  "variables": {
    "FertilizerQuantity": [
      "float"
    ]
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- F: set of fertilizers = {C, Y}

Parameters:
- cost_f: cost per kg for fertilizer f [USD/kg], where cost_C = 2 and cost_Y = 3.
- nitrous_f: units of nitrous oxide per kg for fertilizer f, where nitrous_C = 1.5 and nitrous_Y = 5.
- vitamin_f: units of vitamin mix per kg for fertilizer f, where vitamin_C = 3 and vitamin_Y = 1.
- min_nitrous: minimum required units of nitrous oxide = 5 [units].
- min_vitamin: minimum required units of vitamin mix = 8 [units].

Variables:
- x_f: quantity (kg) of fertilizer f used in the compound [continuous, x_f ≥ 0].

Objective:
- Minimize total cost = cost_C * x_C + cost_Y * x_Y [USD].

Constraints:
- Nitrous oxide requirement: nitrous_C * x_C + nitrous_Y * x_Y ≥ min_nitrous.
- Vitamin mix requirement: vitamin_C * x_C + vitamin_Y * x_Y ≥ min_vitamin.

Notes:
- All costs are in USD per kg.
- The nutrient content for each fertilizer is given per kg. Ensure that the total nutrients from the mix meet or exceed the minimum requirements.
- x_f are continuous variables representing the weight in kilograms of each fertilizer used.'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp
from ortools.sat.python import cp_model

def solve_with_linear_solver():
    # Create a linear solver using GLOP.
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Failed to create linear solver.")
        return None

    # Variables: x_C and x_Y (quantities in kg, continuous >= 0)
    x_C = solver.NumVar(0.0, solver.infinity(), 'x_C')
    x_Y = solver.NumVar(0.0, solver.infinity(), 'x_Y')
    
    # Parameters
    cost_C = 2
    cost_Y = 3
    nitrous_C = 1.5
    nitrous_Y = 5
    vitamin_C = 3
    vitamin_Y = 1
    min_nitrous = 5
    min_vitamin = 8

    # Objective: Minimize cost = 2*x_C + 3*x_Y
    solver.Minimize(cost_C * x_C + cost_Y * x_Y)

    # Constraints:
    # Nitrous oxide: 1.5*x_C + 5*x_Y >= 5
    solver.Add(nitrous_C * x_C + nitrous_Y * x_Y >= min_nitrous)
    # Vitamin mix: 3*x_C + 1*x_Y >= 8
    solver.Add(vitamin_C * x_C + vitamin_Y * x_Y >= min_vitamin)

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        solution = {
            "variables": {
                "FertilizerQuantity": [x_C.solution_value(), x_Y.solution_value()]
            },
            "objective": solver.Objective().Value()
        }
    else:
        solution = {"message": "No feasible solution found using linear solver."}
    return solution

def solve_with_cp_sat():
    # For CP-SAT we need to discretize the continuous variables.
    # We'll assume two decimals of precision. Let scale = 100.
    scale = 100
    model = cp_model.CpModel()

    # Define reasonable upper bounds (say 1000 scaled units which equals 10.00 kg)
    upper_bound = 1000  # represents 10.00 kg
    x_C = model.NewIntVar(0, upper_bound, 'x_C')
    x_Y = model.NewIntVar(0, upper_bound, 'x_Y')

    # Parameters scaled appropriately:
    # Real variable = (int variable)/scale.
    # Objective: minimize (2*x_C + 3*x_Y) / scale. Multiply by scale to avoid fractions.
    # Constraints:
    # Nitrous oxide: 1.5*(x_C/scale) + 5*(x_Y/scale) >= 5  --> 1.5*x_C + 5*x_Y >= 5*scale
    # Vitamin mix: 3*(x_C/scale) + 1*(x_Y/scale) >= 8    --> 3*x_C + x_Y >= 8*scale
    model.Add( (15 * x_C + 50 * x_Y) >= 5 * scale * 10 ) 
    # Explanation: Multiply 1.5*x_C by 10 gives 15*x_C; Multiply 5*x_Y by 10 gives 50*x_Y;
    # then right side: 5*scale*10 = 5*100*10 = 5000. This maintains integer coefficients.
    # Alternatively, we can multiply both sides of the inequality by 10.

    model.Add( 3 * x_C + x_Y >= 8 * scale )

    # Objective: minimize (2*x_C + 3*x_Y) i.e. scaled cost = (2*x_C + 3*x_Y) / scale.
    model.Minimize(2 * x_C + 3 * x_Y)

    # Solve the model.
    cp_solver = cp_model.CpSolver()
    status = cp_solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        # Convert the scaled integer variables back to floats with two-decimal precision.
        sol_x_C = cp_solver.Value(x_C) / scale
        sol_x_Y = cp_solver.Value(x_Y) / scale
        objective_val = (2 * cp_solver.Value(x_C) + 3 * cp_solver.Value(x_Y)) / scale
        solution = {
            "variables": {
                "FertilizerQuantity": [sol_x_C, sol_x_Y]
            },
            "objective": objective_val
        }
    else:
        solution = {"message": "No feasible solution found using CP-SAT."}
    return solution

def main():
    print("Results using OR-Tools Linear Solver (GLOP):")
    linear_solution = solve_with_linear_solver()
    print(linear_solution)
    
    print("\nResults using OR-Tools CP-SAT (discretized version):")
    cp_solution = solve_with_cp_sat()
    print(cp_solution)

if __name__ == "__main__":
    main()

'''Execution Results:
SUCCESS:
Results using OR-Tools Linear Solver (GLOP):
{'variables': {'FertilizerQuantity': [2.592592592592592, 0.22222222222222232]}, 'objective': 5.851851851851851}

Results using OR-Tools CP-SAT (discretized version):
{'variables': {'FertilizerQuantity': [2.6, 0.22]}, 'objective': 5.86}
'''

'''Expected Output:
Expected solution

: {'variables': {'FertilizerQuantity': [2.5925925925925926, 0.22222222222222224]}, 'objective': 5.851851851851852}'''

