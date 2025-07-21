# Problem Description:
'''Problem description: A food company would like to run its commercials on three streaming platforms: Pi TV, Beta Video and Gamma Live. The cost for a commercial as well as the expected audience reach is given. On Pi TV, a commercial costs $1200 and attracts 2000 viewers. On Beta Video, a commercial costs $2000 and attracts 5000 viewers. On Gamma Live, a commercial costs $4000 and attracts 9000 viewers. Beta Video limits the number of commercials from a single company to 8. In order to attract a wide range of people, at most a third of all commercials should occur on Gamma Live and a minimum of 20% should occur on Pi TV. If the weekly budget is $20000, how many commercials should be run in each of the three possible choices in order to maximize audience?

Expected Output Schema:
{
  "variables": {
    "NumberPiTV": "float",
    "NumberBetaVideo": "float",
    "NumberGammaLive": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- P: set of streaming platforms = {PiTV, BetaVideo, GammaLive}

Parameters:
- cost_PiTV = 1200 (USD per commercial on Pi TV)
- cost_BetaVideo = 2000 (USD per commercial on Beta Video)
- cost_GammaLive = 4000 (USD per commercial on Gamma Live)
- reach_PiTV = 2000 (viewers per commercial on Pi TV)
- reach_BetaVideo = 5000 (viewers per commercial on Beta Video)
- reach_GammaLive = 9000 (viewers per commercial on Gamma Live)
- budget = 20000 (USD available per week)
- max_BetaVideo = 8 (maximum commercials allowed on Beta Video)
- gammaMaxFraction = 1/3 (maximum fraction of total commercials that may be on Gamma Live)
- piMinFraction = 0.20 (minimum fraction of total commercials that must be on Pi TV)

Variables:
- NumberPiTV: number of commercials to run on Pi TV [integer ≥ 0, units: commercials]
- NumberBetaVideo: number of commercials to run on Beta Video [integer ≥ 0, units: commercials]
- NumberGammaLive: number of commercials to run on Gamma Live [integer ≥ 0, units: commercials]

Objective:
- Maximize total audience reach, defined as:
  TotalReach = reach_PiTV * NumberPiTV + reach_BetaVideo * NumberBetaVideo + reach_GammaLive * NumberGammaLive

Constraints:
1. Budget constraint:
   cost_PiTV * NumberPiTV + cost_BetaVideo * NumberBetaVideo + cost_GammaLive * NumberGammaLive ≤ budget

2. Beta Video commercial limit:
   NumberBetaVideo ≤ max_BetaVideo

3. Gamma Live proportion constraint:
   NumberGammaLive ≤ gammaMaxFraction * (NumberPiTV + NumberBetaVideo + NumberGammaLive)

4. Pi TV minimum proportion constraint:
   NumberPiTV ≥ piMinFraction * (NumberPiTV + NumberBetaVideo + NumberGammaLive)

Additional Notes:
- All parameters use consistent units. Costs are in USD per commercial, audience reach is in viewers per commercial, and the budget is in USD per week.
- Decision variables are assumed to be integers as partial commercials are not meaningful.
- It is assumed that the specified proportions (at most one third and at least 20%) are computed with respect to the total number of commercials run.
- This model is self-contained and can be directly implemented using optimization libraries such as OR-Tools.

Return in the Expected Output Schema format:
{
  "variables": {
    "NumberPiTV": "integer ≥ 0",
    "NumberBetaVideo": "integer ≥ 0",
    "NumberGammaLive": "integer ≥ 0"
  },
  "objective": "Maximize TotalReach = 2000*NumberPiTV + 5000*NumberBetaVideo + 9000*NumberGammaLive"
}'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_linear_program():
    # Create the solver with the SCIP backend.
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        print("Solver not created.")
        return None

    # Parameters
    cost_PiTV = 1200
    cost_BetaVideo = 2000
    cost_GammaLive = 4000
    reach_PiTV = 2000
    reach_BetaVideo = 5000
    reach_GammaLive = 9000
    budget = 20000
    max_BetaVideo = 8

    # In the constraints,
    # Gamma Live fraction: NumberGammaLive <= (1/3)*TotalCommercials.
    # Let Total = NumberPiTV + NumberBetaVideo + NumberGammaLive.
    # Multiply by 3: 3*NumberGammaLive <= Total => 2*NumberGammaLive <= NumberPiTV + NumberBetaVideo.
    #
    # Pi TV minimum fraction: NumberPiTV >= 0.20*Total.
    # Multiply by 5: 5*NumberPiTV >= Total => 4*NumberPiTV >= NumberBetaVideo + NumberGammaLive.

    # Variables: non-negative integers
    NumberPiTV = solver.IntVar(0, solver.infinity(), "NumberPiTV")
    NumberBetaVideo = solver.IntVar(0, solver.infinity(), "NumberBetaVideo")
    NumberGammaLive = solver.IntVar(0, solver.infinity(), "NumberGammaLive")
    
    # Constraint: Budget
    solver.Add(cost_PiTV * NumberPiTV + cost_BetaVideo * NumberBetaVideo + cost_GammaLive * NumberGammaLive <= budget)
    
    # Constraint: Beta Video max limit
    solver.Add(NumberBetaVideo <= max_BetaVideo)
    
    # Constraint: Gamma Live proportion: 2*NumberGammaLive <= NumberPiTV + NumberBetaVideo.
    solver.Add(2 * NumberGammaLive <= NumberPiTV + NumberBetaVideo)
    
    # Constraint: Pi TV minimum proportion: 4*NumberPiTV >= NumberBetaVideo + NumberGammaLive.
    solver.Add(4 * NumberPiTV >= NumberBetaVideo + NumberGammaLive)
    
    # Objective: Maximize total audience reach
    objective = solver.Objective()
    objective.SetCoefficient(NumberPiTV, reach_PiTV)
    objective.SetCoefficient(NumberBetaVideo, reach_BetaVideo)
    objective.SetCoefficient(NumberGammaLive, reach_GammaLive)
    objective.SetMaximization()
    
    # Solve the problem and check the result status.
    result_status = solver.Solve()
    if result_status != pywraplp.Solver.OPTIMAL and result_status != pywraplp.Solver.FEASIBLE:
        print("The problem does not have an optimal solution!")
        return None

    # Collect the solution results
    solution = {
        "LinearSolver": {
            "NumberPiTV": NumberPiTV.solution_value(),
            "NumberBetaVideo": NumberBetaVideo.solution_value(),
            "NumberGammaLive": NumberGammaLive.solution_value(),
            "ObjectiveValue": objective.Value()
        }
    }
    return solution

def main():
    solutions = {}
    
    # Implementation 1: Using OR-Tools Linear Solver
    lin_solution = solve_linear_program()
    if lin_solution is None:
        solutions["LinearSolver"] = "No optimal solution found or model infeasible."
    else:
        solutions["LinearSolver"] = lin_solution["LinearSolver"]
    
    # Print results in a structured format.
    print("Optimal Solutions:")
    for model, sol in solutions.items():
        print(f"Model: {model}")
        if isinstance(sol, dict):
            print(f"  NumberPiTV: {sol['NumberPiTV']}")
            print(f"  NumberBetaVideo: {sol['NumberBetaVideo']}")
            print(f"  NumberGammaLive: {sol['NumberGammaLive']}")
            print(f"  Objective Value (Total Audience Reach): {sol['ObjectiveValue']}")
        else:
            print(sol)
    
if __name__ == "__main__":
    main()

'''Execution Results:
SUCCESS:
Optimal Solutions:
Model: LinearSolver
  NumberPiTV: 3.0
  NumberBetaVideo: 8.0
  NumberGammaLive: 0.0
  Objective Value (Total Audience Reach): 46000.0
'''

'''Expected Output:
Expected solution

: {'variables': {'NumberPiTV': 3.0, 'NumberBetaVideo': 8.0, 'NumberGammaLive': 0.0}, 'objective': 46000.0}'''

