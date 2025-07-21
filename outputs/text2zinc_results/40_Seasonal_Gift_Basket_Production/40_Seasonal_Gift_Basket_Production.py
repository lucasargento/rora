# Mathematical Formulation:
'''\[
\begin{array}{rcl}
\textbf{Parameters:} & & \\
W &:& \text{Number of weeks (}W=4\text{)}\\[1mm]
\text{RegularCost} &:& \text{Cost per regular labor hour (}30\text{)}\\[1mm]
\text{OvertimeCost} &:& \text{Cost per overtime labor hour (}45\text{)}\\[1mm]
\text{AssemblyTime} &:& \text{Time (hours) required to assemble one basket (}0.4\text{)}\\[1mm]
\text{MaterialCost} &:& \text{Material cost per basket (}25\text{)}\\[1mm]
\text{SellingPrice} &:& \text{Selling price per basket (}65\text{)}\\[1mm]
\text{HoldingCost} &:& \text{Holding cost per basket per week (}4\text{)}\\[1mm]
\text{SalvageValue} &:& \text{Salvage value per unsold basket at season end (}30\text{)}\\[1mm]
\text{Demand}_w &:& \text{Demand in week }w,\quad \text{for }w=1,\ldots,W,\quad\text{with } \text{Demand}=[700,\,1500,\,2800,\,1800]\\[1mm]
\text{RegularLabor}_w &:& \text{Available regular labor hours in week }w,\quad \text{with } \text{RegularLabor}=[450,\,550,\,600,\,600]\\[1mm]
\text{OvertimeLabor}_w &:& \text{Available overtime labor hours in week }w,\quad \text{with } \text{OvertimeLabor}=[40,\,200,\,320,\,160]\\[3mm]
\textbf{Decision Variables:} & & \\
R_w &\ge & 0,\quad \text{regular labor hours used in week }w,\quad  w=1,\ldots,W,\\[2mm]
O_w &\ge & 0,\quad \text{overtime labor hours used in week }w,\quad  w=1,\ldots,W,\\[2mm]
x_w &\ge & 0,\quad \text{number of baskets produced in week }w,\quad  w=1,\ldots,W,\\[2mm]
I_w &\ge & 0,\quad \text{inventory (unsold baskets) at end of week }w,\quad  w=1,\ldots,W.
\end{array}
\]

The production process is assumed to use labor hours as follows: since each basket requires a fixed assembly time, the total number of baskets produced in week \(w\) is determined by the available labor hours:
\[
x_w = \frac{R_w + O_w}{\text{AssemblyTime}},\quad w=1,\ldots,W.
\]

The company must also satisfy the weekly demand. With no starting inventory, the balance equation over the weeks is:
\[
I_0 = 0,\quad I_w = I_{w-1} + x_w - \text{Demand}_w,\quad w=1,\ldots,W.
\]

The objective is to maximize the total profit over the season. The profit consists of:
– Revenue from selling baskets, where every week the full demand is met (i.e. revenue is \(\text{SellingPrice} \times \text{Demand}_w\));  
– A salvage value for unsold inventory held at the end of week \(W\) (i.e. \( \text{SalvageValue} \times I_W\));  
– Costs that include material costs for each basket produced, labor costs (regular and overtime), and holding costs for baskets carried as inventory from one week to the next (no holding cost is incurred in the final week because unsold baskets are salvaged).

The complete optimization model is formulated as follows:

\[
\begin{align*}
\textbf{Maximize} \quad & Z = \underbrace{\sum_{w=1}^W \text{SellingPrice}\cdot \text{Demand}_w + \text{SalvageValue}\cdot I_W}_\text{Total Revenue} 
- \underbrace{\sum_{w=1}^W \Big( \text{MaterialCost}\cdot x_w + \text{RegularCost}\cdot R_w + \text{OvertimeCost}\cdot O_w \Big)
- \sum_{w=1}^{W-1} \text{HoldingCost}\cdot I_w}_{\text{Total Costs}} \\[2mm]
\textbf{subject to} \quad 
& I_0 = 0, \\[2mm]
& I_w = I_{w-1} + x_w - \text{Demand}_w,\quad && w = 1,\ldots,W, \\[2mm]
& x_w \cdot \text{AssemblyTime} = R_w + O_w,\quad && w = 1,\ldots,W, \\[2mm]
& 0 \leq R_w \leq \text{RegularLabor}_w,\quad && w = 1,\ldots,W, \\[2mm]
& 0 \leq O_w \leq \text{OvertimeLabor}_w,\quad && w = 1,\ldots,W, \\[2mm]
& x_w \geq 0,\quad I_w \geq 0,\quad && w = 1,\ldots,W.
\end{align*}
\]

Notes:
1. The revenue component \(\sum_{w=1}^W \text{SellingPrice}\cdot \text{Demand}_w\) is fixed (since demand must be met each week), so this model can also be viewed as minimizing total costs, but it is formulated here as a profit maximization problem.
2. The inventory balance ensures that any basket produced that exceeds the current week’s demand is carried over with an associated holding cost (except in the final week where a salvage value is received).
3. The labor constraint \( x_w \cdot \text{AssemblyTime} = R_w + O_w \) ties production directly to the labor hours utilized.
4. All variables and constraints are defined for each week \(w=1,\ldots,W\) ensuring the feasibility and boundedness of the problem.

This model fully represents the fine foods company’s production planning over the season in a rigorous formal mathematical optimization formulation.'''

# Generated Code:
from ortools.linear_solver import pywraplp

def main():
    # Problem Data
    W = 4
    RegularCost = 30
    OvertimeCost = 45
    AssemblyTime = 0.4
    MaterialCost = 25
    SellingPrice = 65
    HoldingCost = 4
    SalvageValue = 30
    Demand = [700, 1500, 2800, 1800]
    RegularLabor = [450, 550, 600, 600]
    OvertimeLabor = [40, 200, 320, 160]

    # Create the linear solver using the GLOP solver.
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Solver not created.")
        return

    infinity = solver.infinity()

    # Decision Variables: For each week 0,...,W-1
    R = [solver.NumVar(0, RegularLabor[w], f'R_{w}') for w in range(W)]
    O = [solver.NumVar(0, OvertimeLabor[w], f'O_{w}') for w in range(W)]
    x = [solver.NumVar(0, infinity, f'x_{w}') for w in range(W)]
    I = [solver.NumVar(0, infinity, f'I_{w}') for w in range(W)]

    # Inventory initial condition: I_0 = x_0 - Demand_0
    # But we use a recurrence: I_0 = 0 + x_0 - Demand[0]
    solver.Add(I[0] == x[0] - Demand[0])
    # For subsequent weeks: I[w] = I[w-1] + x[w] - Demand[w]
    for w in range(1, W):
        solver.Add(I[w] == I[w-1] + x[w] - Demand[w])

    # Production process: x[w] = (R[w] + O[w]) / AssemblyTime
    for w in range(W):
        solver.Add((R[w] + O[w]) == AssemblyTime * x[w])

    # Objective: maximize total profit
    # Total Revenue: SellingPrice*Demand[w] each week is fixed plus SalvageValue*I_W at the end of last week.
    # Total Cost: MaterialCost*x[w] + RegularCost*R[w] + OvertimeCost*O[w] for each week and HoldingCost * I[w] for weeks 0 to W-2.
    # Since the revenue for baskets sold is fixed (Demand is control), we include it in the objective.
    revenue = solver.Sum([SellingPrice * d for d in Demand]) + SalvageValue * I[W-1]
    production_cost = solver.Sum([MaterialCost * x[w] + RegularCost * R[w] + OvertimeCost * O[w] for w in range(W)])
    holding_cost = solver.Sum([HoldingCost * I[w] for w in range(W - 1)])
    
    profit = revenue - production_cost - holding_cost
    solver.Maximize(profit)

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print("Solution:")
        print("Optimal Profit =", solver.Objective().Value())
        for w in range(W):
            print(f"Week {w+1}:")
            print(f"  Regular Hours (R_{w+1}) = {R[w].solution_value()}")
            print(f"  Overtime Hours (O_{w+1}) = {O[w].solution_value()}")
            print(f"  Baskets Produced (x_{w+1}) = {x[w].solution_value()}")
            print(f"  Inventory (I_{w+1}) = {I[w].solution_value()}")
    else:
        print("The problem does not have an optimal solution.")

if __name__ == '__main__':
    main()