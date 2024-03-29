import time

import numpy as np

from sound_events import MidiControlEvent
from .base import MusicModule


class Hold(MusicModule):
    def __init__(self, setup, sound):
        super().__init__(setup)
        self.control = sound['control']
        self.time_step_size = sound['time_step_size']
        self.delta_t_inc = sound['delta_t_inc'] / sound['time_step_size']
        self.delta_t_dec = sound['delta_t_dec'] / sound['time_step_size']
        self.history = []
        self.timer = time.time()
        self.activation = 0
        self.info = ''

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

    def get_info(self) -> str:
        return self.info

    def calculate_activation(self):
        shadow = 0
        light = 0
        for idx, val in enumerate(self.history):
            light += (self.history[idx] == 0).sum()
            shadow += (self.history[idx] == 1).sum()
        # self.info = f"Hold: {shadow}; {light}"

        target = 127 * light/(shadow + light)

        if target > self.activation:
            change = target / self.delta_t_inc
        else:
            change = (target - 127.) / self.delta_t_dec
            

        if abs(target - self.activation) < abs(change):
            return int(target)

        return min(int(self.activation + change), 127)
