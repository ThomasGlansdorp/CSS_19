import numpy as np
import matplotlib.pyplot as plt
import random
import pandas as pd

class CA_grid:

    def __init__(self, solute_amount=100, height=55, membrane_height=5, width=55) -> None:
        self.height = height
        self.membrane_height = membrane_height
        self.width = width
        self.solute_amount = solute_amount

        self.grid = None

    def make_grid_membrane(self):
        self.grid = np.zeros((self.height, self.width), dtype=np.int32)

        water_molecule_1 = 0
        while(water_molecule_1 < round(self.width * 25 * 0.69)):
            cell1_height = random.randint(0, 24)
            width = random.randint(0, 54)
            if self.grid[cell1_height, width] == 1:
                continue
            else:
                self.grid[cell1_height, width] = 1
                water_molecule_1 += 1

        lipid_molecule = 0
        while(lipid_molecule < round(self.width * 5 * 0.69)):
            membrane_height = random.randint(25, 29)
            width = random.randint(0, 54)
            if self.grid[membrane_height, width] == 4:
                continue
            else:
                self.grid[membrane_height, width] = 4   
                lipid_molecule += 1

        water_molecule_2 = 0
        while(water_molecule_2 < round(self.width * 25 * 0.69)):
            cell2_height = random.randint(30, 54)
            width = random.randint(0, 54)
            if self.grid[cell2_height, width] == 2:
                continue
            else:
                self.grid[cell2_height, width] = 2  
                water_molecule_2 += 1
            
        return self.grid
    
    def make_grid(self):
        self.grid = np.zeros((self.height, self.width), dtype=np.int32)

        water_molecule = 0
        while(water_molecule < round(self.width * self.height * 0.69)):  
            height = random.randint(0, 54)
            width = random.randint(0, 54)
            if self.grid[height, width] == 1:
                continue
            else:
                self.grid[height, width] = 1
                water_molecule += 1

        solute_molecule = 0
        while(solute_molecule < self.solute_amount):  #add variable that can be altered for the amount of solute molecules
            height = random.randint(0, 54)
            width = random.randint(0, 54)
            if self.grid[height, width] == 2 or self.grid[height, width] == 0:
                continue
            else:
                self.grid[height, width] = 2
                solute_molecule += 1

        plt.imshow(self.grid)
        plt.show()

        return self.grid
    
    def make_grid_water(self):
        self.grid = np.zeros((self.height, self.width), dtype=np.int32)

        water_molecule = 0
        while(water_molecule < round(self.width * self.height * 0.69)):  
            height = random.randint(0, 54)
            width = random.randint(0, 54)
            if self.grid[height, width] == 1:
                continue
            else:
                self.grid[height, width] = 1
                water_molecule += 1

        plt.imshow(self.grid)
        plt.show()

        return self.grid

    
class CA_rules:

    def __init__(self, ca_grid: CA_grid) -> None:
        self.grid = ca_grid.make_grid()

        self.pbw = 0.25
        self.pbwl = 0.45
        self.pbl = 0.1

        self.height = ca_grid.height
        self.width = ca_grid.width

    def step(self):
        
        for height in range(self.height):
            for width in range(self.width):
                if self.grid[height, width] == 0:
                    continue

                neighbours = self.get_neighbourings(height, width)
                #print(neighbours)

                if not any([i[2] == 0 for i in neighbours]):  # makes new list of boolean expressions if non are true it continues to next step in for loop
                    continue
                #print('hoi')

                move_probability = self.move_probability(height, width, neighbours)
                #print(move_probability)

                rand = random.random() 
                #print(rand)
                if rand > move_probability: # if it does not break free of cluster continue to next step in for loop
                    continue
                
                #print('cell moves')
                probabilities = [1 if v[2] == 0 else 0 for v in neighbours]

                empty_cells = probabilities.count(1)

                probabilities_normalized = [probability / empty_cells for probability in probabilities]

                index = np.random.choice(len(neighbours), p = probabilities_normalized)

                move_to = neighbours[index]

                self.grid[move_to[0], move_to[1]] = neighbours[0][2]
                self.grid[height, width] = 0                                
                                            
        return self.grid


    def get_neighbourings(self, height, width):
        neighbours = [] # keeps track of neighbours of center cell, in order of center, above, under, left, right
        # neighbours = [(h, w, v), (h, w, v), etc]

        neighbours.append((height, width, self.grid[height, width]))
        neighbours.append((((height - 1) % self.height), width, self.grid[((height - 1) % self.height), width]))
        neighbours.append((((height + 1) % self.height), width, self.grid[((height + 1) % self.height), width]))
        neighbours.append((height, ((width - 1) % self.width), self.grid[height, ((width - 1) % self.width)]))
        neighbours.append((height, ((width + 1) % self.width), self.grid[height, ((width + 1) % self.width)]))

        return neighbours
        
    def move_probability(self, height, width, neighbours):
        pbw_counter = 0
        pbwl_counter = 0
        pbl_counter = 0
        open_cell_counter = 0

        for neighbour in neighbours:
            if neighbour[2] == 0:
                open_cell_counter += 1
            elif neighbour[2] == 1 and neighbours[0][2] == 1:
                pbw_counter += 1
            elif neighbour[2] == 2 and neighbours[0][2] == 1 or neighbour[2] == 1 and neighbours[0][2] == 2:
                pbwl_counter += 1
            elif neighbour[2] == 2 and neighbours[0][2] == 2:
                pbl_counter += 1

        move_probability = self.calculate_probability(pbl_counter, pbwl_counter, pbw_counter, open_cell_counter)
        
        return move_probability

    def calculate_probability(self, pbl_counter, pbwl_counter, pbw_counter, open_cell_counter):
        pbw = 1
        pbwl = 1
        pbl = 1

        if pbw_counter != 0:
            pbw = (self.pbw / pbw_counter)
        
        if pbwl_counter != 0:
            pbwl = (self.pbwl / pbwl_counter)

        if pbl_counter != 0:
            pbl = (self.pbl / pbl_counter)

        q =  pbw * pbwl * pbl
        p = q**(4 - open_cell_counter)

        return p

    def generate_simulation(self):
        for i in range(1, 5000):
            self.grid = self.step()
            print(f'This is iteration {i} of the simulation')

        return self.grid
    
    def calculate_attributes(self):
        unbound_count = 0
        bond_count = {1: 0, 2: 0, 3: 0, 4: 0}
        total_bonds = 0

        for height in range(self.height):
            for width in range(self.width):
                cell_value = self.grid[height, width]
                if cell_value not in (1, 2): 
                    continue
        
                neighbours = self.get_neighbourings(height, width)[1:]  # Exclude the cell itself
                # Count bound and unbound molecules
                bound_neighbours = sum(neighbour[2] == cell_value for neighbour in neighbours)
                if bound_neighbours == 0:
                    unbound_count += 1
                else:
                    bond_count[bound_neighbours] += 1
                
                # For water, calculate the average number of hydrogen bonds
                if cell_value == 1:  # Water
                    total_bonds += bound_neighbours

        # Calculate the fractions
        total_molecules = np.sum(self.grid == 1) + np.sum(self.grid == 2)
        f_o = unbound_count / total_molecules if total_molecules else 0
        f_1 = bond_count[1] / total_molecules if total_molecules else 0
        f_2 = bond_count[2] / total_molecules if total_molecules else 0
        f_3 = bond_count[3] / total_molecules if total_molecules else 0
        f_4 = bond_count[4] / total_molecules if total_molecules else 0
        

        # Calculate average hydrogen bonds for water
        water_count = np.sum(self.grid == 1)
        n_HB = total_bonds / water_count if water_count else 0

        return f_o, f_1, f_2, f_3, f_4, n_HB
    
class CA_rules_only_water:

    def __init__(self, ca_grid: CA_grid) -> None:
        self.grid = ca_grid.make_grid_water()

        self.pbw = 0.25

        self.height = ca_grid.height
        self.width = ca_grid.width

    def step(self):
        
        for height in range(self.height):
            for width in range(self.width):
                if self.grid[height, width] == 0:
                    continue

                neighbours = self.get_neighbourings(height, width)
                #print(neighbours)

                if not any([i[2] == 0 for i in neighbours]):  # makes new list of boolean expressions if non are true it continues to next step in for loop
                    continue
                #print('hoi')

                move_probability = self.move_probability(height, width, neighbours)
                #print(move_probability)

                rand = random.random() 
                #print(rand)
                if rand > move_probability: # if it does not break free of cluster continue to next step in for loop
                    continue
                
                #print('cell moves')
                probabilities = [1 if v[2] == 0 else 0 for v in neighbours]

                empty_cells = probabilities.count(1)

                probabilities_normalized = [probability / empty_cells for probability in probabilities]

                index = np.random.choice(len(neighbours), p = probabilities_normalized)

                move_to = neighbours[index]

                self.grid[move_to[0], move_to[1]] = neighbours[0][2]
                self.grid[height, width] = 0                                
                                            
        return self.grid

    def get_neighbourings(self, height, width):
        neighbours = [] # keeps track of neighbours of center cell, in order of center, above, under, left, right
        # neighbours = [(h, w, v), (h, w, v), etc]

        neighbours.append((height, width, self.grid[height, width]))
        neighbours.append((((height - 1) % self.height), width, self.grid[((height - 1) % self.height), width]))
        neighbours.append((((height + 1) % self.height), width, self.grid[((height + 1) % self.height), width]))
        neighbours.append((height, ((width - 1) % self.width), self.grid[height, ((width - 1) % self.width)]))
        neighbours.append((height, ((width + 1) % self.width), self.grid[height, ((width + 1) % self.width)]))

        return neighbours
    
    def move_probability(self, height, width, neighbours):
        pbw_counter = 0
        open_cell_counter = 0

        for neighbour in neighbours:
            if neighbour[2] == 0:
                open_cell_counter += 1
            else:
                pbw_counter += 1

        move_probability = self.calculate_probability(pbw_counter, open_cell_counter)
        
        return move_probability

    def calculate_probability(self, pbl_counter, pbwl_counter, pbw_counter, open_cell_counter):
        pbw = 1

        if pbw_counter != 0:
            pbw = (self.pbw / pbw_counter)

        p = pbw**(4 - open_cell_counter)

        return p
    
    def generate_simulation(self):
        for i in range(1, 10000):
            self.grid = self.step()
            print(f'This is iteration {i} of the simulation')
        
        return self.grid
    

# see_grid = CA_rules(CA_grid()).generate_simulation()
# plt.imshow(see_grid)
# plt.show()
# ca_grid = CA_grid
# ca_rules = CA_rules(CA_grid)
# ca_rules.generate_simulation()

# see_grid = CA_rules(CA_grid()).generate_simulation()
# plt.imshow(see_grid)
# plt.show()
    
solute_concentrations = [50, 100, 150, 200, 250, 300]
results = []

for solute_amount in solute_concentrations:
    print(f"Running simulation with {solute_amount} solute molecules.")
    ca_grid = CA_grid(solute_amount=solute_amount)
    ca_rules = CA_rules(ca_grid)
    ca_rules.generate_simulation()
    attributes = ca_rules.calculate_attributes()

    results.append({
        'solute concentration': solute_amount, 
        'f_0': attributes[0],
        'f_1': attributes[1],
        'f_2': attributes[2],
        'f_3': attributes[3],
        'f_4': attributes[4],
        'n_HB': attributes[0]
    })

    df = pd.DataFrame(results)
    print(df)


    # plt.imshow(final_grid)
    # plt.title(f"Solute concentration: {solute_amount}")
    # plt.show()



