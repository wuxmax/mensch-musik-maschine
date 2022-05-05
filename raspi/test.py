import ast

import numpy as np

from matrix_processor import MatrixProcessor
from utils import load_config

CONFIG_FILE = "config.yml"

matpro = MatrixProcessor(CONFIG_FILE)


# test_data1 = np.zeros(config['matrix_shape']['horizontal'], config['matrix_shape']['vertical'])
test_data1 = np.array([0, 0, 0, 0, 0]).reshape(1,-1)

#test_data2 = np.zeros(config['matrix_shape']['horizontal'], config['matrix_shape']['vertical'])
test_data2 = np.array([100, 0, 100, 0, 100]).reshape(1,-1)

def read_and_print_log():
    log_file = load_config(CONFIG_FILE)['log_file']
    with open(log_file, "rb") as file:
        while True:
            try:
                print(np.load(file, allow_pickle=True))
            except:
                break

if __name__ == "__main__":
    matpro.process(test_data1)
    matpro.process(test_data2)

    read_and_print_log()

