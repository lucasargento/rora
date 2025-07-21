# Mathematical Formulation:
'''\begin{align*}
\textbf{Indices and Sets:} \quad & i \in \{1,2,\ldots,N\} \quad \text{with } N=5,\\[1mm]
\text{Let } & \mathcal{GP} = \{ i : \text{system } i \text{ is General–Purpose, i.e. } \mathtt{IsWorkstation}_i = \text{False}\},\\[1mm]
& \mathcal{WS} = \{ i : \text{system } i \text{ is a Workstation, i.e. } \mathtt{IsWorkstation}_i = \text{True}\},\\[1mm]
& \mathcal{ALT} = \{ i : \text{alternative memory is compatible with system } i \, (\mathtt{AltCompatible}_i = \text{True})\}.
\end{align*}

\noindent
\textbf{Decision Variables:}
\begin{align*}
x_i \quad &\ge 0,\quad \text{(continuous)} &&\text{Production quantity (number of systems) of type } i,\\[1mm]
a_i \quad &\ge 0,\quad \text{(continuous)} &&\text{Quantity of systems of type } i\text{ that use alternative memory.}
\end{align*}
We require also that for every system:
\begin{align*}
a_i \le x_i,\quad \forall i=1,\ldots,N, \quad \text{and for } i\notin \mathcal{ALT}:\quad a_i = 0.
\end{align*}

\noindent
\textbf{Parameters:} (Data provided)
\begin{align*}
\mathtt{Price}_i,\; \mathtt{DiskDrives}_i,\; \mathtt{MemoryBoards}_i,\; \mathtt{Demand}_i,\; \mathtt{Preorder}_i,\; \text{ for }i=1,\ldots,N;\\[1mm]
\mathtt{MaxCpu} = 7000, \quad \mathtt{MinDisk} = 3000, \quad \mathtt{MaxDisk} = 7000,\\[1mm]
\mathtt{MinMemory} = 8000, \quad \mathtt{MaxMemory} = 16000,\\[1mm]
\mathtt{DemandGP} = 3800,\quad \mathtt{DemandWS} = 3200, \quad \mathtt{AltMemory} = 4000.
\end{align*}

\noindent
\textbf{Objective Function:} Maximize total profit (in dollars)
\begin{align*}
\max_{x,a} \quad Z = \sum_{i=1}^{N} \mathtt{Price}_i\, x_i.
\end{align*}

\noindent
\textbf{Constraints:}
\begin{enumerate}
    \item \textbf{CPU Availability:} Each system requires 1 CPU.
    \begin{align*}
    \sum_{i=1}^{N} x_i \le \mathtt{MaxCpu}.
    \end{align*}
    
    \item \textbf{Disk Drive Supply:} Total disk drives used must be within the available bounds. Each system of type $i$ requires $\mathtt{DiskDrives}_i$ drives.
    \begin{align*}
    \mathtt{MinDisk} \le \sum_{i=1}^{N} \mathtt{DiskDrives}_i \, x_i \le \mathtt{MaxDisk}.
    \end{align*}
    
    \item \textbf{Main (256K) Memory Supply:} Systems using main memory (i.e. not using alternative memory) draw $\mathtt{MemoryBoards}_i$ boards each. The total usage must lie within the available supply.
    \begin{align*}
    \mathtt{MinMemory} \le \sum_{i=1}^{N} \mathtt{MemoryBoards}_i \,(x_i - a_i) \le \mathtt{MaxMemory}.
    \end{align*}
    
    \item \textbf{Alternative Memory Supply:} Only systems for which alternative memory is available may use it. The alternative memory board units required for such systems must not exceed $\mathtt{AltMemory}$.
    \begin{align*}
    \sum_{i \in \mathcal{ALT}} \mathtt{MemoryBoards}_i\, a_i \le \mathtt{AltMemory}.
    \end{align*}
    
    \item \textbf{Individual System Demand:} For each system type, production cannot exceed its maximum estimated demand.
    \begin{align*}
    x_i \le \mathtt{Demand}_i,\quad \forall \, i=1,\ldots,N.
    \end{align*}
    
    \item \textbf{Family Demand (General–Purpose and Workstations):}
    \begin{align*}
    \sum_{i \in \mathcal{GP}} x_i \le \mathtt{DemandGP},\quad \sum_{i \in \mathcal{WS}} x_i \le \mathtt{DemandWS}.
    \end{align*}
    
    \item \textbf{Preorder Fulfillment:} Production must at least meet the number of preordered systems for each type.
    \begin{align*}
    x_i \ge \mathtt{Preorder}_i,\quad \forall \, i=1,\ldots,N.
    \end{align*}
    
    \item \textbf{Alternative Memory Usage Validity:} For every system type:
    \begin{align*}
    a_i \le x_i,\quad \forall\, i=1,\ldots,N, \quad \text{and} \quad a_i = 0 \quad \forall\, i \notin \mathcal{ALT}.
    \end{align*}
    
    \item \textbf{Nonnegativity:}
    \begin{align*}
    x_i \ge 0,\quad a_i \ge 0,\quad \forall\, i=1,\ldots,N.
    \end{align*}
\end{enumerate}

\noindent
\textbf{Final Model Summary:}
\begin{align*}
\max_{x,a}\quad & Z = \sum_{i=1}^{N} \mathtt{Price}_i\, x_i \\[1mm]
\text{s.t.}\quad 
& \sum_{i=1}^{N} x_i \le \mathtt{MaxCpu}, \\[1mm]
& \mathtt{MinDisk} \le \sum_{i=1}^{N} \mathtt{DiskDrives}_i\, x_i \le \mathtt{MaxDisk}, \\[1mm]
& \mathtt{MinMemory} \le \sum_{i=1}^{N} \mathtt{MemoryBoards}_i\,(x_i - a_i) \le \mathtt{MaxMemory}, \\[1mm]
& \sum_{i \in \mathcal{ALT}} \mathtt{MemoryBoards}_i\, a_i \le \mathtt{AltMemory}, \\[1mm]
& x_i \le \mathtt{Demand}_i, \quad \forall\, i=1,\ldots,N, \\[1mm]
& \sum_{i \in \mathcal{GP}} x_i \le \mathtt{DemandGP}, \\[1mm]
& \sum_{i \in \mathcal{WS}} x_i \le \mathtt{DemandWS}, \\[1mm]
& x_i \ge \mathtt{Preorder}_i,\quad \forall\, i=1,\ldots,N, \\[1mm]
& a_i \le x_i,\quad \forall\, i=1,\ldots,N, \quad \text{with } a_i=0 \text{ for } i\notin\mathcal{ALT}, \\[1mm]
& x_i \ge 0,\quad a_i \ge 0,\quad \forall\, i=1,\ldots,N.
\end{align*}

This complete formulation accurately represents the manufacturing and production problem for DEC, incorporating production quantities, memory allocation (split between main and alternative supplies), disk drive usage, CPU availability, demand (individual, family‐and preorder) and resource bounds without any simplification.'''

# Generated Code:
from ortools.linear_solver import pywraplp

def main():
    # Create the solver with the CBC backend.
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Solver not created.")
        return

    # Data
    N = 5
    IsWorkstation = [False, False, False, True, True]
    Price = [60000, 40000, 30000, 30000, 15000]
    DiskDrives = [0.3, 1.7, 0, 1.4, 0]
    MemoryBoards = [4, 2, 2, 2, 1]
    Demand = [1800, 999999, 300, 999999, 999999]
    Preorder = [0, 500, 0, 500, 400]
    
    # Resource limits and family demand
    MaxCpu = 7000
    MinDisk = 3000
    MaxDisk = 7000
    MinMemory = 8000
    MaxMemory = 16000
    DemandGP = 3800  # General Purpose systems (IsWorkstation = False)
    DemandWS = 3200  # Workstation systems (IsWorkstation = True)
    AltMemory = 4000
    AltCompatible = [True, False, False, False, False]
    
    # Sets
    # GP : systems where IsWorkstation is False; WS: where True; ALT: where AltCompatible is True.
    GP_indices = [i for i in range(N) if not IsWorkstation[i]]
    WS_indices = [i for i in range(N) if IsWorkstation[i]]
    ALT_indices = [i for i in range(N) if AltCompatible[i]]
    
    # Decision Variables:
    # x[i]: production quantity for system i
    # a[i]: production quantity for system i using alternative memory.
    x = [solver.NumVar(0.0, Demand[i], f'x[{i}]') for i in range(N)]
    a = []
    for i in range(N):
        if AltCompatible[i]:
            # If alternative memory is available, a[i] can be between 0 and x[i] (upper bound will be enforced by constraint a[i] <= x[i]).
            a.append(solver.NumVar(0.0, Demand[i], f'a[{i}]'))
        else:
            # For systems that are not compatible, force a[i] = 0.
            a.append(solver.NumVar(0.0, 0.0, f'a[{i}]'))
    
    # Objective: Maximize total profit = sum(Price[i] * x[i])
    objective = solver.Objective()
    for i in range(N):
        objective.SetCoefficient(x[i], Price[i])
    objective.SetMaximization()
    
    # Constraints:
    
    # 1. CPU Availability: Total systems <= MaxCpu.
    solver.Add(solver.Sum(x[i] for i in range(N)) <= MaxCpu)
    
    # 2. Disk Drive Supply: MinDisk <= sum(DiskDrives[i]*x[i]) <= MaxDisk
    disk_expr = solver.Sum(DiskDrives[i] * x[i] for i in range(N))
    solver.Add(disk_expr >= MinDisk)
    solver.Add(disk_expr <= MaxDisk)
    
    # 3. Main Memory Supply: MinMemory <= sum(MemoryBoards[i]*(x[i] - a[i])) <= MaxMemory.
    memory_expr = solver.Sum(MemoryBoards[i] * (x[i] - a[i]) for i in range(N))
    solver.Add(memory_expr >= MinMemory)
    solver.Add(memory_expr <= MaxMemory)
    
    # 4. Alternative Memory Supply: sum_{i in ALT} MemoryBoards[i]*a[i] <= AltMemory.
    alt_memory_expr = solver.Sum(MemoryBoards[i] * a[i] for i in ALT_indices)
    solver.Add(alt_memory_expr <= AltMemory)
    
    # 5. Individual System Demand: x[i] <= Demand[i] already set via variable bounds
    
    # 6. Family Demand:
    solver.Add(solver.Sum(x[i] for i in GP_indices) <= DemandGP)
    solver.Add(solver.Sum(x[i] for i in WS_indices) <= DemandWS)
    
    # 7. Preorder Fulfillment: x[i] >= Preorder[i]
    for i in range(N):
        solver.Add(x[i] >= Preorder[i])
    
    # 8. Alternative Memory Usage Validity: For all i, a[i] <= x[i]
    for i in range(N):
        solver.Add(a[i] <= x[i])
    
    # Solve the problem
    status = solver.Solve()
    
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("Solution:")
        print("Optimal objective value = ", objective.Value())
        for i in range(N):
            print(f"System {i}: Produce x = {x[i].solution_value()}, Alternative memory a = {a[i].solution_value()}")
    else:
        print("No feasible solution found.")

if __name__ == '__main__':
    main()