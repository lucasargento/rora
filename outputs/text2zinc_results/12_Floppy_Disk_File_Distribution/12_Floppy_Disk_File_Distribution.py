# Mathematical Formulation:
'''\begin{align*}
\textbf{Indices and Sets:} \quad & i \in \{1, 2, \ldots, N\} \quad \text{(set of available floppy disks)}\\[1mm]
& j \in \{1, 2, \ldots, N\} \quad \text{(set of files)}\\[2mm]
\textbf{Parameters:} \quad & N \quad \text{Number of files}\\[1mm]
& C \quad \text{Capacity of each floppy disk}\\[1mm]
& s_j \quad \text{Size of file } j, \quad j = 1,\ldots, N\\[2mm]
\textbf{Decision Variables:} \quad & x_{ij} \in \{0,1\} \quad \forall i=1,\ldots,N,\; j=1,\ldots,N,\\[1mm]
& \quad\quad\quad\; \text{where } x_{ij} = 
  \begin{cases}
    1, & \text{if file } j \text{ is stored on disk } i, \\
    0, & \text{otherwise.}
  \end{cases}\\[2mm]
& y_i \in \{0,1\} \quad \forall i=1,\ldots,N,\\[1mm]
& \quad\quad\quad\; \text{where } y_i = 
  \begin{cases}
    1, & \text{if disk } i \text{ is used,} \\
    0, & \text{otherwise.}
  \end{cases}\\[2mm]
\textbf{Objective Function:} \quad & \min \; \sum_{i=1}^{N} y_i \quad \text{(minimize the number of disks used)}\\[2mm]
\textbf{Constraints:} \\[1mm]
\text{(1) Assignment Constraint:} \quad & \sum_{i=1}^{N} x_{ij} = 1 \quad \forall j = 1,\ldots,N, \\
& \quad\quad\quad\; \text{(each file is assigned to exactly one disk)} \\[2mm]
\text{(2) Capacity Constraint:} \quad & \sum_{j=1}^{N} s_j \, x_{ij} \leq C \, y_i \quad \forall i = 1,\ldots,N, \\
& \quad\quad\quad\; \text{(the total size of files on disk } i \text{ does not exceed its capacity)}.
\end{align*}  

This complete model accurately formulates the scheduling (or bin-packing) problem where we decide on file-to-disk assignments with the goal of minimizing the number of floppy disks used, ensuring each file is backed up and that each disk’s capacity is not exceeded.'''

# Generated Code:
from ortools.sat.python import cp_model


def main():
    # Problem parameters (scaling factor to convert floats to integers)
    scale = 2
    N = 5
    capacity = 3
    capacity_int = int(capacity * scale)
    sizes = [1, 2, 0.5, 1.5, 2.5]
    sizes_int = [int(s * scale) for s in sizes]

    model = cp_model.CpModel()

    # Decision variables
    # x[i][j] = 1 if file j is stored on disk i
    x = {}
    for i in range(N):
        for j in range(N):
            x[i, j] = model.NewBoolVar(f'x_{i}_{j}')

    # y[i] = 1 if disk i is used
    y = {}
    for i in range(N):
        y[i] = model.NewBoolVar(f'y_{i}')

    # Constraints:
    # (1) Each file must be assigned to exactly one disk.
    for j in range(N):
        model.Add(sum(x[i, j] for i in range(N)) == 1)

    # (2) Capacity constraint: total size on disk i must not exceed disk capacity if disk is used.
    for i in range(N):
        model.Add(sum(sizes_int[j] * x[i, j] for j in range(N)) <= capacity_int * y[i])

    # Objective: minimize the number of disks used.
    model.Minimize(sum(y[i] for i in range(N)))

    # Solve the model.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print("Solution:")
        print("Minimum number of disks used =", solver.ObjectiveValue())
        for i in range(N):
            if solver.Value(y[i]) == 1:
                files_on_disk = []
                for j in range(N):
                    if solver.Value(x[i, j]) == 1:
                        files_on_disk.append(j)
                if files_on_disk:
                    disk_load = sum(sizes[j] for j in files_on_disk)
                    print(f"Disk {i} (load {disk_load}/{capacity}) -> files: {files_on_disk}")
    else:
        print("No feasible solution found.")


if __name__ == '__main__':
    main()