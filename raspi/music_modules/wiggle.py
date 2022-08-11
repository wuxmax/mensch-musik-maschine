import time

import numpy as np

from sound_events import MidiControlEvent
from .base import MusicModule


class Wiggle(MusicModule):
    def __init__(self, setup, sound):
        super().__init__(setup)
        self.control = sound['control']
        self.max_freq = sound['max_freq'] * self.shape[0] * self.shape[1]
        self.time_step_size = sound['time_step_size']
        self.delta_t_inc = sound['delta_t_inc'] / sound['time_step_size']
        self.delta_t_dec = sound['delta_t_dec'] / sound['time_step_size']
        self.history = []
        self.timer = time.time()
        self.activation = 0

    def module_process(self, matrix: np.ndarray):
        self.history.append(matrix)
        
        if time.time() - self.timer > self.time_step_size:
            self.timer += self.time_step_size
            self.activation = self.calculate_activation()
        
            return [MidiControlEvent(
                channel=self.midi_channel,
                control=self.control,
                value=self.activation)]
        
        return []

    def calculate_activation(self):
        print(f"Activation: {self.activation}")
        
        switches = 0
        for idx, val in enumerate(self.history):
            if idx > 0:
                # switches += ((self.history[idx-1] > 0) & (val <= 0)).sum()
                # switches += ((self.history[idx-1] < 0) & (val >= 0)).sum()
                # switches += ((self.history[idx-1] == 0) & (val < 0)).sum()
                # switches += ((self.history[idx-1] == 0) & (val > 0)).sum()
                switches += (self.history[idx-1] != val).sum()
        self.history = []

        print(f"Switches: {switches}")

        target = 127 * (switches / self.max_freq)

        if target > self.activation:
            change = target / self.delta_t_inc
        else:
            change = (self.activation - target) / self.delta_t_dec

        if abs(target - self.activation) < change:
            return int(target)

        return min(int(self.activation + change), 127)