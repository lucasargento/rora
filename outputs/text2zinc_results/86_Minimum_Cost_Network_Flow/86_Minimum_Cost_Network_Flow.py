# Mathematical Formulation:
'''\[
\begin{array}{rcl}
\textbf{Indices:} & & \\
l & = & 1,\ldots, L \quad \text{with } L \text{ = NumLinks}, \\
f & = & 1,\ldots, F \quad \text{with } F \text{ = NumFlowReqs}, \\
n & \in & N \quad \text{(set of all nodes in the network)}. \\[1ex]

\textbf{Parameters:} & & \\
\text{StartNode}_l & = & \text{Starting node of link } l, \quad l=1,\ldots,L, \\
\text{EndNode}_l & = & \text{Ending node of link } l, \quad l=1,\ldots,L, \\
\text{Capacity}_l & = & \text{Maximum data capacity of link } l, \quad l=1,\ldots,L, \\
\text{Cost}_l & = & \text{Cost per unit data transmitted on link } l, \quad l=1,\ldots,L, \\
s_f & = & \text{Source node for data flow } f, \quad f=1,\ldots,F, \\
t_f & = & \text{Destination node for data flow } f, \quad f=1,\ldots,F, \\
d_f & = & \text{Required data rate for flow } f, \quad f=1,\ldots,F. \\[1ex]

\textbf{Decision Variables:} & & \\
x_{l}^{(f)} & \ge & 0, \quad \forall \, l=1,\ldots,L, \, \forall \, f=1,\ldots,F, \\
& & \text{where } x_{l}^{(f)} \text{ is the amount of data from flow } f \\
& & \text{transmitted along link } l. \\[1ex]

\textbf{Objective Function:} & & \\
\min \quad Z & = & \sum_{l=1}^{L} \sum_{f=1}^{F} \text{Cost}_l \; x_{l}^{(f)}.
\end{array}
\]

\[
\begin{array}{rcl}
\textbf{Subject to:} & & \\[1ex]
\text{(1) \quad Capacity constraints for each link:} && \\
\quad \sum_{f=1}^{F} x_{l}^{(f)} & \le & \text{Capacity}_l, \quad \forall \, l=1,\ldots, L. \\[1ex]
\text{(2) \quad Flow conservation constraints for each flow at each node:} && \\
\quad \sum_{\substack{l: \ \text{StartNode}_l = n}} x_{l}^{(f)} - \sum_{\substack{l:\ \text{EndNode}_l = n}} x_{l}^{(f)} 
& = & 
\begin{cases}
d_f, & \text{if } n = s_f, \\
-\,d_f, & \text{if } n = t_f, \\
0, & \text{if } n \in N \setminus \{s_f,t_f\},
\end{cases} \\
&& \forall \, n\in N, \quad \forall \, f=1,\ldots,F.
\end{array}
\]

\[
\begin{array}{rcl}
\textbf{Domain:} && \\
x_{l}^{(f)} & \in & \mathbb{R}_{+} \quad \forall\, l=1,\ldots,L,\; \forall\, f=1,\ldots,F.
\end{array}
\]

This model completely describes the problem of routing multiple data flows over a network. The flow for each commodity f is split arbitrarily over the given links in such a way that the total data on each link does not exceed its capacity, and the overall cost 
\[
\sum_{l=1}^{L} \sum_{f=1}^{F} \text{Cost}_l \; x_{l}^{(f)}
\]
is minimized.'''

# Generated Code:
from ortools.linear_solver import pywraplp

def main():
    # Problem data
    NumLinks = 4
    StartNode = [1, 2, 2, 3]
    EndNode = [2, 3, 4, 4]
    Capacity = [50, 40, 60, 50]
    Cost = [2, 3, 1, 1]
    
    NumFlowReqs = 2
    SourceNode = [1, 2]
    DestinationNode = [4, 3]
    DataRate = [40, 30]

    # Identify all nodes in the network
    nodes = set(StartNode + EndNode + SourceNode + DestinationNode)
    
    # Create solver instance using CBC
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Error: CBC solver not found.")
        return

    # Decision variables:
    # x[l][f] is the amount of data from flow f transmitted along link l.
    x = {}
    for l in range(NumLinks):
        for f in range(NumFlowReqs):
            # Create continuous variables x[l,f] >= 0
            x[(l, f)] = solver.NumVar(0.0, solver.infinity(), f'x_{l}_{f}')

    # Objective: minimize sum_l sum_f (Cost[l] * x[l,f])
    objective = solver.Objective()
    for l in range(NumLinks):
        for f in range(NumFlowReqs):
            objective.SetCoefficient(x[(l, f)], Cost[l])
    objective.SetMinimization()

    # Capacity constraints for each link: sum_f x[l,f] <= Capacity[l]
    for l in range(NumLinks):
        constraint = solver.Constraint(0, Capacity[l])
        for f in range(NumFlowReqs):
            constraint.SetCoefficient(x[(l, f)], 1)

    # Build mapping for outgoing and incoming links for each node
    # For each node, store list of links that start at node and links that end at node.
    outgoing = {n: [] for n in nodes}
    incoming = {n: [] for n in nodes}
    for l in range(NumLinks):
        outgoing[StartNode[l]].append(l)
        incoming[EndNode[l]].append(l)

    # Flow conservation constraints for each flow f at each node n
    for f in range(NumFlowReqs):
        for n in nodes:
            # Calculate net flow: outgoing - incoming = rhs
            if n == SourceNode[f]:
                rhs = DataRate[f]
            elif n == DestinationNode[f]:
                rhs = -DataRate[f]
            else:
                rhs = 0
            constraint = solver.Constraint(rhs, rhs)
            for l in outgoing.get(n, []):
                constraint.SetCoefficient(x[(l, f)], 1)
            for l in incoming.get(n, []):
                constraint.SetCoefficient(x[(l, f)], -1)

    # Solve the model
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print("Optimal solution found with objective value =", solver.Objective().Value())
        for l in range(NumLinks):
            for f in range(NumFlowReqs):
                val = x[(l, f)].solution_value()
                if val > 0:
                    print(f"Link {l+1} (from {StartNode[l]} to {EndNode[l]}), Flow {f+1} = {val}")
    elif status == pywraplp.Solver.INFEASIBLE:
        print("The problem is infeasible.")
    else:
        print("Solver ended with status", status)

if __name__ == '__main__':
    main()