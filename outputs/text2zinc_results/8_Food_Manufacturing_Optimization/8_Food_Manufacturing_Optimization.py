# Mathematical Formulation:
'''\begin{align*}
\textbf{Sets and Indices:}\quad & m = 1,\ldots, M,\quad i = 1,\ldots, I. \\[1mm]
\textbf{Parameters:}\quad &
\begin{array}{rcl}
\text{BuyPrice}_{m,i}     &:& \text{Purchase cost per ton of oil } i \text{ in month } m,\\[1mm]
\text{SellPrice}          &:& \text{Fixed selling price per ton of final product},\\[1mm]
\text{IsVegetable}_{i}    &:& \begin{cases}
1, & \text{if oil } i \text{ is a vegetable oil},\\[1mm]
0, & \text{if oil } i \text{ is a non‐vegetable oil},
\end{cases}\\[1mm]
\text{MaxVegRefine}       &:& \text{Maximum total tons of vegetable oil that can}\\[0.5mm]
                        & & \quad \text{be refined in any month},\\[1mm]
\text{MaxNonVegRefine}    &:& \text{Maximum total tons of non–vegetable oil that can}\\[0.5mm]
                        & & \quad \text{be refined in any month},\\[1mm]
\text{StorageSize}        &:& \text{Maximum total tonnage of raw oil that can be stored in any month},\\[1mm]
\text{StorageCost}        &:& \text{Cost per ton per month for storing raw oil},\\[1mm]
\text{MinHardness}        &:& \text{Minimum hardness allowed for the final product},\\[1mm]
\text{MaxHardness}        &:& \text{Maximum hardness allowed for the final product},\\[1mm]
\text{Hardness}_{i}       &:& \text{Hardness value of raw oil } i, \\[1mm]
\text{InitialAmount}_{i}  &:& \text{Initial inventory (in tons) of raw oil } i.
\end{array} \\[2mm]
\textbf{Decision Variables:}\quad &  
\begin{array}{rcl}
x_{m,i} &\ge& 0,\quad \text{tons of raw oil } i \text{ purchased in month } m,\\[1mm]
r_{m,i} &\ge& 0,\quad \text{tons of raw oil } i \text{ refined in month } m,\\[1mm]
s_{m,i} &\ge& 0,\quad \text{tons of raw oil } i \text{ held in storage at end of month } m.
\end{array} \\[2mm]
\textbf{Objective Function:}\\[0.5mm]
\text{Maximize} \quad Z =\; & \underbrace{\text{SellPrice} \cdot \sum_{m=1}^{M} \sum_{i=1}^{I} r_{m,i}}_{\text{Revenue from final product}} \;-\; \underbrace{\sum_{m=1}^{M} \sum_{i=1}^{I} \text{BuyPrice}_{m,i}\, x_{m,i}}_{\text{Purchasing cost}} \;-\; \underbrace{\text{StorageCost} \cdot \sum_{m=1}^{M} \sum_{i=1}^{I} s_{m,i}}_{\text{Storage cost}}.
\\[2mm]
\textbf{Subject to:}\\[1mm]
\textbf{(1) Inventory Balance (for each } m=1,\ldots,M,\; i=1,\ldots,I\textbf{):} \quad &
s_{m,i} = s_{m-1,i} + x_{m,i} - r_{m,i}, \quad \text{with } s_{0,i} = \text{InitialAmount}_{i}.\\[2mm]
\textbf{(2) Final Storage Requirement (for each } i=1,\ldots,I\textbf{):} \quad & s_{M,i} = \text{InitialAmount}_{i}.\\[2mm]
\textbf{(3) Storage Capacity (for each month } m=1,\ldots,M\textbf{):} \quad &
\sum_{i=1}^{I} s_{m,i} \le \text{StorageSize}.\\[2mm]
\textbf{(4) Refining Capacity for Vegetable Oils (for each month } m=1,\ldots,M\textbf{):} \quad &
\sum_{i=1}^{I} \text{IsVegetable}_{i}\; r_{m,i} \le \text{MaxVegRefine}.\\[2mm]
\textbf{(5) Refining Capacity for Non–Vegetable Oils (for each month } m=1,\ldots,M\textbf{):} \quad &
\sum_{i=1}^{I} \bigl(1-\text{IsVegetable}_{i}\bigr)\; r_{m,i} \le \text{MaxNonVegRefine}.\\[2mm]
\textbf{(6) Hardness Blending Constraint (for each month } m=1,\ldots,M\textbf{):} \quad &
\text{MinHardness} \cdot \sum_{i=1}^{I} r_{m,i} \; \le \; \sum_{i=1}^{I} \text{Hardness}_{i}\, r_{m,i} \; \le \; \text{MaxHardness} \cdot \sum_{i=1}^{I} r_{m,i}.\\[2mm]
\textbf{(7) Nonnegativity:} \quad & x_{m,i} \ge 0,\quad r_{m,i} \ge 0,\quad s_{m,i}\ge 0,\quad \forall \; m=1,\ldots,M,\; i=1,\ldots,I.
\end{align*}

\vspace{2mm}
This formulation fully captures the decisions of purchasing raw oils, storing them under a capacity limit (with associated holding costs), and refining them subject to separate monthly capacity limits for vegetable and non–vegetable oils. The refined oils are blended to produce the final product subject to a weighted–average hardness requirement while ensuring that the initial storage levels are exactly reproduced at the end of the planning horizon. The objective is to maximize the net profit defined as revenue minus purchasing and storage costs. This model is both feasible (with appropriate parameter values) and bounded.'''

# Generated Code:
#!/usr/bin/env python3
"""
This script implements the manufacturing and production optimization problem
using Google's OR-Tools linear_solver (GLOP). It determines the optimal policy 
for purchasing, storage, and refining of raw oils over a planning horizon.
Note: The provided data had a slight inconsistency between the initial inventory
and the overall storage capacity. Here we assume that the total initial inventory 
of 500 is split equally among the 5 oils (i.e. 100 each).
"""

from ortools.linear_solver import pywraplp

def main():
    # Data
    M = 6  # number of months
    I = 5  # number of oils
    
    # BuyPrice[m][i] for m=0..5, i=0..4 (converted from 1-indexed data)
    buy_price = [
        [110, 120, 130, 110, 115],  # Month 1
        [130, 130, 110, 90, 115],   # Month 2
        [110, 140, 130, 100, 95],   # Month 3
        [120, 110, 120, 120, 125],  # Month 4
        [100, 120, 150, 110, 105],  # Month 5
        [90, 100, 140, 80, 135]     # Month 6
    ]
    
    sell_price = 150
    # IsVegetable: 1 if vegetable, 0 otherwise.
    is_vegetable = [1, 1, 0, 0, 0]
    max_veg_refine = 200
    max_nonveg_refine = 250
    storage_capacity = 1000
    storage_cost = 5
    min_hardness = 3
    max_hardness = 6
    hardness = [8.8, 6.1, 2.0, 4.2, 5.0]
    # Adjusted initial amount per oil: total of 500 equally divided among 5 oils.
    initial_amount = [100, 100, 100, 100, 100]
    
    # Create the linear solver with the GLOP backend.
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Solver not created.")
        return

    infinity = solver.infinity()
    
    # Decision variables
    # x[m][i]: tons purchased of oil i in month m.
    # r[m][i]: tons refined of oil i in month m.
    # s[m][i]: tons in storage of oil i at end of month m.
    x = [[solver.NumVar(0, infinity, f'x_{m}_{i}') for i in range(I)] for m in range(M)]
    r = [[solver.NumVar(0, infinity, f'r_{m}_{i}') for i in range(I)] for m in range(M)]
    s = [[solver.NumVar(0, infinity, f's_{m}_{i}') for i in range(I)] for m in range(M)]
    
    # Constraints
    # (1) Inventory Balance: For each month and oil.
    for m in range(M):
        for i in range(I):
            if m == 0:
                # s[0][i] = initial_amount[i] + x[0][i] - r[0][i]
                solver.Add(s[0][i] == initial_amount[i] + x[0][i] - r[0][i])
            else:
                # s[m][i] = s[m-1][i] + x[m][i] - r[m][i]
                solver.Add(s[m][i] == s[m-1][i] + x[m][i] - r[m][i])
    
    # (2) Final Storage Requirement: for each oil type, final storage equals initial.
    for i in range(I):
        solver.Add(s[M-1][i] == initial_amount[i])
    
    # (3) Storage Capacity: sum of storage for all oils in each month <= storage_capacity.
    for m in range(M):
        solver.Add(sum(s[m][i] for i in range(I)) <= storage_capacity)
    
    # (4) Refining Capacity for Vegetable Oils.
    for m in range(M):
        solver.Add(sum(is_vegetable[i] * r[m][i] for i in range(I)) <= max_veg_refine)
    
    # (5) Refining Capacity for Non-Vegetable Oils.
    for m in range(M):
        solver.Add(sum((1 - is_vegetable[i]) * r[m][i] for i in range(I)) <= max_nonveg_refine)
    
    # (6) Hardness Blending Constraint.
    for m in range(M):
        total_refined = sum(r[m][i] for i in range(I))
        weighted_hardness = sum(hardness[i] * r[m][i] for i in range(I))
        solver.Add(weighted_hardness >= min_hardness * total_refined)
        solver.Add(weighted_hardness <= max_hardness * total_refined)
    
    # Objective Function:
    # Maximize: sell_price * total refined - sum(buy_price * purchase) - storage_cost * total_storage
    revenue = sell_price * solver.Sum(r[m][i] for m in range(M) for i in range(I))
    purchase_cost = solver.Sum(buy_price[m][i] * x[m][i] for m in range(M) for i in range(I))
    storage_cost_total = storage_cost * solver.Sum(s[m][i] for m in range(M) for i in range(I))
    
    solver.Maximize(revenue - purchase_cost - storage_cost_total)
    
    # Solve
    status = solver.Solve()
    
    if status == pywraplp.Solver.OPTIMAL:
        print("Optimal solution found!")
        print("Optimal objective value: ", solver.Objective().Value())
        print("")
        for m in range(M):
            print(f"Month {m+1}:")
            for i in range(I):
                print(f"  Oil {i+1}: Purchase = {x[m][i].solution_value():.2f}, Refine = {r[m][i].solution_value():.2f}, Storage = {s[m][i].solution_value():.2f}")
            print("")
    elif status == pywraplp.Solver.FEASIBLE:
        print("A feasible solution was found, but it may not be optimal.")
    else:
        print("The problem does not have an optimal solution.")

if __name__ == '__main__':
    main()