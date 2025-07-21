# Mathematical Formulation:
'''\begin{align*}
\textbf{Indices and Sets:} \quad & t \in \{1,2,\ldots,T\} \\[1mm]
\textbf{Parameters:} \quad & T \quad \text{(planning horizon in years)}\\[0.5mm]
& \text{Demand}_t \quad \text{(electricity demand in period } t\text{)}\\[0.5mm]
& \text{OilCap}_t \quad \text{(existing oil-fired capacity in period } t\text{)}\\[0.5mm]
& \text{CoalCost} \quad \text{(capital cost per unit of coal capacity)}\\[0.5mm]
& \text{NukeCost} \quad \text{(capital cost per unit of nuclear capacity)}\\[0.5mm]
& \text{MaxNuke} \quad \text{(upper bound on active nuclear capacity in any period)}\\[0.5mm]
& \text{CoalLife} \quad \text{(lifetime of a coal plant, in years)}\\[0.5mm]
& \text{NukeLife} \quad \text{(lifetime of a nuclear plant, in years)}\\[2mm]
\textbf{Decision Variables:} \quad & x_t^{coal} \ge 0 \quad \text{(new coal capacity built in period } t\text{)}\\[0.5mm]
& x_t^{nuke} \ge 0 \quad \text{(new nuclear capacity built in period } t\text{)}\\[2mm]
\textbf{Objective Function:} \quad & \text{Minimize } Z = \sum_{t=1}^{T} \Bigl( \text{CoalCost}\, x_t^{coal} + \text{NukeCost}\, x_t^{nuke} \Bigr) \\[2mm]
\textbf{Constraints:}\\[0.5mm]
\text{(1) Demand Satisfaction:} \quad & \text{For each } t=1,\ldots,T, \text{ the total available capacity must meet or exceed demand:} \\[0.5mm]
& \text{OilCap}_t + \sum_{i=\max\{1,t-\text{CoalLife}+1\}}^{t} x_i^{coal} + \sum_{i=\max\{1,t-\text{NukeLife}+1\}}^{t} x_i^{nuke} \ge \text{Demand}_t, \\[2mm]
\text{(2) Nuclear Capacity Limit:} \quad & \text{For each } t=1,\ldots,T, \text{ the active nuclear capacity cannot exceed the predetermined maximum:} \\[0.5mm]
& \sum_{i=\max\{1,t-\text{NukeLife}+1\}}^{t} x_i^{nuke} \le \text{MaxNuke}, \\[2mm]
\text{(3) Nonnegativity:} \quad & x_t^{coal} \ge 0, \quad x_t^{nuke} \ge 0, \quad \forall\, t = 1,\ldots,T.
\end{align*}

\textbf{Explanation:}  
1. The decision variables, \( x_t^{coal} \) and \( x_t^{nuke} \), represent the new capacities installed in period \( t \) for coal and nuclear technologies, respectively.  
2. The objective is to minimize the total capital cost incurred over the planning horizon.  
3. The Demand Satisfaction constraint aggregates the capacity available from (i) the non-retired oil-fired plants, (ii) coal plants built in the last \(\text{CoalLife}\) years, and (iii) nuclear plants built in the last \(\text{NukeLife}\) years, ensuring that yearly demand is met.  
4. The Nuclear Capacity Limit constraint ensures that in any period, the cumulative active nuclear capacity does not exceed the maximum allowable nuclear capacity due to political and safety considerations.  

This complete formulation accurately models the energy capacity planning problem while accounting for capacity lifetimes, demand requirements, and political constraints.'''

# Generated Code:
from ortools.linear_solver import pywraplp

def main():
    # Problem Data
    T = 12
    Demand = [10, 15, 17, 20, 13, 19, 10, 25, 30, 33, 30, 35]
    OilCap = [15, 14, 13, 10, 10, 7, 5, 5, 5, 5, 5, 5]
    CoalCost = 10
    NukeCost = 5
    MaxNuke = 20
    CoalLife = 5
    NukeLife = 10

    # Create the solver using CBC (Mixed Integer Programming)
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("CBC solver unavailable.")
        return

    infinity = solver.infinity()

    # Decision Variables:
    # x_coal[t] and x_nuke[t] represent the new capacity built in period t (t=0...T-1)
    x_coal = [solver.NumVar(0, infinity, f'x_coal_{t}') for t in range(T)]
    x_nuke = [solver.NumVar(0, infinity, f'x_nuke_{t}') for t in range(T)]

    # Objective: Minimize the total capital cost
    objective = solver.Objective()
    for t in range(T):
        objective.SetCoefficient(x_coal[t], CoalCost)
        objective.SetCoefficient(x_nuke[t], NukeCost)
    objective.SetMinimization()

    # Constraints
    for t in range(T):
        # Compute indices for coal capacity (capacity installed in periods t' that are active in period t)
        coal_start = max(0, t - CoalLife + 1)
        nuke_start = max(0, t - NukeLife + 1)

        capacity_expr = solver.Sum([x_coal[i] for i in range(coal_start, t + 1)])
        capacity_expr += solver.Sum([x_nuke[i] for i in range(nuke_start, t + 1)])
        # Add existing oil capacity
        capacity_expr += OilCap[t]

        # Demand satisfaction constraint
        solver.Add(capacity_expr >= Demand[t])

        # Nuclear capacity limit constraint: active nuclear capacity does not exceed MaxNuke
        nuke_expr = solver.Sum([x_nuke[i] for i in range(nuke_start, t + 1)])
        solver.Add(nuke_expr <= MaxNuke)

    # Solve the problem
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print('Optimal solution found:')
        print(f'Objective Value = {solver.Objective().Value()}')
        for t in range(T):
            print(f'Year {t+1}: Coal Added = {x_coal[t].solution_value()}, Nuclear Added = {x_nuke[t].solution_value()}')
    elif status == pywraplp.Solver.FEASIBLE:
        print('A feasible solution was found, but it may not be optimal.')
    else:
        print('No solution could be found.')

if __name__ == '__main__':
    main()