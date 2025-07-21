# Mathematical Formulation:
'''\[
\begin{array}{rcl}
\textbf{Parameters:} \\[1mm]
n &\in& \mathbb{Z}_{>0} \quad \text{(total number of currencies)} \\[1mm]
m &\in& \mathbb{Z}_{>0} \quad \text{(number of exchange operations performed in the arbitrage loop)} \\[1mm]
S &\in& \mathbb{R}_{>0} \quad \text{(initial amount in the base currency)} \\[1mm]
r_{ij} &\in& \mathbb{R}_{>0} \quad \forall\, i,j\in\{1,\dots,n\} \quad \text{(exchange rate from currency }i\text{ to currency }j\text{)} \\[1mm]
i_0 &\in& \{1,\dots,n\} \quad \text{(index of the given base currency)} \\[2mm]
\textbf{Decision Variables:} \\[1mm]
\sigma_k &\in& \{1,\dots,n\}, \quad k=0,1,\dots,m \\[1mm]
&& \text{where } \sigma_k \text{ denotes the index of the currency chosen at position } k \text{ in the sequence.} \\[1mm]
&& \text{In particular, } \sigma_0 \text{ is fixed to } i_0 \text{ (the base currency) and the cycle closes with } \sigma_m = \sigma_0. \\[2mm]
\textbf{Product Yield:} \\[1mm]
Y(\sigma) &=& \prod_{k=0}^{m-1} r_{\sigma_k\,\sigma_{k+1}}. \\[2mm]
\textbf{Objective Function:} \\[1mm]
\text{Maximize} \quad P(\sigma) &=& S \cdot Y(\sigma) - S, \\[1mm]
&& \text{which is the net profit (i.e. final amount minus the initial amount)}. \\[2mm]
\textbf{Constraints:} \\[1mm]
\text{(1)} \quad & \sigma_0 &=& i_0, \\[1mm]
\text{(2)} \quad & \sigma_m &=& \sigma_0, \\[1mm]
\text{(3)} \quad & \sigma_k \neq \sigma_j, \quad & \forall\, 0 \le k < j \le m-1, \\
&&& \text{(all intermediate currencies must be distinct)} \\[1mm]
\text{(4)} \quad & S\cdot Y(\sigma) &\ge& S, \quad \text{or equivalently} \quad Y(\sigma)\ge 1, \\[1mm]
&&& \text{(to ensure that the cycle constitutes an arbitrage, i.e. the conversion returns at least the amount started with)}.
\end{array}
\]

A few remarks:
• The decision vector \(\sigma = (\sigma_0,\sigma_1,\dots,\sigma_m)\) represents the arbitrage loop, where the loop starts at the base currency (given by \(\sigma_0=i_0\)) and must return to it (\(\sigma_m=\sigma_0\)).  
• The product \(Y(\sigma) = \prod_{k=0}^{m-1} r_{\sigma_k\,\sigma_{k+1}}\) expresses the multiplicative effect of successive currency exchanges.  
• The objective is to maximize the net profit \(P(\sigma)=S\cdot\big(Y(\sigma)-1\big)\).  
• The constraint (3) enforces that, except for the closing return to the base currency, all currencies in the loop are distinct so that trivial self-loop repetitions are disallowed.  
• Constraint (4) guarantees feasibility in the sense that only cycles with non‐negative net gain (or arbitrage) are considered.

This complete mathematical formulation accurately captures the given finance and investment arbitrage problem without any simplifications.'''

# Generated Code:
#!/usr/bin/env python3
import math
from ortools.sat.python import cp_model

def main():
    # Data
    n = 6  # total number of currencies
    m = 3  # number of exchange operations (cycle length)
    start_amount = 1000.0
    currencies = [
        [0.00000, 0.23400, 1.72460, 0.80600, 0.18300, 1.92960],  # aud
        [4.27350, 0.00000, 7.44602, 3.44353, 0.78190, 8.24490],  # dkk
        [0.57984, 0.13430, 0.00000, 0.46250, 0.10500, 1.10730],  # eur
        [1.24069, 0.29040, 2.16216, 0.00000, 0.22710, 2.39410],  # nzd
        [5.46448, 1.27894, 9.52381, 4.40335, 0.00000, 10.54000],  # sek
        [0.51824, 0.12129, 0.90310, 0.41769, 0.09488, 0.00000]   # usd
    ]
    currencies_s = ["aud", "dkk", "eur", "nzd", "sek", "usd"]
    
    # Base currency index (fix starting currency); in the provided example, base is "aud" => index 0.
    base_currency = 0

    # Scale factor for approximating logarithms as integers.
    scale = 10**6

    # Precompute cost matrix: cost[i][j] = round(scale * log(r_ij))
    # Note: since we never allow self-loop (i==j) thanks to all-different constraint (except closing),
    # these values might not matter.
    cost_matrix = []
    for i in range(n):
        row = []
        for j in range(n):
            rate = currencies[i][j]
            # Avoid log(0); if rate==0, set a very negative number.
            if rate > 0:
                cost = int(round(scale * math.log(rate)))
            else:
                cost = -10**9  # a very low cost to discourage this transition.
            row.append(cost)
        cost_matrix.append(row)

    # Flatten the cost_matrix for element constraint: index = i*n + j.
    flat_cost = [cost_matrix[i][j] for i in range(n) for j in range(n)]

    # Create CP model.
    model = cp_model.CpModel()

    # Decision variables: sigma[0] .. sigma[m] where sigma[k] in {0,...,n-1}.
    sigma = [model.NewIntVar(0, n - 1, f'sigma_{k}') for k in range(m + 1)]

    # Fix starting currency and closing constraint.
    model.Add(sigma[0] == base_currency)
    model.Add(sigma[m] == sigma[0])

    # All intermediate currencies must be distinct: indices 0..m-1
    model.AddAllDifferent(sigma[:m])

    # Auxiliary variables for the cost (log-sum) on each edge k: sigma[k] -> sigma[k+1].
    edge_cost = []
    for k in range(m):
        # Lower and upper bounds for edge cost: from flat_cost minimum and maximum.
        lb = min(flat_cost)
        ub = max(flat_cost)
        ec = model.NewIntVar(lb, ub, f'edge_cost_{k}')
        edge_cost.append(ec)
        # Compute linear index = sigma[k] * n + sigma[k+1]
        index_expr = model.NewIntVar(0, n * n - 1, f'index_{k}')
        model.Add(index_expr == sigma[k] * n + sigma[k+1])
        # Link the index_expr to the flat_cost array using Element constraint.
        model.AddElement(index_expr, flat_cost, ec)

    # Total log gain (scaled) = sum of edge costs.
    total_cost = model.NewIntVar(sum([min(flat_cost)]*m), sum([max(flat_cost)]*m), 'total_cost')
    model.Add(total_cost == sum(edge_cost))

    # Arbitrage feasibility constraint: product yield must be >= 1  <=> log(yield) >= 0.
    model.Add(total_cost >= 0)

    # Objective: maximize total profit = start_amount * (exp(total_cost/scale) - 1)
    # Since exp is nonlinear, we maximize the total log-sum instead.
    # This is equivalent to maximizing the product Y, because log is monotonic.
    model.Maximize(total_cost)

    # Create a solver and solve.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        # Retrieve the arbitrage loop sequence.
        sequence = [solver.Value(sigma[k]) for k in range(m + 1)]
        # Compute the actual product yield.
        prod = 1.0
        for k in range(m):
            i = sequence[k]
            j = sequence[k+1]
            prod *= currencies[i][j]
        net_profit = start_amount * (prod - 1)
        # Print solution.
        seq_names = [currencies_s[i] for i in sequence]
        print("Arbitrage loop:", seq_names)
        print("Product yield:", prod)
        print("Net profit: {:.6f} in base currency {}".format(net_profit, currencies_s[base_currency]))
        # Also print scaled log-sum value.
        print("Total scaled log-sum:", solver.Value(total_cost))
    else:
        print("No profitable arbitrage loop found.")

if __name__ == '__main__':
    main()