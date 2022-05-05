from abc import ABC

import numpy as np

from utils import load_config
import music_modules
from visualization import Interface


class MatrixProcessor:    
    def __init__(self, config_file: str = 'config.yaml'):
        config = load_config(config_file)
        self.matrix_shape = (config['matrix_shape']['vertical'], config['matrix_shape']['horizontal'])

        self.modules = []
        for module_name in config['modules']:
            self.set_module(config['modules'][module_name])

        self.log_file = config['log_file']
        open(self.log_file, 'w').close()

        self.visualization = Interface(modules=self.modules, shape=self.matrix_shape)

    def set_module(self, config: dict):
        module_class = getattr(music_modules, config['module'])
        self.modules.append(module_class(config['setup'], config['sound']))
        
    def process(self, value_matrix: np.ndarray):
        assert value_matrix.shape == self.matrix_shape
        
        for module in self.modules:
            module.process(value_matrix[module.top:module.bottom,module.left:module.right])

        # render CLI output
        self.visualization.render()

        # logging
        with open(self.log_file, "ab") as file:
            np.save(file, value_matrix)