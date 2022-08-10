from collections import deque
from itertools import groupby
from math import copysign

import numpy as np

from sound_events import MidiControlEvent
from .base import MusicModule

class Fader(MusicModule):
    def __init__(self, setup, sound):
        super().__init__(setup)
        try:
            assert self.matrix_shape[0] == 1
        except AssertionError:
            print(f"Fader matrix shape must be (1, X), but is {self.matrix_shape}")
            exit(1)

        self.control_left = sound['control_left']
        self.control_right = sound['control_right']
        self.window_size = sound['window_size']
        self.error_threshold = sound['error_threshold']
        self.position_history = deque([], maxlen=self.window_size)
        self.last_midi_values = {self.control_left: None, self.control_right: None}
        self.fader_side = None
    

    
    def module_process(self, matrix: np.ndarray) -> list[MidiControlEvent]:
        position = self.single_shadow_pos(matrix)
        self.position_history.append(position)

        # wait for position history to be filled
        if not len(self.position_history) == self.window_size:
            return []
        
        # if there is no shadow for the entire window size, reset both faders
        if all(pos is None for pos in self.position_history):
            self.fader_side = None
            return self.get_return_values(self, 0, self.control_left) + self.get_return_values(self, 0, self.control_right)
        
        # if there is no single shadow just now, do nothing
        if position is None:
            return []
        
        # if no last fader, start 'new fader' based on on which half we started
        if position <= int(self.matrix_shape[1] / 2):
            self.fader_side = 'left'
        else:
            self.fader_side = 'right'
    
        if self.fader_side == 'left':
            midi_value = self.get_midi_value(position)
            return_values = self.get_return_values(midi_value, self.control_left)
        else:
            midi_value = self.get_midi_value(self.matrix_shape[1] - position)
            return_values = self.get_return_values(midi_value, self.control_right)

        print(f"{position=}")
        print(f"{self.position_history=}")
        print(f"{self.fader_side=}")
        
        
        return return_values

            
    def single_shadow_pos(self, matrix):
        zero_value_indices = matrix == 0
        if not zero_value_indices:
            return None
        
        if zero_value_indices.shape[0] == 1:
            return zero_value_indices[0]

        if zero_value_indices.shape[0] > 1 and np.all(np.diff(zero_value_indices) <= 1 + self.error_threshold):
            return int(zero_value_indices[-1] - zero_value_indices[0] / 2)
            
        return None


    def get_return_values(self, midi_value, midi_control):
        if not self.last_midi_value[midi_control]:
            self.last_midi_value[midi_control] = midi_value
        
        direction = int(copysign(1, midi_value - self.last_midi_value))

        return_events = [MidiControlEvent(
                channel=self.midi_channel,
                control=midi_control,
                value=value) for value in range(self.last_midi_value[midi_control], midi_value, direction)]
            
        self.last_midi_value[midi_control] = midi_value
        return return_events
     
     
    def get_midi_value(self, position: int) -> int:
        # Figure out how 'wide' each range is
        fader_range_min = 0
        fader_range_max = self.shape[1]
        fader_range = fader_range_max - fader_range_min
        midi_range_min = MidiControlEvent.value_range[0]
        midi_range_max = MidiControlEvent.value_range[-1] 
        midi_range = midi_range_max - midi_range_min

        # Convert the left range into a 0-1 range (float)
        value_scaled = float(position - fader_range_min) / float(fader_range)

        # Convert the 0-1 range into a value in the right range.
        return int(midi_range_min + (value_scaled * midi_range))


# def all_equal(iterable):
#     g = groupby(iterable)
#     return next(g, True) and not next(g, False)