# Problem Description:
'''Problem description: A printing company sells math workbooks and English workbooks. To meet demand, they must make at least 40 math workbooks and at least 60 English workbooks. However, they can make at most 140 math workbooks and at most 170 English workbooks. The company has a contract with a school to send at least 200 workbooks of either type. If the profit per math workbook is $15 and the profit per English workbook is $17, how many of each should the company make to maximize profit?

Expected Output Schema:
{
  "variables": {
    "QuantityMathWorkbooks": "float",
    "QuantityEnglishWorkbooks": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- Workbooks: {Math, English}

Parameters:
- profit_math: Profit per math workbook (15 USD per unit)
- profit_english: Profit per English workbook (17 USD per unit)
- min_math: Minimum number of math workbooks (40 units)
- max_math: Maximum number of math workbooks (140 units)
- min_english: Minimum number of English workbooks (60 units)
- max_english: Maximum number of English workbooks (170 units)
- school_contract_min: Minimum total workbooks required by the school contract (200 units)
  (All quantity units refer to individual workbooks produced.)

Variables:
- QuantityMathWorkbooks: Number of math workbooks produced [integer ≥ 0]
- QuantityEnglishWorkbooks: Number of English workbooks produced [integer ≥ 0]

Objective:
- Maximize total profit = (profit_math * QuantityMathWorkbooks) + (profit_english * QuantityEnglishWorkbooks)

Constraints:
1. Math production lower bound: QuantityMathWorkbooks ≥ min_math
2. Math production upper bound: QuantityMathWorkbooks ≤ max_math
3. English production lower bound: QuantityEnglishWorkbooks ≥ min_english
4. English production upper bound: QuantityEnglishWorkbooks ≤ max_english
5. School contract requirement: QuantityMathWorkbooks + QuantityEnglishWorkbooks ≥ school_contract_min

Expected Output Schema:
{
  "variables": {
    "QuantityMathWorkbooks": "float",
    "QuantityEnglishWorkbooks": "float"
  },
  "objective": "float"
}'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp
from ortools.sat.python import cp_model

def solve_with_linear_solver():
    # Create the solver using CBC for mixed integer programming.
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        return {"error": "Linear solver not available."}
    
    # Parameters
    profit_math = 15
    profit_english = 17
    min_math = 40
    max_math = 140
    min_english = 60
    max_english = 170
    school_contract_min = 200

    # Variables: integer variables with given lower and upper bounds.
    math_workbooks = solver.IntVar(min_math, max_math, 'QuantityMathWorkbooks')
    english_workbooks = solver.IntVar(min_english, max_english, 'QuantityEnglishWorkbooks')

    # Constraint: School contract requirement.
    solver.Add(math_workbooks + english_workbooks >= school_contract_min)
    
    # Objective: Maximize profit = 15 * math_workbooks + 17 * english_workbooks.
    solver.Maximize(profit_math * math_workbooks + profit_english * english_workbooks)
    
    status = solver.Solve()

    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "variables": {
                "QuantityMathWorkbooks": math_workbooks.solution_value(),
                "QuantityEnglishWorkbooks": english_workbooks.solution_value()
            },
            "objective": solver.Objective().Value()
        }
    else:
        result = {"error": "No optimal solution found for the linear model."}
    return result

def solve_with_cp_model():
    # Create a CP-SAT model.
    model = cp_model.CpModel()

    # Parameters
    profit_math = 15
    profit_english = 17
    min_math = 40
    max_math = 140
    min_english = 60
    max_english = 170
    school_contract_min = 200

    # Variables: integer variables.
    math_workbooks = model.NewIntVar(min_math, max_math, 'QuantityMathWorkbooks')
    english_workbooks = model.NewIntVar(min_english, max_english, 'QuantityEnglishWorkbooks')

    # Constraint: School contract requirement.
    model.Add(math_workbooks + english_workbooks >= school_contract_min)

    # Objective: Maximize profit = 15 * math_workbooks + 17 * english_workbooks.
    model.Maximize(profit_math * math_workbooks + profit_english * english_workbooks)

    # Solve the model.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    result = {}
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        result = {
            "variables": {
                "QuantityMathWorkbooks": solver.Value(math_workbooks),
                "QuantityEnglishWorkbooks": solver.Value(english_workbooks)
            },
            "objective": solver.ObjectiveValue()
        }
    else:
        result = {"error": "No optimal solution found for the CP-SAT model."}
    return result

def main():
    print("Solving using Linear Solver (ortools.linear_solver):")
    linear_result = solve_with_linear_solver()
    print(linear_result)
    
    print("\nSolving using CP-SAT Solver (ortools.sat.python.cp_model):")
    cp_result = solve_with_cp_model()
    print(cp_result)

if __name__ == "__main__":
    main()

'''Execution Results:
SUCCESS:
Solving using Linear Solver (ortools.linear_solver):
{'variables': {'QuantityMathWorkbooks': 140.0, 'QuantityEnglishWorkbooks': 170.0}, 'objective': 4990.0}

Solving using CP-SAT Solver (ortools.sat.python.cp_model):
{'variables': {'QuantityMathWorkbooks': 140, 'QuantityEnglishWorkbooks': 170}, 'objective': 4990.0}
'''

'''Expected Output:
Expected solution

: {'variables': {'QuantityMathWorkbooks': 140.0, 'QuantityEnglishWorkbooks': 170.0}, 'objective': 4990.0}'''

