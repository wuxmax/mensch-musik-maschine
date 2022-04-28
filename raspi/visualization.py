from sys import modules
from typing import List, Tuple

import numpy as np


class Interface():
    
    def __init__(self, modules, shape) -> None:
        self.shape: Tuple(int, int) = shape
        self.modules: List[Tuple] = []
        self.lines: List[int] = []

        for module in modules:
            self.modules.append(module)
            if module.left != 0:
                for i in range(module.top, module.bottom):
                  self.vlines.append((module.left, i))
            if module.top != 0:
                for i in range(module.left, module.right):
                  self.hlines.append((i, module.top))

    def render(self) -> None:
        vertical, horizontal = self.shape
        activations, names = self.get_activations_and_names()
        names = self.get_names()
        print(" _ " * (horizontal * 2), flush=True)
        for i in range(horizontal):
            print_line: str = "| "
            for j in range(vertical):
                if names[i][j] != 0:
                    print_line += names[i][j]


    def get_activations_and_names(self) -> np.ndarray:
        activations = np.zeros(self.shape)
        names = np.zeros(self.shape)
        for module in self.modules:
            # get activation values for sensors in module
            module_activations = module.get_values()
            for i in range(module_activations.shape[0]):
                for j in range(module_activations.shape[1]):
                    activations[i+module.top][j+module.left] = module_activations[i][j]
            # save name of module
            names[module.top][module.left] = module.name
        return activations, names