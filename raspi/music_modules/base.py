from abc import ABC

import numpy as np
import time

class MusicModule(ABC):
    def __init__(self, setup: dict):
        self.name: str = setup['name']
        self.midi_channel: int = setup['midi_channel']
        self.top: int = setup['top']
        self.left: int = setup['left']
        self.bottom: int = setup['bottom']
        self.right: int = setup['right']
        self.shape = (setup['bottom'] - setup['top'], setup['right'] - setup['left'])
        self.last_matrix: np.ndarray = np.zeros(self.shape)

    def pre_process(self, matrix: np.ndarray):
        try:
            assert matrix.shape == self.shape
        except AssertionError:
            print(f"AssertionError: matrix shape: {matrix.shape} != module shape: {self.shape}")


    
    def process(self, matrix: np.ndarray):
        self.pre_process(matrix)
        return_events = self.module_process(matrix)
        self.post_process(matrix)
        return return_events
    
    def post_process(self, matrix: np.ndarray):
        self.last_matrix = matrix.copy()
        self.last_processing_timestamp = time.time()

    def get_values(self) -> np.ndarray:
        return self.last_matrix

    def get_info(self) -> str:
        return ''
