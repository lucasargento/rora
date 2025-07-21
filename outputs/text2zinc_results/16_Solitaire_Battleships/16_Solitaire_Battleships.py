# Mathematical Formulation:
'''\[
\begin{array}{rcl}
\textbf{Parameters:} & & \\[1mm]
\text{Board dimensions:} & I=\{1,\ldots,12\},\quad J=\{1,\ldots,12\} & \\[1mm]
\text{Maximal ship length:} & L_{\max} = 5, & \\[1mm]
\text{Fleet composition:} & \text{For } \ell=1,\ldots,5,\quad n_\ell = \text{ship}[\ell] \quad \Bigl( n_1=2,\; n_2=0,\; n_3=1,\; n_4=4,\; n_5=4\Bigr) & \\[1mm]
\text{Row totals:} & r_i,\quad i\in I,\quad \text{with } r=(6,2,2,6,1,5,1,4,4,3,4,3) & \\[1mm]
\text{Column totals:} & c_j,\quad j\in J,\quad \text{with } c=(1,7,3,3,7,1,1,4,5,0,9,0) & \\[1mm]
\text{Hints:} & h_{ij},\quad (i,j)\in I\times J, \quad \text{with values } h_{ij}\in\{0,1,\text{unknown}\} & \\[2mm]
\multicolumn{3}{l}{\textbf{Sets for Ship Indexing and Placements:}} \\[1mm]
\text{Let } S & = & \{ s : s \text{ indexes a ship in the fleet} \},\\[1mm]
 & & \text{with associated length } L_s\in\{1,\ldots,5\}\text{. In particular, for each } \ell=1,\ldots,5,\\[1mm]
 &&\;\; \#\{s\in S: L_s=\ell\}= n_\ell.\\[2mm]
\text{For each ship } s\in S, & &\text{define the set of valid placements } P_s: \\[1mm]
P_s & = & \Bigl\{ (i,j,d):\; d\in\{0,1\},\; \begin{array}{l}
\text{if } d=0 \ (\text{horizontal})\text{ then } i\in I,\; j\in\{1,\ldots, 12 - L_s +1\},\\[1mm]
\text{if } d=1 \ (\text{vertical})\text{ then } i\in\{1,\ldots, 12-L_s+1\},\; j\in J
\end{array}\Bigr\}. \\[2mm]
\text{For any } s\in S \text{ and placement } p=(i,j,d)\in P_s, & & \text{define its cell coverage} \\[1mm]
C(s,i,j,d)& = & \begin{cases}
\{ (i, j+k): k=0,\ldots,L_s-1 \}, & \text{if } d=0,\\[1mm]
\{ (i+k, j): k=0,\ldots,L_s-1 \}, & \text{if } d=1.
\end{cases}
\end{array}
\]

\vspace{2mm}
\[
\begin{array}{rcl}
\multicolumn{3}{l}{\textbf{Decision Variables:}}\\[1mm]
y_{s,i,j,d} & \in & \{0,1\}, \quad \forall s\in S,\; \forall (i,j,d) \in P_s,\\[1mm]
& & \quad\text{where } y_{s,i,j,d}=1 \text{ means ship } s \text{ is placed with its “head” at } (i,j) \text{ in orientation } d\\[2mm]
x_{ij} & \in & \{0,1\}, \quad \forall (i,j) \in I\times J,\\[1mm]
& & \quad\text{where } x_{ij}=1 \text{ indicates that cell } (i,j) \text{ is occupied by a ship.}
\end{array}
\]

\vspace{2mm}
\[
\begin{array}{rcl}
\multicolumn{3}{l}{\textbf{Objective Function:}}\\[1mm]
\text{(Feasibility model)} \quad \min \quad & 0.
\end{array}
\]

\vspace{2mm}
\[
\begin{array}{rcl}
\multicolumn{3}{l}{\textbf{Constraints:}}\\[1mm]
\text{(1) Ship Placement:} & & \displaystyle \sum_{(i,j,d)\in P_s} y_{s,i,j,d} = 1 \quad \forall s\in S. \\[2mm]
\text{(2) Define Occupancy:} & & \displaystyle x_{ij} = \sum_{s\in S} \; \sum_{\substack{(i',j',d)\in P_s:\\ (i,j)\in C(s,i',j',d)}} y_{s,i',j',d} \quad \forall (i,j)\in I\times J. \\[2mm]
\text{(3) Row Sum Requirements:} & & \displaystyle \sum_{j=1}^{12} x_{ij} = r_i \quad \forall i\in I. \\[2mm]
\text{(4) Column Sum Requirements:} & & \displaystyle \sum_{i=1}^{12} x_{ij} = c_j \quad \forall j\in J. \\[2mm]
\text{(5) Hint Consistency:} & & \displaystyle x_{ij} = h_{ij} \quad \forall (i,j)\in I\times J \text{ for which } h_{ij}\in\{0,1\}. \\[2mm]
\text{(6) Non–overlap of Ships:} & & \displaystyle x_{ij} \le 1 \quad \forall (i,j)\in I\times J. \\[2mm]
\text{(7) Non–adjacency Between Distinct Ships:} & & \displaystyle \sum_{\substack{s\in S}} \; \sum_{\substack{(i',j',d)\in P_s:\\ p\in C(s,i',j',d)}} y_{s,i',j',d} + \; \sum_{\substack{s'\in S \\ s'\neq s}} \; \sum_{\substack{(i'',j'',d')\in P_{s'}:\\ q\in C(s',i'',j'',d')}} y_{s',i'',j'',d'} \le 1 \\[1mm]
& & \quad \forall (p,q)\in N,\text{ where } N\\[1mm]
& & \quad=\Bigl\{ \bigl( p=(i,j),~ q=(k,\ell) \bigr) \in (I\times J)^2: \; \| (i-k,\,j-\ell)\|_{\infty} = 1\Bigr\} \setminus \Bigl\{ (p,q): p,q \text{ belong to the same ship } \Bigr\}. 
\end{array}
\]

\vspace{1mm}
A more explicit (but equivalent) way to write the non–adjacency constraint is as follows. For every two distinct ships s and s′, and for every pair of valid placements
\[
(i,j,d)\in P_s\quad \text{and}\quad (i',j',d')\in P_{s'},
\]
if the sets of cells covered by the placements, together with their immediate adjacent (buffer) cells, intersect then
\[
y_{s,i,j,d}+ y_{s', i',j',d'} \le 1.
\]
More precisely, define for each placement the “buffer set”
\[
B(s,i,j,d)= \Bigl\{ (k,\ell): (k,\ell)\in C(s,i,j,d) \text{ or } \exists (u,v)\in C(s,i,j,d) \; \text{with} \; \| (k-u,\,\ell-v)\|_{\infty}=1 \Bigr\}.
\]
Then, for every two distinct ships (i.e., for all \( s,s'\in S,\; s\neq s'\)), impose
\[
y_{s,i,j,d}+ y_{s', i',j',d'} \le 1 \quad \forall (i,j,d)\in P_s,\; \forall (i',j',d')\in P_{s'} \text{ such that } B(s,i,j,d)\cap C(s',i',j',d')\neq\varnothing.
\]

\vspace{2mm}
\textbf{Summary:} This formulation introduces binary decision variables 
– the placement variables \(y_{s,i,j,d}\) for each ship \(s\) and valid position–orientation combination, and the cell occupancy variables \(x_{ij}\) – and enforces that
each ship is placed exactly once; the ships’ placements imply the occupancy of board cells; the occupancy sums in each row and column match the given totals; hints are respected; and finally, any two different ships have a “buffer” (non–adjacency) that prevents them from touching—even diagonally. The objective is simply to find a feasible assignment.

This model is bounded (only finitely many binary variables) and guaranteed to be feasible provided that the instance (fleet, hints, row and column sums) has a solution. 
\]

'''

# Generated Code:
from ortools.sat.python import cp_model


def main():
    # Problem data
    height = 12
    width = 12
    maxship = 5
    # Fleet composition: ship lengths from 1 up to maxship.
    # ship[0] corresponds to ships of length 1, ship[1] to length 2, etc.
    ship_numbers = [2, 0, 1, 4, 4]
    # Hints: if a cell is known (0 = water, 1 = ship), use that value.
    # In our instance, -1 indicates unknown.
    hint_input = [
        [ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 ],
        [ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 ],
        [ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 ],
        [ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 ],
        [ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 ],
        [ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 ],
        [ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 ],
        [ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 ],
        [ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 ],
        [ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 ],
        [ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 ],
        [ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 ],
    ]
    rowsum = [6,2,2,6,1,5,1,4,4,3,4,3]
    colsum = [1,7,3,3,7,1,1,4,5,0,9,0]

    # Build list of ships with indices and lengths.
    ships = []
    ship_id = 0
    for length, count in enumerate(ship_numbers, start=1):
        for _ in range(count):
            ships.append({'id': ship_id, 'length': length})
            ship_id += 1

    # Create the model.
    model = cp_model.CpModel()

    # Precompute valid placements for each ship.
    # Each placement defined by (i, j, d, cells, buffer)
    # d = 0 for horizontal, d = 1 for vertical.
    placements = {}  # key: ship id, value: list of placements.
    for s in ships:
        sid = s['id']
        L = s['length']
        placements[sid] = []
        # Horizontal placements.
        for i in range(height):
            for j in range(width - L + 1):
                cells = [(i, j + k) for k in range(L)]
                # Compute buffer: for every cell covered, add all cells in 3x3 block.
                buf = set()
                for (ci, cj) in cells:
                    for di in [-1, 0, 1]:
                        for dj in [-1, 0, 1]:
                            ni = ci + di
                            nj = cj + dj
                            if 0 <= ni < height and 0 <= nj < width:
                                buf.add((ni, nj))
                placements[sid].append({'i': i, 'j': j, 'd': 0, 'cells': cells, 'buffer': buf})
        # Vertical placements.
        for i in range(height - L + 1):
            for j in range(width):
                cells = [(i + k, j) for k in range(L)]
                buf = set()
                for (ci, cj) in cells:
                    for di in [-1, 0, 1]:
                        for dj in [-1, 0, 1]:
                            ni = ci + di
                            nj = cj + dj
                            if 0 <= ni < height and 0 <= nj < width:
                                buf.add((ni, nj))
                placements[sid].append({'i': i, 'j': j, 'd': 1, 'cells': cells, 'buffer': buf})

    # Decision variables:
    # y[sid][p] = 1 if ship 'sid' is placed using placement index p.
    y = {}
    for s in ships:
        sid = s['id']
        y[sid] = {}
        for p_idx, p in enumerate(placements[sid]):
            y[sid][p_idx] = model.NewBoolVar(f'y_s{sid}_p{p_idx}')
    # x[i][j] = 1 if cell (i,j) is occupied.
    x = {}
    for i in range(height):
        for j in range(width):
            x[(i, j)] = model.NewBoolVar(f'x_{i}_{j}')

    # Constraint (1): Each ship is placed exactly once.
    for s in ships:
        sid = s['id']
        model.Add(sum(y[sid][p_idx] for p_idx in y[sid]) == 1)

    # Constraint (2): Define occupancy: for each cell (i,j), x[i,j] equals the sum of placements covering it.
    # We'll accumulate contributions from every ship placement covering the cell.
    for i in range(height):
        for j in range(width):
            cell_cover = []
            for s in ships:
                sid = s['id']
                for p_idx, p in enumerate(placements[sid]):
                    if (i, j) in p['cells']:
                        cell_cover.append(y[sid][p_idx])
            model.Add(x[(i, j)] == sum(cell_cover))

    # Constraint (3): Row sum requirements.
    for i in range(height):
        model.Add(sum(x[(i, j)] for j in range(width)) == rowsum[i])

    # Constraint (4): Column sum requirements.
    for j in range(width):
        model.Add(sum(x[(i, j)] for i in range(height)) == colsum[j])

    # Constraint (5): Hint consistency.
    for i in range(height):
        for j in range(width):
            if hint_input[i][j] in [0, 1]:
                model.Add(x[(i, j)] == hint_input[i][j])

    # (6) Non-overlap is already enforced via occupancy sum (x[i,j] computed from placements).
    # Constraint (7): Non-adjacency (buffer) constraint between distinct ships.
    ship_ids = [s['id'] for s in ships]
    for idx1 in range(len(ship_ids)):
        sid1 = ship_ids[idx1]
        for idx2 in range(idx1 + 1, len(ship_ids)):
            sid2 = ship_ids[idx2]
            # For each pair of placements from ship sid1 and sid2:
            for p1_idx, p1 in enumerate(placements[sid1]):
                for p2_idx, p2 in enumerate(placements[sid2]):
                    # Check if the placement of ship2 (its cells) conflicts with placement of ship1 (its buffer).
                    conflict = False
                    for cell in p2['cells']:
                        if cell in p1['buffer']:
                            conflict = True
                            break
                    # Alternatively, one could check the other direction, but the conflict relation is symmetric.
                    if conflict:
                        model.Add(y[sid1][p1_idx] + y[sid2][p2_idx] <= 1)

    # Objective: feasibility model
    model.Minimize(0)

    # Solve the model.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    if status in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
        print("Solution found:")
        print("Objective value =", solver.ObjectiveValue())
        # Print ship placements.
        for s in ships:
            sid = s['id']
            L = s['length']
            for p_idx, p in enumerate(placements[sid]):
                if solver.Value(y[sid][p_idx]) == 1:
                    orientation = "Horizontal" if p['d'] == 0 else "Vertical"
                    print(f"Ship {sid} (length {L}) placed at row {p['i']} col {p['j']} with orientation {orientation}.")
                    break
        # Print board occupancy.
        print("\nBoard occupancy (0: water, 1: ship):")
        for i in range(height):
            row_str = ""
            for j in range(width):
                row_str += str(solver.Value(x[(i, j)])) + " "
            print(row_str)
    else:
        print("No solution found.")


if __name__ == '__main__':
    main()