import time

import numpy as np

from sound_events import MidiControlEvent
from .base import MusicModule
from module_logger import ModuleLogger


class Hold(MusicModule):
    def __init__(self, setup, sound, module_logger: ModuleLogger):
        super().__init__(setup)
        self.control = sound['control']
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
            self.history = []

            return [MidiControlEvent(
                channel=self.midi_channel,
                control=self.control,
                value=self.activation)]

        return []

    def calculate_activation(self):
        shadow = 0
        light = 0
        for idx, val in enumerate(self.history):
            light += (self.history[idx] == 0).sum()
            shadow += (self.history[idx] == 1).sum()

        target = 127 * light/(shadow + light)

        if target > self.activation:
            change = target / self.delta_t_inc
        else:
            change = (target - 127.) / self.delta_t_dec
            
        self.set_info('this is working')

        if abs(target - self.activation) < abs(change):
            return int(target)

        return min(int(self.activation + change), 127)
