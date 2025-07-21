# Mathematical Formulation:
'''\[
\begin{array}{rcll}
\textbf{Parameters:} \\
S & = & 9, & \text{(slots per template)}\\[1mm]
t & = & 2, & \text{(number of templates)}\\[1mm]
n & = & 7, & \text{(number of design variations)}\\[1mm]
d_j,\; j=1,\dots,n & : & \text{demand for variation } j, & d = [250,\,255,\,260,\,500,\,500,\,800,\,1100]
\\[2mm]
\textbf{Decision Variables:}\\[1mm]
x_{ij} & \in & \mathbb{Z}_{\ge 0}, & \forall\, i=1,\dots,t,\; j=1,\dots,n,\\[1mm]
& & \text{(number of slots on template } i \text{ assigned to variation } j)\\[1mm]
N_i & \in & \mathbb{Z}_{> 0}, & \forall\, i=1,\dots,t,\\[1mm]
& & \text{(number of times template } i \text{ is used in production)}\\[1mm]
p_{ij} & \in & \mathbb{Z}_{\ge 0}, & \forall\, i=1,\dots,t,\; j=1,\dots,n,\\[1mm]
& & \text{(number of copies of product } j \text{ produced using template } i)\\[2mm]
\textbf{Linking:} & &  p_{ij} = x_{ij} \, N_i, & \forall\, i=1,\dots,t,\; j=1,\dots,n.
\\[2mm]
\textbf{Model:} & & & \\
\text{Minimize} \quad & Z = & \displaystyle \sum_{j=1}^{n} \left( \sum_{i=1}^{t} p_{ij} - d_j \right) & \quad \text{(total surplus)}\\[2mm]
\text{subject to} \quad
& \displaystyle \sum_{j=1}^{n} x_{ij} = S, & \forall\, i=1,\dots,t, \\
& p_{ij} = x_{ij} \, N_i, & \forall\, i=1,\dots,t,\; j=1,\dots,n,\\[1mm]
& \displaystyle \sum_{i=1}^{t} p_{ij} \ge d_j, & \forall\, j=1,\dots,n,\\[2mm]
& \displaystyle \sum_{j=1}^{n} 2^{\,n-j}\,\Bigl(x_{ij} - x_{(i+1)j}\Bigr) \le 0, & \forall\, i=1,\dots,t-1,\\[2mm]
& \text{Additional non‐triviality requirements:} & & \text{(the production mix must cover more than one variation)}\\[1mm]
& & & \text{(in particular, the constraints } \sum_{i=1}^{t} p_{ij} \ge d_j \text{ for all } j \text{ ensure no variation is omitted)}\\[2mm]
& x_{ij} \in \mathbb{Z}_{\ge 0}, \; N_i \in \mathbb{Z}_{>0}, \; p_{ij} \in \mathbb{Z}_{\ge 0}, & & \forall\, i=1,\dots,t,\; j=1,\dots,n.
\end{array}
\]

\vspace{2mm}
\textbf{Explanation:}

1. Decision Variables:
 • x₍ᵢⱼ₎ tells how many of the S slots on template i are assigned to design j.
 • Nᵢ indicates how many times template i is produced (i.e. how many mother sheets are run with that template).
 • p₍ᵢⱼ₎ is the production quantity of design j from template i. They satisfy p₍ᵢⱼ₎ = x₍ᵢⱼ₎·Nᵢ.

2. Objective:
 We minimize the total surplus over all variations, where surplus for design j is the total production minus the demand dⱼ.

3. Constraints:
 (a) Each template i must have exactly S slots assigned across all design variations.  
 (b) The linking non‐linear (bilinear) constraints relate the slot assignments with production quantities.
 (c) For each design j, the summed production over templates must meet or exceed the demand dⱼ.
 (d) The lexicographic ordering is enforced by the weighted sum constraints: for every two consecutive templates (i and i+1), the weighted difference is non‐positive. (Here the weights 2^(n–j) guarantee that the vector (x_{i1}, …, x_{in}) is lexicographically not greater than (x_{(i+1)1}, …, x_{(i+1)n)).  
 (e) The inherent demand constraints guarantee that a trivial mix (i.e. producing only one product while neglecting others) is not optimal.

This formulation is self‐contained, reflects every detail of the problem, and is feasible and bounded given the finite template slots and the requirement to cover given demands. '''

# Generated Code:
from ortools.sat.python import cp_model


def main():
    # Problem Data
    S = 9  # number of slots per template
    t = 2  # number of templates
    n = 7  # number of design variations
    d = [250, 255, 260, 500, 500, 800, 1100]  # demands for each design

    model = cp_model.CpModel()

    # Upper bounds for variables (determined heuristically)
    # x[i][j] in [0, S]
    # N[i] should be at least 1, and max production can be set from demand.
    # Worst-case: if a template dedicates only 1 slot to a design, then N can be as high as demand.
    max_N = max(d)  
    # p[i][j] can be at most S*max_N.
    max_production = S * max_N

    # Decision Variables
    x = {}
    N = {}
    p = {}

    for i in range(t):
        for j in range(n):
            x[(i, j)] = model.NewIntVar(0, S, f'x_{i}_{j}')
        N[i] = model.NewIntVar(1, max_N, f'N_{i}')
        for j in range(n):
            p[(i, j)] = model.NewIntVar(0, max_production, f'p_{i}_{j}')

    # Constraint: each template has S slots assigned in total.
    for i in range(t):
        model.Add(sum(x[(i, j)] for j in range(n)) == S)

    # Linking constraints: p[i][j] = x[i][j] * N[i]
    for i in range(t):
        for j in range(n):
            model.AddMultiplicationEquality(p[(i, j)], [x[(i, j)], N[i]])

    # Demand constraints: total production for design j must be >= d[j]
    for j in range(n):
        model.Add(sum(p[(i, j)] for i in range(t)) >= d[j])

    # Lexicographic ordering constraints: for each i=0,...,t-2 compare template i and template i+1.
    # Use weighted differences with weights 2^(n-1-j)
    for i in range(t - 1):
        weights = [2 ** (n - 1 - j) for j in range(n)]
        model.Add(
            sum(weights[j] * (x[(i, j)] - x[(i + 1, j)]) for j in range(n)) <= 0
        )

    # Objective: minimize total surplus = total production (sum p_ij) - total demand (sum d)
    total_production = sum(p[(i, j)] for i in range(t) for j in range(n))
    total_demand = sum(d)
    # Since total_demand is constant we can minimize total_production directly.
    surplus = model.NewIntVar(0, t * n * max_production, 'surplus')
    model.Add(surplus == total_production - total_demand)
    model.Minimize(surplus)

    # Solve the model.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    # Check result and print if found.
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        print("Solution Found:")
        print("Total Surplus: ", solver.Value(surplus))
        for i in range(t):
            print(f"\nTemplate {i + 1}:")
            print("  x (slot assignments): ", [solver.Value(x[(i, j)]) for j in range(n)])
            print("  N (number of uses): ", solver.Value(N[i]))
            p_vals = [solver.Value(p[(i, j)]) for j in range(n)]
            print("  p (production per design): ", p_vals)
        print("\nObjective Value (total surplus) = ", solver.ObjectiveValue())
    else:
        print("No solution found.")


if __name__ == '__main__':
    main()