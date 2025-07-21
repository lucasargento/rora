# Mathematical Formulation:
'''\begin{align*}
\textbf{Parameters:}\\[1mm]
& N \quad=\quad \text{Number of translators (here, } N=6\text{)}\\[1mm]
& M \quad=\quad \text{Number of required languages (here, } M=8\text{)}\\[1mm]
& \text{Cost}_i \quad=\quad \text{Cost of translator } i, \quad i=1,\ldots,N\\[1mm]
& a_{ij} \quad=\quad \text{Element of the TranslatorLanguagesMatrix, which is }\\
& \qquad\quad 1 \text{ if translator } i \text{ can translate into required language } j, \quad 0 \text{ otherwise},\\[1mm]
& \text{RequiredLanguages: a list of } M \text{ languages (e.g., }``\text{FR, AR, GE, RU, SP, CH, IT, PO}"\text{)}.\\[2mm]

\textbf{Decision Variables:}\\[1mm]
& x_i \; \in \; \{0, 1\} \quad && \forall i \in \{1,2,\ldots,N\} \\
& && \text{where } x_i = 
\begin{cases}
1, & \text{if translator } i \text{ is selected,} \\
0, & \text{otherwise.}
\end{cases}\\[2mm]

\textbf{Objective Function:}\\[1mm]
& \textbf{minimize} \quad Z \;=\; \sum_{i=1}^{N} \text{Cost}_i\, x_i. \\[2mm]

\textbf{Constraints:}\\[1mm]
& \sum_{i=1}^{N} a_{ij}\, x_i \;\ge\; 1, \quad && \forall j \in \{1,2,\ldots,M\} \\
& && \text{(Ensures that each required language } j \text{ is covered by at least one selected translator.)} \\[2mm]

\textbf{Model Summary:}\\[1mm]
\begin{aligned}
\underset{x}{\text{minimize}} \quad & Z = \sum_{i=1}^{N} \text{Cost}_i\, x_i \\[1mm]
\text{subject to} \quad & \sum_{i=1}^{N} a_{ij}\, x_i \ge 1 \quad \forall j \in \{1,2,\ldots,M\}, \\[1mm]
& x_i \in \{0,1\} \quad \forall i \in \{1,2,\ldots,N\}.
\end{aligned}
\end{align*}'''

# Generated Code:
from ortools.sat.python import cp_model

def main():
    # Data
    N = 6
    M = 8
    Cost = [12000, 16000, 13000, 15000, 9000, 7000]
    TranslatorLanguagesMatrix = [
        [1, 1, 0, 0, 0, 0, 1, 0],  # Translator 1: FR, AR, IT
        [0, 0, 1, 1, 0, 1, 0, 0],  # Translator 2: GE, RU, CH
        [0, 1, 0, 0, 0, 1, 0, 0],  # Translator 3: AR, CH
        [1, 0, 0, 0, 1, 0, 1, 1],  # Translator 4: FR, SP, IT, PO
        [1, 0, 1, 1, 1, 0, 0, 0],  # Translator 5: FR, GE, RU, SP
        [0, 0, 1, 0, 1, 0, 0, 1]   # Translator 6: GE, SP, PO
    ]
    RequiredLanguages = ["FR", "AR", "GE", "RU", "SP", "CH", "IT", "PO"]

    # Create the model
    model = cp_model.CpModel()

    # Variables: x[i] = 1 if translator i is selected, 0 otherwise.
    x = [model.NewBoolVar(f'x{i}') for i in range(N)]

    # Constraints: ensure each required language is covered
    for j in range(M):
        # Sum of translators that cover language j must be >= 1
        model.Add(sum(TranslatorLanguagesMatrix[i][j] * x[i] for i in range(N)) >= 1)

    # Objective: Minimize total cost
    model.Minimize(sum(Cost[i] * x[i] for i in range(N)))

    # Create the solver and solve
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print("Optimal solution found:")
        total_cost = 0
        for i in range(N):
            if solver.Value(x[i]) == 1:
                print(f"Translator {i+1} is selected with cost {Cost[i]}.")
                total_cost += Cost[i]
        print(f"Total cost = {total_cost}")
    else:
        print("No solution found.")

if __name__ == '__main__':
    main()