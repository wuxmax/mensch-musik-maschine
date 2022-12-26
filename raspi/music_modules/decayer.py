import time

import numpy as np

from sound_events import MidiControlEvent
from .base import MusicModule
from ..module_logger import ModuleLogger


class Decayer(MusicModule):
    def __init__(self, setup, sound, module_logger: ModuleLogger):
        super().__init__(setup)
        self.control = sound['control']
        self.decay_rate = sound['decay_rate']
        self.decay_delay = sound['decay_delay']

        self.activation = 0
        self.activation_timestamps = [time.time()]
        self.timestamps_needed = 6
        self.old_matrix = []


    def module_process(self, matrix: np.ndarray):
        if self.old_matrix != [] and np.any(matrix - self.old_matrix):
            self.activation_timestamps.append(time.time())
            if len(self.activation_timestamps) > self.timestamps_needed:
                self.activation_timestamps.pop(0)
        self.old_matrix = matrix

        new_value = 0
        for timestamp in self.activation_timestamps:
            decay_time = time.time() - timestamp - self.decay_delay
            signal_loss = np.clip(decay_time * self.decay_rate, 0, 1)
            new_value += int(100 * (1 - signal_loss) / self.timestamps_needed)
        if new_value == 0:
            new_value = 20

        self.set_info('this is working')

        if self.activation != new_value:
            self.activation = new_value


            return [MidiControlEvent(
                channel=self.midi_channel,
                control=self.control,
                value=self.activation)]
        
        return []
