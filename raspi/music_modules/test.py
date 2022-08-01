import time

from sound_events import MidiControlEvent
from .base import MusicModule

import numpy as np

class MidiTester(MusicModule):
    def __init__(self, setup, sound):
        super().__init__(setup)
        self.control = sound['control']

        self.counter = 0

    def module_process(self, matrix: np.ndarray):
        time.sleep(0.2)

        self.counter += 1
        if self.counter == 128:
            self.counter = 0

        return [MidiControlEvent(
            channel=self.midi_channel, 
            control=self.control, 
            value=self.counter)]