import time
from collections import deque

import numpy as np

from sound_events import MidiControlEvent
from .base import MusicModule
from module_logger import ModuleLogger


class Hold(MusicModule):
    def __init__(self, setup, sound, module_logger: ModuleLogger):
        super().__init__(setup, module_logger)
        self.time_step_size = sound['time_step_size']
        self.stack_size = sound['stack_size']
        self.delta_t_inc = sound['delta_t_inc'] / sound['time_step_size']
        self.delta_t_dec = sound['delta_t_dec'] / sound['time_step_size']
        self.history = deque(maxlen=self.stack_size)
        self.timer = time.time()
        self.activation = np.zeros([setup['bottom'] - setup['top'], setup['right'] - setup['left']])

    def module_process(self, matrix: np.ndarray):
        self.history.append(matrix)
        if time.time() - self.timer > self.time_step_size:
            events = []
            self.timer = time.time()
            for i, array in enumerate(self.activation):
                for j, _ in enumerate(array):
                    self.activation[i][j] = self.calculate_activation(self.activation[i][j], np.array(self.history)[:, i, j])
                    events.append(MidiControlEvent(
                        channel=self.midi_channel,
                        control=1 + (i * 2) + (j + 1),  # control_values 4, 5, 6, 7
                        value=self.activation[i][j]))
            self.set_info(np.array(self.activation).flatten())
            return events
        return []

    def calculate_activation(self, activation, array):
        light = (array == 0).sum()
        shadow = (array == 1).sum()
        target = 127 * light/(shadow + light)

        if target > activation:
            change = target / self.delta_t_inc
        else:
            change = (target - 127.) / self.delta_t_dec

        if abs(target - activation) < abs(change):
            return int(target)

        return min(int(activation + change), 127)
