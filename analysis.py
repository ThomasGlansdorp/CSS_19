def count_unbound_molecule(grid, total_height, total_width, cell_type=1):
    unbound_molecule = 0

    for height in range(total_height):
        for width in range(total_width):
            neighbours = get_neighbours(height, width, grid, total_height, total_width)

            if grid[height, width] == 0 or grid[height, width] == cell_type:
                continue

            if any([i[2] == 2 for i in neighbours]):
                continue
            else:
                unbound_molecule += 1
                
    return unbound_molecule


def get_neighbours(height, width, grid, total_height, total_width):
    neighbours = []

    neighbours.append((height, width, grid[height, width]))
    neighbours.append((((height - 1) % total_height), width, grid[((height - 1) % total_height), width]))
    neighbours.append((((height + 1) % total_height), width, grid[((height + 1) % total_height), width]))
    neighbours.append((height, ((width - 1) % total_width), grid[height, ((width - 1) % total_width)]))
    neighbours.append((height, ((width + 1) % total_width), grid[height, ((width + 1) % total_width)]))

    return neighbours



