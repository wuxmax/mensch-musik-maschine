from abc import ABC
import datetime
import time

import numpy as np

from sound_events import MidiNoteEvent, MidiControlEvent


class MusicModule(ABC):
    def __init__(self, setup: dict):
        self.name: str = setup['name']
        self.midi_channel: int = setup['midi_channel']
        self.top: int = setup['top']
        self.left: int = setup['left']
        self.bottom: int = setup['bottom']
        self.right: int = setup['right']
        self.shape = (setup['bottom'] - setup['top'], setup['right'] - setup['left'])
        self.last_matrix: np.ndarray = np.zeros(self.shape)

    def pre_process(self, matrix: np.ndarray):
        try:
            assert matrix.shape == self.shape
        except AssertionError:
            print(f"AssertionError: matrix shape: {matrix.shape} != module shape: {self.shape}")
    
    def process(self, matrix: np.ndarray):
        self.pre_process(matrix)
        return_events = self.module_process(matrix)
        self.post_process(matrix)
        return return_events
    
    def post_process(self, matrix: np.ndarray):
        self.last_matrix = matrix.copy()

    def get_values(self) -> np.ndarray:
        return self.last_matrix


class Keyboard(MusicModule):
    def __init__(self, setup, sound):
        super().__init__(setup)
        self.note_duration = sound['note_duration']
        self.note_mapping: np.ndarray = np.array(sound['note_mapping']).reshape(self.shape[0], self.shape[1])
        
    def module_process(self, matrix: np.ndarray):        
        return_list = []
        for idx, product in np.ndenumerate(matrix * self.last_matrix):
            if product <= 0 and (product == 0 and matrix[idx] != self.last_matrix[idx]):
                return_list.append(
                    MidiNoteEvent(
                        channel=self.midi_channel,
                        note=self.note_mapping[idx],
                        velocity=abs(int(matrix[idx]))
                    )
                )
        # print(f"keyboard: {sound_events}")
        return return_list
        

class Sequencer(MusicModule):
    def __init__(self, setup, sound):
        super().__init__(setup)
        self.beat_duration = 60 / sound['bpm']
        self.note_duration = sound['note_duration']
        self.midi_note = sound['midi_note']
        self.start_time = datetime.datetime.now()
        self.beats = 0

    def module_process(self, matrix: np.ndarray):
        return_list = []
        # check for correct time
        if (datetime.datetime.now() - self.start_time).total_seconds() / self.beat_duration > self.beat_duration * self.beats:
            # check for correct value
            if matrix[0][self.beats % self.shape[1]] != 0:
                return_list = [
                    MidiNoteEvent(
                        channel=self.midi_channel,
                        note=self.midi_note,
                        velocity=MidiNoteEvent.value_range[-1],
                        duration=self.note_duration)
                        ]
            self.beats += 1
        
        # print(f"sequencer: {return_list}")
        return return_list

class MiniSequencer(MusicModule):
    def __init__(self, setup, sound):
        super().__init__(setup)
        self.beat_duration = 60 / sound['bpm']
        self.note_duration = sound['note_duration']
        self.midi_note = sound['midi_note']
        self.start_time = datetime.datetime.now()
        self.beats = 0

    def module_process(self, matrix: np.ndarray):
        return_list = []
        # check for correct time
        if (datetime.datetime.now() - self.start_time).total_seconds() / self.beat_duration > self.beat_duration:
            # check for correct value
            if matrix[0][0] != 0:
                return_list = [
                    MidiNoteEvent(
                        channel=self.midi_channel,
                        note=self.midi_note,
                        velocity=MidiNoteEvent.value_range[-1],
                        duration=self.note_duration)
                        ]

        # print(f"sequencer: {return_list}")
        return return_list


class SimpleControl(MusicModule):
    def __init__(self, setup, sound):
        super().__init__(setup)
        self.control = sound['control']

    def module_process(self, matrix: np.ndarray):
        return [MidiControlEvent(
            channel=self.midi_channel,
            control=self.control,
            value=abs(int(np.mean(matrix))))]


class MidiTester(MusicModule):
    def __init__(self, setup, sound):
        super().__init__(setup)
        self.control = sound['control']

        self.counter = 0

    def module_process(self, matrix: np.ndarray):
        time.sleep(0.2)

        self.counter += 1
        if self.counter == 128:
            self.counter = 0

        return [MidiControlEvent(
            channel=self.midi_channel, 
            control=self.control, 
            value=self.counter)]



