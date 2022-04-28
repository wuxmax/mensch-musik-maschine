import numpy as np

from matrix_processor import MatrixProcessor

CONFIG_FILE = "config.yml"

matpro = MatrixProcessor(CONFIG_FILE)


# test_data1 = np.zeros(config['matrix_shape']['horizontal'], config['matrix_shape']['vertical'])
test_data1 = np.array([0, 0, 0, 0, 0]).reshape(1,-1)

#test_data2 = np.zeros(config['matrix_shape']['horizontal'], config['matrix_shape']['vertical'])
test_data2 = np.array([100, 0, 100, 0, 100]).reshape(1,-1)


if __name__ == "__main__":
    matpro.process(test_data1)
    matpro.process(test_data2)

