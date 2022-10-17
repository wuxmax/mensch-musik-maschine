import time

import numpy as np

from sound_events import MidiControlEvent
from .base import MusicModule


class Decayer(MusicModule):
    def __init__(self, setup, sound):
        super().__init__(setup)
        self.control = sound['control']
        self.decay_rate = sound['decay_rate']
        self.decay_delay = sound['decay_delay']

        self.activation = 0
        self.activation_timestamp = None
        self.info = ''

    def get_info(self) -> str:
        return self.info

    def module_process(self, matrix: np.ndarray):
        if np.any(matrix):
            self.activation_timestamp = time.time()
        
        decay_time = time.time() - self.activation_timestamp - self.decay_delay
        signal_loss = np.clip(decay_time * self.decay_rate, 0, 1)

        new_value = int(127 * (1 - signal_loss))
        if self.activation != new_value:
            self.activation = new_value
            self.info = f"Hold: {self.activation}"

            return [MidiControlEvent(
                channel=self.midi_channel,
                control=self.control,
                value=self.activation)]
        
        return []