# Mathematical Formulation:
'''\begin{align*}
\textbf{Indices and Parameters:} \quad &\text{Let } j = 1,\ldots, M \text{ denote the goods (with } M=4\text{)},\\[1mm]
&\text{and } i = 1,\ldots, N \text{ denote the raw materials (with } N=5\text{)}.\\[1mm]
&\textbf{Available: } b_i,\; i=1,\ldots,5,\quad \text{with } b_1=10,\; b_2=20,\; b_3=15,\; b_4=35,\; b_5=25.\\[1mm]
&\textbf{Prices: } p_j,\; j=1,\ldots,4,\quad \text{with } p_1=7,\; p_2=10,\; p_3=5,\; p_4=9.\\[1mm]
&\textbf{Raw Material Requirements:} \quad a_{ij} \text{ is the amount of raw material } i \text{ required to produce one unit of good } j.\\[1mm]
&\text{Since the provided data is}\\[0.5mm]
&\quad \texttt{Requirements = array2d(1..4,1..5, [3,2,0,0,0,\; 0,5,2,1,0,\; 1,0,0,5,3,\; 0,3,1,1,5])},\\[0.5mm]
&\text{we interpret the rows (indexed by } j=1,\ldots,4\text{) as the goods and the columns (indexed by } i=1,\ldots,5\text{) as the raw materials.}\\[0.5mm]
&\text{Thus, to align with our notation } a_{ij} \text{ for } i=1,\ldots,5,\; j=1,\ldots,4, \text{ we define:}\\[0.5mm]
&\quad a_{1,1}=3,\quad a_{1,2}=0,\quad a_{1,3}=1,\quad a_{1,4}=0,\\[0.5mm]
&\quad a_{2,1}=2,\quad a_{2,2}=5,\quad a_{2,3}=0,\quad a_{2,4}=3,\\[0.5mm]
&\quad a_{3,1}=0,\quad a_{3,2}=2,\quad a_{3,3}=0,\quad a_{3,4}=1,\\[0.5mm]
&\quad a_{4,1}=0,\quad a_{4,2}=1,\quad a_{4,3}=5,\quad a_{4,4}=1,\\[0.5mm]
&\quad a_{5,1}=0,\quad a_{5,2}=0,\quad a_{5,3}=3,\quad a_{5,4}=5.
\end{align*}

\begin{align*}
\textbf{Decision Variables:} \quad & x_j \ge 0,\quad j=1,\ldots,4, \quad \text{representing the production quantity of good } j.\\[1mm]
\text{(Optionally, if production must be integer, we define } & x_j \in \mathbb{Z}_+.)\\[2mm]
\textbf{Objective Function (Maximization):}\\[0.5mm]
& \max_{x_1,x_2,x_3,x_4} \quad Z = \sum_{j=1}^{4} p_j\, x_j = 7\,x_1 + 10\,x_2 + 5\,x_3 + 9\,x_4.\\[2mm]
\textbf{Constraints:} \quad & \text{For each raw material } i=1,\ldots,5, \text{ the total consumption cannot exceed its available quantity:}\\[0.5mm]
& \text{For } i=1: \quad a_{1,1}\, x_1 + a_{1,2}\, x_2 + a_{1,3}\, x_3 + a_{1,4}\, x_4 \leq b_1,\\[0.5mm]
& \quad \quad \quad \; 3\,x_1 + 0\,x_2 + 1\,x_3 + 0\,x_4 \leq 10,\\[0.5mm]
& \text{For } i=2: \quad a_{2,1}\, x_1 + a_{2,2}\, x_2 + a_{2,3}\, x_3 + a_{2,4}\, x_4 \leq b_2,\\[0.5mm]
& \quad \quad \quad \; 2\,x_1 + 5\,x_2 + 0\,x_3 + 3\,x_4 \leq 20,\\[0.5mm]
& \text{For } i=3: \quad a_{3,1}\, x_1 + a_{3,2}\, x_2 + a_{3,3}\, x_3 + a_{3,4}\, x_4 \leq b_3,\\[0.5mm]
& \quad \quad \quad \; 0\,x_1 + 2\,x_2 + 0\,x_3 + 1\,x_4 \leq 15,\\[0.5mm]
& \text{For } i=4: \quad a_{4,1}\, x_1 + a_{4,2}\, x_2 + a_{4,3}\, x_3 + a_{4,4}\, x_4 \leq b_4,\\[0.5mm]
& \quad \quad \quad \; 0\,x_1 + 1\,x_2 + 5\,x_3 + 1\,x_4 \leq 35,\\[0.5mm]
& \text{For } i=5: \quad a_{5,1}\, x_1 + a_{5,2}\, x_2 + a_{5,3}\, x_3 + a_{5,4}\, x_4 \leq b_5,\\[0.5mm]
& \quad \quad \quad \; 0\,x_1 + 0\,x_2 + 3\,x_3 + 5\,x_4 \leq 25.\\[2mm]
\textbf{Non-triviality and Feasibility:} \quad & \text{The model is constructed such that an optimal solution will typically involve producing}\\[0.5mm]
& \text{a mix of goods (i.e. not just one product) to maximize revenue, while the constraints guarantee that}\\[0.5mm]
& \text{the production plan is both feasible and bounded.}
\end{align*}'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def main():
    # Create the solver with CBC backend for Mixed Integer Programming.
    solver = pywraplp.Solver.CreateSolver('CBC_MIXED_INTEGER_PROGRAMMING')
    if not solver:
        print("Solver not found.")
        return

    # Data
    M = 4  # number of goods
    N = 5  # number of raw materials

    # Available raw material amounts for each i (i=0,...,4)
    available = [10, 20, 15, 35, 25]

    # Requirements matrix a[i][j] where i indexes raw materials and j indexes goods.
    # a[i][j] = amount of raw material i required to produce one unit of good j.
    # Based on the given interpretation:
    # a_{1,1}=3, a_{1,2}=0, a_{1,3}=1, a_{1,4}=0,
    # a_{2,1}=2, a_{2,2}=5, a_{2,3}=0, a_{2,4}=3,
    # a_{3,1}=0, a_{3,2}=2, a_{3,3}=0, a_{3,4}=1,
    # a_{4,1}=0, a_{4,2}=1, a_{4,3}=5, a_{4,4}=1,
    # a_{5,1}=0, a_{5,2}=0, a_{5,3}=3, a_{5,4}=5.
    requirements = [
        [3, 0, 1, 0],  # raw material 1
        [2, 5, 0, 3],  # raw material 2
        [0, 2, 0, 1],  # raw material 3
        [0, 1, 5, 1],  # raw material 4
        [0, 0, 3, 5]   # raw material 5
    ]

    # Prices for each good j (j=0,...,3)
    prices = [7, 10, 5, 9]

    # Decision variables: production quantity for each good.
    # Assuming integer production amounts.
    x = [solver.IntVar(0, solver.infinity(), f'x_{j}') for j in range(M)]

    # Constraints for each raw material (i from 0 to 4)
    for i in range(N):
        constraint_expr = solver.Sum(requirements[i][j] * x[j] for j in range(M))
        solver.Add(constraint_expr <= available[i])

    # Objective: maximize total revenue = sum(prices[j] * x[j])
    objective = solver.Objective()
    for j in range(M):
        objective.SetCoefficient(x[j], prices[j])
    objective.SetMaximization()

    # Solve the model.
    status = solver.Solve()

    # Check the result status.
    if status == pywraplp.Solver.OPTIMAL:
        print('Optimal objective value =', objective.Value())
        for j in range(M):
            print(f'Production of good {j+1}:', x[j].solution_value())
    elif status == pywraplp.Solver.FEASIBLE:
        print('A feasible solution was found, but it may not be optimal.')
        print('Objective value =', objective.Value())
        for j in range(M):
            print(f'Production of good {j+1}:', x[j].solution_value())
    else:
        print('The problem does not have an optimal solution.')

if __name__ == '__main__':
    main()