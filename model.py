import numpy as np
import matplotlib.pyplot as plt

class CA_grid:

    def __init__(self, height=55, membrane_height=5, width=55) -> None:
        self.height = height
        self.membrane_height = membrane_height
        self.width = width

        self.grid = None

    def make_grid(self):
        return