import numpy as np
from tqdm import tqdm

from i2c_reader import I2CReader
from raspi.config_manager import ConfigManager
from raspi.value_stack import ValueStack
from utils import load_config


class MatrixDataPreprocessor:
    def __init__(self, config_manager: ConfigManager, value_stack: ValueStack):
        self.config_manager = config_manager
        self.value_stack = value_stack
        self.cluster_borders = [[-1 for _ in range(self.config_manager.n_device_sensors())] for _ in range(len(self.config_manager.i2c_addresses()))]
        print(self.cluster_borders)

    def normalize(self, matrix: np.ndarray):
        if self.cluster_borders[0][0] == -1:
            print("No values! Needs calibration before normalization.")
            exit(1)
        return_matrix = matrix.copy()
        for x in range(len(matrix)):
            for y in range(len(matrix[x])):
                return_matrix[x][y] = 1 if matrix[x][y] > self.cluster_borders[x][y] else 0
        return return_matrix

    def calibrate(self, i2c_addess: str = ''):
        if i2c_addess:
            index = self.config_manager.i2c_addresses().index(int(i2c_addess))
            print(index)
            values = self.value_stack.get_values()
            self.cluster_borders = [[self.calibrate_sensor(np.array(values)[:, i, j])
                                    for j in range(len(values[0][0]))] for i in [index]]
            self.value_stack.update_init_values(self.cluster_borders, index)
        else:
            values = self.value_stack.get_values()
            self.cluster_borders = [[self.calibrate_sensor(np.array(values)[:, i, j])
                                    for j in range(len(values[0][0]))] for i in range(len(values[0]))]
            self.value_stack.update_init_values(self.cluster_borders)

    def calibrate_sensor(self, array):
        smallest_values = np.partition(array, self.config_manager.n_smallest_values())[:self.config_manager.n_smallest_values() - 1]
        return smallest_values.mean() + self.config_manager.threshold()


if __name__=="__main__":
    cm = ConfigManager(config_name='config_real.yml')

    vs = ValueStack(cm)
    datpro = MatrixDataPreprocessor(cm, vs)

    vs.append([[1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6]])
    vs.append([[1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6]])
    vs.append([[1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6]])
    vs.append([[1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6]])
    vs.append([[1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6]])
    vs.append([[1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6]])
    vs.append([[1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6]])
    vs.append([[1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6]])
    vs.append([[1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6]])
    vs.append([[1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6]])
    vs.append([[1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6]])
    datpro.calibrate()
    print(vs.init_values)
    print(datpro.normalize([[51, 2, 53, 4, 55, 6], [1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6]]))



