from abc import ABC

import numpy as np

from utils import load_config
import music_modules


class MatrixProcessor:    
    def __init__(self, config_file: str = 'config.yaml'):
        config = load_config(config_file)
        self.matrix_shape = (config['matrix_shape']['vertical'], config['matrix_shape']['horizontal'])

        self.modules = []
        for module_name in config['modules']:
            self.set_module(config['modules'][module_name])

        self.log_file = config['log_file']
        with open(self.log_file, "w") as file:
            file.write(self.matrix_shape)

    def set_module(self, config: dict):
        module_class = getattr(music_modules, config['module'])
        self.modules.append(module_class(config['setup'], config['sound']))
        
    def process(self, value_matrix: np.ndarray):
        assert value_matrix.shape == self.matrix_shape
        
        for module in self.modules:
            module.process(value_matrix[module.top:module.bottom,module.left:module.right])

        # logging
        # retrievable using np.fromstring(value_matrix.tostring(), dtype=np.dtype('float64')).reshape(self.matrix.shape)
        with open(self.log_file, "a") as file:
            file.write("\n" + value_matrix.tostring())