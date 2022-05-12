from abc import ABC
import datetime
import numpy as np

from sound_events import MidiNoteEvent


class MusicModule(ABC):
    def __init__(self, setup: dict):
        self.name: str = setup['name']
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
        sound_events = self.module_process(matrix)
        self.post_process(matrix)
        return sound_events
    
    def post_process(self, matrix: np.ndarray):
        self.last_matrix = matrix.copy()

    def get_values(self) -> np.ndarray:
        return self.last_matrix


class Keyboard(MusicModule):
    def __init__(self, setup, config):
        super().__init__(setup)
        # TODO: implement note mapping as given in config file
        self.note_mapping: np.ndarray = np.array(config['note_mapping']).reshape(self.shape[0], self.shape[1])
        self.threshold: float = config['threshold']

    def module_process(self, matrix: np.ndarray):        
        sound_events = []
        for note_idx, difference in np.ndenumerate(matrix - self.last_matrix):
            if difference <= -self.threshold:
                sound_events.append(
                    MidiNoteEvent(
                        note=self.note_mapping[note_idx],
                        velocity=int(min(difference * (-1), MidiNoteEvent.value_range[-1]))
                    )
                )
        return sound_events

class Sequencer(MusicModule):
    def __init__(self, setup, sound):
        super().__init__(setup)
        self.beat_duration = 60 / sound['bpm']
        self.threshold = sound['threshold']
        self.midi_note = sound['midi_note']
        self.start_time = datetime.datetime.now()
        self.beats = 0

    def module_process(self, matrix: np.ndarray):
        return_list = []
        if (datetime.datetime.now() - self.start_time).total_seconds() / self.beat_duration > self.beat_duration * self.beats:
            if matrix[0][self.beats % 8] < self.threshold:
                return_list = [MidiNoteEvent(note=self.midi_note, velocity=int(127), duration = 0.2)]
            self.beats += 1
        return return_list
