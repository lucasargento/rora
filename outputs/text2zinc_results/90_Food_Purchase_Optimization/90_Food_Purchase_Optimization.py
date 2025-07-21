# Mathematical Formulation:
'''\begin{align*}
\textbf{Parameters:} \quad & K \quad \text{(number of food types)} \\
& M \quad \text{(number of nutrients)} \\
& \text{Price}_k \quad \text{(price per unit of food } k\text{), for } k=1,\ldots,K \\
& \text{Demand}_m \quad \text{(required amount of nutrient } m\text{), for } m=1,\ldots,M \\
& \text{Nutrition}_{km} \quad \text{(amount of nutrient } m \text{ in one unit of food } k\text{), for } k=1,\ldots,K,\; m=1,\ldots,M \\[1ex]
\textbf{Decision Variables:} \quad & x_k \geq 0, \quad k = 1, \ldots, K, \\
& \quad \text{where } x_k \text{ is the quantity of food type } k \text{ to buy.} \\[1ex]
\textbf{Objective Function:} \quad & \min \; Z = \sum_{k=1}^{K} \text{Price}_k \, x_k \\
& \quad \text{(minimize the total cost of purchasing the food).} \\[1ex]
\textbf{Constraints:} \quad & \sum_{k=1}^{K} \text{Nutrition}_{km} \, x_k \geq \text{Demand}_m, \quad \forall \; m \in \{1, \ldots, M\}, \\
& \quad \text{(ensure that the amount of each nutrient } m \text{ meets or exceeds its demand).} \\[1ex]
& \text{Additionally, } x_k \ge 0, \quad \forall \; k \in \{1, \ldots, K\} \\
& \quad \text{(non-negativity constraints, ensuring feasibility and a bounded solution).}
\end{align*}'''

# Generated Code:
from ortools.linear_solver import pywraplp

def main():
    # Problem data
    K = 3  # number of food types
    M = 2  # number of nutrients

    Price = [1, 2, 3]
    Demand = [10, 20]
    # Nutrition matrix: rows correspond to food types, columns to nutrients
    Nutrition = [
        [3, 5],  # Food 1
        [1, 3],  # Food 2
        [4, 4]   # Food 3
    ]

    # Create the linear solver with the GLOP backend.
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Solver not created.")
        return

    # Decision variables: quantity to purchase for each food type (continuous and >= 0)
    x = [solver.NumVar(0, solver.infinity(), f'x[{k}]') for k in range(K)]
    
    # Constraint: For each nutrient, ensure the total nutrition meets the demand.
    for m in range(M):
        constraint_expr = solver.Sum(Nutrition[k][m] * x[k] for k in range(K))
        solver.Add(constraint_expr >= Demand[m])
    
    # Objective: Minimize total cost = sum(Price[k] * x[k])
    objective = solver.Objective()
    for k in range(K):
        objective.SetCoefficient(x[k], Price[k])
    objective.SetMinimization()
    
    # Solve the problem
    status = solver.Solve()
    
    if status == pywraplp.Solver.OPTIMAL:
        print("Optimal solution found:")
        for k in range(K):
            print(f"Food {k+1}: {x[k].solution_value()}")
        print("Total cost =", solver.Objective().Value())
    elif status == pywraplp.Solver.FEASIBLE:
        print("A feasible solution was found, but it may not be optimal")
    else:
        print("The problem does not have an optimal solution.")

if __name__ == '__main__':
    main()