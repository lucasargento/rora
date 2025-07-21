# Mathematical Formulation:
'''\begin{align*}
\textbf{Indices and Parameters:}\\[1mm]
& i,j \in \{1,\ldots, n\},\quad i < j, \quad \text{with } n = n_{\text{containers}},\\[1mm]
& k \in \{1,\ldots, n\} \quad \text{(container index)};\\[1mm]
& \text{Let } w_i \text{ and } \ell_i \text{ denote the width and length of container } i,\\[1mm]
& c_i \in \{1,\ldots,n_{\text{classes}}\} \quad \text{be the given class of container } i,\\[1mm]
& \delta_{rs} \ge 0 \quad \text{be the minimum separation required between a container of class } r \text{ and one of class } s\quad (r,s = 1,\ldots,n_{\text{classes}}).\\[1mm]
& \text{Deck dimensions: } W = \text{deck\_width}, \quad L = \text{deck\_length}.\\[3mm]
\textbf{Decision Variables:}\\[1mm]
& x_i \in \mathbb{R} \quad \text{for } i=1,\ldots,n,\quad \text{the } x\text{-coordinate of the bottom‐left corner of container } i,\\[1mm]
& y_i \in \mathbb{R} \quad \text{for } i=1,\ldots,n,\quad \text{the } y\text{-coordinate of the bottom‐left corner of container } i,\\[1mm]
& \delta_{ij}^k \in \{0,1\} \quad\text{for each } i,j\ (i<j) \text{ and } k\in\{1,2,3,4\},\\[1mm]
& \quad\text{where:} \\
& \quad \delta_{ij}^1 = 1 \Longrightarrow \text{container } i \text{ is completely to the left of container } j,\\[1mm]
& \quad \delta_{ij}^2 = 1 \Longrightarrow \text{container } j \text{ is completely to the left of container } i,\\[1mm]
& \quad \delta_{ij}^3 = 1 \Longrightarrow \text{container } i \text{ is completely below container } j,\\[1mm]
& \quad \delta_{ij}^4 = 1 \Longrightarrow \text{container } j \text{ is completely below container } i.\\[2mm]
& \sigma_{ij}^k \in \{0,1\} \quad\text{for each } i,j\ (i<j) \text{ and } k\in\{1,2,3,4\},\\[1mm]
& \quad\text{where:} \\
& \quad \sigma_{ij}^1 = 1 \Longrightarrow \text{horizontally, container } i \text{ (with separation gap) is to the left of } j,\\[1mm]
& \quad \sigma_{ij}^2 = 1 \Longrightarrow \text{horizontally, container } j \text{ (with separation gap) is to the left of } i,\\[1mm]
& \quad \sigma_{ij}^3 = 1 \Longrightarrow \text{vertically, container } i \text{ (with separation gap) is below } j,\\[1mm]
& \quad \sigma_{ij}^4 = 1 \Longrightarrow \text{vertically, container } j \text{ (with separation gap) is below } i.\\[3mm]
\textbf{Objective Function:}\\[1mm]
& \text{Since the problem is feasibility (``can the layout be done?''), we set:}\\[1mm]
& \min \; 0.\\[3mm]
\textbf{Constraints:}\\[1mm]
\textbf{(1) Container Placement within the Deck:}\\[1mm]
& 0 \le x_i \le W - w_i,\quad \forall\, i=1,\ldots,n,\\[1mm]
& 0 \le y_i \le L - \ell_i,\quad \forall\, i=1,\ldots,n.\\[3mm]
\textbf{(2) Non‐overlap Constraints:}\\[1mm]
& \text{For every pair } i < j,\text{ at least one of the following must hold:}\\[1mm]
& x_i + w_i \le x_j + M (1-\delta_{ij}^1),\\[1mm]
& x_j + w_j \le x_i + M (1-\delta_{ij}^2),\\[1mm]
& y_i + \ell_i \le y_j + M (1-\delta_{ij}^3),\\[1mm]
& y_j + \ell_j \le y_i + M (1-\delta_{ij}^4),\\[1mm]
& \delta_{ij}^1 + \delta_{ij}^2 + \delta_{ij}^3 + \delta_{ij}^4 \ge 1,\quad \forall\, i<j,\\[1mm]
& \text{where } M \text{ is a sufficiently large constant (e.g. } M\ge \max\{W,L\}\text{)}.\\[3mm]
\textbf{(3) Separation Constraints:}\\[1mm]
& \text{For every pair } i < j,\text{ let } d_{ij} = \delta_{\,c_i,c_j} \text{ be the specified separation gap}\\[1mm]
& \quad \text{between containers of classes } c_i \text{ and } c_j.\\[1mm]
& \text{If } d_{ij}>0 \text{ (i.e. separation is required), then enforce:}\\[1mm]
& x_i + w_i + d_{ij} \le x_j + M(1-\sigma_{ij}^1),\\[1mm]
& x_j + w_j + d_{ij} \le x_i + M(1-\sigma_{ij}^2),\\[1mm]
& y_i + \ell_i + d_{ij} \le y_j + M(1-\sigma_{ij}^3),\\[1mm]
& y_j + \ell_j + d_{ij} \le y_i + M(1-\sigma_{ij}^4),\\[1mm]
& \sigma_{ij}^1 + \sigma_{ij}^2 + \sigma_{ij}^3 + \sigma_{ij}^4 \ge 1,\quad \forall\, i<j \text{ with } d_{ij}>0.\\[3mm]
\textbf{(4) Integrality and Binary Domain:}\\[1mm]
& \delta_{ij}^k \in \{0,1\}, \quad \sigma_{ij}^k \in \{0,1\},\quad \forall\, i<j,\; k=1,2,3,4.
\end{align*}

\textbf{Notes:}
1. The binary variables $\delta_{ij}^k$ enforce that containers do not overlap; one of the four spatial disjunctive conditions must hold for each pair $(i,j)$.
2. The binary variables $\sigma_{ij}^k$ enforce the additional separation requirement (if any) for containers belonging to classes that require a minimum gap.
3. The constant $M$ (big‐M) must be chosen large enough compared to the deck dimensions so that the constraints are not restrictive when the corresponding binary variable is 0.
4. This model is a full formulation of the container placement problem as a feasibility/mixed‐integer programming problem, with a dummy objective function (minimize 0) to capture the decision problem.

This formulation is self-contained and can be used as a basis for implementing an OR-Tools model or any mixed–integer programming solver.'''

# Generated Code:
#!/usr/bin/env python3
from ortools.sat.python import cp_model


def main():
    # Data
    deck_width = 5
    deck_length = 5
    n_containers = 3
    n_classes = 2

    # For each container index i, the container dimensions and its class.
    # Here container dimensions are given explicitly per container.
    container_widths = [5, 2, 3]
    container_lengths = [1, 4, 4]
    container_classes = [1, 1, 1]  # Classes are 1-indexed

    # Separation matrix for classes (2x2 matrix)
    # separation[r][s] is the minimum gap required between a container of class r+1 and class s+1.
    separation = [
        [0, 0],
        [0, 0]
    ]

    # Big constant for disjunctive constraints.
    # We choose M to be big enough compared to deck dimensions and container sizes.
    M = max(deck_width, deck_length) + max(max(container_widths), max(container_lengths))

    model = cp_model.CpModel()

    # Decision variables: x and y coordinates for bottom-left corner of each container.
    xs = []
    ys = []
    for i in range(n_containers):
        # Ensure the container is placed fully inside the deck.
        x_var = model.NewIntVar(0, deck_width - container_widths[i], f'x_{i}')
        y_var = model.NewIntVar(0, deck_length - container_lengths[i], f'y_{i}')
        xs.append(x_var)
        ys.append(y_var)

    # Binary variables for non-overlap disjunctions.
    # For each pair (i, j) with i < j, we create four binary variables:
    # delta[(i, j, 1)]: container i is to the left of container j.
    # delta[(i, j, 2)]: container j is to the left of container i.
    # delta[(i, j, 3)]: container i is below container j.
    # delta[(i, j, 4)]: container j is below container i.
    delta = {}
    pairs = []
    for i in range(n_containers):
        for j in range(i + 1, n_containers):
            pairs.append((i, j))
            for k in range(1, 5):
                delta[(i, j, k)] = model.NewBoolVar(f'delta_{i}_{j}_{k}')

    # Non-overlap constraints for every pair of containers.
    for i, j in pairs:
        # At least one disjunct must be true.
        model.Add(delta[(i, j, 1)] +
                  delta[(i, j, 2)] +
                  delta[(i, j, 3)] +
                  delta[(i, j, 4)] >= 1)

        # If container i is to the left of container j.
        model.Add(xs[i] + container_widths[i] <= xs[j] + M * (1 - delta[(i, j, 1)]))
        # If container j is to the left of container i.
        model.Add(xs[j] + container_widths[j] <= xs[i] + M * (1 - delta[(i, j, 2)]))
        # If container i is below container j.
        model.Add(ys[i] + container_lengths[i] <= ys[j] + M * (1 - delta[(i, j, 3)]))
        # If container j is below container i.
        model.Add(ys[j] + container_lengths[j] <= ys[i] + M * (1 - delta[(i, j, 4)]))

    # Separation constraints.
    # For every pair (i, j) for which a separation gap is required (> 0) between their classes.
    sigma = {}
    for i, j in pairs:
        # Get the required separation distance based on container classes.
        # Note: container_classes are 1-indexed so adjust index by subtracting 1.
        sep_val = separation[container_classes[i] - 1][container_classes[j] - 1]
        if sep_val > 0:
            # Create four separation binary variables similar to delta.
            sigma[(i, j, 1)] = model.NewBoolVar(f'sigma_{i}_{j}_1')
            sigma[(i, j, 2)] = model.NewBoolVar(f'sigma_{i}_{j}_2')
            sigma[(i, j, 3)] = model.NewBoolVar(f'sigma_{i}_{j}_3')
            sigma[(i, j, 4)] = model.NewBoolVar(f'sigma_{i}_{j}_4')
            # At least one separation disjunct must hold.
            model.Add(sigma[(i, j, 1)] +
                      sigma[(i, j, 2)] +
                      sigma[(i, j, 3)] +
                      sigma[(i, j, 4)] >= 1)
            # Separation for horizontal ordering.
            model.Add(xs[i] + container_widths[i] + sep_val <= xs[j] + M * (1 - sigma[(i, j, 1)]))
            model.Add(xs[j] + container_widths[j] + sep_val <= xs[i] + M * (1 - sigma[(i, j, 2)]))
            # Separation for vertical ordering.
            model.Add(ys[i] + container_lengths[i] + sep_val <= ys[j] + M * (1 - sigma[(i, j, 3)]))
            model.Add(ys[j] + container_lengths[j] + sep_val <= ys[i] + M * (1 - sigma[(i, j, 4)]))
        # For sep_val == 0, no extra constraints are needed.

    # Objective: Feasibility problem so we define a dummy objective (minimize 0).
    model.Minimize(0)

    # Solve the model.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status in {cp_model.OPTIMAL, cp_model.FEASIBLE}:
        print('Solution Found:')
        for i in range(n_containers):
            x_val = solver.Value(xs[i])
            y_val = solver.Value(ys[i])
            print(f'Container {i}: x = {x_val}, y = {y_val}, width = {container_widths[i]}, length = {container_lengths[i]}, class = {container_classes[i]}')
        print(f'Objective value: {solver.ObjectiveValue()}')
    else:
        print('No solution found.')


if __name__ == '__main__':
    main()