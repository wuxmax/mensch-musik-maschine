from typing import List

import numpy as np

from utils import load_config

INPUT_VALUE_RANGE = (0, 1023)
OUTPUT_VALUE_RANGE = (0, 127)
MARGIN_FACTOR = 0

class MatrixDataPreprocessor: 
    def __init__(self, config: dict):
        self.matrix_shape = (config['matrix_shape']['vertical'], config['matrix_shape']['horizontal'])
        self.output_range = OUTPUT_VALUE_RANGE[-1] - OUTPUT_VALUE_RANGE[0]
        
        # last axis indices: 0 = min, 1 = max
        self.calibration_values = np.empty((*self.matrix_shape, 2))  
        self.normalization_values = np.empty((*self.matrix_shape, 2))
        
    def calibrate(self, reference_values: List[np.ndarray]):
        try:
            assert reference_values[0].shape == self.calibration_values.shape[:2]
        except AssertionError:
            print(f"AssertionError: reference shape: {reference_values[0].shape} != matrix shape: {self.calibration_values.shape[:2]}")

        reference_values_stacked = np.stack(reference_values, axis=2)
        self.calibration_values[:,:,0] = reference_values_stacked.min(axis=2)
        self.calibration_values[:,:,1] = reference_values_stacked.max(axis=2)

        margin_values = (self.calibration_values[:,:,1] - self.calibration_values[:,:,0]) * MARGIN_FACTOR
        self.calibration_values[:,:,0] = np.maximum(np.full(self.matrix_shape, INPUT_VALUE_RANGE[0]),  self.calibration_values[:,:,0] - margin_values)
        self.calibration_values[:,:,1] = np.minimum(np.full(self.matrix_shape, INPUT_VALUE_RANGE[-1]),  self.calibration_values[:,:,1] + margin_values)

        self.normalization_values = self.calibration_values.copy()

    def normalize(self, matrix: np.ndarray):
        try:
            assert matrix.shape == self.calibration_values.shape[:2]
        except AssertionError:
            print(f"AssertionError: reference shape: {matrix.shape} != matrix shape: {self.calibration_values.shape[:2]}")
        
        lower_indeces = matrix < self.calibration_values[:,:,0]
        higher_indeces = matrix > self.calibration_values[:,:,1]

        self.normalization_values[:,:,0][lower_indeces] = np.minimum(self.normalization_values[:,:,0], matrix)[lower_indeces]
        self.normalization_values[:,:,1][higher_indeces] = np.maximum(self.normalization_values[:,:,1], matrix)[higher_indeces]
        
        normalized_matrix = np.zeros(matrix.shape)
        normalized_matrix[lower_indeces] = (matrix - self.calibration_values[:,:,0])[lower_indeces]  # all negative
        normalized_matrix[higher_indeces] = (matrix - self.calibration_values[:,:,1])[higher_indeces]  # all positive
        
        negative_range = np.abs(self.normalization_values[:,:,0] - self.calibration_values[:,:,0])
        negative_range[negative_range == 0.0] = np.abs(self.calibration_values[:,:,0] - INPUT_VALUE_RANGE[0])[negative_range == 0.0]
        positive_range = np.abs(self.normalization_values[:,:,1] - self.calibration_values[:,:,1])
        positive_range[positive_range == 0.0] = np.abs(self.calibration_values[:,:,1] - INPUT_VALUE_RANGE[-1])[positive_range == 0.0]
        
        normalized_matrix[lower_indeces] = ((normalized_matrix / negative_range) * self.output_range)[lower_indeces]
        normalized_matrix[higher_indeces] = ((normalized_matrix / positive_range) * self.output_range)[higher_indeces]

        return normalized_matrix

if __name__=="__main__":
    np.set_printoptions(formatter={'float_kind':"{:.1f}".format})
    
    def test_array(low, high):
        return np.random.uniform(float(low), float(high), size=(2, 6))
    
    test_values = [test_array(500, 550) for _ in range(100)]

    datpro = MatrixDataPreprocessor(load_config('config.yml'))
    datpro.calibrate(test_values)
    print(datpro.normalize(test_array(0, 200)))
    print(datpro.normalize(test_array(200, 400)))
    print(datpro.normalize(test_array(500, 550)))
    print(datpro.normalize(test_array(800, 1000)))
    print(datpro.normalize(test_array(600, 800)))
    print(datpro.normalize(test_array(100, 700)))

    
    
    