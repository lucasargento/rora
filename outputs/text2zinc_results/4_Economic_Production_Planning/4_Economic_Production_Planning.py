# Mathematical Formulation:
'''\[
\begin{array}{rcll}
\textbf{Indices and Sets:} & & & \\[1mm]
i,k &\in& \{1,\ldots, n\} & \text{(Industries)}\\[1mm]
t &\in& \{0,1,2,\ldots,T\} & \text{(Time periods; note that } t=0 \text{ is the initial period)}\\[1mm]
t &\in& \mathcal{P} = \{1,\ldots,T\} & \text{(Periods in which production occurs)}\\[1mm]
t &\in& \mathcal{V} = \{1,\ldots,T-2\} & \text{(Periods in which capacity investment decisions are made)}
\\[3mm]
\multicolumn{4}{l}{\textbf{Parameters:}}\\[1mm]
T &:& \text{Number of periods (planning horizon).}\\[1mm]
\text{InputOne}_{i,k} &:& \text{Units of output from industry } i \text{ required per unit production in industry } k \text{ (production input)}.\\[1mm]
\text{ManpowerOne}_{k} &:& \text{Manpower required per unit production in industry } k.\\[1mm]
\text{InputTwo}_{i,k} &:& \text{Units of output from industry } i \text{ required per unit capacity built for industry } k.\\[1mm]
\text{ManpowerTwo}_{k} &:& \text{Manpower required per unit capacity built for industry } k.\\[1mm]
\text{Stock}_{i} &:& \text{Initial stock available of product } i \text{ (at } t=0\text{)}.\\[1mm]
\text{Capacity}_{k} &:& \text{Initial production capacity of industry } k \text{ (at } t=0\text{)}.\\[1mm]
\text{ManpowerLimit} &:& \text{Maximum available manpower per period.}\\[3mm]
\multicolumn{4}{l}{\textbf{Decision Variables:}}\\[1mm]
x_{k,t} &\ge& 0,\quad \forall k\in\{1,\ldots,n\},\; t\in \mathcal{P} &
\begin{array}{l}
\text{Production (in £1’s worth units) in industry } k \text{ in period } t.\\[0.5mm]
\text{(Note: a “unit” is £1 of production value.)}
\end{array}\\[2mm]
v_{k,t} &\ge& 0,\quad \forall k\in\{1,\ldots,n\},\; t\in \mathcal{V} &
\begin{array}{l}
\text{Capacity investment in industry } k \text{ in period } t.\\[0.5mm]
\text{One unit of } v_{k,t} \text{, when realized in period } t+2, \\[0.5mm]
\text{increases the capacity available (permanently) by one unit.}
\end{array}\\[2mm]
I_{i,t} &\ge& 0,\quad \forall i\in\{1,\ldots,n\},\; t=0,1,\ldots,T & 
\begin{array}{l}
\text{Inventory (“stock”) level of product } i \text{ available at the beginning}\\[0.5mm]
\text{of period } t.
\end{array}\\[2mm]
C_{k,t} &\ge& 0,\quad \forall k\in\{1,\ldots,n\},\; t=0,1,\ldots,T &
\begin{array}{l}
\text{Production capacity available to industry } k \text{ in period } t.
\end{array}\\[3mm]
\multicolumn{4}{l}{\textbf{Objective Function:}}\\[1mm]
\text{Maximize}\quad Z &=& \sum_{k=1}^{n} \Bigl( x_{k,T-1} + x_{k,T} \Bigr) & 
\begin{array}{l}
\text{Total production in the last two periods (i.e., periods } T-1 \text{ and } T\text{).}
\end{array}
\\[3mm]
\multicolumn{4}{l}{\textbf{Constraints:}}\\[1mm]
\textbf{(1) Inventory Consumption and Flow:}&&&\\[1mm]
\text{For } t=0: \quad & 
\displaystyle \sum_{k=1}^{n} \text{InputOne}_{i,k}\, x_{k,1} 
&\le& I_{i,0}, \quad \forall i=1,\ldots,n. 
\label{inv0}\\[2mm]
\text{For } t=1, \; \text{(using period } t=1 \text{ inventories):} \quad & 
\displaystyle \sum_{k=1}^{n} \text{InputOne}_{i,k}\, x_{k,2} + \sum_{k=1}^{n} \text{InputTwo}_{i,k}\, v_{k,1} 
&\le& I_{i,1}, \quad \forall i=1,\ldots,n. 
\label{inv1}\\[2mm]
\text{For } t \ge 2 \text{ (if defined):} \quad & 
\displaystyle \sum_{k=1}^{n} \text{InputOne}_{i,k}\, x_{k,t+1} + \left\{\begin{array}{ll}
\sum_{k=1}^{n} \text{InputTwo}_{i,k}\, v_{k,t} & \text{if } t\in \mathcal{V},\\[1mm]
0 & \text{if } t\notin \mathcal{V},
\end{array}\right.
&\le& I_{i,t}, \quad \forall i=1,\ldots,n,\; t=2,\ldots,T-1.
\label{invt}
\\[3mm]
\textbf{Inventory Update Equations:}&&&\\[1mm]
I_{i,1} &=& I_{i,0} - \sum_{k=1}^{n} \text{InputOne}_{i,k}\, x_{k,1} + x_{i,1}, \quad
\forall i=1,\ldots,n, 
\label{invupdate1}\\[2mm]
I_{i,t+1} &=& I_{i,t} - \left( \sum_{k=1}^{n} \text{InputOne}_{i,k}\, x_{k,t+1} + \chi_{\{t\in \mathcal{V}\}}\, \sum_{k=1}^{n} \text{InputTwo}_{i,k}\, v_{k,t} \right) + x_{i,t+1},\\[1mm]
&&& \forall i=1,\ldots,n,\; t=1,\ldots,T-1,
\label{invupdatet}
\\[3mm]
\textbf{(2) Manpower (Labor) Constraints:}&&&\\[1mm]
\text{For inputs allocated in period } t=0: \quad & 
\displaystyle \sum_{k=1}^{n} \text{ManpowerOne}_{k}\, x_{k,1} 
&\le& \text{ManpowerLimit}.
\label{mp0}\\[2mm]
\text{For period } t=1: \quad & 
\displaystyle \sum_{k=1}^{n} \text{ManpowerOne}_{k}\, x_{k,2} + \sum_{k=1}^{n} \text{ManpowerTwo}_{k}\, v_{k,1} 
&\le& \text{ManpowerLimit}.
\label{mp1}\\[2mm]
\text{For period } t=2, \; (\text{and similarly for } t\ge 2 \text{ if defined}): \quad & 
\displaystyle \sum_{k=1}^{n} \text{ManpowerOne}_{k}\, x_{k,3} + \left\{\begin{array}{ll}
\sum_{k=1}^{n} \text{ManpowerTwo}_{k}\, v_{k,2} & \text{if } 2\in \mathcal{V},\\[1mm]
0 & \text{otherwise},
\end{array}\right.
&\le& \text{ManpowerLimit}.
\label{mp2}
\\[3mm]
\textbf{(3) Capacity Limits and Dynamics:}&&&\\[1mm]
\text{Production Capacity Constraint:}\quad & 
x_{k,t} &\le& C_{k,t}, \quad \forall k=1,\ldots,n,\; t\in \mathcal{P}.
\label{capprod}\\[2mm]
\text{Initial Capacity:}\quad & 
C_{k,0} &=& \text{Capacity}_{k}, \quad \forall k=1,\ldots,n.
\label{capinit}\\[2mm]
\text{Capacity Update:}\quad & 
C_{k,t} &=& C_{k,t-1} + \left\{ \begin{array}{ll}
v_{k,t-2}, & \text{if } t\ge 3,\\[0.5mm]
0, & \text{if } t=1,2,
\end{array} \right. \quad \forall k=1,\ldots,n,\; t=1,\ldots,T.
\label{capupdate}
\\[3mm]
\textbf{(4) Nonnegativity:}&&&\\[1mm]
x_{k,t} &\ge& 0, &&\forall k\in\{1,\ldots,n\},\; t\in \mathcal{P},\\[2mm]
v_{k,t} &\ge& 0, &&\forall k\in\{1,\ldots,n\},\; t\in \mathcal{V},\\[2mm]
I_{i,t} &\ge& 0, &&\forall i\in\{1,\ldots,n\},\; t=0,1,\ldots,T,\\[2mm]
C_{k,t} &\ge& 0, &&\forall k\in\{1,\ldots,n\},\; t=0,1,\ldots,T.
\end{array}
\]

\vspace{2mm}
\textbf{Explanation of the Formulation:}

1. \textbf{Decision Variables:}  
 • xₖ,ₜ represents the production (in £1’s worth) in industry k during period t.  
 • vₖ,ₜ represents the capacity‐investment decision for industry k in period t; the new capacity becomes effective in period t+2.  
 • Iᵢ,ₜ is the inventory level for product i available at the beginning of period t (stocks can be carried over).  
 • Cₖ,ₜ is the production capacity available for industry k in period t.  

2. \textbf{Objective Function:}  
We maximize the total production in the last two periods (i.e. periods T–1 and T):
  max Z = ∑ₖ ( xₖ,₍T–1₎ + xₖ,₍T₎ ).

3. \textbf{Constraints:}  
 • \emph{Inventory consumption and flow:} In every period the inventory available from the previous period must be sufficient to meet the “input demands” required both for production (according to InputOne) and for capacity investments (according to InputTwo). The update equations record that the available inventory in the next period equals what is left after input consumption plus the production output of that period.  
 • \emph{Manpower constraints:} In each period the total manpower required—both for processing the inputs to produce goods (using ManpowerOne) and to build capacity (using ManpowerTwo)—cannot exceed ManpowerLimit.  
 • \emph{Capacity limits and dynamics:} Production in each industry cannot exceed the available capacity. Capacity is initially given and increases (permanently) when capacity investment decisions (v) are realized two periods later.  
 • \emph{Nonnegativity:} All decision variables are required to be nonnegative.

4. \textbf{Model Features:}  
This formulation does not “force” trivial solutions (e.g. producing only one product) since the input‐consumption and capacity buildup constraints couple all industries together. All constraints—including flow balances, capacity and manpower limits—ensure that the problem is both feasible and bounded.

This complete mathematical model faithfully captures the economic and business decision problem described and is ready for translation into an OR-Tools implementation.
'''

# Generated Code:
from ortools.linear_solver import pywraplp


def main():
    # Data
    n = 3  # number of industries/products
    T = 3  # planning horizon periods (t = 1,2,3 for production; t = 0,...,3 for inventory/capacity)
    
    # Parameters (indices: 0-indexed)
    InputOne = [
        [0.1, 0.1, 0.2],
        [0.5, 0.1, 0.1],
        [0.5, 0.2, 0.2],
    ]
    InputTwo = [
        [0.0, 0.1, 0.2],
        [0.7, 0.1, 0.1],
        [0.9, 0.2, 0.2],
    ]
    ManpowerOne = [0.6, 0.3, 0.2]
    ManpowerTwo = [0.4, 0.2, 0.1]
    Stock = [150, 80, 100]
    Capacity = [300, 350, 280]
    ManpowerLimit = 470000000.0

    # Create solver
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Solver not created.")
        return

    infinity = solver.infinity()

    # Decision variables
    # x[k,t] production for industry k in period t (t = 1,2,3)
    x = {}
    for k in range(n):
        for t in range(1, T + 1):
            x[k, t] = solver.NumVar(0.0, infinity, f'x_{k}_{t}')

    # v[k,t] capacity investment for industry k in period t (investment periods: t in V = {1,...,T-2})
    # For T = 3, V = {1} only.
    v = {}
    for k in range(n):
        # t=1 is the only period in V
        v[k, 1] = solver.NumVar(0.0, infinity, f'v_{k}_1')

    # I[i,t] inventory level for product i in period t (t = 0,1,2,3)
    I = {}
    for i in range(n):
        for t in range(0, T + 1):
            I[i, t] = solver.NumVar(0.0, infinity, f'I_{i}_{t}')

    # C[k,t] production capacity for industry k in period t (t = 0,1,2,3)
    C = {}
    for k in range(n):
        for t in range(0, T + 1):
            C[k, t] = solver.NumVar(0.0, infinity, f'C_{k}_{t}')

    # Initial conditions (set equality constraints)
    for i in range(n):
        solver.Add(I[i, 0] == Stock[i])
    for k in range(n):
        solver.Add(C[k, 0] == Capacity[k])

    # (1) Inventory Consumption and Flow constraints
    # For t = 0: consumption for production in period 1 cannot exceed available stock I[i,0]
    for i in range(n):
        consumption = solver.Sum(InputOne[i][k] * x[k, 1] for k in range(n))
        solver.Add(consumption <= I[i, 0])

    # For t = 1: consumption for production in period 2 plus capacity investment inputs from period 1
    for i in range(n):
        consumption = solver.Sum(InputOne[i][k] * x[k, 2] for k in range(n)) + \
                      solver.Sum(InputTwo[i][k] * v[k, 1] for k in range(n))
        solver.Add(consumption <= I[i, 1])

    # For t = 2: consumption for production in period 3 (no capacity investment because V only includes period 1)
    for i in range(n):
        consumption = solver.Sum(InputOne[i][k] * x[k, 3] for k in range(n))
        solver.Add(consumption <= I[i, 2])

    # Inventory Update Equations:
    # For t = 1
    for i in range(n):
        produced = x[i, 1]  # production from industry i adds to inventory of product i
        consumption = solver.Sum(InputOne[i][k] * x[k, 1] for k in range(n))
        solver.Add(I[i, 1] == I[i, 0] - consumption + produced)

    # For t = 2
    for i in range(n):
        produced = x[i, 2]
        consumption = solver.Sum(InputOne[i][k] * x[k, 2] for k in range(n)) + \
                      solver.Sum(InputTwo[i][k] * v[k, 1] for k in range(n))
        solver.Add(I[i, 2] == I[i, 1] - consumption + produced)

    # For t = 3
    for i in range(n):
        produced = x[i, 3]
        consumption = solver.Sum(InputOne[i][k] * x[k, 3] for k in range(n))
        solver.Add(I[i, 3] == I[i, 2] - consumption + produced)

    # (2) Manpower (Labor) Constraints
    # Period 1: Production in period 1
    solver.Add(solver.Sum(ManpowerOne[k] * x[k, 1] for k in range(n)) <= ManpowerLimit)

    # Period 2: Production in period 2 and capacity investment in period 1
    solver.Add(solver.Sum(ManpowerOne[k] * x[k, 2] for k in range(n)) +
               solver.Sum(ManpowerTwo[k] * v[k, 1] for k in range(n)) <= ManpowerLimit)

    # Period 3: Production in period 3 (no capacity investment as v for period 2 not defined)
    solver.Add(solver.Sum(ManpowerOne[k] * x[k, 3] for k in range(n)) <= ManpowerLimit)

    # (3) Capacity Limits and Dynamics
    # Production Capacity Constraint: x[k,t] <= C[k,t] for t = 1,2,3
    for k in range(n):
        for t in range(1, T + 1):
            solver.Add(x[k, t] <= C[k, t])

    # Capacity Update Equations:
    # For t = 1: C[k,1] = C[k,0]
    for k in range(n):
        solver.Add(C[k, 1] == C[k, 0])
    # For t = 2: C[k,2] = C[k,1]
    for k in range(n):
        solver.Add(C[k, 2] == C[k, 1])
    # For t = 3: C[k,3] = C[k,2] + v[k,1]
    for k in range(n):
        solver.Add(C[k, 3] == C[k, 2] + v[k, 1])

    # (4) Nonnegativity is ensured by variable definitions.

    # Objective: Maximize total production in periods T-1 and T (i.e., periods 2 and 3)
    objective = solver.Sum(x[k, 2] + x[k, 3] for k in range(n))
    solver.Maximize(objective)

    # Solve the model
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print("Optimal objective value =", solver.Objective().Value())
        for k in range(n):
            for t in range(1, T + 1):
                print(f'x[{k},{t}] =', x[k, t].solution_value())
        for k in range(n):
            # v exists only for period 1
            print(f'v[{k},1] =', v[k, 1].solution_value())
        for i in range(n):
            for t in range(0, T + 1):
                print(f'I[{i},{t}] =', I[i, t].solution_value())
        for k in range(n):
            for t in range(0, T + 1):
                print(f'C[{k},{t}] =', C[k, t].solution_value())
    else:
        print("The problem does not have an optimal solution.")


if __name__ == '__main__':
    main()