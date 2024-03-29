from collections import deque
from math import copysign

import numpy as np

from sound_events import MidiControlEvent
from .base import MusicModule

class Fader(MusicModule):
    def __init__(self, setup, sound):
        super().__init__(setup)
        try:
            assert self.shape[0] == 1
        except AssertionError:
            print(f"Fader matrix shape must be (1, X), but is {self.shape}")
            exit(1)

        self.control_left = sound['control_left']
        self.control_right = sound['control_right']
        self.window_size_move = sound['window_size_move']
        self.window_size_drop = sound['window_size_drop']
        self.error_threshold = sound['error_threshold']
        self.position_history = deque([], maxlen=self.window_size_drop)
        self.last_midi_values = {self.control_left: None, self.control_right: None}
        self.fader_side = None
    
    
    def module_process(self, matrix: np.ndarray) -> list[MidiControlEvent]:
        position = self.single_shadow_pos(matrix)
        self.position_history.append(position)

        # print(f"{position=}")
        # print(f"{self.position_history=}")
        # print(f"{self.fader_side=}")

        # wait for position history to be filled
        if not len(self.position_history) == self.window_size_drop:
            return []
    
        # if there is no shadow for the entire window size, reset both faders
        if self.fader_side and position is None and all_equal(self.position_history):
            self.fader_side = None
            return self.get_return_values(127, self.control_left) + self.get_return_values(0, self.control_right)
            
        # check if all positions in position history are equal (cant slice a deque)
        if not all_equal([self.position_history[i] for i in range(self.window_size_drop - self.window_size_move, self.window_size_drop)]):
            return []

        # if there is no single shadow just now, do nothing
        if position is None:
            return []
        
        # if no last fader, start 'new fader' based on on which half we started
        if not self.fader_side and position <= int(self.shape[1] / 2):
            self.fader_side = 'left'
        elif not self.fader_side:
            self.fader_side = 'right'
    
        if self.fader_side == 'left':
            midi_value = self.get_midi_value(self.shape[1] - position)  # reversed because of effect
            return_values = self.get_return_values(midi_value, self.control_left)
        else:
            midi_value = self.get_midi_value(self.shape[1] - position)  # reversed because of direction
            return_values = self.get_return_values(midi_value, self.control_right)

        # print(f"{position=}")
        # print(f"{self.position_history=}")
        # print(f"{self.fader_side=}")
        
        # print(return_values)

        return return_values

            
    def single_shadow_pos(self, matrix):
        zero_value_indices = np.nonzero(matrix.squeeze() == 0)[0]
        
        # print(f"{matrix=}")
        # print(f"{zero_value_indices=}")
        # print(f"{zero_value_indices.shape=}")
        
        if not zero_value_indices.shape[0]:
            return None
        
        if zero_value_indices.shape[0] == 1:
            return zero_value_indices[0]

        if zero_value_indices.shape[0] > 1 and np.all(np.diff(zero_value_indices) <= 1 + self.error_threshold):
            return float(zero_value_indices[0] + (zero_value_indices[-1] - zero_value_indices[0]) / 2)
            
        return None


    def get_return_values(self, midi_value, midi_control):
        if not self.last_midi_values[midi_control]:
            self.last_midi_values[midi_control] = midi_value
        
        direction = int(copysign(1, midi_value - self.last_midi_values[midi_control]))

        return_events = [MidiControlEvent(
                channel=self.midi_channel,
                control=midi_control,
                value=value) for value in range(self.last_midi_values[midi_control], midi_value, direction)]
            
        self.last_midi_values[midi_control] = midi_value
        return return_events
     
     
    def get_midi_value(self, position: float) -> int:
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


def all_equal(iterator):
    return len(set(iterator)) <= 1