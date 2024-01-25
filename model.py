import numpy as np
import matplotlib.pyplot as plt
import random

class CA_grid:

    def __init__(self, height=55, membrane_height=5, width=55) -> None:
        self.height = height
        self.membrane_height = membrane_height
        self.width = width

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
        while(solute_molecule < 100):  #add variable that can be altered for the amount of solute molecules
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
    
class CA_rules:

    def __init__(self, ca_grid: CA_grid) -> None:
        self.grid = ca_grid.make_grid()

        self.pbw = 0.375
        self.pbwl = 0.9
        self.pbl = 0.375

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

        if neighbours[1][2] == 0:
            open_cell_counter += 1
        elif neighbours[1][2] == 1 and neighbours[0][2] == 1:
            pbw_counter += 1
        elif neighbours[1][2] == 2 and neighbours[0][2] == 1 or neighbours[1][2] == 1 and neighbours[0][2] == 2:
            pbwl_counter += 1
        elif neighbours[1][2] == 2 and neighbours[0][2] == 2:
            pbl_counter += 1

        if neighbours[2][2] == 0:
            open_cell_counter += 1
        elif neighbours[2][2] == 1 and neighbours[0][2] == 1:
            pbw_counter += 1
        elif neighbours[2][2] == 2 and neighbours[0][2] == 1 or neighbours[1][2] == 1 and neighbours[0][2] == 2:
            pbwl_counter += 1
        elif neighbours[2][2] == 2 and neighbours[0][2] == 2:
            pbl_counter += 1
        
        if neighbours[3][2] == 0:
            open_cell_counter += 1
        elif neighbours[3][2] == 1 and neighbours[0][2] == 1:
            pbw_counter += 1
        elif neighbours[3][2] == 2 and neighbours[0][2] == 1 or neighbours[1][2] == 1 and neighbours[0][2] == 2:
            pbwl_counter += 1
        elif neighbours[3][2] == 2 and neighbours[0][2] == 2:
            pbl_counter += 1

        if neighbours[4][2] == 0:
            open_cell_counter += 1
        elif neighbours[4][2] == 1 and neighbours[0][2] == 1:
            pbw_counter += 1
        elif neighbours[4][2] == 2 and neighbours[0][2] == 1 or neighbours[1][2] == 1 and neighbours[0][2] == 2:
            pbwl_counter += 1
        elif neighbours[4][2] == 2 and neighbours[0][2] == 2:
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
        for i in range(1, 10000):
            self.grid = self.step()
            print(f'This is iteration {i} of the simulation')
        
        return self.grid

    
# ca_grid = CA_grid()
# see_grid = ca_grid.make_grid()
# plt.imshow(see_grid)
# plt.show()
# ca_grid = CA_grid
# ca_rules = CA_rules(CA_grid)
# ca_rules.generate_simulation()

see_grid = CA_rules(CA_grid()).generate_simulation()
plt.imshow(see_grid)
plt.show()
