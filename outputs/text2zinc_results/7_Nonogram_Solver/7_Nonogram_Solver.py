# Mathematical Formulation:
'''\begin{align*}
\textbf{Indices and Parameters:}\\[1mm]
&\text{Let } R,\; C \in \mathbb{Z}_{>0} \text{ be the number of rows and columns respectively,} \\
&\quad K_r \text{ be the (maximum) number of row‐constraints (row\_rule\_len)},\\[1mm]
&\quad K_c \text{ be the (maximum) number of column‐constraints (col\_rule\_len)}.\\[1mm]
&\text{For each row } i=1,\ldots,R \text{ and } k=1,\ldots,K_r,\; r_{i,k} \in \mathbb{Z}_{\ge0} \text{ is the }k\text{th row rule for row }i.\\[1mm]
&\text{For each column } j=1,\ldots,C \text{ and } k=1,\ldots,K_c,\; c_{j,k} \in \mathbb{Z}_{\ge0} \text{ is the }k\text{th column rule for column }j.\\[2mm]
\textbf{Decision Variables:}\\[1mm]
&x_{i,j}\in \{0,1\}\quad\forall\, i=1,\ldots,R,\; j=1,\ldots,C,\\[1mm]
&\text{For each row } i \text{ and for each block } k \text{ with } r_{i,k}>0,\text{ introduce } s_{i,k}\in \mathbb{Z},\\[1mm]
&\quad\text{with } s_{i,k}\in \{1,2,\ldots,\, C - r_{i,k} +1\},\\[1mm]
&\text{For each column } j \text{ and for each block } k \text{ with } c_{j,k}>0,\text{ introduce } t_{j,k}\in \mathbb{Z},\\[1mm]
&\quad\text{with } t_{j,k}\in \{1,2,\ldots,\, R - c_{j,k} +1\}.\\[2mm]
\textbf{Objective Function:}\\[1mm]
&\min\quad 0 \quad \text{(we only require feasibility, so a trivial objective is chosen)}.\\[2mm]
\textbf{Row-Constraints (Nonogram conditions per row):}\\[1mm]
&\text{For every row } i \text{ and for every block index } k \text{ with } r_{i,k}>0:\\[1mm]
&\quad \textbf{(a)}\quad s_{i,k}+r_{i,k}-1 \le C,\\[1mm]
&\quad \textbf{(b)}\quad \text{If } k=1,\text{ no preceding block is required; for } k\ge2 \text{ with } r_{i,k-1}>0 \text{ and } r_{i,k}>0,\\[1mm]
&\qquad s_{i,k} \ge s_{i,k-1} + r_{i,k-1} + 1.\\[2mm]
&\textbf{Linking } x \text{ and the row blocks:}\\[1mm]
&\text{For each row } i \text{ and each column } j=1,\ldots,C, \text{ we require:}\\[1mm]
&\quad x_{i,j}= 1 \quad \Longleftrightarrow \quad \exists\, k\in\{1,\ldots,K_r\}\text{ with } r_{i,k}>0 \text{ such that } s_{i,k} \le j \le s_{i,k}+r_{i,k}-1.\\[2mm]
\textbf{Column-Constraints (Nonogram conditions per column):}\\[1mm]
&\text{For every column } j \text{ and for every block index } k \text{ with } c_{j,k}>0:\\[1mm]
&\quad \textbf{(a)}\quad t_{j,k}+c_{j,k}-1 \le R,\\[1mm]
&\quad \textbf{(b)}\quad \text{If } k=1,\text{ no preceding block is required; for } k\ge2 \text{ with } c_{j,k-1}>0 \text{ and } c_{j,k}>0,\\[1mm]
&\qquad t_{j,k} \ge t_{j,k-1} + c_{j,k-1} + 1.\\[2mm]
&\textbf{Linking } x \text{ and the column blocks:}\\[1mm]
&\text{For each column } j \text{ and each row } i=1,\ldots,R, \text{ we require:}\\[1mm]
&\quad x_{i,j}= 1 \quad \Longleftrightarrow \quad \exists\, k\in\{1,\ldots,K_c\}\text{ with } c_{j,k}>0 \text{ such that } t_{j,k} \le i \le t_{j,k}+c_{j,k}-1.\\[2mm]
\textbf{Consistency of the Two Descriptions:}\\[1mm]
&\text{Since } x_{i,j} \text{ is common to both the row and column descriptions, the following logical equivalence must hold:}\\[1mm]
&\quad \text{For all } i=1,\ldots,R,\; j=1,\ldots,C,\\[1mm]
&\qquad \Biggl[ x_{i,j}=1 \Longleftrightarrow \Bigl( \exists\, k\in\{1,\ldots,K_r\}: s_{i,k}\le j \le s_{i,k}+r_{i,k}-1 \Bigr) \Biggr] \\
&\qquad\qquad \text{and} \quad \Biggl[ x_{i,j}=1 \Longleftrightarrow \Bigl( \exists\, k\in\{1,\ldots,K_c\}: t_{j,k}\le i \le t_{j,k}+c_{j,k}-1 \Bigr) \Biggr].\\[2mm]
\textbf{Notes:}\\[1mm]
&\text{(i) The constraints above enforce that in each row (respectively, column) the }\\[1mm]
&\quad \text{shaded cells appear in exactly the }\\[1mm]
&\quad \text{specified consecutive blocks, in order, with at least one blank cell between successive blocks.}\\[1mm]
&\text{(ii) The “if and only if” conditions linking } x_{i,j} \text{ with the placement variables } s_{i,k} \text{ and } t_{j,k}\\[1mm]
&\quad \text{are to be understood as logical constraints (or can be modeled via}\\[1mm]
&\quad \text{appropriate mixed-integer formulations using indicator constraints).}\\[2mm]
&\text{(iii) The objective is a dummy one (minimize 0) so that the model is feasibility}\\[1mm]
&\quad \text{driven.}\\[2mm]
\textbf{Summary:}\\[1mm]
\text{Find } \{ x_{i,j},\, s_{i,k},\, t_{j,k} \} \text{ satisfying all the above constraints.}
\end{align*}'''

# Generated Code:
from ortools.sat.python import cp_model

def generate_line_patterns(line_length, clues):
    """Generate all binary patterns of given length that satisfy the clues.
       Clues is a list of positive integers indicating the lengths of blocks.
       If clues is empty, then the only valid pattern is all zeros.
    """
    patterns = []
    def rec(prefix, clues_remaining):
        if not clues_remaining:
            # No more blocks, fill the rest with zeros.
            pattern = prefix + [0] * (line_length - len(prefix))
            patterns.append(tuple(pattern))
            return
        # If prefix is not empty then we need at least one 0 as separator.
        min_sep = 1 if prefix else 0
        # Try every possible separation.
        for sep in range(min_sep, line_length - len(prefix) - clues_remaining[0] + 1):
            new_prefix = prefix + [0]*sep + [1]*clues_remaining[0]
            rec(new_prefix, clues_remaining[1:])
    rec([], clues)
    return patterns

def main():
    # Problem Data from Wikipedia (Nonogram, soccer player)
    rows = 20
    row_rule_len = 5
    row_rules_raw = [
         0,0,0,0,3,
         0,0,0,0,5,
         0,0,0,3,1,
         0,0,0,2,1,
         0,0,3,3,4,
         0,0,2,2,7,
         0,0,6,1,1,
         0,0,4,2,2,
         0,0,0,1,1,
         0,0,0,3,1,
         0,0,0,0,6,
         0,0,0,2,7,
         0,0,6,3,1,
         1,2,2,1,1,
         0,4,1,1,3,
         0,0,4,2,2,
         0,0,3,3,1,
         0,0,0,3,3,
         0,0,0,0,3,
         0,0,0,2,1
    ]
    # Convert row_rules_raw into a list of lists for each row.
    row_rules = []
    for i in range(rows):
        start = i * row_rule_len
        end = start + row_rule_len
        # Only consider positive numbers as clues.
        clues = [row_rules_raw[j] for j in range(start, end) if row_rules_raw[j] > 0]
        row_rules.append(clues)

    cols = 20
    col_rule_len = 5
    col_rules_raw = [
         0,0,0,0,2,
         0,0,0,1,2,
         0,0,0,2,3,
         0,0,0,2,3,
         0,0,3,1,1,
         0,0,2,1,1,
         1,1,1,2,2,
         1,1,3,1,3,
         0,0,2,6,4,
         0,3,3,9,1,
         0,0,5,3,2,
         0,3,1,2,2,
         0,0,2,1,7,
         0,0,3,3,2,
         0,0,0,2,4,
         0,0,2,1,2,
         0,0,2,2,1,
         0,0,0,2,2,
         0,0,0,0,1,
         0,0,0,0,1
    ]
    # Convert col_rules_raw into a list of lists for each column.
    col_rules = []
    for j in range(cols):
        start = j * col_rule_len
        end = start + col_rule_len
        clues = [col_rules_raw[k] for k in range(start, end) if col_rules_raw[k] > 0]
        col_rules.append(clues)

    model = cp_model.CpModel()

    # Decision variables: x[i][j] for each cell in grid.
    x = {}
    for i in range(rows):
        for j in range(cols):
            x[i, j] = model.NewIntVar(0, 1, f'x[{i},{j}]')

    # Row constraints: for each row, the sequence must be one of the allowed patterns.
    row_allowed_patterns = []
    for i in range(rows):
        allowed = generate_line_patterns(cols, row_rules[i])
        # Ensure there is at least one allowed pattern.
        if not allowed:
            # if no clues (like an empty list) then only pattern is all 0's.
            allowed = [tuple(0 for _ in range(cols))]
        row_allowed_patterns.append(allowed)
        row_vars = [x[i, j] for j in range(cols)]
        model.AddAllowedAssignments(row_vars, allowed)

    # Column constraints: for each column, the sequence must be one of the allowed patterns.
    col_allowed_patterns = []
    for j in range(cols):
        allowed = generate_line_patterns(rows, col_rules[j])
        if not allowed:
            allowed = [tuple(0 for _ in range(rows))]
        col_allowed_patterns.append(allowed)
        col_vars = [x[i, j] for i in range(rows)]
        model.AddAllowedAssignments(col_vars, allowed)

    # Dummy objective: minimize 0 (we only require feasibility).
    model.Minimize(0)

    # Create the solver and solve.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print("Solution:")
        for i in range(rows):
            line = ""
            for j in range(cols):
                if solver.Value(x[i, j]) == 1:
                    line += "X"
                else:
                    line += "."
            print(line)
        print("\nObjective value:", solver.ObjectiveValue())
    else:
        print("No solution found.")

if __name__ == '__main__':
    main()