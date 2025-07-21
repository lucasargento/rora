# Problem Description:
'''Problem description: A biotechnology company has 35,000 units of antibiotics available which is important to the process of making a first-dose and second-dose of vaccines. The first-dose vaccine requires 30 units of antibiotics and 20 mg of gelatine whereas the second-dose vaccine requires 65 units of antibiotics and 60 mg of gelatine. Since the first-dose vaccine is required before the second-dose vaccine, there must be more first-dose than second-dose vaccines manufactured. However, at least 40 second-dose vaccines must be made. How many of each vaccine should be made to minimize the amount of gelatine used?

Expected Output Schema:
{
  "variables": {
    "FirstDoseVaccines": "float",
    "SecondDoseVaccines": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- Vaccines = {FirstDose, SecondDose}

Parameters:
- antibiotic_total = 35000 (total available antibiotic units)
- antibiotic_per_first = 30 (antibiotic units required for one first-dose vaccine)
- gelatine_per_first = 20 (gelatine required in mg for one first-dose vaccine)
- antibiotic_per_second = 65 (antibiotic units required for one second-dose vaccine)
- gelatine_per_second = 60 (gelatine required in mg for one second-dose vaccine)
- min_second_dose = 40 (minimum number of second-dose vaccines to manufacture)
  [Note: All units are assumed consistent with the problem description]

Variables:
- FirstDoseVaccines: number of first-dose vaccines to produce (integer, ≥ 0)
- SecondDoseVaccines: number of second-dose vaccines to produce (integer, ≥ 0)

Objective:
- Minimize total gelatine used (in mg) = gelatine_per_first * FirstDoseVaccines + gelatine_per_second * SecondDoseVaccines

Constraints:
1. Antibiotic resource constraint:
   antibiotic_per_first * FirstDoseVaccines + antibiotic_per_second * SecondDoseVaccines ≤ antibiotic_total

2. Vaccine order requirement (more first-dose than second-dose):
   FirstDoseVaccines ≥ SecondDoseVaccines + 1

3. Minimum second-dose production requirement:
   SecondDoseVaccines ≥ min_second_dose

This structured model fully captures the given real-world problem and can be directly mapped into implementations using Python or OR-Tools.'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def run_model():
    # Create the MIP solver with the CBC backend.
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Solver not created.")
        return None

    # Data parameters
    antibiotic_total = 35000
    antibiotic_per_first = 30
    gelatine_per_first = 20
    antibiotic_per_second = 65
    gelatine_per_second = 60
    min_second_dose = 40

    # Decision variables:
    # FirstDoseVaccines and SecondDoseVaccines are integer variables (>=0)
    first_dose = solver.IntVar(0, solver.infinity(), 'FirstDoseVaccines')
    second_dose = solver.IntVar(0, solver.infinity(), 'SecondDoseVaccines')

    # Constraints:
    # 1. Antibiotic resource constraint: 30 * first_dose + 65 * second_dose <= 35000
    solver.Add(antibiotic_per_first * first_dose + antibiotic_per_second * second_dose <= antibiotic_total)

    # 2. Vaccine order requirement: first_dose >= second_dose + 1
    solver.Add(first_dose >= second_dose + 1)

    # 3. Minimum second-dose production requirement: second_dose >= 40
    solver.Add(second_dose >= min_second_dose)

    # Objective: minimize total gelatine used (20 * first_dose + 60 * second_dose)
    objective = solver.Objective()
    objective.SetCoefficient(first_dose, gelatine_per_first)
    objective.SetCoefficient(second_dose, gelatine_per_second)
    objective.SetMinimization()

    # Solve the model
    status = solver.Solve()

    # Prepare results dictionary
    results = {}
    if status == pywraplp.Solver.OPTIMAL:
        results["variables"] = {
            "FirstDoseVaccines": first_dose.solution_value(),
            "SecondDoseVaccines": second_dose.solution_value()
        }
        results["objective"] = objective.Value()
    else:
        results["error"] = "No optimal solution found."

    return results

def main():
    # Since there is a single mathematical formulation provided,
    # we implement one version using ortools.linear_solver.
    model_results = run_model()
    
    print("Results for Model 1:")
    if "error" in model_results:
        print(model_results["error"])
    else:
        print("FirstDoseVaccines =", model_results["variables"]["FirstDoseVaccines"])
        print("SecondDoseVaccines =", model_results["variables"]["SecondDoseVaccines"])
        print("Objective (Total gelatine used in mg) =", model_results["objective"])

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Results for Model 1:
FirstDoseVaccines = 41.0
SecondDoseVaccines = 40.0
Objective (Total gelatine used in mg) = 3220.0
'''

'''Expected Output:
Expected solution

: {'variables': {'FirstDoseVaccines': 40.0, 'SecondDoseVaccines': 40.0}, 'objective': 3200.0}'''

