# Mathematical Formulation:
'''\begin{align*}
\textbf{Indices:}\quad & i,j \in \{1,2,\ldots,n\} \\[1mm]
\textbf{Parameters:}\quad & n \text{ is the size of the grid.} \\[1mm]
& \text{For each cell } (i,j),\; c_{ij} \in \{0,1,2,\dots,9\} \cup \{\mathtt{X}\} \text{ is given by the input puzzle.} \\[1mm]
& \text{Here, } c_{ij} = \mathtt{X} \text{ indicates an unknown (i.e., no clue) cell, while if } c_{ij} \text{ is numeric it is a clue.} \\[1mm]
\textbf{Decision Variables:}\quad & x_{ij} \in \{0,1\} \quad \forall i,j = 1,\ldots,n, \\[1mm]
& \quad \text{where } x_{ij} = 1 \text{ if cell } (i,j) \text{ is painted, and } 0 \text{ otherwise.} \\[1mm]
\textbf{Auxiliary Sets:}\quad & \text{For each cell } (i,j), \text{ define the set of adjacent cells that are within the grid} \\
& \quad \mathcal{N}(i,j) = \{ (p,q) \,:\, p \in \{i-1,i,i+1\}, \; q \in \{j-1,j,j+1\}, \; 1\le p \le n,\; 1\le q \le n\}. \\[1mm]
\textbf{Objective Function:}\quad & \text{Since the problem is a feasibility puzzle we choose a dummy objective.} \\
& \text{Minimize } z = 0. \\[1mm]
\textbf{Constraints:} \\[1mm]
& \text{For every cell } (i,j) \text{ such that } c_{ij} \neq \mathtt{X}, \text{ enforce:} \\[1mm]
& \quad \sum_{(p,q) \in \mathcal{N}(i,j)} x_{pq} = c_{ij} \quad \forall\, (i,j) \text{ with } c_{ij} \in \{0,1,2,\dots,9\}. \\[1mm]
& \text{(There are no restrictions on cells with } c_{ij}=\mathtt{X} \text{ apart from } x_{ij} \in \{0,1\}.) 
\end{align*} 

\noindent This model completely represents the Fill-a-Pix puzzle as a feasibility problem where the painted cells (variables $x_{ij}$) must be chosen so that for every cell with a clue the sum of painted cells in its 3$\times$3 neighborhood (including itself) matches exactly the provided clue value. The problem is both feasible (if a solution exists) and bounded, and the dummy objective ensures that a solution satisfying all constraints is found.'''

# Generated Code:
from ortools.sat.python import cp_model

def main():
    # Puzzle parameters
    n = 10
    # Puzzle grid where 'X' represents an unknown cell, and an integer is a clue.
    puzzle = [
        [0, 'X', 'X', 'X', 'X', 'X', 3, 4, 'X', 3],
        ['X', 'X', 'X', 4, 'X', 'X', 'X', 7, 'X', 'X'],
        ['X', 'X', 5, 'X', 2, 2, 'X', 4, 'X', 3],
        [4, 'X', 6, 6, 'X', 2, 'X', 'X', 'X', 'X'],
        ['X', 'X', 'X', 'X', 3, 3, 'X', 'X', 3, 'X'],
        ['X', 'X', 8, 'X', 'X', 4, 'X', 'X', 'X', 'X'],
        ['X', 9, 'X', 7, 'X', 'X', 'X', 'X', 5, 'X'],
        ['X', 'X', 'X', 7, 5, 'X', 'X', 3, 3, 0],
        ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
        [4, 4, 'X', 'X', 2, 3, 3, 4, 3, 'X']
    ]
    
    model = cp_model.CpModel()
    
    # Create decision variables: x[i][j] = 1 if cell (i, j) is painted, 0 otherwise.
    x = {}
    for i in range(n):
        for j in range(n):
            x[(i, j)] = model.NewBoolVar(f'x_{i}_{j}')
    
    # Add constraints for each cell with a clue
    for i in range(n):
        for j in range(n):
            if puzzle[i][j] != 'X':
                clue_value = puzzle[i][j]
                # Compute the neighborhood indices (ensuring they are within grid bounds)
                cells = []
                for di in [-1, 0, 1]:
                    for dj in [-1, 0, 1]:
                        ni = i + di
                        nj = j + dj
                        if 0 <= ni < n and 0 <= nj < n:
                            cells.append(x[(ni, nj)])
                # The sum of painted cells in the neighborhood must equal the clue
                model.Add(sum(cells) == clue_value)
    
    # Dummy objective: minimize 0
    model.Minimize(0)
    
    # Solve the model.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print(f'Objective value: {solver.ObjectiveValue()}')
        print('Grid solution (1 represents painted, 0 not painted):')
        for i in range(n):
            row = []
            for j in range(n):
                row.append(str(solver.Value(x[(i, j)])))
            print(' '.join(row))
    else:
        print('No solution found.')

if __name__ == '__main__':
    main()