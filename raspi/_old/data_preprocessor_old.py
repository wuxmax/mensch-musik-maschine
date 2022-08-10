from typing import List

import numpy as np

from utils import load_config

class MatrixDataPreprocessor: 
    def __init__(self, config: dict):
        self.matrix_shape = (config['matrix_shape']['vertical'], config['matrix_shape']['horizontal'])
        self.output_value_range = config['data_preprocessor']['output_value_range']
        self.input_value_range = config['data_preprocessor']['input_value_range']
        self.margin_factor = config['data_preprocessor']['margin_factor']
        self.minimal_margin = config['data_preprocessor']['minimal_margin']
        self.output_range = self.output_value_range[-1] - self.output_value_range[0]
        
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

        margin_values = (self.calibration_values[:,:,1] - self.calibration_values[:,:,0]) * self.margin_factor / 2
        margin_values = np.maximum(self.minimal_margin, margin_values)

        self.calibration_values[:,:,0] = np.maximum(self.input_value_range[0],  self.calibration_values[:,:,0] - margin_values)
        self.calibration_values[:,:,1] = np.minimum(self.input_value_range[-1], self.calibration_values[:,:,1] + margin_values)
        # self.calibration_values[:,:,0] = np.maximum(np.full(self.matrix_shape, self.input_value_range[0]),  self.calibration_values[:,:,0] - margin_values)
        # self.calibration_values[:,:,1] = np.minimum(np.full(self.matrix_shape, self.input_value_range[-1]),  self.calibration_values[:,:,1] + margin_values)

        self.normalization_values = self.calibration_values.copy()

    def normalize(self, matrix: np.ndarray):
        try:
            assert matrix.shape == self.calibration_values.shape[:2]
        except AssertionError:
            print(f"AssertionError: reference shape: {matrix.shape} != matrix shape: {self.calibration_values.shape[:2]}")
        
        lower_indeces = matrix < self.calibration_values[:,:,0]
        higher_indeces = matrix > self.calibration_values[:,:,1]

        lower_indices_norm = matrix < self.normalization_values[:,:,0]
        higher_indices_norm = matrix > self.normalization_values[:,:,1]
        self.normalization_values[:,:,0][lower_indices_norm] = matrix[lower_indices_norm]
        self.normalization_values[:,:,1][higher_indices_norm] = matrix[higher_indices_norm]
        
        normalized_matrix = np.zeros(matrix.shape)
        normalized_matrix[lower_indeces] = (matrix - self.calibration_values[:,:,0])[lower_indeces]  # all negative
        normalized_matrix[higher_indeces] = (matrix - self.calibration_values[:,:,1])[higher_indeces]  # all positive
        
        negative_range = np.abs(self.normalization_values[:,:,0] - self.calibration_values[:,:,0])
        negative_range[negative_range == 0.0] = np.inf
        positive_range = np.abs(self.normalization_values[:,:,1] - self.calibration_values[:,:,1])
        positive_range[positive_range == 0.0] = np.inf
        
        normalized_matrix[lower_indeces] = ((normalized_matrix / negative_range) * self.output_range + self.output_value_range[0])[lower_indeces]
        normalized_matrix[higher_indeces] = ((normalized_matrix / positive_range) * self.output_range  + self.output_value_range[0])[higher_indeces]

        return normalized_matrix

if __name__=="__main__":
    np.set_printoptions(formatter={'float_kind':"{:.1f}".format})
    
    def test_array(low, high):
        return np.random.uniform(float(low), float(high), size=(4, 6))
    
    test_values = [test_array(500, 550) for _ in range(100)]

    datpro = MatrixDataPreprocessor(load_config('config.yml'))
    datpro.calibrate(test_values)
    print(datpro.normalize(test_array(0, 200)))
    print(datpro.normalize(test_array(200, 400)))
    print(datpro.normalize(test_array(500, 550)))
    print(datpro.normalize(test_array(800, 1000)))
    print(datpro.normalize(test_array(600, 800)))
    print(datpro.normalize(test_array(100, 700)))

    
    
    