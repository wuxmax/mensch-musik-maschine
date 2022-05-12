from time import sleep

import click
import numpy as np

from matrix_processor import MatrixProcessor
from utils import load_config

CONFIG_FILE = "config.yml"

test_data0 = np.array([[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]])
test_data1 = np.array([[100, 0, 0, 0, 0, 0, 0, 0], [700, 0, 0, 0, 700, 0, 0, 0]])
test_data2 = np.array([[100, 0, 0, 0, 0, 0, 0, 0], [700, 0, 0, 0, 700, 0, 0, 0]])
test_data3 = np.array([[0, 0, 0, 0, 0, 0, 0, 0], [700, 0, 0, 0, 700, 0, 0, 0]])
test_data4 = np.array([[0, 100, 0, 0, 0, 0, 0, 0], [700, 0, 0, 0, 700, 0, 0, 0]])
test_data5 = np.array([[0, 0, 100, 0, 0, 0, 0, 0], [700, 0, 0, 0, 700, 0, 0, 0]])
test_data6 = np.array([[0, 0, 0, 100, 0, 0, 0, 0], [700, 0, 0, 0, 700, 0, 0, 0]])
test_data7 = np.array([[0, 0, 0, 0, 100, 0, 0, 0], [700, 0, 0, 0, 700, 0, 0, 0]])


@click.command()
@click.option('--apply_log', default='',
              help='Reapply sensor activation data from log file specified')
def start_mmm(apply_log):
    # start MatrixProcessor
    matpro = MatrixProcessor(CONFIG_FILE, logging=not bool(apply_log))
    matpro.midi_player.reset()

    if apply_log:
        log_file = 'logs/' + apply_log
        with open(log_file, "rb") as file:
            value_matrix = np.loadtxt(file, delimiter=',')
            shape = matpro.matrix_shape[0], matpro.matrix_shape[1]
            entries_per_activation = shape[0] * shape[1]
            log_entries_count = int(value_matrix.size / entries_per_activation)
            value_matrix = value_matrix.reshape(log_entries_count, shape[0], shape[1])
            for entry in value_matrix:
                print(entry)
                matpro.process(entry)
                sleep(0.15)
    else:
        test_data = [test_data0, test_data1, test_data2, test_data3, test_data4, test_data5, test_data6, test_data7]
        try:
            for value_matrix in test_data * 100:
                print(value_matrix)
                matpro.process(value_matrix)
                sleep(1)
        except KeyboardInterrupt:
            matpro.midi_player.reset()


if __name__ == "__main__":
    start_mmm()

