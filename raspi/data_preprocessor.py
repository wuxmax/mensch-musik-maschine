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
        self.recalibration_period = config['data_preprocessor']['recalibration_period']
        self.recalibration_window = config['data_preprocessor']['recalibration_window']
        self.recalibration_cluster_center_weight = config['data_preprocessor']['recalibration_cluster_center_weight']
        self.feature_disabled = np.zeros(self.matrix_shape)  # store if feature was 0 in initial calibration

        self.n_clusters = config['data_preprocessor']['n_clusters']
        self.error_threshold = config['data_preprocessor']['error_threshold']  # values must be greater than this to be considered valid readings
        self.return_values = range(self.n_clusters)  # could be more complex, length needs to be n_clusters
        self.cluster_predictors = [KMeans(n_clusters=self.n_clusters, random_state=0) for _ in range((self.matrix_shape[0] * self.matrix_shape[1]))]
        self.cluster_label_mapping = None  # mapping from predicted label to sorted value in return values
        
        self.value_history = None
        self.value_history_stacked = None
        self.normalized_value_history = None

    def calibrate(self, i2c_reader: I2CReader = None, values = None):
        print("Calibrating...")
        if not values and i2c_reader:
            print("Reading values...")
            values = [i2c_reader.get_value_matrix() for _ in tqdm(range(self.calibration_period))]
            print("Reading done!")
        elif not values and not i2c_reader and not self.value_history:
            print("No values or I2C reader given and value history empty! Need values to calibrate.")
            exit(1)

        if values:  # initial calibration
            self.value_history_stacked = np.stack(values, axis=2)
            values_stacked = self.value_history_stacked
        else:  # recalibration
            self.value_history_stacked = np.concatenate([self.value_history_stacked] + [np.stack(self.value_history, axis=2)], axis=2)
            values_stacked = self.value_history_stacked[:,:,:-self.recalibration_window]
            
            # add cluster centers proportionally to values_stacked
            cluster_centers = np.empty(*self.matrix_shape, self.n_clusters)
            for flat_idx, predictor in enumerate(self.cluster_predictors):
                matrix_idx = np.unravel_index(flat_idx, self.matrix_shape)
                cluster_centers[matrix_idx[0], matrix_idx[1], :] = predictor.cluster_centers_

            cluster_center_repeats = int(self.recalibration_window / self.n_clusters * self.recalibration_cluster_center_weight)
            values_stacked = np.concatenate([values_stacked, np.repeat(cluster_centers, cluster_center_repeats , axis=2)])

        # set all normalized values to -1 (error value), so error readings have a value also
        normalized_values_stacked = np.full((*self.matrix_shape, values_stacked.shape[-1]), -1)
       
        self.cluster_label_mapping = {}
        for flat_idx, predictor in enumerate(self.cluster_predictors):
            matrix_idx = np.unravel_index(flat_idx, self.matrix_shape)
            sensor_values = values_stacked[matrix_idx[0], matrix_idx[1], :]
            
            # filter out below threshold values -> most probably broken readings
            non_zero_value_indices = sensor_values > self.error_threshold
            sensor_values_filtered = sensor_values[non_zero_value_indices]

            if not np.any(sensor_values_filtered):
              self.feature_disabled[matrix_idx] = 1
            else:
                # fit predictor and return labels computed in training
                cluster_labels_sensor_values = predictor.fit_predict(sensor_values_filtered.reshape(-1, 1))

                # values are computed in the 3rd dimension, store labels in history
                normalized_values_stacked[matrix_idx[0], matrix_idx[1], non_zero_value_indices] = cluster_labels_sensor_values
                
                # create mapping of cluster labels to return values, so cluster labels are ordered by cluster center (low to high)
                cluster_center_label_tuples = list(zip((float(c) for c in predictor.cluster_centers_), range(self.n_clusters)))
                cluster_labels_sorted = [t[1] for t in sorted(cluster_center_label_tuples, key=lambda t: t[0])]
                cluster_label_mapping = {cluster_label: self.return_values[sort_idx] for sort_idx, cluster_label in enumerate(cluster_labels_sorted)}
                self.cluster_label_mapping[flat_idx] = cluster_label_mapping

        # initial calibration
        if not self.normalized_value_history:
            self.normalized_value_history = np.split(normalized_values_stacked, len(values), axis=2)
        
        self.value_history = []
        print("Calibration done!")


    def normalize(self, matrix: np.ndarray):
        if self.value_history_stacked is None:
            print("No value history! Needs calibration before normalization.")
            exit(1)
        
        self.value_history.append(matrix)

        # periodic recalibration
        if len(self.value_history) == self.recalibration_period:
            self.calibrate()
        
        normalized_matrix = np.empty(self.matrix_shape)
        for flat_idx, predictor in enumerate(self.cluster_predictors):
            matrix_idx = np.unravel_index(flat_idx, self.matrix_shape)
            
            # check if feature was disabled during initial calibration
            if self.feature_disabled[matrix_idx]:
                normalized_matrix[matrix_idx] = -1
                continue
            
            # check if sensor value was below threshold -> most probably reading error
            sensor_value = matrix[matrix_idx]
            if sensor_value <= self.error_threshold:
                normalized_matrix[matrix_idx] = self.get_last_value(matrix_idx)
                continue

            prediction = predictor.predict(matrix[matrix_idx[0], matrix_idx[1]].reshape(-1, 1))
            normalized_matrix[matrix_idx] = self.cluster_label_mapping[flat_idx][int(prediction)]

        self.normalized_value_history.append(normalized_matrix)
        return normalized_matrix
    
    def get_last_value(self, matrix_idx):
        offset = 0
        last_value = -1
        
        while last_value == -1:
            if self.normalized_value_history and len(self.normalized_value_history) >= offset + 1:
                last_value = self.normalized_value_history[-(1 + offset)][matrix_idx]
            # elif self.normalized_value_history and not len(self.normalized_value_history) >= offset + 1:
            #     last_value = self.normalized_value_history_stacked[matrix_idx[0], matrix_idx[1], -(1 + offset - len(self.normalized_value_history))]
            # elif not self.normalized_value_history and self.normalized_value_history_stacked.shape[-1] >= offset + 1:
            #     last_value = self.normalized_value_history_stacked[matrix_idx[0], matrix_idx[1], -(1 + offset)]
            else:
                break

            offset += 1
        
        return last_value
     
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

    
    
    