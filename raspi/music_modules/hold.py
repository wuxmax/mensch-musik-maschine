import time

import numpy as np

from sound_events import MidiControlEvent
from .base import MusicModule


class Hold(MusicModule):
    def __init__(self, setup, sound):
        super().__init__(setup)
        self.control = sound['control']
        self.time_step_size = sound['time_step_size']
        self.timer = time.time()
        self.activation = 0
        self.sensor_activation_buckets = np.zeros(self.shape)
        self.decay_rate = sound['decay_rate']

    def module_process(self, matrix: np.ndarray):
        if time.time() - self.timer > self.time_step_size:
            self.timer += self.time_step_size
            self.sensor_activation_buckets[matrix > 0] = np.minimum(self.sensor_activation_buckets[matrix > 0] + self.bucket_increase, self.bucket_size)
            self.sensor_activation_buckets[matrix <= 0] = np.maximum(self.sensor_activation_buckets[matrix <= 0] - self.decay_rate, 0)
            self.activation = (self.sensor_activation_buckets.sum() / (self.shape[0] * self.shape[1] * self.bucket_size)) * 127
        
            return [MidiControlEvent(
                channel=self.midi_channel,
                control=self.control,
                value=self.activation)]
        
        return []