# Mathematical Formulation:
'''\begin{align*}
\textbf{Parameters:} \quad &K \in \{1,2,\dots,5\} \quad &&\text{(set of available alloys)}\\[1mm]
&M \in \{1,2\} \quad &&\text{(set of metals)}\\[1mm]
&Q = 1000 \quad &&\text{(total alloy production in lb)}\\[1mm]
&T_m,\; m \in M,\quad &&\text{Target amount of metal } m,\quad T_1 = 300,\; T_2 = 700\\[1mm]
&r_{k,m},\; k\in K,\; m\in M,\quad &&\text{Fraction of metal } m \text{ in alloy } k,\\[1mm]
&&& \begin{array}{lll}
r_{1,1}=0.10, & r_{1,2}=0.90;\\[1mm]
r_{2,1}=0.25, & r_{2,2}=0.75;\\[1mm]
r_{3,1}=0.50, & r_{3,2}=0.50;\\[1mm]
r_{4,1}=0.75, & r_{4,2}=0.25;\\[1mm]
r_{5,1}=0.95, & r_{5,2}=0.05;
\end{array}\\[2mm]
&p_k,\; k\in K,\quad &&\text{Unit price of alloy } k,\quad p_1=5,\; p_2=4,\; p_3=3,\; p_4=2,\; p_5=1.5.
\end{align*}

\bigskip

\noindent
\textbf{Decision Variables:}  
\begin{itemize}
    \item Let $x_k$ denote the quantity in lb of alloy $k$ used in the production, for each $k\in\{1,\ldots,5\}$.
    \item Domain: \quad $x_k \geq 0$, for all $k\in\{1,2,\dots,5\}$.
\end{itemize}

\bigskip

\noindent
\textbf{Objective Function:}  
\[
\text{Minimize} \quad Z = \sum_{k=1}^{5} p_k\, x_k,
\]
i.e., minimize the total production cost.

\bigskip

\noindent
\textbf{Constraints:}
\begin{enumerate}
    \item \emph{Total Alloy Production:}  
    \[
    \sum_{k=1}^{5} x_k = Q.
    \]
    
    \item \emph{Metal Composition Constraints:}  
    For each metal $m \in \{1,2\}$, the sum of the metal contributed by all alloys must equal the target amount:
    \[
    \sum_{k=1}^{5} r_{k,m}\, x_k = T_m,\quad \forall m\in\{1,2\}.
    \]
    
    \item \emph{Non-negativity:}  
    \[
    x_k \ge 0,\quad \forall k\in \{1,2,\dots,5\}.
    \]
    
    \item \emph{Non-trivial Alloy Mix:}  
    To avoid a degenerate production mix where only one alloy is used (unless forced by the targets), we enforce that the quantities of at least two alloys are strictly positive. One way to enforce this is by introducing a sufficiently small positive number $\epsilon>0$ and binary variables $y_k\in\{0,1\}$, for $k\in \{1,\dots,5\}$, and then requiring
    \[
    x_k \ge \epsilon\, y_k,\quad \forall k\in \{1,\dots,5\},
    \]
    and
    \[
    \sum_{k=1}^{5} y_k \ge 2.
    \]
    This set of constraints forces that at least two alloys have a production quantity of at least $\epsilon$. (The choice of $\epsilon$ should be small relative to $Q$ but large enough to be meaningful in context.)
\end{enumerate}

\bigskip

\noindent
\textbf{Complete Mathematical Model:}
\begin{align*}
\text{Minimize} \quad & Z = \sum_{k=1}^{5} p_k\, x_k \\[1mm]
\text{subject to} \quad 
& \sum_{k=1}^{5} x_k = Q, \\[1mm]
& \sum_{k=1}^{5} r_{k,1}\, x_k = T_1, \\[1mm]
& \sum_{k=1}^{5} r_{k,2}\, x_k = T_2, \\[1mm]
& x_k \geq \epsilon\, y_k,\quad \forall k \in \{1,2,\dots,5\}, \\[1mm]
& \sum_{k=1}^{5} y_k \geq 2, \\[1mm]
& x_k \geq 0,\quad y_k \in \{0,1\} \quad \forall k \in \{1,2,\dots,5\}.
\end{align*}

\bigskip

This formulation is self-contained, explicitly defines all decision variables, parameters, objective, and constraints, and avoids trivial solutions by ensuring that the production mix utilizes at least two alloys. The model is both feasible and bounded given the provided data.'''

# Generated Code:
from ortools.linear_solver import pywraplp

def main():
    # Data
    K = 5
    M = 2
    Q = 1000
    T = [300, 700]
    Ratio = [
        [0.1, 0.9],
        [0.25, 0.75],
        [0.5, 0.5],
        [0.75, 0.25],
        [0.95, 0.05]
    ]
    Price = [5, 4, 3, 2, 1.5]
    epsilon = 1  # A small positive number, can be adjusted as needed
    
    # Create the MILP solver with the CBC backend.
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Solver not created.")
        return

    # Decision variables
    x = [solver.NumVar(0.0, solver.infinity(), f'x_{k}') for k in range(K)]
    y = [solver.BoolVar(f'y_{k}') for k in range(K)]

    # Constraint 1: Total Alloy Production
    solver.Add(solver.Sum(x[k] for k in range(K)) == Q)

    # Constraint 2: Metal Composition Constraints for each metal m
    for m in range(M):
        solver.Add(solver.Sum(Ratio[k][m] * x[k] for k in range(K)) == T[m])

    # Constraint 3: Non-trivial Alloy Mix
    for k in range(K):
        solver.Add(x[k] >= epsilon * y[k])
    solver.Add(solver.Sum(y[k] for k in range(K)) >= 2)

    # Objective: Minimize total cost
    objective = solver.Sum(Price[k] * x[k] for k in range(K))
    solver.Minimize(objective)

    # Solve
    status = solver.Solve()

    # Output results
    if status == pywraplp.Solver.OPTIMAL:
        print("Optimal solution found:")
        for k in range(K):
            print(f"x_{k+1} = {x[k].solution_value()}")
        print("Objective value =", solver.Objective().Value())
    elif status == pywraplp.Solver.FEASIBLE:
        print("A feasible solution was found, but it is not proven optimal.")
    else:
        print("The problem does not have an optimal solution.")

if __name__ == '__main__':
    main()