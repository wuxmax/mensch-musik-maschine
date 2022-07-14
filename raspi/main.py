from time import sleep

from data_preprocessor import MatrixDataPreprocessor
from matrix_processor import MatrixProcessor
from i2c_reader import I2CReader
from sound_events import MidiNoteEvent
from utils import load_config


CONFIG_FILE = "config.yml"

config = load_config(CONFIG_FILE)
reader = I2CReader()
datpro = MatrixDataPreprocessor(config)
matpro = MatrixProcessor(config)


import threading


if __name__ == "__main__":
    print("Calibrating...")
    reference_values = [reader.get_value_matrix() for _ in range(config['data_preprocessor']['calibration_period'])]
    datpro.calibrate(reference_values)
    print("Calibration done!")

    
    while True:
        sensor_values = reader.get_value_matrix()
        normalized_values = datpro.normalize(sensor_values)
        
        print(threading.active_count())
        
        matpro.process(normalized_values)
        sleep(1)
    
    # while True:
    #     matpro.midi_player.play_note(MidiNoteEvent(69, 100))
    #     sleep(2)

