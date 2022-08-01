import numpy as np

from base import MusicModule
from raspi.sound_events import MidiControlEvent

class SimpleControl(MusicModule):
    def __init__(self, setup, sound):
        super().__init__(setup)
        self.control = sound['control']

    def module_process(self, matrix: np.ndarray):

        value = np.mean(matrix[matrix > 0])
        if not value or np.isnan(value):
            value = 0
        value = int(value)
        
        return [MidiControlEvent(
            channel=self.midi_channel,
            control=self.control,
            value=abs(int(np.mean(matrix))))]
