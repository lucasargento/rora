# Mathematical Formulation:
'''\begin{align*}
\textbf{Indices:}\quad & i,j \in \{1,2,\ldots,n\}.\\[1mm]
\textbf{Decision Variables:}\quad & x_{ij} \in \{0,1\} \quad \forall\, i,j, \quad\text{where } x_{ij}=1 \text{ if cell } (i,j) \text{ is alive, and } 0 \text{ otherwise}.\\[1mm]
\textbf{Auxiliary Definitions:}\\[1mm]
&\text{For each cell } (i,j), \text{ define its (discrete) neighbourhood}\\[1mm]
&\quad \mathcal{N}(i,j)= \{(k,\ell) \in \{1,\ldots,n\}^2 : \max\{|i-k|,|j-\ell|\}=1 \text{ and } (k,\ell) \neq (i,j)\}.\\[1mm]
&\text{Let } s_{ij} \text{ denote the number of live neighbours of cell } (i,j):\\[1mm]
&\quad s_{ij} = \sum_{(k,\ell)\in \mathcal{N}(i,j)} x_{k\ell}\quad\forall\, i,j.\\[2mm]
\textbf{Objective Function:}\\[1mm]
&\text{Maximize the total number of live cells:}\\[1mm]
&\quad \max \; Z = \sum_{i=1}^{n}\sum_{j=1}^{n} x_{ij}.\\[2mm]
\textbf{Constraints (Still-life conditions):}\\[1mm]
&\text{The configuration must be stable under the Game of Life update rules.}\\[1mm]
&\quad \textbf{(a)}\;\; \text{If a cell has exactly three live neighbours, it must be alive:} \\[1mm]
&\qquad \text{For all } (i,j):\quad s_{ij} = 3 \implies x_{ij}=1.\\[1mm]
&\quad \textbf{(b)}\;\; \text{If a cell has fewer than two or more than three live neighbours, it must be dead:} \\[1mm]
&\qquad \text{For all } (i,j):\quad \big(s_{ij} \le 1 \text{ or } s_{ij} \ge 4\big) \implies x_{ij}=0.\\[1mm]
&\quad \textbf{(c)}\;\; \text{If a cell has exactly two live neighbours, no state‐change is enforced (i.e., its state is free).}\\[2mm]
\textbf{Summary of the Model:}\\[1mm]
& \begin{array}{rcll}
\max & Z = \displaystyle \sum_{i=1}^{n}\sum_{j=1}^{n} x_{ij} & & \\
\text{s.t.} & s_{ij} = \displaystyle \sum_{(k,\ell)\in \mathcal{N}(i,j)} x_{k\ell}, & \forall\, i,j, & \\
& s_{ij} = 3 \implies x_{ij} = 1, & \forall\, i,j, & \text{(Enforce life when exactly three neighbours)}\\[1mm]
& \big(s_{ij} \le 1 \text{ or } s_{ij}\ge 4 \big)\implies x_{ij} = 0,  & \forall\, i,j, & \text{(Enforce death when too few or too many neighbours)}\\[1mm]
& x_{ij} \in \{0,1\}, & \forall\, i,j. & \\
\end{array}
\end{align*}

\vspace{2mm}
\textbf{Notes:}  
\begin{itemize}
    \item The logical implications above may be reformulated using indicator constraints or big-M formulations when implementing in a mixed‐integer programming solver.
    \item Cells outside the $n\times n$ board are assumed dead; hence, in computing $s_{ij}$ for boundary cells, only those neighbours within $\{1,\ldots,n\}^2$ contribute.
    \item The model is non‐trivial since the still-life conditions create intricate combinatorial restrictions and the objective is to maximize the live cell count within the board.
\end{itemize}'''

# Generated Code:
from ortools.sat.python import cp_model


def main():
    # Board size; you can change n to any desired value.
    n = 8

    model = cp_model.CpModel()

    # Create decision variables: x[i][j] = 1 if cell (i,j) is alive
    x = {}
    for i in range(n):
        for j in range(n):
            x[(i, j)] = model.NewBoolVar(f"x_{i}_{j}")

    # Auxiliary variables: s[i,j] = number of live neighbours of cell (i,j)
    s = {}
    # For each cell, create a variable s in [0, num_neighbours]
    for i in range(n):
        for j in range(n):
            # Get valid neighbours (considering boundaries)
            neighbours = []
            for di in [-1, 0, 1]:
                for dj in [-1, 0, 1]:
                    if di == 0 and dj == 0:
                        continue
                    ni, nj = i + di, j + dj
                    if 0 <= ni < n and 0 <= nj < n:
                        neighbours.append((ni, nj))
            num_neigh = len(neighbours)
            s[(i, j)] = model.NewIntVar(0, num_neigh, f"s_{i}_{j}")
            # Sum of the live neighbours
            model.Add(s[(i, j)] == sum(x[(ni, nj)] for (ni, nj) in neighbours))

            # Create boolean indicators for conditions:
            is_three = model.NewBoolVar(f"is_three_{i}_{j}")
            le_one = model.NewBoolVar(f"le_one_{i}_{j}")
            ge_four = model.NewBoolVar(f"ge_four_{i}_{j}")

            # is_three: s == 3
            model.Add(s[(i, j)] == 3).OnlyEnforceIf(is_three)
            model.Add(s[(i, j)] != 3).OnlyEnforceIf(is_three.Not())

            # le_one: s <= 1
            model.Add(s[(i, j)] <= 1).OnlyEnforceIf(le_one)
            model.Add(s[(i, j)] >= 2).OnlyEnforceIf(le_one.Not())

            # ge_four: s >= 4 (note: maximum of s is num_neigh so we use 4 as threshold)
            model.Add(s[(i, j)] >= 4).OnlyEnforceIf(ge_four)
            model.Add(s[(i, j)] <= 3).OnlyEnforceIf(ge_four.Not())

            # Enforce still-life conditions:
            # If a cell has exactly three neighbours then it must be alive.
            model.Add(x[(i, j)] == 1).OnlyEnforceIf(is_three)
            # If a cell has fewer than two neighbours then it must be dead.
            model.Add(x[(i, j)] == 0).OnlyEnforceIf(le_one)
            # If a cell has more than three neighbours then it must be dead.
            model.Add(x[(i, j)] == 0).OnlyEnforceIf(ge_four)
            # No constraint is enforced when s == 2 (free state)

    # Objective: maximize the total number of live cells
    objective = sum(x[(i, j)] for i in range(n) for j in range(n))
    model.Maximize(objective)

    # Solve the model
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print("Optimal solution found:")
        print(f"Objective (number of live cells): {solver.ObjectiveValue()}")
        for i in range(n):
            row = ""
            for j in range(n):
                row += "1 " if solver.Value(x[(i, j)]) == 1 else "0 "
            print(row)
    else:
        print("No solution found.")


if __name__ == '__main__':
    main()