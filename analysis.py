import numpy as np

def calculate_attributes(grid=None, rules=None, cell_type=1):

    unbound_count = 0
    bond_count = {1: 0, 2: 0, 3: 0, 4: 0}
    total_bonds = 0

    for height in range(grid.height):
        for width in range(grid.width):
            cell_value = grid.grid[height, width]
            if cell_value != cell_type: 
                continue
    
            neighbours = rules.get_neighbourings(height, width)[1:]  # Exclude the cell itself
            # Count bound and unbound molecules
            bound_neighbours = sum(neighbour[2] == cell_value for neighbour in neighbours)
            if bound_neighbours == 0:
                unbound_count += 1
            else:
                bond_count[bound_neighbours] += 1

    # Calculate the fractions
    total_molecules = np.sum(rules.grid == 1) + np.sum(rules.grid == 2)
    f_o = unbound_count / total_molecules if total_molecules else 0
    f_1 = bond_count[1] / total_molecules if total_molecules else 0
    f_2 = bond_count[2] / total_molecules if total_molecules else 0
    f_3 = bond_count[3] / total_molecules if total_molecules else 0
    f_4 = bond_count[4] / total_molecules if total_molecules else 0

    return f_o, f_1, f_2, f_3, f_4

def count_neighbours(grid, total_height, total_width, cell_type=0):
    count = 0

    for height in range(total_height):
        for width in range(total_width):
            neighbours = get_neighbours(height, width, grid, total_height, total_width)

            center = neighbours[1]

            for neighbour in neighbours[1:]:
                if center[2] == neighbour[2]:
                    count += 1
                else:
                    count -= 1
                
    return count


def get_neighbours(height, width, grid, total_height, total_width):
    neighbours = []

    neighbours.append((height, width, grid[height, width]))
    neighbours.append((((height - 1) % total_height), width, grid[((height - 1) % total_height), width]))
    neighbours.append((((height + 1) % total_height), width, grid[((height + 1) % total_height), width]))
    neighbours.append((height, ((width - 1) % total_width), grid[height, ((width - 1) % total_width)]))
    neighbours.append((height, ((width + 1) % total_width), grid[height, ((width + 1) % total_width)]))

    return neighbours

