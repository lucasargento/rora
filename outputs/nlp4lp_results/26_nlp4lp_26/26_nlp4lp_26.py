# Problem Description:
'''Problem description: An ice cream store makes chocolate and vanilla ice cream by the gallon. In a week, they must make at least 5 gallons of each type but at most 10 gallons of chocolate ice cream and at most 8 gallons of vanilla ice cream. It takes 1 hour to produce a gallon of chocolate ice cream and 2 hours to produce a gallon of vanilla ice cream. In a week, 30 hours are available to make ice cream. In addition at least 6 workers are needed with 1 working on the chocolate ice cream and 2 on the vanilla ice cream at any time. If the profit per gallon of chocolate ice cream is $200 and the profit per gallon of vanilla ice cream is $300, how many gallons of each should be made to maximize profit?

Expected Output Schema:
{
  "variables": {
    "GallonsChocolateProduced": "float",
    "GallonsVanillaProduced": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Below is one complete formulation that faithfully captures the problem using the five‐element format. In this formulation we assume that the 30 available production hours already reflect the combined effect of having 6 workers available throughout the week. (A note on the staffing requirement: the problem states that a minimum of 6 workers are needed with at least 1 working on chocolate and 2 on vanilla at any time. One interpretation is that the available 30 production hours are achieved by those 6 workers – if the reader prefers, an alternative formulation could introduce explicit worker assignment variables. Here we assume that the production-hour limit implicitly enforces the worker capacity.) 

--------------------------------------------------
Sets:
• F: set of ice cream flavors = {Chocolate, Vanilla}

--------------------------------------------------
Parameters:
• minProd[Chocolate] = 5   // minimum gallons of chocolate ice cream (gallons)
• maxProd[Chocolate] = 10  // maximum gallons of chocolate ice cream (gallons)
• minProd[Vanilla] = 5     // minimum gallons of vanilla ice cream (gallons)
• maxProd[Vanilla] = 8     // maximum gallons of vanilla ice cream (gallons)
• prodTime[Chocolate] = 1  // production time needed per gallon of chocolate (hours/gallon)
• prodTime[Vanilla] = 2    // production time needed per gallon of vanilla (hours/gallon)
• availableHours = 30      // total available production hours per week (hours)
• profit[Chocolate] = 200  // profit per gallon of chocolate ice cream (USD/gallon)
• profit[Vanilla] = 300    // profit per gallon of vanilla ice cream (USD/gallon)

// Note on workers: It is given that at least 6 workers are available (with a minimum of 1 on chocolate and 2 on vanilla at any time). 
// In this formulation, we assume that the provided availableHours (30) are the result of the labor available from these workers.

--------------------------------------------------
Variables:
• x[Chocolate] = GallonsChocolateProduced, continuous variable (gallons produced)
• x[Vanilla] = GallonsVanillaProduced, continuous variable (gallons produced)

--------------------------------------------------
Objective:
Maximize total profit = profit[Chocolate]*x[Chocolate] + profit[Vanilla]*x[Vanilla]
// That is, maximize 200*x[Chocolate] + 300*x[Vanilla]

--------------------------------------------------
Constraints:
1. Production quantity bounds for Chocolate:
   - x[Chocolate] >= minProd[Chocolate]   (x[Chocolate] >= 5)
   - x[Chocolate] <= maxProd[Chocolate]   (x[Chocolate] <= 10)

2. Production quantity bounds for Vanilla:
   - x[Vanilla] >= minProd[Vanilla]   (x[Vanilla] >= 5)
   - x[Vanilla] <= maxProd[Vanilla]   (x[Vanilla] <= 8)

3. Total production time available:
   - prodTime[Chocolate]*x[Chocolate] + prodTime[Vanilla]*x[Vanilla] <= availableHours
   - i.e., 1*x[Chocolate] + 2*x[Vanilla] <= 30

// (Optional Additional Worker-Staggered Constraint: Although not needed when assuming availableHours covers worker availability, an alternative formulation might include constraints reflecting that whenever production is operating, at least 1 worker must be dedicated to chocolate and 2 to vanilla. Here, we assume that these staffing requirements are satisfied by the predetermined availableHours.)

--------------------------------------------------

Below is the expected output JSON schema mapping decision variables and the overall objective expression (profit expressed in USD):

{
  "variables": {
    "GallonsChocolateProduced": "float",
    "GallonsVanillaProduced": "float"
  },
  "objective": "float"
}

This complete formulation should be unambiguous and easy to implement in Python or OR-Tools.'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_model1():
    # Model 1: Standard formulation using availableHours to cover worker capacity.
    # Create the solver using GLOP (linear programming solver).
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("GLOP solver unavailable.")
        return None

    # Variables: production quantities for Chocolate and Vanilla.
    x_choco = solver.NumVar(5.0, 10.0, 'GallonsChocolateProduced')
    x_van = solver.NumVar(5.0, 8.0, 'GallonsVanillaProduced')

    # Constraint: Total production time constraint: 1*x_choco + 2*x_van <= 30 hours.
    solver.Add(x_choco + 2 * x_van <= 30)

    # Objective: maximize profit = 200*x_choco + 300*x_van.
    solver.Maximize(200 * x_choco + 300 * x_van)

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "variables": {
                "GallonsChocolateProduced": x_choco.solution_value(),
                "GallonsVanillaProduced": x_van.solution_value()
            },
            "objective": solver.Objective().Value()
        }
    else:
        result = {
            "error": "The problem does not have an optimal solution."
        }
    return result

def solve_model2():
    # Model 2: Alternative formulation with explicit worker assignment variables.
    # We use a Mixed Integer Programming solver.
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("CBC solver unavailable.")
        return None

    # Production variables: production quantities for Chocolate and Vanilla.
    x_choco = solver.NumVar(5.0, 10.0, 'GallonsChocolateProduced')
    x_van = solver.NumVar(5.0, 8.0, 'GallonsVanillaProduced')

    # Worker decision variables (integer):
    # w_choco: number of workers dedicated to chocolate production, at least 1.
    # w_van: number of workers dedicated to vanilla production, at least 2.
    w_choco = solver.IntVar(1, 6, 'WorkersChocolate')
    w_van = solver.IntVar(2, 6, 'WorkersVanilla')

    # Constraint: total available workers is exactly 6.
    solver.Add(w_choco + w_van == 6)

    # Production time constraint remains the same: 1*x_choco + 2*x_van <= 30 hours.
    solver.Add(x_choco + 2 * x_van <= 30)

    # (Optional linkage could be added between production and worker capacity;
    # however, here we assume availableHours already limits production.
    # The worker variables are added to explicitly enforce minimum staffing.)
    
    # Objective: maximize profit = 200*x_choco + 300*x_van.
    solver.Maximize(200 * x_choco + 300 * x_van)

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "variables": {
                "GallonsChocolateProduced": x_choco.solution_value(),
                "GallonsVanillaProduced": x_van.solution_value(),
                "WorkersChocolate": w_choco.solution_value(),
                "WorkersVanilla": w_van.solution_value()
            },
            "objective": solver.Objective().Value()
        }
    else:
        result = {
            "error": "The problem does not have an optimal solution in Model 2."
        }
    return result

def main():
    result_model1 = solve_model1()
    result_model2 = solve_model2()
    
    # Printing the results in a structured way.
    output = {
        "Model1": result_model1,
        "Model2": result_model2
    }
    print(output)

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
{'Model1': {'variables': {'GallonsChocolateProduced': 10.0, 'GallonsVanillaProduced': 8.0}, 'objective': 4400.0}, 'Model2': {'variables': {'GallonsChocolateProduced': 10.0, 'GallonsVanillaProduced': 8.0, 'WorkersChocolate': 4.0, 'WorkersVanilla': 2.0}, 'objective': 4400.0}}
'''

'''Expected Output:
Expected solution

: {'variables': {'GallonsChocolateProduced': 10.0, 'GallonsVanillaProduced': 8.0}, 'objective': 4400.0}'''

