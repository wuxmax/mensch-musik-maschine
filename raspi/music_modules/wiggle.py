import datetime

import numpy as np

from sound_events import MidiControlEvent
from .base import MusicModule


class Wiggle(MusicModule):
    def __init__(self, setup, sound):
        super().__init__(setup)
        self.control = sound['control']
        self.max_freq = sound['max_freq'] * self.shape[0] * self.shape[1]
        self.history = []
        self.timer = datetime.datetime.now()
        self.activation = None
        self.threshold = sound['threshold']

    def module_process(self, matrix: np.ndarray):
        self.history.append(matrix)
        
        if datetime.datetime.now() - self.timer > 1:
            self.timer += 1
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
        return switches/self.max_freq * 127 if switches < self.max_freq else 127