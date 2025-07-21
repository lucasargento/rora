# Problem Description:
'''Problem description: A lighting company has access to two types of lights to provide their customers, an LED fixture, and a fluorescence lamp. The LED light uses 5 units of electricity per hour and needs to be changed 3 times a decade. Conversely, the fluorescence lamp uses 8 units of electricity per hour and needs to be changed 4 times a decade. Due to previous installations, at least 30% implemented lights must be fluorescence lamps. If the customer requires at least 300 light fixtures and can use at most 2000 units of electricity, how many of each light should be installed to reduce the total number of light changes?

Expected Output Schema:
{
  "variables": {
    "NumFixtures": {
      "0": "float",
      "1": "float"
    },
    "NumFluorescenceFixtures": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Below is one complete formulation of the problem using the five‐element structure. Note that because the description mixes “per hour” electricity data with a total available “units of electricity” budget and “fixture change frequencies per decade,” we assume for this model that the parameters apply over the same planning period (for example, one standardized period of usage where “electricity per hour” is interpreted as electricity consumption per fixture over that period). This assumption should be revisited if a more precise time‐scaling is available.

----------------------------------------------------------------
Sets:
- L: set of light types = {LED, Fluorescence}

----------------------------------------------------------------
Parameters:
- elec_usage[l]: electricity usage per light fixture of type l (in electricity units per period)
    • elec_usage[LED] = 5
    • elec_usage[Fluorescence] = 8
- changes_per_fixture[l]: number of light changes required per fixture in the planning period (e.g., per decade)
    • changes_per_fixture[LED] = 3
    • changes_per_fixture[Fluorescence] = 4
- min_total_fixtures: minimum total number of fixtures required
    • min_total_fixtures = 300
- max_electricity: maximum allowed total electricity usage (electricity units)
    • max_electricity = 2000
- min_fluorescence_ratio: minimum fraction of installed fixtures that must be Fluorescence lamps
    • min_fluorescence_ratio = 0.3

----------------------------------------------------------------
Variables:
- x[l]: number of light fixtures of type l to install (non-negative integer)
  (Specifically, x[LED] and x[Fluorescence] are decision variables.)

----------------------------------------------------------------
Objective:
Minimize total light changes across all fixtures
    Objective = changes_per_fixture[LED] * x[LED] + changes_per_fixture[Fluorescence] * x[Fluorescence]

----------------------------------------------------------------
Constraints:
1. Total Fixtures Constraint:
   x[LED] + x[Fluorescence] >= min_total_fixtures

2. Electricity Usage Constraint:
   elec_usage[LED] * x[LED] + elec_usage[Fluorescence] * x[Fluorescence] <= max_electricity

3. Fluorescence Requirement Constraint:
   x[Fluorescence] >= min_fluorescence_ratio * (x[LED] + x[Fluorescence])

----------------------------------------------------------------
Notes:
- Units: The electricity usage parameter is given in “units per period” and the change frequency is provided per decade. We assume both apply over the same planning horizon.
- Decision variables are assumed integer since one cannot install a fractional fixture.
- If a different time scaling is desired (e.g., converting “per hour” usage to total usage over a fixed number of operating hours), the parameters should be adjusted accordingly.
- The model seeks to minimize the total number of fixture changes under the specified constraints.

----------------------------------------------------------------
Expected Output Schema (example):
{
  "variables": {
    "NumFixtures": {
      "LED": "integer",
      "Fluorescence": "integer"
    }
  },
  "objective": "Total light changes = 3 * x[LED] + 4 * x[Fluorescence]"
}'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp
from ortools.sat.python import cp_model

def solve_with_linear_solver():
    # Create the MIP solver using CBC.
    solver = pywraplp.Solver.CreateSolver('CBC')
    if solver is None:
        print("Linear solver not available.")
        return None

    # Parameters
    min_total_fixtures = 300
    max_electricity = 2000
    # Electricity usage per fixture
    elec_usage_LED = 5
    elec_usage_Fluoro = 8
    # Light change frequencies (objective coefficients)
    changes_LED = 3
    changes_Fluoro = 4

    # Variables: number of LED and Fluorescence fixtures (non-negative integers)
    xLED = solver.IntVar(0, solver.infinity(), 'LED')
    xFluoro = solver.IntVar(0, solver.infinity(), 'Fluorescence')

    # Constraint 1: Total fixtures >= 300
    solver.Add(xLED + xFluoro >= min_total_fixtures)

    # Constraint 2: Electricity usage constraint.
    solver.Add(elec_usage_LED * xLED + elec_usage_Fluoro * xFluoro <= max_electricity)

    # Constraint 3: At least 30% of installed fixtures are Fluorescence.
    # Original constraint: xFluoro >= 0.3 * (xLED + xFluoro)
    # Multiply both sides by 10: 10*xFluoro >= 3*(xLED + xFluoro)  => 10*xFluoro - 3*xLED - 3*xFluoro >= 0
    # Simplify: 7*xFluoro >= 3*xLED.
    solver.Add(7 * xFluoro >= 3 * xLED)

    # Objective: Minimize total number of light changes = 3*xLED + 4*xFluoro.
    objective = solver.Objective()
    objective.SetCoefficient(xLED, changes_LED)
    objective.SetCoefficient(xFluoro, changes_Fluoro)
    objective.SetMinimization()

    status = solver.Solve()

    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result['status'] = 'optimal'
        result['NumFixtures'] = {
            'LED': xLED.solution_value(),
            'Fluorescence': xFluoro.solution_value()
        }
        result['objective'] = objective.Value()
    else:
        result['status'] = 'infeasible'
        result['message'] = 'No optimal solution found with the linear solver.'
    return result

def solve_with_cp_model():
    # Create the CP-SAT model.
    model = cp_model.CpModel()

    # Parameters
    min_total_fixtures = 300
    max_electricity = 2000
    elec_usage_LED = 5
    elec_usage_Fluoro = 8
    changes_LED = 3
    changes_Fluoro = 4

    # Define a safe upper bound for the number of fixtures.
    ub_led = 1000
    ub_fluoro = 1000

    # Decision variables.
    xLED = model.NewIntVar(0, ub_led, 'LED')
    xFluoro = model.NewIntVar(0, ub_fluoro, 'Fluorescence')

    # Constraint 1: Total fixtures >= 300.
    model.Add(xLED + xFluoro >= min_total_fixtures)

    # Constraint 2: Electricity usage constraint.
    model.Add(elec_usage_LED * xLED + elec_usage_Fluoro * xFluoro <= max_electricity)

    # Constraint 3: Fluorescence ratio constraint (30% minimum).
    # As before: xFluoro >= 0.3*(xLED+xFluoro)  --> 7*xFluoro >= 3*xLED.
    model.Add(7 * xFluoro >= 3 * xLED)

    # Objective: Minimize total light changes = 3*xLED + 4*xFluoro.
    model.Minimize(changes_LED * xLED + changes_Fluoro * xFluoro)

    # Solve the model.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    result = {}
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        result['status'] = 'optimal' if status == cp_model.OPTIMAL else 'feasible'
        result['NumFixtures'] = {
            'LED': solver.Value(xLED),
            'Fluorescence': solver.Value(xFluoro)
        }
        result['objective'] = solver.ObjectiveValue()
    else:
        result['status'] = 'infeasible'
        result['message'] = 'No optimal solution found with the CP-SAT solver.'
    return result

def main():
    print("Solving Problem using Linear Solver (CBC):")
    linear_result = solve_with_linear_solver()
    if linear_result['status'] == 'optimal':
        print("Optimal solution found:")
        print("  NumFixtures:")
        print("    LED:          ", linear_result['NumFixtures']['LED'])
        print("    Fluorescence: ", linear_result['NumFixtures']['Fluorescence'])
        print("  Objective (Total light changes):", linear_result['objective'])
    else:
        print("Linear Solver:", linear_result.get('message', 'No solution found.'))

    print("\nSolving Problem using CP-SAT Model:")
    cp_result = solve_with_cp_model()
    if cp_result['status'] in ['optimal', 'feasible']:
        print("Solution found (" + cp_result['status'] + "):")
        print("  NumFixtures:")
        print("    LED:          ", cp_result['NumFixtures']['LED'])
        print("    Fluorescence: ", cp_result['NumFixtures']['Fluorescence'])
        print("  Objective (Total light changes):", cp_result['objective'])
    else:
        print("CP-SAT Model:", cp_result.get('message', 'No solution found.'))

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Solving Problem using Linear Solver (CBC):
Optimal solution found:
  NumFixtures:
    LED:           210.0
    Fluorescence:  90.0
  Objective (Total light changes): 990.0

Solving Problem using CP-SAT Model:
Solution found (optimal):
  NumFixtures:
    LED:           210
    Fluorescence:  90
  Objective (Total light changes): 990.0
'''

'''Expected Output:
Expected solution

: {'variables': {'NumFixtures': {'0': 0.0, '1': 0.0}, 'NumFluorescenceFixtures': 2000000000.0}, 'objective': 0.0}'''

