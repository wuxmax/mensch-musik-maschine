from typing import List

import numpy as np
from sklearn.cluster import KMeans
from tqdm import tqdm

from i2c_reader import I2CReader
from utils import load_config

class MatrixDataPreprocessor: 
    def __init__(self, config: dict):
        self.matrix_shape = (config['matrix_shape']['vertical'], config['matrix_shape']['horizontal'])
        self.calibration_period = config['data_preprocessor']['calibration_period']

        self.cluster_predictors = [KMeans(n_clusters=config['data_preprocessor']['n_clusters'], random_state=0)] * (self.matrix_shape[0] * self.matrix_shape[1])
        self.return_values = range(config['data_preprocessor']['n_clusters'])
        self.cluster_label_mapping = None  # mapping from predicted label to sorted value in return valuers

        self.value_history = None
        self.last_calibration = None

    def calibrate(self, i2c_reader: I2CReader = None, values = None):
        print("Calibrating...")
        if values:
            self.value_history = np.stack(values, axis=2)
        elif i2c_reader:
            self.value_history = np.stack([i2c_reader.get_value_matrix() for _ in tqdm(range(self.calibration_period))])
        elif not i2c_reader:
            print("No values or I2C reader given! Need values to calibrate.")
        
        self.cluster_label_mapping = []
        for flat_idx, predictor in enumerate(self.cluster_predictors):
            matrix_idx = np.unravel_index(flat_idx, self.matrix_shape)
            predictor.fit(self.value_history[matrix_idx[0], matrix_idx[1], :].reshape(-1, 1))
            
            cluster_center_label_mapping_sorted = sorted(list(zip(predictor.cluster_centers_, predictor.labels_)), key=lambda t: t[0])
            cluster_labels_sorted = [t[1] for t in cluster_center_label_mapping_sorted]
            cluster_label_mapping = {cluster_label: self.return_values[sort_idx] for sort_idx, cluster_label in enumerate(cluster_labels_sorted)}
            self.cluster_label_mapping.append(cluster_label_mapping)

        self.last_calibration = self.calibration_period
        print("Calibration done!")

    def normalize(self, matrix: np.ndarray):
        if self.value_history is None:
            print("No value history! Needs calibration before normalization.")
        
        normalized_matrix = np.empty(self.matrix_shape)
        for flat_idx, predictor in enumerate(self.cluster_predictors):
            matrix_idx = np.unravel_index(flat_idx, self.matrix_shape)
            normalized_matrix[matrix_idx] = predictor.predict(matrix[matrix_idx[0], matrix_idx[1]].reshape(-1, 1))

        return normalized_matrix


if __name__=="__main__":
    np.set_printoptions(formatter={'float_kind':"{:.1f}".format})
    datpro = MatrixDataPreprocessor(load_config('config.yml'))

    def test_array(low, high):
        return np.random.uniform(float(low), float(high), size=datpro.matrix_shape)
    
    test_values = [test_array(100, 300) for _ in range(100)] + [test_array(700, 900) for _ in range(100)]

    datpro.calibrate(values=test_values)
    print("Very low state")
    print(datpro.normalize(test_array(0, 200)))
    print("Low state")
    print(datpro.normalize(test_array(200, 400)))
    print("Middle state")
    print(datpro.normalize(test_array(400, 600)))
    print("High state")
    print(datpro.normalize(test_array(600, 800)))
    print("Very high state")
    print(datpro.normalize(test_array(800, 1000)))
    print("Random state")
    print(datpro.normalize(test_array(100, 900)))

    
    
    