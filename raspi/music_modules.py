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

    def process(self, sub_matrix: np.ndarray):
        raise NotImplementedError

    def get_values(self) -> np.ndarray:
        return np.zeros((self.bottom, self.right))


class Keyboard(MusicModule):
    def __init__(self, setup, config):
        super().__init__(setup)
        # TODO: implement note mapping as given in config file
        self.note_mapping: np.ndarray = np.array([28, 31, 33, 35, 38]).reshape(1, -1)
        self.threshold: float = config['threshold']

        self.last_matrix: np.ndarray = np.zeros(self.note_mapping.shape)

    def process(self, matrix: np.ndarray):
        assert matrix.shape == self.note_mapping.shape
        
        sound_events = []
        
        for note_idx, difference in np.ndenumerate(matrix - self.last_matrix):
            if difference > self.threshold:
                sound_events.append(MidiNoteEvent(note=self.note_mapping[note_idx], velocity=int(difference)))

        self.last_matrix = matrix
        return sound_events

    def get_values(self) -> np.ndarray:
        return self.last_matrix


class Sequencer(MusicModule):
    def __init__(self, setup, config):
        super().__init__(setup)
        self.beat_duration = 60 / setup['bpm']
        self.threshold = config['threshold']
        self.midi_note = config['midi_note']
        self.start_time = datetime.datetime.now()
        self.beats = 0

    def process(self, matrix: np.ndarray):
        return_list = []
        if (datetime.datetime.now() - self.start_time).total_seconds() / self.beat_duration > self.beat_duration * self.beats:
            if matrix[0][self.beats % 8] > self.threshold:
                return_list = [MidiNoteEvent(note=self.midi_note, velocity=int(127))]
            self.beats += 1
        return return_list
