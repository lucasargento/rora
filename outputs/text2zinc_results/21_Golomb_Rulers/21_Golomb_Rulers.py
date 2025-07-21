# Mathematical Formulation:
'''\begin{align*}
\textbf{Indices:} \quad & i,j,k,l \in \{1,2,\dots,m\}, \text{ with } 1 \le i < j \le m \text{ and } 1 \le k < l \le m.\\[1ex]
\textbf{Decision Variables:} \quad & a_i \in \mathbb{Z}_{\ge 0}, \quad i=1,\dots,m, \quad \text{with } a_1 = 0,\\[1ex]
& \text{and define } d_{ij} = a_j - a_i, \quad \forall\, 1 \le i < j \le m.\\[1ex]
\textbf{Objective Function:} \quad & \min \quad L, \quad \text{where } L = a_m.\\[1ex]
\textbf{Constraints:}\\[0.5ex]
\text{(1) Order of marks:} \quad & a_1 = 0,\quad a_1 < a_2 < a_3 < \cdots < a_m.\\[1ex]
\text{(2) Distinct differences:} \quad & \text{For all } (i,j) \neq (k,l) \text{ with } 1\le i<j\le m \text{ and } 1\le k<l\le m,\\[0.5ex]
& \quad d_{ij} \neq d_{kl}, \quad \text{that is,} \quad a_j - a_i \neq a_l - a_k.\\[1ex]
\text{(3) Symmetry removal:} \quad & a_2 - a_1 < a_m - a_{m-1}.\\[1ex]
\textbf{Parameter:} \quad & m = 10.
\end{align*} 

\noindent This model precisely encapsulates the problem of finding the Golomb ruler with 10 marks of minimum length, ensuring that every difference between two marks is unique and the symmetry is removed by enforcing the condition on the first and last differences.'''

# Generated Code:
from ortools.sat.python import cp_model

def main():
    m = 10
    # Create the model.
    model = cp_model.CpModel()

    # Upper bound based on known optimal Golomb ruler lengths.
    max_length = 100

    # Decision variables: positions of marks.
    a = [model.NewIntVar(0, max_length, f'a[{i}]') for i in range(m)]
    
    # First mark is 0.
    model.Add(a[0] == 0)
    
    # Order constraints: a[i] < a[i+1].
    for i in range(m - 1):
        model.Add(a[i] < a[i+1])
    
    # Compute all differences: d[i][j] = a[j] - a[i] for i < j.
    differences = []
    diff_vars = {}
    for i in range(m - 1):
        for j in range(i + 1, m):
            d = model.NewIntVar(1, max_length, f'diff_{i}_{j}')
            model.Add(d == a[j] - a[i])
            differences.append(d)
            diff_vars[(i,j)] = d

    # Add all-different constraints for differences.
    model.AddAllDifferent(differences)

    # Symmetry breaking: first difference < last difference.
    model.Add(diff_vars[(0, 1)] < diff_vars[(m - 2, m - 1)])

    # Objective: minimize the last mark a[m-1].
    model.Minimize(a[m - 1])

    # Create solver and solve.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        print("Optimal Golomb ruler with {} marks:".format(m))
        marks = [solver.Value(a[i]) for i in range(m)]
        print("Marks:", marks)
        print("Length (a[m]):", solver.Value(a[m-1]))
    else:
        print("No solution found.")
    
if __name__ == "__main__":
    main()