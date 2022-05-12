from re import M
from matrix_processor import MatrixProcessor
from i2c_reader import I2CReader

from sound_events import MidiNoteEvent
from time import sleep

CONFIG_FILE = "config.yml"

matpro = MatrixProcessor(CONFIG_FILE)
reader = I2CReader()


if __name__ == "__main__":
    while True:
        matpro.process(reader.get_value_matrix())
        # sleep(3)
    
    # while True:
    #     matpro.midi_player.play_note(MidiNoteEvent(69, 100))
    #     sleep(2)

