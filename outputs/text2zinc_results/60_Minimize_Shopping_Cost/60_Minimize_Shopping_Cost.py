# Mathematical Formulation:
'''\begin{align*}
\textbf{Indices:} \quad & p \in \{1,2,\ldots, P\}, \quad s \in \{1,2,\ldots, S\}, \quad \text{with } P = \texttt{num\_parts}, \; S = \texttt{num\_stores}. \\[1mm]

\textbf{Parameters:} \quad & c_s \coloneqq \texttt{store\_delivery\_costs}[s] \quad \forall s \in S, \\
& p_{ps} \coloneqq \texttt{product\_stores}[p,s] \quad \forall p \in \{1,\dots,P\}, \; s \in \{1,\dots,S\}. \\[1mm]

\textbf{Decision Variables:} \quad & x_{ps} \in \{0,1\} \quad \forall p \in \{1,\dots,P\}, \; s \in \{1,\dots,S\}, \\
& \quad\text{where } x_{ps} = \begin{cases} 1, & \text{if part } p \text{ is bought from store } s, \\[0.5mm] 0, & \text{otherwise.} \end{cases} \\[1mm]
& y_s \in \{0,1\} \quad \forall s \in \{1,\dots,S\}, \\
& \quad\text{where } y_s = \begin{cases} 1, & \text{if at least one part is purchased from store } s, \\[0.5mm] 0, & \text{otherwise.} \end{cases} \\[1mm]

\textbf{Objective Function:} \quad & \text{Minimize } Z, \text{ where} \\
& Z = \sum_{s=1}^{S} c_s\, y_s + \sum_{p=1}^{P} \sum_{s=1}^{S} p_{ps}\, x_{ps}. \\[1mm]

\textbf{Constraints:} \\[1mm]
1.\quad & \text{Each part must be purchased from exactly one store:} \\
& \sum_{s=1}^{S} x_{ps} = 1 \quad \forall\, p = 1,\dots,P. \\[1mm]
2.\quad & \text{Linking store usage with part purchases:} \\
& x_{ps} \leq y_s \quad \forall\, p = 1,\dots,P, \; \forall\, s = 1,\dots,S. \\[1mm]
3.\quad & \text{Non-availability conditions: If a part is not available at a store,} \\
& \quad \text{then it cannot be purchased there. That is, } \\
& \text{if } p_{ps} = 0 \text{ then } x_{ps} = 0, \quad \forall\, p = 1,\dots,P, \; \forall\, s = 1,\dots,S. 
\end{align*}

\noindent This model is a Binary Integer Programming formulation where the objective is to minimize the total cost comprising both the purchase costs of the parts and the fixed delivery costs incurred whenever one or more parts are ordered from a store. The constraints ensure that each part is purchased exactly once, that the delivery cost for a store is only applied if at least one part is bought there, and that parts are only purchased from stores where they are available (i.e., where the price is nonzero).'''

# Generated Code:
from ortools.sat.python import cp_model


def main():
    # Data
    num_parts = 3
    num_stores = 3
    product_stores = [
        [0.0, 2.25, 2.9],
        [0.0, 3.00, 0.0],
        [2.0, 15.00, 7.0],
    ]
    store_delivery_costs = [12.56, 15.2, 33.5]

    # Create the CP-SAT model.
    model = cp_model.CpModel()

    # Decision variables: x[p][s] = 1 if part p is bought from store s
    x = {}
    for p in range(num_parts):
        for s in range(num_stores):
            # Only define variable if product is available (price > 0.0)
            if product_stores[p][s] > 0.0:
                x[p, s] = model.NewBoolVar(f"x_{p}_{s}")
            else:
                # For non available parts, set variable to 0
                x[p, s] = model.NewConstant(0)

    # Decision variables: y[s] = 1 if at least one part is purchased from store s.
    y = {}
    for s in range(num_stores):
        y[s] = model.NewBoolVar(f"y_{s}")

    # Constraint 1: Each part must be purchased from exactly one store.
    for p in range(num_parts):
        # Sum over available stores for part p should equal 1.
        model.Add(sum(x[p, s] for s in range(num_stores)) == 1)

    # Constraint 2: Linking store usage and part purchases.
    for p in range(num_parts):
        for s in range(num_stores):
            model.Add(x[p, s] <= y[s])

    # Objective: Minimize total cost = sum(store_delivery_costs[s]*y[s]) + sum(product_stores[p][s]*x[p,s])
    # Multiply floats by a factor to avoid floating issues.
    scale = 100  # scale factor to convert float to integer costs
    objective_terms = []

    # Delivery cost terms
    for s in range(num_stores):
        cost = int(store_delivery_costs[s] * scale)
        objective_terms.append(cost * y[s])
    # Product cost terms
    for p in range(num_parts):
        for s in range(num_stores):
            price = product_stores[p][s]
            if price > 0.0:
                cost = int(price * scale)
                objective_terms.append(cost * x[p, s])
    model.Minimize(sum(objective_terms))

    # Solve the model.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    # Process results
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        print("Solution:")
        # Convert back the scaled objective value to original scale.
        total_cost = solver.ObjectiveValue() / scale
        print("Total cost =", total_cost)
        for p in range(num_parts):
            for s in range(num_stores):
                if solver.Value(x[p, s]) == 1:
                    print(f"Part {p+1} is purchased from Store {s+1} at price {product_stores[p][s]}")
    else:
        print("No feasible solution found.")


if __name__ == '__main__':
    main()