# Problem Description:
'''Problem description: A dog school trains labradors and golden retrievers to deliver newspaper. A labrador can deliver 7 newspapers at a time and requires 5 small bone treats for service. A golden retriever can deliver 10 newspapers at a time and requires 6 small bone treats per service. The school only has 1500 small bone treats available. In addition, at least 50 golden retrievers must be used and at most 60% of the dogs can be labradors. How many of each dog should be used to maximize the number of newspapers that can be delivered?

Expected Output Schema:
{
  "variables": {
    "ServicesDelivered": {
      "0": "float",
      "1": "float"
    },
    "NumGoldenRetrievers": "float",
    "NumLabradors": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Below is the complete five‐element structured model for the dog school problem.

──────────────────────────────
Sets:
- DogTypes = {Labrador, GoldenRetriever}

──────────────────────────────
Parameters:
- deliver_capacity[d] (newspapers per service):
  • deliver_capacity[Labrador] = 7
  • deliver_capacity[GoldenRetriever] = 10
    (Each labrador delivers 7 newspapers; each golden retriever delivers 10.)
- treats_required[d] (small bone treats per service):
  • treats_required[Labrador] = 5
  • treats_required[GoldenRetriever] = 6
    (Each labrador requires 5 treats; each golden retriever requires 6 treats.)
- total_treats = 1500    (total small bone treats available)
- min_golden_retrievers = 50  (minimum number of golden retrievers to use)
- max_lab_fraction = 0.6   (At most 60% of all dogs can be labradors. Equivalently, labradors ≤ 60% of (labradors + golden retrievers).)

──────────────────────────────
Variables:
- x[d] for each d in DogTypes: Number of dogs of type d to be used
  • x[Labrador] = NumLabradors (nonnegative integer; number of labradors)
  • x[GoldenRetriever] = NumGoldenRetrievers (nonnegative integer; number of golden retrievers)
- NewspapersDelivered: Total number of newspapers delivered (continuous; computed as 7*x[Labrador] + 10*x[GoldenRetriever])
  • For clarity in implementations, one may define:
    ServicesDelivered[0] = 7 * x[Labrador]
    ServicesDelivered[1] = 10 * x[GoldenRetriever]

──────────────────────────────
Objective:
Maximize NewspapersDelivered = 7 * x[Labrador] + 10 * x[GoldenRetriever]
  (We seek the choice of dogs that maximizes the total number of newspapers delivered.)

──────────────────────────────
Constraints:
1. Treat Supply Constraint:
  5 * x[Labrador] + 6 * x[GoldenRetriever] ≤ 1500
  (The total treats consumed by all dogs cannot exceed the available 1500 treats.)

2. Minimum Golden Retriever Usage:
  x[GoldenRetriever] ≥ 50
  (At least 50 golden retrievers must be used.)

3. Labrador Fraction Constraint:
  x[Labrador] ≤ 0.6 * (x[Labrador] + x[GoldenRetriever])
   Alternatively, rearrange to:
   0.4 * x[Labrador] ≤ 0.6 * x[GoldenRetriever]
   or equivalently,
   x[Labrador] ≤ 1.5 * x[GoldenRetriever]
  (This ensures that labradors represent no more than 60% of the total dogs.)

──────────────────────────────
Expected Output Schema (Mapping for implementation):

{
  "variables": {
    "ServicesDelivered": {
      "0": "7 * NumLabradors (newspapers by labradors)",
      "1": "10 * NumGoldenRetrievers (newspapers by golden retrievers)"
    },
    "NumGoldenRetrievers": "x[GoldenRetriever] (nonnegative integer)",
    "NumLabradors": "x[Labrador] (nonnegative integer)"
  },
  "objective": "7 * NumLabradors + 10 * NumGoldenRetrievers (total newspapers delivered)"
}

──────────────────────────────
Notes:
- All variable counts (dogs) are assumed to be integer. If the implementation requires a continuous relaxation, then enforce non-negativity.
- The constraint expressing that no more than 60% of dogs are labradors is implemented either as 
  x[Labrador] ≤ 0.6 * (x[Labrador] + x[GoldenRetriever]) 
or equivalently as 
  x[Labrador] ≤ 1.5 * x[GoldenRetriever]. 
Both formulations capture the same requirement.
- Units for newspapers and treats are consistent with the problem description.

This model fully represents the real-world problem in a clear and structured manner for subsequent implementation.'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_model_version1():
    # Create the linear solver with the CBC backend.
    solver = pywraplp.Solver.CreateSolver('CBC_MIXED_INTEGER_PROGRAMMING')
    if not solver:
        return None, "Solver not created."

    # Variables: nonnegative integers.
    # x_Labrador: number of labradors (nonnegative integer).
    # x_GoldenRetriever: number of golden retrievers (nonnegative integer).
    x_Labrador = solver.IntVar(0, solver.infinity(), 'NumLabradors')
    x_GoldenRetriever = solver.IntVar(0, solver.infinity(), 'NumGoldenRetrievers')
    
    # Objective: Maximize total newspapers delivered = 7*x_Labrador + 10*x_GoldenRetriever.
    objective = solver.Objective()
    objective.SetCoefficient(x_Labrador, 7)
    objective.SetCoefficient(x_GoldenRetriever, 10)
    objective.SetMaximization()
    
    # Constraint 1: Treat supply constraint: 5*x_Labrador + 6*x_GoldenRetriever <= 1500.
    solver.Add(5 * x_Labrador + 6 * x_GoldenRetriever <= 1500)
    
    # Constraint 2: Minimum golden retrievers: x_GoldenRetriever >= 50.
    solver.Add(x_GoldenRetriever >= 50)
    
    # Constraint 3 (Version 1): Labrador fraction constraint:
    # x_Labrador <= 0.6 * (x_Labrador + x_GoldenRetriever)
    # Rearranging: x_Labrador - 0.6*x_Labrador - 0.6*x_GoldenRetriever <= 0
    # which simplifies to 0.4*x_Labrador - 0.6*x_GoldenRetriever <= 0.
    solver.Add(0.4 * x_Labrador - 0.6 * x_GoldenRetriever <= 0)
    
    # Solve the model.
    status = solver.Solve()
    
    if status == pywraplp.Solver.OPTIMAL:
        solution = {
            "variables": {
                "ServicesDelivered": {
                    "0": 7 * x_Labrador.solution_value(),  # newspapers delivered by labradors
                    "1": 10 * x_GoldenRetriever.solution_value()  # newspapers delivered by golden retrievers
                },
                "NumGoldenRetrievers": x_GoldenRetriever.solution_value(),
                "NumLabradors": x_Labrador.solution_value()
            },
            "objective": objective.Value()
        }
        return solution, None
    elif status == pywraplp.Solver.INFEASIBLE:
        return None, "The problem is infeasible."
    else:
        return None, "The solver did not find an optimal solution."

def solve_model_version2():
    # Create another independent solver for Model Version 2.
    solver = pywraplp.Solver.CreateSolver('CBC_MIXED_INTEGER_PROGRAMMING')
    if not solver:
        return None, "Solver not created."

    # Variables: nonnegative integers.
    x_Labrador = solver.IntVar(0, solver.infinity(), 'NumLabradors')
    x_GoldenRetriever = solver.IntVar(0, solver.infinity(), 'NumGoldenRetrievers')
    
    # Objective: Maximize total newspapers delivered.
    objective = solver.Objective()
    objective.SetCoefficient(x_Labrador, 7)
    objective.SetCoefficient(x_GoldenRetriever, 10)
    objective.SetMaximization()
    
    # Constraint 1: Treat supply constraint.
    solver.Add(5 * x_Labrador + 6 * x_GoldenRetriever <= 1500)
    
    # Constraint 2: Minimum golden retrievers: at least 50.
    solver.Add(x_GoldenRetriever >= 50)
    
    # Constraint 3 (Version 2): Labrador fraction constraint alternative:
    # x_Labrador <= 1.5 * x_GoldenRetriever
    solver.Add(x_Labrador <= 1.5 * x_GoldenRetriever)
    
    # Solve the model.
    status = solver.Solve()
    
    if status == pywraplp.Solver.OPTIMAL:
        solution = {
            "variables": {
                "ServicesDelivered": {
                    "0": 7 * x_Labrador.solution_value(),  # newspapers delivered by labradors
                    "1": 10 * x_GoldenRetriever.solution_value()  # newspapers delivered by golden retrievers
                },
                "NumGoldenRetrievers": x_GoldenRetriever.solution_value(),
                "NumLabradors": x_Labrador.solution_value()
            },
            "objective": objective.Value()
        }
        return solution, None
    elif status == pywraplp.Solver.INFEASIBLE:
        return None, "The problem is infeasible."
    else:
        return None, "The solver did not find an optimal solution."

def main():
    # Solve model version 1 using the formulation:
    # x_Labrador <= 0.6*(x_Labrador + x_GoldenRetriever)
    sol1, err1 = solve_model_version1()
    
    # Solve model version 2 using the alternative formulation:
    # x_Labrador <= 1.5*x_GoldenRetriever
    sol2, err2 = solve_model_version2()
    
    print("Results for Model Version 1 (using x_Labrador <= 0.6*(x_Labrador + x_GoldenRetriever)):")
    if sol1:
        print(sol1)
    else:
        print("Error:", err1)
    
    print("\nResults for Model Version 2 (using x_Labrador <= 1.5*x_GoldenRetriever):")
    if sol2:
        print(sol2)
    else:
        print("Error:", err2)

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Results for Model Version 1 (using x_Labrador <= 0.6*(x_Labrador + x_GoldenRetriever)):
{'variables': {'ServicesDelivered': {'0': 0.0, '1': 2500.0}, 'NumGoldenRetrievers': 250.0, 'NumLabradors': 0.0}, 'objective': 2500.0}

Results for Model Version 2 (using x_Labrador <= 1.5*x_GoldenRetriever):
{'variables': {'ServicesDelivered': {'0': 0.0, '1': 2500.0}, 'NumGoldenRetrievers': 250.0, 'NumLabradors': 0.0}, 'objective': 2500.0}
'''

'''Expected Output:
Expected solution

: {'variables': {'ServicesDelivered': {'0': -0.0, '1': 250.0}, 'NumGoldenRetrievers': 50.0, 'NumLabradors': -0.0}, 'objective': 2500.0}'''

