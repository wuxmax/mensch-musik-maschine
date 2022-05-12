from typing import List

import numpy as np

from utils import load_config

class MatrixDataPreprocessor: 
    def __init__(self, config_file: str = 'config.yml'):
        config = load_config(config_file)
        self.calibration_values = np.empty((config['matrix_shape']['horizontal'], config['matrix_shape']['vertical'], 2))
        self.threshold = config['data_preprocessor']['threshold']
        
    def calibrate(self, reference_values: List[np.ndarray]):
        try:
            assert reference_values[0].shape == self.calibration_values.shape[:2]
        except AssertionError:
            print(f"AssertionError: reference shape: {reference_values[0].shape} != matrix shape: {self.calibration_values.shape[:2]}")

        self.reference_values = np.stack(reference_values, axis=-1)
        self.calibration_values[:,:,0] = self.reference_values.min(axis=2)
        self.calibration_values[:,:,1] = self.reference_values.max(axis=2)

    def normalize(self, matrix: np.ndarray):
        try:
            assert matrix.shape == self.calibration_values.shape[:2]
        except AssertionError:
            print(f"AssertionError: reference shape: {matrix.shape} != matrix shape: {self.calibration_values.shape[:2]}")

        normalized_matrix = np.zeros(matrix.shape)
        normalized_matrix[matrix < self.calibration_values[:,:,0] - self.threshold] = - 1
        normalized_matrix[matrix > self.calibration_values[:,:,1] + self.threshold] = 1

        return normalized_matrix

if __name__=="__main__":
    def test_array():
        return np.random.rand(8, 2) + 1000
    
    test_values = [test_array()] * 100

    datpro = MatrixDataPreprocessor()
    datpro.calibrate(test_values)
    print(datpro.normalize(test_array() * 0.9))
    print(datpro.normalize(test_array()))
    print(datpro.normalize(test_array() * 1.1))
    
    