# Problem Description:
'''Problem description: A pharmacy has two factories, factory 1 and factory 2, where they make acne cream and anti-bacterial cream. Factory 1 produces 12 units of acne cream and 15 units of anti-bacterial cream per hour. Factory 2 produces 20 units of acne cream and 10 units of anti-bacterial cream per hour. Factory 1 requires 30 units of base gel per hour while factory 2 requires 45 units of base gel per hour. The pharmacy has available 5000 units of base gel. Further, they must make at least 800 units of acne cream and 1000 units of anti-bacterial cream. How many hours should each factory be run to minimize the total time needed?

Expected Output Schema:
{
  "variables": {
    "ProductionMatrix": {
      "(0, 0)": "float",
      "(0, 1)": "float",
      "(1, 0)": "float",
      "(1, 1)": "float"
    },
    "MaxOperatingHours": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Below is one complete formulation using the five‐element framework. In this version we assume that the two factories are operated sequentially so that the total time is simply the sum of operating hours (t0 for factory 1 and t1 for factory 2). (An alternative formulation could interpret “total time” as the makespan if the factories run in parallel; in that case you would introduce a variable for the maximum of t0 and t1. Here, following the expected output schema, we minimize t0 + t1.)

----------------------------------------------------------------------------------------------------
Sets:
• F = {0, 1} – the index set for factories (0 represents factory 1 and 1 represents factory 2)
• P = {0, 1} – the index set for cream types, where 0 is acne cream and 1 is anti-bacterial cream

Parameters:
• prod_rate[i,j] – production rate for factory i and product j in units per hour
  • prod_rate[0,0] = 12 (factory 1 produces 12 units of acne cream per hour)
  • prod_rate[0,1] = 15 (factory 1 produces 15 units of anti-bacterial cream per hour)
  • prod_rate[1,0] = 20 (factory 2 produces 20 units of acne cream per hour)
  • prod_rate[1,1] = 10 (factory 2 produces 10 units of anti-bacterial cream per hour)
• gel_usage[i] – base gel consumed per hour by factory i (units per hour)
  • gel_usage[0] = 30 (factory 1 uses 30 units of base gel per hour)
  • gel_usage[1] = 45 (factory 2 uses 45 units of base gel per hour)
• available_gel = 5000 – total base gel available (units)
• min_production[0] = 800 – minimum required production of acne cream (units)
• min_production[1] = 1000 – minimum required production of anti-bacterial cream (units)

Variables:
• t[i] – operating hours for factory i where t[0] and t[1] are nonnegative real numbers (t[i] ≥ 0, hours)
• ProductionMatrix[i,j] – amount produced of product j from factory i (units); defined by the relation:
  ProductionMatrix[i,j] = prod_rate[i,j] * t[i]
• MaxOperatingHours – total operating hours, defined as t[0] + t[1] (hours)

Objective:
Minimize total operating time:
  Minimize MaxOperatingHours = t[0] + t[1]

Constraints:
1. Base Gel Constraint (total gel consumption does not exceed available gel):
  gel_usage[0]*t[0] + gel_usage[1]*t[1] ≤ available_gel
  i.e., 30*t[0] + 45*t[1] ≤ 5000
2. Acne Cream Production (minimum production requirement):
  Production of acne cream: prod_rate[0,0]*t[0] + prod_rate[1,0]*t[1] ≥ min_production[0]
  i.e., 12*t[0] + 20*t[1] ≥ 800
3. Anti-bacterial Cream Production (minimum production requirement):
  Production of anti-bacterial cream: prod_rate[0,1]*t[0] + prod_rate[1,1]*t[1] ≥ min_production[1]
  i.e., 15*t[0] + 10*t[1] ≥ 1000
4. Nonnegativity:
  t[0] ≥ 0, t[1] ≥ 0

----------------------------------------------------------------------------------------------------
Below is a sample JSON-like output (following the Expected Output Schema) that summarizes the decision variables and the objective result structure. (Note: The JSON below does not include the full sets, parameters, and constraints but shows the computed variables in an implementation.)

{
  "variables": {
    "ProductionMatrix": {
      "(0, 0)": "prod_rate[0,0] * t[0]",
      "(0, 1)": "prod_rate[0,1] * t[0]",
      "(1, 0)": "prod_rate[1,0] * t[1]",
      "(1, 1)": "prod_rate[1,1] * t[1]"
    },
    "MaxOperatingHours": "t[0] + t[1]"
  },
  "objective": "Minimize t[0] + t[1]"
}

This formulation is self-contained and directly maps to Python or OR-Tools code. It clearly links the production output to the operator hours through the ProductionMatrix while enforcing the resource (base gel) and minimum production requirements.'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_sequential_model():
    # Create the linear solver with the SCIP backend.
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        print("Solver not created.")
        return None

    # Variables: t0 and t1 represent operating hours for factory 1 and factory 2.
    t0 = solver.NumVar(0.0, solver.infinity(), 't0')
    t1 = solver.NumVar(0.0, solver.infinity(), 't1')

    # Parameters
    # Production rates:
    # Factory 1: acne cream: 12 units/hour, antibacterial: 15 units/hour
    # Factory 2: acne cream: 20 units/hour, antibacterial: 10 units/hour
    prod_rate = {
        (0, 0): 12,  # factory 1, acne
        (0, 1): 15,  # factory 1, antibacterial
        (1, 0): 20,  # factory 2, acne
        (1, 1): 10   # factory 2, antibacterial
    }
    # Base gel usage per hour:
    gel_usage = {0: 30, 1: 45}
    available_gel = 5000
    # Minimum production requirements:
    min_production = {0: 800, 1: 1000}  # 0: acne, 1: antibacterial

    # Constraints:
    # 1. Base gel constraint: 30*t0 + 45*t1 <= 5000
    solver.Add(gel_usage[0] * t0 + gel_usage[1] * t1 <= available_gel)

    # 2. Acne cream production constraint: 12*t0 + 20*t1 >= 800
    solver.Add(prod_rate[(0, 0)] * t0 + prod_rate[(1, 0)] * t1 >= min_production[0])

    # 3. Anti-bacterial cream production constraint: 15*t0 + 10*t1 >= 1000
    solver.Add(prod_rate[(0, 1)] * t0 + prod_rate[(1, 1)] * t1 >= min_production[1])

    # Objective: Minimize total operating time: t0 + t1
    solver.Minimize(t0 + t1)

    status = solver.Solve()
    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        # Build ProductionMatrix dictionary
        production_matrix = {
            "(0, 0)": prod_rate[(0, 0)] * t0.solution_value(),
            "(0, 1)": prod_rate[(0, 1)] * t0.solution_value(),
            "(1, 0)": prod_rate[(1, 0)] * t1.solution_value(),
            "(1, 1)": prod_rate[(1, 1)] * t1.solution_value(),
        }
        result["variables"] = {
            "ProductionMatrix": production_matrix,
            "MaxOperatingHours": t0.solution_value() + t1.solution_value()
        }
        result["objective"] = t0.solution_value() + t1.solution_value()
        result["model"] = "Sequential Model (Total Time = t0 + t1)"
    else:
        result["error"] = "No optimal solution found for the sequential model."

    return result

def solve_parallel_model():
    # In the parallel model, we assume the two factories can operate concurrently.
    # We then define T >= t0 and T >= t1, and minimize T (i.e., the makespan).
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        print("Solver not created.")
        return None

    # Variables: t0 and t1 represent operating hours, T represents the makespan.
    t0 = solver.NumVar(0.0, solver.infinity(), 't0')
    t1 = solver.NumVar(0.0, solver.infinity(), 't1')
    T = solver.NumVar(0.0, solver.infinity(), 'T')  # Makespan variable

    # Parameters
    prod_rate = {
        (0, 0): 12,  # factory 1, acne
        (0, 1): 15,  # factory 1, antibacterial
        (1, 0): 20,  # factory 2, acne
        (1, 1): 10   # factory 2, antibacterial
    }
    gel_usage = {0: 30, 1: 45}
    available_gel = 5000
    min_production = {0: 800, 1: 1000}

    # Constraints:
    # 1. Base gel constraint.
    solver.Add(gel_usage[0] * t0 + gel_usage[1] * t1 <= available_gel)
    # 2. Acne cream production.
    solver.Add(prod_rate[(0, 0)] * t0 + prod_rate[(1, 0)] * t1 >= min_production[0])
    # 3. Anti-bacterial cream production.
    solver.Add(prod_rate[(0, 1)] * t0 + prod_rate[(1, 1)] * t1 >= min_production[1])
    # 4. Makespan constraints: T >= t0 and T >= t1.
    solver.Add(T >= t0)
    solver.Add(T >= t1)

    # Objective: Minimize makespan T.
    solver.Minimize(T)

    status = solver.Solve()
    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        production_matrix = {
            "(0, 0)": prod_rate[(0, 0)] * t0.solution_value(),
            "(0, 1)": prod_rate[(0, 1)] * t0.solution_value(),
            "(1, 0)": prod_rate[(1, 0)] * t1.solution_value(),
            "(1, 1)": prod_rate[(1, 1)] * t1.solution_value(),
        }
        # Here, MaxOperatingHours is interpreted as the makespan.
        result["variables"] = {
            "ProductionMatrix": production_matrix,
            "MaxOperatingHours": T.solution_value()
        }
        result["objective"] = T.solution_value()
        result["model"] = "Parallel Model (Makespan: max(t0, t1))"
    else:
        result["error"] = "No optimal solution found for the parallel model."

    return result

def main():
    sequential_result = solve_sequential_model()
    parallel_result = solve_parallel_model()
    
    # Combine results in a structured output
    full_output = {
        "SequentialModel": sequential_result,
        "ParallelModel": parallel_result
    }
    print(full_output)

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
{'SequentialModel': {'variables': {'ProductionMatrix': {'(0, 0)': 800.0, '(0, 1)': 1000.0000000000001, '(1, 0)': 0.0, '(1, 1)': 0.0}, 'MaxOperatingHours': 66.66666666666667}, 'objective': 66.66666666666667, 'model': 'Sequential Model (Total Time = t0 + t1)'}, 'ParallelModel': {'variables': {'ProductionMatrix': {'(0, 0)': 480.0, '(0, 1)': 600.0, '(1, 0)': 800.0, '(1, 1)': 400.0}, 'MaxOperatingHours': 40.0}, 'objective': 40.0, 'model': 'Parallel Model (Makespan: max(t0, t1))'}}
'''

'''Expected Output:
Expected solution

: {'variables': {'ProductionMatrix': {'(0, 0)': 1200.0, '(0, 1)': 1000.0, '(1, 0)': 0.0, '(1, 1)': 0.0}, 'MaxOperatingHours': 0.0}, 'objective': 0.0}'''

