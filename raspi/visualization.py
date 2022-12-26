import sys
import os
from typing import List, Tuple

import numpy as np
from tabulate import tabulate

from config_manager import ConfigManager


class Interface:
    
    def __init__(self, modules, config_manager: ConfigManager) -> None:
        self.modules: List[Tuple] = modules
        self.config_manager = config_manager
        self.shape: Tuple[int, int] = (len(self.config_manager.i2c_addresses()), self.config_manager.n_device_sensors())
        self.lines: List[int] = []
        self.module_name_spacer: int = max([len(module.name) for module in self.modules])

    def render(self) -> None:
        return self.quick_and_dirty_for_testing_values()
        activations, names = self.get_activations_and_names()
        
        table = []
        for i in range(len(activations)):
            # add names if any
            if any(elem is not None for elem in names[i]):
                table.append([name if name else "-" * self.module_name_spacer for name in names[i]])
            
            # add activations
            table.append([f"{a:.0f}" for a in activations[i]])

        # print(tabulate(table), flush=True)
        # sys.stdout.flush()
        # os.system('cls' if os.name == 'nt' else 'clear')
        sys.stdout.write(tabulate(table))
        sys.stdout.flush()

    def quick_and_dirty_for_testing_values(self):
        activations = ''
        infos = []
        for module in self.modules:
            # get activation values for sensors in module
            activations += ' '.join(str(f"{v:.0f}") for v in module.get_values().flatten())
            if module.get_info():
                activations += f" ({module.get_info()})"
            activations += ' | '
        sys.stdout.write("\r{0}".format(activations))
        sys.stdout.flush()

    def get_activations_and_names(self) -> np.ndarray:
        activations = np.zeros(self.shape)
        names = [[None for i in range(self.shape[1])] for i in range(self.shape[0])]
        for module in self.modules:
            # get activation values for sensors in module
            module_activations = module.get_values()
            for i in range(module_activations.shape[0]):
                for j in range(module_activations.shape[1]):
                    activations[i+module.top][j+module.left] = module_activations[i][j]
            # save name of module
            names[module.top][module.left] = module.name
        return activations, names
