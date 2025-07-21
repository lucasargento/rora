# Mathematical Formulation:
'''\[
\begin{array}{rcl}
\textbf{Indices:} & & k \in \mathcal{K} = \{1,\ldots,K\}, \quad t \in \mathcal{T} = \{1,\ldots,T\}, \\
\\
\textbf{Parameters:} & & \\
&& K \quad \text{(number of mines)}, \\
&& T \quad \text{(number of years; note: } T \text{ is taken as the length of the RequiredQuality vector)},\\[1mm]
&& \text{MaxWork} \quad \text{(maximum number of mines that can operate in any year)}, \\
&& \text{Royalty}_k \quad \text{(yearly royalty cost for mine } k\text{)},\\
&& \text{Limit}_k \quad \text{(production limit [ton] for mine } k\text{ in any year)},\\
&& \text{Quality}_k \quad \text{(ore quality from mine } k\text{)},\\
&& \text{RequiredQuality}_t \quad \text{(required blended ore quality in year } t\text{)},\\
&& \text{Price} \quad \text{(selling price per ton of blended ore)},\\
&& \delta \quad \text{(discount rate per annum)}.\\[1mm]
\text{For convenience, define } D_t &=& \frac{1}{(1+\delta)^{t-1}},\quad \forall t\in\mathcal{T}.
\end{array}
\]

\vspace{3mm}

\[
\begin{array}{rcl}
\textbf{Decision Variables:} & & \\[1mm]
x_{k,t} &\ge & 0,\quad \forall k\in\mathcal{K},\;t\in\mathcal{T}, \quad \text{(production from mine } k \text{ in year } t\text{ [tons])},\\[1mm]
y_{k,t} &\in & \{0,1\},\quad \forall k\in\mathcal{K},\;t\in\mathcal{T}, \quad \text{(1 if mine } k \text{ is operated in year } t,\;0 \text{ otherwise)},\\[1mm]
z_{k,t} &\in & \{0,1\},\quad \forall k\in\mathcal{K},\;t\in\mathcal{T}, \quad \text{(1 if mine } k \text{ is permanently closed at the end of year } t,\;0 \text{ otherwise)}.
\end{array}
\]

\vspace{3mm}

\[
\begin{array}{rcl}
\textbf{Auxiliary Definitions:} && \\[1mm]
\text{For each } k\in\mathcal{K} \text{ and } t\in\mathcal{T},\; \text{define the open status } o_{k,t} &=& 1 - \sum_{s=1}^{t-1} z_{k,s}.
\end{array}
\]
Note that by definition, if a mine has never been closed in a prior period then \( o_{k,t}=1 \) (open), and if it has been closed (i.e. some \( z_{k,s}=1 \) for \( s < t \)) then \( o_{k,t}=0 \). Also, if a mine is closed then it is not eligible to be operated:
\[
y_{k,t} \le o_{k,t},\quad \forall k\in\mathcal{K},\; t\in\mathcal{T}.
\]

\vspace{3mm}

\[
\begin{align*}
\textbf{Objective:} \quad \max \quad & \displaystyle Z = \sum_{t=1}^{T} D_t \left[ \text{Price} \left( \sum_{k\in\mathcal{K}} x_{k,t} \right) - \sum_{k\in\mathcal{K}} \text{Royalty}_k\; o_{k,t} \right] \\[1mm]
\textbf{subject to:} \quad & \\[1mm]
\textbf{(1) Production Limits and Operation Link:} \quad & x_{k,t} \le \text{Limit}_k\, y_{k,t}, && \forall k\in\mathcal{K},\, t\in\mathcal{T}; \\[1mm]
\textbf{(2) Mine Availability:} \quad & x_{k,t} \le \text{Limit}_k\, o_{k,t}, && \forall k\in\mathcal{K},\, t\in\mathcal{T}; \\[1mm]
& & y_{k,t} \le o_{k,t}, && \forall k\in\mathcal{K},\, t\in\mathcal{T}; \\[1mm]
\textbf{(3) Maximum Operating Mines per Year:} \quad & \sum_{k\in\mathcal{K}} y_{k,t} \le \text{MaxWork}, && \forall t\in\mathcal{T}; \\[1mm]
\textbf{(4) Blending Quality Constraint:} \quad & \sum_{k\in\mathcal{K}} \text{Quality}_k\, x_{k,t} = \text{RequiredQuality}_t \sum_{k\in\mathcal{K}} x_{k,t}, && \forall t\in\mathcal{T}; \\[1mm]
\textbf{(5) Closure Decision:} \quad & \sum_{t=1}^{T} z_{k,t} \le 1, && \forall k\in\mathcal{K}; \\[1mm]
\textbf{(6) No Production after Closure:} \quad & x_{k,t} \le \text{Limit}_k\left(1 - \sum_{s=1}^{t-1} z_{k,s} \right), && \forall k\in\mathcal{K},\, t\in\mathcal{T}; \\[1mm]
\textbf{(7) Nontrivial Production Requirement:} \quad & \sum_{k\in\mathcal{K}} x_{k,t} \ge \epsilon, \quad \text{with } \epsilon>0 \text{ small}, && \forall t\in\mathcal{T}; \\[2mm]
\textbf{(8) Variable Domains:} \quad & x_{k,t} \ge 0,\; y_{k,t} \in \{0,1\},\; z_{k,t} \in \{0,1\}, && \forall k\in\mathcal{K},\, t\in\mathcal{T}.
\end{align*}
\]

\vspace{2mm}
\textbf{Comments on the Model:}

1. Decision variable \(x_{k,t}\) represents the continuous tons produced from mine \(k\) in year \(t\).  
2. Binary variable \(y_{k,t}\) indicates whether mine \(k\) is “operated” (i.e. produces a positive amount) in year \(t\).  
3. Binary variable \(z_{k,t}\) indicates the decision to permanently close mine \(k\) at the end of year \(t\). Once closed, its open status \(o_{k,t}\) becomes 0 for all subsequent years, and no further production is allowed, thus saving future royalty payments.  
4. Constraint (1) couples production to an “operated” decision and (2)–(6) ensure that production can only occur while the mine remains open.  
5. Constraint (3) ensures that no more than \(\text{MaxWork}\) mines are operated in any given year.  
6. Constraint (4) forces the weighted average (blend) quality of the ore produced in each year to equal the client’s required quality.  
7. Constraint (7) is included to avoid the trivial solution of zero production (i.e. at least a small positive production is required each year).  
8. Future cash flows are discounted by \(D_t\) to compute net present value in the objective function.

This complete and self‐contained formulation faithfully reflects the given Energy and Natural Resources mining optimization problem. '''

# Generated Code:
from ortools.linear_solver import pywraplp

def main():
    # Problem Data
    K = 4  # number of mines
    MaxWork = 3  # maximum mines operated per year
    Royalty = [5e6, 4e6, 4e6, 5e6]
    Limit = [2e6, 2.5e6, 1.3e6, 3e6]
    Quality = [1.0, 0.7, 1.5, 0.5]
    RequiredQuality = [0.9, 0.8, 1.2, 0.6, 1.0]  # one for each year
    Price = 10
    Discount = 0.1
    epsilon = 1  # small nontrivial production amount
    
    T = len(RequiredQuality)  # number of years

    # Create solver instance using CBC Mixed Integer Programming solver.
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Solver not created.")
        return

    # Decision Variables
    x = {}  # production: continuous >= 0
    y = {}  # operating decision: binary
    z = {}  # closure decision: binary

    for k in range(K):
        for t in range(T):
            x[k, t] = solver.NumVar(0, Limit[k], f'x_{k}_{t}')
            y[k, t] = solver.IntVar(0, 1, f'y_{k}_{t}')
            z[k, t] = solver.IntVar(0, 1, f'z_{k}_{t}')

    # Pre-calculate discount factors: D[t] = 1 / (1+Discount)**t for t=0,...,T-1
    D = [1.0 / ((1 + Discount) ** t) for t in range(T)]

    # Constraints
    # (1) Production limit and link with y: x[k,t] <= Limit[k] * y[k,t]
    for k in range(K):
        for t in range(T):
            solver.Add(x[k, t] <= Limit[k] * y[k, t])
    
    # Define open status o[k,t] as 1 - sum_{s=0}^{t-1} z[k,s]
    # and add constraints that enforce:
    # (2) Mine availability: x[k,t] <= Limit[k] * o[k,t]
    # (3) y[k,t] <= o[k,t]
    for k in range(K):
        for t in range(T):
            # Build expression for o_{k,t}
            o_expr = 1
            for s in range(t):
                o_expr -= z[k, s]
            solver.Add(x[k, t] <= Limit[k] * o_expr)
            solver.Add(y[k, t] <= o_expr)
    
    # (3) Maximum operating mines per year: sum_k y[k,t] <= MaxWork
    for t in range(T):
        solver.Add(solver.Sum([y[k, t] for k in range(K)]) <= MaxWork)

    # (4) Blending quality constraint:
    # sum_k Quality_k * x[k,t] = RequiredQuality[t] * sum_k x[k,t]
    # Rearranged: sum_k (Quality_k - RequiredQuality[t]) * x[k,t] = 0.
    for t in range(T):
        blend_expr = solver.Sum([(Quality[k] - RequiredQuality[t]) * x[k, t] for k in range(K)])
        solver.Add(blend_expr == 0)

    # (5) Closure decision: each mine can be closed at most once.
    for k in range(K):
        solver.Add(solver.Sum([z[k, t] for t in range(T)]) <= 1)

    # (7) Nontrivial production requirement: total production each year >= epsilon.
    for t in range(T):
        solver.Add(solver.Sum([x[k, t] for k in range(K)]) >= epsilon)

    # Objective: maximize sum_t D[t]*(Price*sum_k x[k,t] - sum_k Royalty[k]*o[k,t]),
    # with o[k,t] defined as 1 - sum_{s=0}^{t-1} z[k,s].
    objective_terms = []
    for t in range(T):
        # Production revenue
        production_term = Price * solver.Sum([x[k, t] for k in range(K)])
        # Royalty payments for mines that are still open: o[k,t] = 1 - sum_{s=0}^{t-1} z[k,s]
        royalty_term = solver.Sum([Royalty[k] * (1 - solver.Sum([z[k, s] for s in range(t)])) for k in range(K)])
        objective_terms.append(D[t] * (production_term - royalty_term))
    
    solver.Maximize(solver.Sum(objective_terms))

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print("Optimal objective value =", solver.Objective().Value())
        for t in range(T):
            print(f"Year {t+1}:")
            total_production = 0
            for k in range(K):
                production = x[k, t].solution_value()
                operate = y[k, t].solution_value()
                closure = z[k, t].solution_value()
                total_production += production
                print(f"  Mine {k+1}: production = {production:.2f}, operated = {int(operate)}, closed = {int(closure)}")
            print(f"  Total production = {total_production:.2f}\n")
    else:
        print("No optimal solution found.")

if __name__ == '__main__':
    main()