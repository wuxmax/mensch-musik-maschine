from time import sleep

import click
import numpy as np

from matrix_processor import MatrixProcessor
from utils import load_config

CONFIG_FILE = "config.yml"

test_data0 = np.array([0, 0, 0, 0, 0]).reshape(1,-1)
test_data1 = np.array([100, 0, 0, 0, 0]).reshape(1,-1)
test_data2 = np.array([0, 100, 0, 0, 0]).reshape(1,-1)
test_data3 = np.array([0, 0, 100, 0, 0]).reshape(1,-1)
test_data4 = np.array([0, 0, 0, 100, 0]).reshape(1,-1)
test_data5 = np.array([0, 0, 0, 0, 100]).reshape(1,-1)
test_data6 = np.array([100, 0, 0, 0, 0]).reshape(1,-1)
test_data7 = np.array([100, 100, 0, 0, 0]).reshape(1,-1)


@click.command()
@click.option('--apply_log', default=False, is_flag=True,
              help='Reapply sensor activation data from log file specified in config')
def start_mmm(apply_log):
    # start MatrixProcessor
    matpro = MatrixProcessor(CONFIG_FILE)
    matpro.midi_player.reset()

    if apply_log:
        log_file = load_config(CONFIG_FILE)['log_file']
        with open(log_file, "rb") as file:
            while True:
                try:
                    value_matrix = np.load(file, allow_pickle=True)
                    print(value_matrix)
                    matpro.process(value_matrix)
                    sleep(1)
                except Exception:
                    matpro.midi_player.reset()
                    break
    else:
        test_data = [test_data6, test_data7]
        try:
            for value_matrix in test_data * 100:
                print(value_matrix)
                matpro.process(value_matrix)
                sleep(1)
        except KeyboardInterrupt:
            matpro.midi_player.reset()


if __name__ == "__main__":
    start_mmm()

