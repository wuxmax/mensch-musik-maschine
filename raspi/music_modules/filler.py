import numpy as np
from base import MusicModule
from sound_events import MidiControlEvent


class Filler(MusicModule):
    # variables:
    # - fill_time
    # - empty_time
    # - control

    def __init__(self, setup, sound):
        super().__init__(setup)
        self.fill_time = sound['fill_time']
        self.empty_time = sound['empty_time']
        self.control = sound['control']
        self.value = 0

    def module_process(self, matrix: np.ndarray):
        negative_power = (self.time_since_last_processing / self.empty_time) * (self.negative_value_count / self.value_count)
        positive_power = (self.time_since_last_processing / self.fill_time) * ((self.zero_value_count + self.positive_value_count) / self.value_count)
        self.value -= negative_power
        self.value += positive_power

        return [MidiControlEvent(
            channel=self.midi_channel,
            control=self.control,
            value=self.value)]




