from collections import deque
from itertools import groupby
from math import copysign

import numpy as np

from sound_events import MidiControlEvent
from .base import MusicModule

class SimpleControl(MusicModule):
    def __init__(self, setup, sound):
        super().__init__(setup)
        self.control = sound['control']

    def module_process(self, matrix: np.ndarray) -> list(MidiControlEvent):
        value = np.mean(matrix[matrix > 0])
        if not value or np.isnan(value):
            value = 0
        value = int(value)
        
        return [MidiControlEvent(
            channel=self.midi_channel,
            control=self.control,
            value=value)]


class Fader(MusicModule):
    def __init__(self, setup, sound):
        super().__init__(setup)
        self.control = sound['control']
        self.buffer_size = sound['buffer_size']
        self.pos_buffer = deque([], maxlen=self.buffer_size)
        self.last_midi_value = None

    
    def module_process(self, matrix: np.ndarray) -> list(MidiControlEvent):
        # get matrix postion with highest value
        position = np.argmax(value)
        self.pos_buffer.append(position)
        
        if not len(self.pos_buffer) == self.buffer_size:
            return []

        if all_equal(self.pos_buffer):
            midi_value = get_midi_value(position)
            direction = copysign(midi_value - self.last_midi_value)

            return_events = [MidiControlEvent(
                channel=self.midi_channel,
                control=self.control,
                value=value) for value in range(self.last_midi_value, midi_value, direction)]
            
            self.last_midi_value = midi_value
            return return_events

    def get_midi_value(position: float) -> int:
        # Figure out how 'wide' each range is
        fader_range_min = self.shape[1][0]
        fader_range_max = self.shape[1][-1]
        fader_range = fader_range_max - fader_range_mi
        midi_range_min = MidiControlEvent.value_range[0]
        midi_range_max = MidiControlEvent.value_range[-1] 
        midi_range = midi_range_max - midi_range_min

        # Convert the left range into a 0-1 range (float)
        value_scaled = float(position - fader_range_min) / float(fader_range)

        # Convert the 0-1 range into a value in the right range.
        return int(midi_range_min + (value_scaled * midi_range))

    def all_equal(iterable):
        g = groupby(iterable)
        return next(g, True) and not next(g, False)