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
        self.delta_t = sound['delta_t'] * 1/sound['time_step_size']
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
        switches = 0
        for idx, val in enumerate(self.history):
            if idx > 0:
                switches += ((self.history[idx-1] > 0) & (val <= 0)).sum()
                switches += ((self.history[idx-1] < 0) & (val >= 0)).sum()
                switches += ((self.history[idx-1] == 0) & (val < 0)).sum()
                switches += ((self.history[idx-1] == 0) & (val > 0)).sum()
        self.history = []

        target = 127 * (switches/self.max_freq)
        
        if self.activation == target:
            return self.activation
        

        if target > self.activation:
            increase = target/self.delta_t
        else:
            if self.delta_t > 1:
                increase = (target - self.activation)/(self.delta_t/2)
            
        if increase > 0 and increase > target - self.activation or increase < 0 and increase < target - self.activation:
            increase = target - self.activation


        print(f"Switches: {switches}")
        print(f"Target: {target}")
        print(f"Old Activation: {self.activation}")
        print(f"Increase: {increase}")
        print(f"New Activation: {self.activation + increase}")
        return min(int(self.activation + increase), 127)