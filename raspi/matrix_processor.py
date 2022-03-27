from typing import Tuple
from abc import ABC

import numpy as np

class MatrixProcessor:
    
    def __init__(self, matrix_shape: Tuple[int, int]):
        self.matrix_shape = matrix_shape
        self.module_mapping: np.ndarray

    def set_modules():
        # assign modules to differnt regions of the matrix
        pass

    def process(self, value_matrix: np.ndarray):
        assert value_matrix.shape == self.matrix_shape

        # iterate trough module mapping and apply different modules


class MusicModule(ABC):
    def __init__(self, config):
        raise NotImplementedError

    def process(sub_matrix: np.ndarray):
        raise NotImplementedError


class Keyboard(MusicModule):
    def __init__(self, config):
        self.note_mapping: np.ndarray

    def process(self, sub_matrix: np.ndarray):
        assert sub_matrix.shape == self.note_mapping.shape

        



