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
        while(water_molecule_1 < 948):
            cell1_height = random.randint(0, 24)
            width = random.randint(0, 54)
            if self.grid[cell1_height, width] == 1:
                continue
            else:
                self.grid[cell1_height, width] = 1
                water_molecule_1 += 1

        lipid_molecule = 0
        while(lipid_molecule < 190):
            membrane_height = random.randint(25, 29)
            width = random.randint(0, 54)
            if self.grid[membrane_height, width] == 4:
                continue
            else:
                self.grid[membrane_height, width] = 4   
                lipid_molecule += 1

        water_molecule_2 = 0
        while(water_molecule_2 < 948):
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

        return self.grid
    
ca_grid = CA_grid()
see_grid = ca_grid.make_grid()
plt.imshow(see_grid)
plt.show()
