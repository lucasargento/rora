# Problem Description:
'''Problem description: Forest Paper makes two types of products: graph paper and music paper. Each type of paper requires the use of two machines, a printing machine and a scanning machine. It takes 3 minutes on the printing machine and 5.5 minutes on the scanning machine to make a ream of graph paper. On the other hand, it takes 1.5 minutes on the printing machine and 3 minutes on the scanning machine to make a ream of music paper. Each machine is available for a maximum of 350 minutes per day. The company sells a package of graph paper at a profit of $4 and a package of music paper at a profit of $2.5. The company can sell all the paper it makes. How many reams of each type should the company produce in a day in order to maximize profit? What is that profit?

Expected Output Schema:
{
  "variables": {
    "ProductionQuantity": {
      "0": "float",
      "1": "float"
    }
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Below is a complete and unambiguous formulation using the five‐element framework.

------------------------------------------------------------
Sets:
• P = {Graph, Music}  
  (P is the set of paper types produced by Forest Paper)

Parameters:
• profit_p: profit per ream for paper type p [USD per ream]  
  profit_Graph = 4  
  profit_Music = 2.5

• printing_time_p: printing machine time required per ream for paper type p [minutes per ream]  
  printing_time_Graph = 3  
  printing_time_Music = 1.5

• scanning_time_p: scanning machine time required per ream for paper type p [minutes per ream]  
  scanning_time_Graph = 5.5  
  scanning_time_Music = 3

• max_printing_time: total available printing machine time per day = 350 [minutes]  
• max_scanning_time: total available scanning machine time per day = 350 [minutes]

(Comments: All time parameters are in minutes per ream and machine availabilities are in minutes per day. We assume that the production decision can be taken as a continuous amount.)

Variables:
• x_p: number of reams of paper type p to produce per day [continuous, nonnegative]  
  x_Graph: reams of graph paper  
  x_Music: reams of music paper

Objective:
• Maximize total_profit = profit_Graph * x_Graph + profit_Music * x_Music  
  (i.e., maximize 4 * x_Graph + 2.5 * x_Music)

Constraints:
1. Printing machine time constraint:  
  printing_time_Graph * x_Graph + printing_time_Music * x_Music ≤ max_printing_time  
  => 3 * x_Graph + 1.5 * x_Music ≤ 350

2. Scanning machine time constraint:  
  scanning_time_Graph * x_Graph + scanning_time_Music * x_Music ≤ max_scanning_time  
  => 5.5 * x_Graph + 3 * x_Music ≤ 350

------------------------------------------------------------

This structured model clearly defines the sets, parameters, decision variables, objective function, and constraints. It can be used directly to generate a working implementation in Python or OR-Tools.

Below is a JSON schema snippet that corresponds to the decision variables and objective for reference:

{
  "variables": {
    "ProductionQuantity": {
      "Graph": "float",
      "Music": "float"
    }
  },
  "objective": "float"
}'''

# Generated Code:
#!/usr/bin/env python3
"""
We solve the following production optimization problem for Forest Paper:
  - Produce Graph Paper and Music Paper.
  - Each ream of Graph Paper requires 3 minutes on the printing machine and 5.5 minutes on the scanning machine.
  - Each ream of Music Paper requires 1.5 minutes on the printing machine and 3 minutes on the scanning machine.
  - Each machine is available for 350 minutes per day.
  - Profit per ream: $4 for Graph Paper, $2.5 for Music Paper.
  
We implement two separate models:
1. A continuous linear programming formulation using ortools.linear_solver.
2. An integer model using the CP-SAT solver (CP model) after scaling the coefficients
   to get rid of fractional numbers. In this version production quantities are integer.
  
Each model is implemented fully separately and then both are executed in the main() function.
  
The expected output schema for each is:
{
  "variables": {
    "ProductionQuantity": {
      "Graph": <value>,
      "Music": <value>
    }
  },
  "objective": <objective_value>
}
  
Note: The continuous model is the exact formulation, while the CP-SAT version requires scaling.
"""

from ortools.linear_solver import pywraplp
from ortools.sat.python import cp_model

def solve_with_linear_solver():
    # Create the solver with GLOP for continuous LP.
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Failed to create the linear solver!")
        return None

    # Variables: production quantities (continuous nonnegative)
    x_graph = solver.NumVar(0.0, solver.infinity(), 'x_graph')
    x_music = solver.NumVar(0.0, solver.infinity(), 'x_music')

    # Parameters
    profit_graph = 4.0
    profit_music = 2.5
    printing_time_graph = 3.0
    printing_time_music = 1.5
    scanning_time_graph = 5.5
    scanning_time_music = 3.0
    max_printing_time = 350.0
    max_scanning_time = 350.0

    # Objective: maximize profit = 4*x_graph + 2.5*x_music
    objective = solver.Objective()
    objective.SetCoefficient(x_graph, profit_graph)
    objective.SetCoefficient(x_music, profit_music)
    objective.SetMaximization()

    # Constraints:
    # 1. Printing machine time: 3*x_graph + 1.5*x_music <= 350
    solver.Add(printing_time_graph * x_graph + printing_time_music * x_music <= max_printing_time)
    
    # 2. Scanning machine time: 5.5*x_graph + 3*x_music <= 350
    solver.Add(scanning_time_graph * x_graph + scanning_time_music * x_music <= max_scanning_time)
    
    status = solver.Solve()
    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result["variables"] = {
            "ProductionQuantity": {
                "Graph": x_graph.solution_value(),
                "Music": x_music.solution_value()
            }
        }
        result["objective"] = objective.Value()
    else:
        result["error"] = "The LP problem does not have an optimal solution."
    return result

def solve_with_cp_model():
    # Create the CP-SAT model.
    # In CP-SAT, only integer variables are available, so we scale coefficients by factor 2
    # to eliminate decimals:
    #  Printing constraint: 3*x_graph + 1.5*x_music <= 350   -> multiply by 2 -> 6*x_graph + 3*x_music <= 700
    #  Scanning constraint: 5.5*x_graph + 3*x_music <= 350   -> multiply by 2 -> 11*x_graph + 6*x_music <= 700
    #  Objective: maximize 4*x_graph + 2.5*x_music   -> multiply by 2 -> maximize 8*x_graph + 5*x_music
    model = cp_model.CpModel()
    
    # We assume the production quantities are integers.
    # Set reasonable upper bounds. For example, graph production cannot exceed 700/6.
    max_graph = 700 // 6 + 10
    max_music = 700 // 3 + 10
    x_graph = model.NewIntVar(0, int(max_graph), 'x_graph')
    x_music = model.NewIntVar(0, int(max_music), 'x_music')
    
    # Constraints:
    # 1. Printing machine time: 6*x_graph + 3*x_music <= 700
    model.Add(6 * x_graph + 3 * x_music <= 700)
    # 2. Scanning machine time: 11*x_graph + 6*x_music <= 700
    model.Add(11 * x_graph + 6 * x_music <= 700)
    
    # Objective: maximize 8*x_graph + 5*x_music. 
    # Note: The true profit corresponds to (objective_value/2) in dollars.
    model.Maximize(8 * x_graph + 5 * x_music)
    
    # Solve the CP model.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    
    result = {}
    if status in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
        # To get the profit in original dollars, we divide the objective by 2.
        objective_value = solver.ObjectiveValue() / 2.0
        result["variables"] = {
            "ProductionQuantity": {
                "Graph": solver.Value(x_graph),
                "Music": solver.Value(x_music)
            }
        }
        result["objective"] = objective_value
    else:
        result["error"] = "The CP-SAT problem does not have an optimal solution."
    return result

def main():
    # Solve using the continuous linear programming formulation.
    lp_result = solve_with_linear_solver()
    
    # Solve using the CP-SAT (integer, scaled) formulation.
    cp_result = solve_with_cp_model()
    
    # Print the structured results.
    print("Results from Linear Solver (Continuous LP):")
    if "error" in lp_result:
        print(lp_result["error"])
    else:
        print(lp_result)
        
    print("\nResults from CP-SAT Model (Integer variables, scaled formulation):")
    if "error" in cp_result:
        print(cp_result["error"])
    else:
        print(cp_result)

if __name__ == "__main__":
    main()

'''Execution Results:
SUCCESS:
Results from Linear Solver (Continuous LP):
{'variables': {'ProductionQuantity': {'Graph': 0.0, 'Music': 116.66666666666666}}, 'objective': 291.66666666666663}

Results from CP-SAT Model (Integer variables, scaled formulation):
{'variables': {'ProductionQuantity': {'Graph': 2, 'Music': 113}}, 'objective': 290.5}
'''

'''Expected Output:
Expected solution

: {'variables': {'ProductionQuantity': {'0': 0.0, '1': 116.66666666666667}}, 'objective': 291.6666666666667}'''

