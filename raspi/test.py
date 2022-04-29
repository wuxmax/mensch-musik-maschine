from cgi import test
from time import sleep

import numpy as np

from matrix_processor import MatrixProcessor
from midi_note_player import MidiNotePlayer

CONFIG_FILE = "config.yml"

matpro = MatrixProcessor(CONFIG_FILE)


test_data0 = np.array([0, 0, 0, 0, 0]).reshape(1,-1)
test_data1 = np.array([100, 0, 0, 0, 0]).reshape(1,-1)
test_data2 = np.array([0, 100, 0, 0, 0]).reshape(1,-1)
test_data3 = np.array([0, 0, 100, 0, 0]).reshape(1,-1)
test_data4 = np.array([0, 0, 0, 100, 0]).reshape(1,-1)
test_data5 = np.array([0, 0, 0, 0, 100]).reshape(1,-1)

test_data6 = np.array([100, 0, 0, 0, 0]).reshape(1,-1)
test_data7 = np.array([100, 100, 0, 0, 0]).reshape(1,-1)


# test_data = [test_data1, test_data0, test_data2, test_data0, test_data3, test_data0, test_data4, test_data0, test_data5, test_data0] * 100
# test_data = [test_data1, test_data2, test_data3, test_data4, test_data5] * 100
test_data = [test_data6, test_data7]


if __name__ == "__main__":
    # matpro.midi_player.reset()
    
    

    # try:
    #     for value_matrix in test_data * 100:
    #         print(value_matrix)
    #         matpro.process(value_matrix)
    #         sleep(1)
    # except KeyboardInterrupt:
    #     matpro.midi_player.reset()
        