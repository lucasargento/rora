# Mathematical Formulation:
'''\[
\begin{array}{rcll}
\multicolumn{4}{l}{\textbf{Parameters:}}\\[1mm]
r,\,c &:& \text{number of rows and columns, respectively}, \\
N &=& r\cdot c, & \text{the total number of cells (and numbers)};\\[1mm]
a_{ij} &\in& \{0,1,\dots,N\},\quad i=1,\dots,r,\;j=1,\dots,c, & \text{given puzzle grid, with } a_{ij}>0 \text{ fixed.}\\[3mm]
\multicolumn{4}{l}{\textbf{Decision Variables:}}\\[1mm]
x_{ij} &\in& \{1,2,\dots,N\},\quad i=1,\dots,r,\;j=1,\dots,c, & \text{number assigned to cell } (i,j); \\[1mm]
y_{ij,kl} &\in& \{0,1\},\quad \forall (i,j),(k,l) \text{ with } |i-k|\le1,\;|j-l|\le1,\; (i,j)\neq(k,l), 
& \text{linking binary variable indicating whether}\\[1mm]
&&&\quad\text{if cell } (k,l) \text{ receives the consecutive number of cell } (i,j),\\[3mm]
\multicolumn{4}{l}{\textbf{Objective Function:}}\\[1mm]
\min &\;& 0, & \text{(the problem is a feasibility model)}; \\[3mm]
\multicolumn{4}{l}{\textbf{Constraints:}}\\[1mm]
\textbf{(1) Uniqueness (Permutation):}\\[1mm]
\sum_{i=1}^{r}\sum_{j=1}^{c} \mathbb{I}\{x_{ij} = k\} &=& 1, & \forall k=1,\dots, N, \\
&&& \text{where } \mathbb{I}\{\cdot\} \text{ is the indicator function.} \\[2mm]
\textbf{(2) Pre-assignment Fixing:}\\[1mm]
x_{ij} &=& a_{ij}, & \forall i=1,\dots,r,\; j=1,\dots,c \text{ such that } a_{ij} > 0; \\[2mm]
\textbf{(3) Consecutive Adjacency Using Link Variables:}\\[1mm]
\textbf{(a)}\quad \text{For each cell } (i,j) \text{ with } x_{ij} \in \{1,\dots,N-1\}:\\[1mm]
\sum_{(k,l)\in \mathcal{N}(i,j)} y_{ij,kl} &=& 1, & \forall (i,j) \text{ with } x_{ij}<N,\\[1mm]
\textbf{(b)}\quad \text{For each cell } (k,l) \text{ with } x_{kl} \in \{2,\dots,N\}:\\[1mm]
\sum_{(i,j)\,:\,(k,l) \in \mathcal{N}(i,j)} y_{ij,kl} &=& 1, & \forall (k,l) \text{ with } x_{kl}>1,\\[2mm]
\text{where } \mathcal{N}(i,j) &=& \{(k,l):|i-k|\le1,\;|j-l|\le1,\,(k,l)\neq(i,j)\}. &\\[2mm]
\textbf{(4) Linking the } y\text{-variables with the } x\text{-values:}\\[1mm]
\text{For every neighbor pair } (i,j) \text{ and } (k,l):\\[1mm]
x_{kl} &\ge& x_{ij} + 1 - M\,(1 - y_{ij,kl}), & \forall (i,j),(k,l)\text{ with } (k,l)\in\mathcal{N}(i,j),\\[1mm]
x_{kl} &\le& x_{ij} + 1 + M\,(1 - y_{ij,kl}), & \forall (i,j),(k,l)\text{ with } (k,l)\in\mathcal{N}(i,j),\\[1mm]
&&& \text{with } M \text{ a sufficiently large constant (e.g., } M=N\text{)},\\[2mm]
\textbf{(5) Domain:}\\[1mm]
x_{ij} &\in& \{1,2,\dots,N\}, & \forall i=1,\dots,r,\;j=1,\dots,c,\\[1mm]
y_{ij,kl} &\in& \{0,1\}, & \forall (i,j),(k,l) \text{ with } (k,l)\in \mathcal{N}(i,j).
\end{array}
\]

\vspace{2mm}
\textbf{Explanation of the Model:}

1. The variables x₍ᵢ,ⱼ₎ assign a unique integer from 1 to N (with N = r·c) to every cell in the grid so that the whole set {1, 2, …, N} is used exactly once. This enforces that the numbers form a permutation of 1 through N.

2. The pre-assignment constraint fixes the values in cells where the puzzle already provided a number (i.e. when a₍ᵢ,ⱼ₎ > 0).

3. The binary variables y₍ᵢⱼ,ₖₗ₎ are used to “link” a cell with its neighbor that must contain the consecutive number. For example, if y₍ᵢⱼ,ₖₗ₎ = 1 then cell (k,l) must have the value x₍ᵢ,ⱼ₎+1. The constraints (3) ensure that every number (except the last) has exactly one consecutive neighbor and, conversely, every number (except the first) has exactly one preceding neighbor.

4. The linking constraints (4) use a big–M formulation to enforce that y₍ᵢⱼ,ₖₗ₎ = 1 if and only if x₍ₖ,ₗ₎ = x₍ᵢ,ⱼ₎+1. (One may choose M = N since N is an upper bound on the numbers.)

5. The objective is simply to find a feasible assignment satisfying all these constraints – there is no cost to minimize or maximize beyond feasibility.

This complete formulation exactly captures the Hidato puzzle requirements: assigning each cell a unique number while ensuring that consecutive numbers appear in adjacent cells (neighbors can be horizontal, vertical or diagonal), and pre–assigned numbers remain fixed.'''

# Generated Code:
from ortools.sat.python import cp_model

def main():
    # Problem parameters
    r = 12
    c = 12
    N = r * c  # Total number to place
    # Puzzle grid. 0 means empty; a positive number represents a given pre-assignment.
    puzzle = [
        [0,   0,134,  2,  4,  0,  0,  0,  0,  0,  0,  0],
        [136,  0,  0,  1,  0,  5,  6, 10,115,106,  0,  0],
        [139,  0,  0,124,  0,122,117,  0,  0,107,  0,  0],
        [0,  131,126,  0,123,  0,  0, 12,  0,  0,  0,103],
        [0,    0,144,  0,  0,  0,  0,  0, 14,  0, 99,101],
        [0,    0,129,  0, 23, 21,  0, 16, 65, 97, 96,  0],
        [30,  29, 25,  0,  0, 19,  0,  0,  0, 66, 94,  0],
        [32,   0,  0, 27, 57, 59, 60,  0,  0,  0,  0, 92],
        [0,   40, 42,  0, 56, 58,  0,  0, 72,  0,  0,  0],
        [0,   39,  0,  0,  0,  0, 78, 73, 71, 85, 69,  0],
        [35,   0,  0, 46, 53,  0,  0,  0, 80, 84,  0,  0],
        [36,   0, 45,  0,  0, 52, 51,  0,  0,  0,  0, 88],
    ]

    model = cp_model.CpModel()
    
    # Variables: x[i][j] is the number for cell (i,j), domain 1..N.
    x = {}
    for i in range(r):
        for j in range(c):
            # Pre-assigned cells are fixed.
            if puzzle[i][j] > 0:
                x[i, j] = model.NewIntVar(puzzle[i][j], puzzle[i][j], f"x_{i}_{j}")
            else:
                x[i, j] = model.NewIntVar(1, N, f"x_{i}_{j}")
    
    # AllDifferent constraint to enforce unique assignment.
    model.AddAllDifferent([x[i, j] for i in range(r) for j in range(c)])
    
    # Define neighbor function (8-connected grid)
    def neighbors(i, j):
        for di in [-1, 0, 1]:
            for dj in [-1, 0, 1]:
                if di == 0 and dj == 0:
                    continue
                ni, nj = i + di, j + dj
                if 0 <= ni < r and 0 <= nj < c:
                    yield (ni, nj)
    
    # Big M constant
    M = N
    
    # Binary linking variables: y[i,j,k,l] = 1 if cell (k,l) holds x[i,j]+1.
    y = {}
    for i in range(r):
        for j in range(c):
            for (k, l) in neighbors(i, j):
                y[i, j, k, l] = model.NewBoolVar(f"y_{i}_{j}_{k}_{l}")
    
    # For each cell (i,j), add constraint (3a):
    # if x[i,j] < N then exactly one outgoing link must be active,
    # and if x[i,j] == N then no outgoing link.
    for i in range(r):
        for j in range(c):
            # Create a boolean indicating whether x[i,j] is at most N-1.
            is_not_last = model.NewBoolVar(f"is_not_last_{i}_{j}")
            model.Add(x[i, j] <= N - 1).OnlyEnforceIf(is_not_last)
            model.Add(x[i, j] >= N).OnlyEnforceIf(is_not_last.Not())
            # Sum of y's for neighbors.
            outgoing = [y[i, j, k, l] for (k, l) in neighbors(i, j)]
            model.Add(sum(outgoing) == 1).OnlyEnforceIf(is_not_last)
            model.Add(sum(outgoing) == 0).OnlyEnforceIf(is_not_last.Not())
    
    # For each cell (k,l), add constraint (3b):
    # if x[k,l] > 1 then exactly one incoming link must be active,
    # and if x[k,l] == 1 then no incoming link.
    for i in range(r):
        for j in range(c):
            is_not_first = model.NewBoolVar(f"is_not_first_{i}_{j}")
            model.Add(x[i, j] >= 2).OnlyEnforceIf(is_not_first)
            model.Add(x[i, j] <= 1).OnlyEnforceIf(is_not_first.Not())
            # Incoming links: all y from neighbor cells that point to (i,j)
            incoming = []
            for (pi, pj) in neighbors(i, j):
                incoming.append(y[pi, pj, i, j])
            model.Add(sum(incoming) == 1).OnlyEnforceIf(is_not_first)
            model.Add(sum(incoming) == 0).OnlyEnforceIf(is_not_first.Not())
    
    # Linking constraints (4): Enforce that if y[i,j,k,l]==1 then x[k,l] == x[i,j] + 1.
    for i in range(r):
        for j in range(c):
            for (k, l) in neighbors(i, j):
                # Lower bound: x[k,l] >= x[i,j] + 1 - M*(1 - y)
                model.Add(x[k, l] >= x[i, j] + 1 - M * (1 - y[i, j, k, l]))
                # Upper bound: x[k,l] <= x[i,j] + 1 + M*(1 - y)
                model.Add(x[k, l] <= x[i, j] + 1 + M * (1 - y[i, j, k, l]))
    
    # Objective: feasibility problem (minimize 0).
    objective = model.NewIntVar(0, 0, "obj")
    model.Add(objective == 0)
    model.Minimize(objective)
    
    # Solve the model.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print("Solution:")
        for i in range(r):
            row = []
            for j in range(c):
                row.append(solver.Value(x[i, j]))
            print(row)
        print("Objective value:", solver.ObjectiveValue())
    else:
        print("No solution found.")

if __name__ == '__main__':
    main()