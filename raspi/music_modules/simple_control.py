import numpy as np

from sound_events import MidiControlEvent
from .base import MusicModule

class SimpleControl(MusicModule):
    def __init__(self, setup, sound):
        super().__init__(setup)
        self.control = sound['control']

    def module_process(self, matrix: np.ndarray) -> list[MidiControlEvent]:
        value = np.mean(matrix[matrix > 0])
        if not value or np.isnan(value):
            value = 0
        value = int(value)
        
        return [MidiControlEvent(
            channel=self.midi_channel,
            control=self.control,
            value=value)]