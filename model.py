import numpy as np
import matplotlib.pyplot as plt
import random
import statistics
from matplotlib import animation, rc
from IPython.display import HTML
import math

class CA_grid:

    def __init__(self, solute_amount=100, height=55, width=55) -> None:
        """Initilizes the class CA_grid

        input: self - the properties of the class CA_grid
               solute amount - the amount of solute cells that need to be added instead of water cells. Integer value
               height - the height of the grid that is made. Integer value
               width - the width of the grid that is made. Integer value
        """
        self.height = height
        self.width = width

        self.solute_amount = solute_amount
        self.grid = None
    
    def make_grid(self):
        """Makes the grid based on the given properties to the class CA_grid

        input: self - the properties of the class CA_grid
        output: returns a grid of size L by L
        """
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

        return self.grid
    
class CA_rules:

    def __init__(self, ca_grid: CA_grid, pbw=0.25, pbwl= 0.45, pbl=0.1, pbw_parameter=True, pbl_parameter=True, pbwl_parameter=True, overlook_cell=0) -> None:
        """Initilizes the class CA_rules

        input: self - the properties of the class CA_rules
               ca grid - a class the returns a grid. Class
               pbw - the breaking probability between water cells. Integer value
               pbl - the breaking probability between solute cells. Integer value
               pbwl - the breaking probability betweeen solute and water cells. Integer value
               pbw parameter - parameter that determines if the water breaking probability is used in the simulation. Boolean expression
               pbl parameter - parameter that determines if the solute breaking probability is used in the simulation. Boolean expression
               pbwl parameter - parameter that determines if the water/solute breaking probability is used in the simulation. Boolean expression
               overlook cell - value of 0, 1 or 2 that tells the class to skip a cell type if necessary. Integer value 
        """
        self.grid = ca_grid.make_grid()

        self.pbw = pbw
        self.pbwl = pbwl
        self.pbl = pbl

        self.pbw_parameter = pbw_parameter
        self.pbl_parameter = pbl_parameter
        self.pbwl_parameter = pbwl_parameter

        self.overlook_cell = overlook_cell

        self.height = ca_grid.height
        self.width = ca_grid.width

    def step(self):
        """Iterates over the grid and determines if and how each cell will move.

        input: self - the properties of the class CA_rules
        output: returns a grid of size L by L
        """
        for height in range(self.height):
            for width in range(self.width):
                if self.grid[height, width] == 0 or self.grid[height, width] == self.overlook_cell:
                    continue

                neighbours = self.get_neighbourings(height, width)

                if not any([i[2] == 0 for i in neighbours]):  # makes new list of boolean expressions if non are true it continues to next step in for loop
                    continue

                move_probability = self.move_probability(neighbours)

                rand = random.random() 

                if rand > move_probability: # if it does not break free of cluster continue to next step in for loop
                    continue
                

                probabilities = [1 if v[2] == 0 else 0 for v in neighbours]

                empty_cells = probabilities.count(1)

                probabilities_normalized = [probability / empty_cells for probability in probabilities]

                index = np.random.choice(len(neighbours), p = probabilities_normalized)

                move_to = neighbours[index]

                self.grid[move_to[0], move_to[1]] = neighbours[0][2]
                self.grid[height, width] = 0         
                  
                                        
        return self.grid


    def get_neighbourings(self, height, width):
        """Finds the neighbouring cells of a center cell and stores the coordinates and value of each neighbour.

        input: self - the properties of the class CA_rules
               height - y coordinate of the center cell
               width - x coordinate of the center cell
        output: returns a list of the center and its neighbours. With coordinates of its location and its value
        """
        neighbours = []

        neighbours.append((height, width, self.grid[height, width]))
        neighbours.append((((height - 1) % self.height), width, self.grid[((height - 1) % self.height), width]))
        neighbours.append((((height + 1) % self.height), width, self.grid[((height + 1) % self.height), width]))
        neighbours.append((height, ((width - 1) % self.width), self.grid[height, ((width - 1) % self.width)]))
        neighbours.append((height, ((width + 1) % self.width), self.grid[height, ((width + 1) % self.width)]))

        return neighbours
        
    def move_probability(self, neighbours):
        """Determines the moving probability of a cell based on its neighbours.

        input: self - the properties of the class CA_rules
               neighbours - list of the center cell and its neighbours
        output: returns the moving probability of a cell. Integer value
        """
        pbw_counter = 0
        pbwl_counter = 0
        pbl_counter = 0
        open_cell_counter = 0

        for neighbour in neighbours:
            if neighbour[2] == 0:
                open_cell_counter += 1
            elif neighbour[2] == 1 and neighbours[0][2] == 1 and self.pbw_parameter:
                pbw_counter += 1
            elif (neighbour[2] == 2 and neighbours[0][2] == 1 or neighbour[2] == 1 and neighbours[0][2] == 2) and self.pbwl_parameter:
                pbwl_counter += 1
            elif neighbour[2] == 2 and neighbours[0][2] == 2 and self.pbl_parameter:
                pbl_counter += 1

        move_probability = self.calculate_probability(pbl_counter, pbwl_counter, pbw_counter, open_cell_counter)
        
        return move_probability

    def calculate_probability(self, pbl_counter, pbwl_counter, pbw_counter, open_cell_counter):
        """Calculates the moving probability of a cell based on its neighbours.

        input: self - the properties of the class CA_rules
               pbw counter - the amount of water neighbouring cells of a water center cell. Integer value
               pbl counter - the amount of solute neighbouring cells of a solute center cell. Integer value
               pbwl counter -  the amount of solute neighbours of water center cell or water neighbours of solute center cell. Integer value
               open cell counter - the amount of empty neighbours of the center cell. Integer value
        output: returns the moving probability of a cell. Integer value
        """
        pbw = 1
        pbwl = 1
        pbl = 1

        if pbw_counter != 0:
            pbw = (self.pbw / pbw_counter)
        
        if pbwl_counter != 0:
            pbwl = (self.pbwl / pbwl_counter)

        if pbl_counter != 0:
            pbl = (self.pbl / pbl_counter)

        if pbw_counter == 0 and pbl_counter == 0 and pbwl_counter == 0:
            q = 0.5
        else:
            q =  pbw * pbwl * pbl
    
        p = q**(4 - open_cell_counter)

        return p

    
    def generate_simulation(self, pbw=0, pbl=0, pbwl=0):
        """Runs the simulation of the moving grid with 5000 iterations.

        input: self - the properties of the class CA_rules
               pbw - the breaking probability between water cells. Integer value
               pbl - the breaking probability between solute cells. Integer value
               pbwl - the breaking probability betweeen solute and water cells. Integer value
        output: returns a grid of size L by L
        """
        self.pbw = pbw
        self.pbl = pbl
        self.pbwl = pbwl

        for i in range(1, 5000):
            self.grid = self.step()
        
        return self.grid
    
# In this main function the model can be checked visually with a animation of the moving grid
if __name__ == '__main__':   
    # Define the CA_grid and CA_rules instances
    ca_grid = CA_grid()
    ca_rules = CA_rules(ca_grid)

    # Create a figure and axis
    fig, ax = plt.subplots()

    # Function to initialize the plot
    def init():
        ax.imshow(ca_grid.grid)
        return [ax]

    # Function to update the plot for each animation frame
    def update(frame):
        ca_rules.step()
        ax.clear()  # Clear the previous plot
        ax.imshow(ca_grid.grid)
        return [ax]

    # Create the animation
    anim = animation.FuncAnimation(fig, update, frames=200, init_func=init, blit=True)
    plt.show()
