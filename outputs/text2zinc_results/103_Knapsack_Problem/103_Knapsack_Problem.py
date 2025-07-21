# Mathematical Formulation:
'''\begin{align*}
\textbf{Parameters:} \quad & C \in \mathbb{R}_+,\quad \text{the total capacity of the knapsack (given } C=10\text{)},\\[1mm]
& v_k \in \mathbb{R}_+,\quad \text{the value of item } k,\quad \text{with } v_1=10,\; v_2=20,\\[1mm]
& s_k \in \mathbb{R}_+,\quad \text{the size of item } k,\quad \text{with } s_1=8,\; s_2=6.\\[2mm]
\textbf{Indices:} \quad & k \in \{1,2\}.\\[2mm]
\textbf{Decision Variables:} \quad & x_k \in \{0,1\},\quad \forall\, k \in \{1,2\},\\[1mm]
& \quad \text{where } x_k = \begin{cases} 
1, & \text{if item } k \text{ is selected},\\[1mm]
0, & \text{otherwise}.
\end{cases}\\[2mm]
\textbf{Objective Function:} \quad & \text{maximize } Z = \sum_{k=1}^{2} v_k x_k.\\[2mm]
\textbf{Constraints:} \quad & \sum_{k=1}^{2} s_k x_k \leq C.
\end{align*}'''

# Generated Code:
from ortools.linear_solver import pywraplp

def main():
    # Create the solver using CBC backend.
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Solver not found.")
        return

    # Problem Data
    C = 10
    values = [10, 20]
    sizes = [8, 6]
    n_items = len(values)

    # Decision Variables: x[i] = 1 if item i is selected, 0 otherwise.
    x = [solver.IntVar(0, 1, f'x[{i}]') for i in range(n_items)]

    # Constraint: sum(sizes[i]*x[i]) <= C
    solver.Add(sum(sizes[i] * x[i] for i in range(n_items)) <= C)

    # Objective: maximize sum(values[i]*x[i])
    solver.Maximize(solver.Sum(values[i] * x[i] for i in range(n_items)))

    # Solve the problem.
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print("Optimal solution found:")
        total_value = solver.Objective().Value()
        total_size = sum(sizes[i] * x[i].solution_value() for i in range(n_items))
        for i in range(n_items):
            print(f"Item {i+1}: selected = {int(x[i].solution_value())}")
        print(f"Total value: {total_value}")
        print(f"Total size: {total_size}")
    elif status == pywraplp.Solver.FEASIBLE:
        print("A feasible solution was found, but it might not be optimal.")
    else:
        print("The problem does not have an optimal solution.")

if __name__ == '__main__':
    main()