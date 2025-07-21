# Problem Description:
'''Problem description: A company is deciding where to promote their product. Some options include z-tube, soorchle engine, and wassa advertisements. The cost for each option and the number of viewers they each attract is given. On z-tube, each ad costs $1000 and attracts 400,000 viewers. On soorchle, each ad costs $200 and attracts 5,000 viewers. On wassa, each ad costs $100 and attracts 3,000 viewers. Soorchle limits the number of advertisements from a single company to fifteen. Moreover, in order to balance the advertising among the three types of media, at most a third of the total number of advertisements should occur on wassa. And at least 5% should occur on z-tube. The weekly advertising budget is $10000. How many advertisements should be run in each of the three types of media to maximize the total audience?

Expected Output Schema:
{
  "variables": {
    "NumberAdsZTube": "float",
    "NumberAdsSoorchle": "float",
    "NumberAdsWassa": "float",
    "xZ": "float",
    "xS": "float",
    "xW": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Below is a complete and structured mathematical formulation of the advertising placement problem following the five‐element framework.

--------------------------------------------------
Sets:
• MediaOptions = {ZTube, Soorchle, Wassa}

--------------------------------------------------
Parameters:
• cost_ZTube = 1000           // Cost in USD per advertisement on z-tube
• cost_Soorchle = 200         // Cost in USD per advertisement on soorchle engine
• cost_Wassa = 100            // Cost in USD per advertisement on wassa
• viewers_ZTube = 400000      // Number of viewers reached by one ad on z-tube
• viewers_Soorchle = 5000     // Number of viewers reached by one ad on soorchle engine
• viewers_Wassa = 3000        // Number of viewers reached by one ad on wassa
• weekly_budget = 10000       // Total advertising budget per week in USD
• max_Soorchle_ads = 15       // Maximum number of advertisements allowed on soorchle per company
• maxFrac_Wassa = 1/3         // At most one third of the total ads may be on wassa
• minFrac_ZTube = 0.05        // At least 5% of the total ads must appear on z-tube

--------------------------------------------------
Variables:
• x_ZTube: integer ≥ 0  // Number of advertisements to place on z-tube
• x_Soorchle: integer ≥ 0  // Number of advertisements to place on soorchle engine
• x_Wassa: integer ≥ 0  // Number of advertisements to place on wassa

--------------------------------------------------
Objective:
Maximize Total_Viewers
  = (viewers_ZTube * x_ZTube) + (viewers_Soorchle * x_Soorchle) + (viewers_Wassa * x_Wassa)
  = (400000 * x_ZTube) + (5000 * x_Soorchle) + (3000 * x_Wassa)

--------------------------------------------------
Constraints:
1. Budget Constraint:
  (cost_ZTube * x_ZTube) + (cost_Soorchle * x_Soorchle) + (cost_Wassa * x_Wassa)
   ≤ weekly_budget
  => (1000 * x_ZTube) + (200 * x_Soorchle) + (100 * x_Wassa) ≤ 10000

2. Soorchle Advertisement Limit:
  x_Soorchle ≤ max_Soorchle_ads
  => x_Soorchle ≤ 15

3. Wassa Advertisement Fraction Constraint:
  The number of wassa ads must be at most one third of the overall number of ads.
  Expressed as:  x_Wassa ≤ maxFrac_Wassa * (x_ZTube + x_Soorchle + x_Wassa)
  A helpful reformulation (multiplying both sides by 3) is:
   3 * x_Wassa ≤ x_ZTube + x_Soorchle + x_Wassa
  or equivalently:
   2 * x_Wassa ≤ x_ZTube + x_Soorchle

4. ZTube Advertisement Fraction Constraint:
  At least 5% of total ads must be on z-tube.
  Expressed as:  x_ZTube ≥ minFrac_ZTube * (x_ZTube + x_Soorchle + x_Wassa)
  That is:  x_ZTube ≥ 0.05 * (x_ZTube + x_Soorchle + x_Wassa)

--------------------------------------------------
Comments:
• All cost parameters are in USD per advertisement, and the budget is in USD per week.
• The viewer numbers are per individual advertisement.
• The decision variables are defined as nonnegative integers since advertisements must be indivisible.
• The fraction constraints on media balance (for wassa and z-tube) ensure a mix of advertising options.
• The reformulated inequality for the wassa fraction may be easier to implement in some optimization frameworks. 

--------------------------------------------------
This completes the precise and self-contained mathematical model for the problem.'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_version1():
    # Create solver instance using CBC.
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Could not create solver for Version 1.")
        return None

    # Decision Variables: nonnegative integers.
    x_ZTube = solver.IntVar(0, solver.infinity(), 'x_ZTube')
    x_Soorchle = solver.IntVar(0, solver.infinity(), 'x_Soorchle')
    x_Wassa = solver.IntVar(0, solver.infinity(), 'x_Wassa')

    # Parameters
    cost_ZTube = 1000
    cost_Soorchle = 200
    cost_Wassa = 100
    weekly_budget = 10000
    max_Soorchle_ads = 15

    viewers_ZTube = 400000
    viewers_Soorchle = 5000
    viewers_Wassa = 3000

    # Constraint 1: Budget constraint
    solver.Add(cost_ZTube * x_ZTube + cost_Soorchle * x_Soorchle + cost_Wassa * x_Wassa <= weekly_budget)

    # Constraint 2: Soorchle Advertisement Limit
    solver.Add(x_Soorchle <= max_Soorchle_ads)

    # Constraint 3: Wassa Advertisement Fraction Constraint (Version 1 formulation)
    # Original constraint: x_Wassa <= (1/3)*(x_ZTube + x_Soorchle + x_Wassa)
    # Multiply both sides by 3: 3*x_Wassa <= x_ZTube + x_Soorchle + x_Wassa
    solver.Add(3 * x_Wassa <= x_ZTube + x_Soorchle + x_Wassa)

    # Constraint 4: ZTube Advertisement Fraction Constraint
    # x_ZTube >= 0.05*(x_ZTube + x_Soorchle + x_Wassa)
    # Multiply both sides by 20 to remove decimals: 20*x_ZTube >= (x_ZTube + x_Soorchle + x_Wassa)
    # Simplify: 19*x_ZTube >= (x_Soorchle + x_Wassa) or 19*x_ZTube - x_Soorchle - x_Wassa >= 0
    solver.Add(19 * x_ZTube - x_Soorchle - x_Wassa >= 0)

    # Objective: Maximize Total_Viewers
    objective = solver.Objective()
    objective.SetCoefficient(x_ZTube, viewers_ZTube)
    objective.SetCoefficient(x_Soorchle, viewers_Soorchle)
    objective.SetCoefficient(x_Wassa, viewers_Wassa)
    objective.SetMaximization()

    status = solver.Solve()

    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "variables": {
                "NumberAdsZTube": x_ZTube.solution_value(),
                "NumberAdsSoorchle": x_Soorchle.solution_value(),
                "NumberAdsWassa": x_Wassa.solution_value()
            },
            "objective": objective.Value()
        }
    else:
        result = {"message": "No optimal solution found for Version 1."}
    return result

def solve_version2():
    # Create solver instance using CBC.
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Could not create solver for Version 2.")
        return None

    # Decision Variables: nonnegative integers.
    xZ = solver.IntVar(0, solver.infinity(), 'xZ')
    xS = solver.IntVar(0, solver.infinity(), 'xS')
    xW = solver.IntVar(0, solver.infinity(), 'xW')

    # Parameters
    cost_ZTube = 1000
    cost_Soorchle = 200
    cost_Wassa = 100
    weekly_budget = 10000
    max_Soorchle_ads = 15

    viewers_ZTube = 400000
    viewers_Soorchle = 5000
    viewers_Wassa = 3000

    # Constraint 1: Budget constraint
    solver.Add(cost_ZTube * xZ + cost_Soorchle * xS + cost_Wassa * xW <= weekly_budget)

    # Constraint 2: Soorchle Advertisement Limit
    solver.Add(xS <= max_Soorchle_ads)

    # Constraint 3: Wassa Advertisement Fraction Constraint (Version 2 reformulated)
    # Reformulated constraint: 2*xW <= xZ + xS
    solver.Add(2 * xW <= xZ + xS)

    # Constraint 4: ZTube Advertisement Fraction Constraint
    # xZ >= 0.05*(xZ + xS + xW)
    # Multiply both sides by 20: 20*xZ >= (xZ + xS + xW) => 19*xZ >= xS + xW
    solver.Add(19 * xZ - xS - xW >= 0)

    # Objective: Maximize Total_Viewers
    objective = solver.Objective()
    objective.SetCoefficient(xZ, viewers_ZTube)
    objective.SetCoefficient(xS, viewers_Soorchle)
    objective.SetCoefficient(xW, viewers_Wassa)
    objective.SetMaximization()

    status = solver.Solve()

    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "variables": {
                "xZ": xZ.solution_value(),
                "xS": xS.solution_value(),
                "xW": xW.solution_value()
            },
            "objective": objective.Value()
        }
    else:
        result = {"message": "No optimal solution found for Version 2."}
    return result

def main():
    results = {}
    version1_result = solve_version1()
    version2_result = solve_version2()

    results["Version1"] = version1_result
    results["Version2"] = version2_result

    print("Optimization Results:")
    print(results)

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Optimization Results:
{'Version1': {
'variables': {'NumberAdsZTube': 10.0, 'NumberAdsSoorchle': 0.0, 
'NumberAdsWassa': 0.0}, 'objective': 4000000.0}, 

'Version2': 
{'variables': {'xZ': 10.0, 'xS': 0.0, 'xW': 0.0}, 'objective': 4000000.0}}
'''

'''Expected Output:
Expected solution

: {'variables': {
'NumberAdsZTube': -0.0, 
'NumberAdsSoorchle': -0.0,
'NumberAdsWassa': -0.0, 
'xZ': 1e+30, 
'xS': 1e+30, 'xW': 9.999985000007499e+29}, 
'objective': 4.0799999550000226e+35
}'''

