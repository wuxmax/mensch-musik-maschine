from abc import ABC
import numpy as np

from sound_events import MidiNoteEvent

class MusicModule(ABC):
    def __init__(self, setup: dict):
        self.name: str = setup['name']
        self.top: int = setup['top']
        self.left: int = setup['left']
        self.bottom: int = setup['bottom']
        self.right: int = setup['right']
        
    def process(sub_matrix: np.ndarray):
        raise NotImplementedError


class Keyboard(MusicModule):
    def __init__(self, setup, config):
        super().__init__(setup)
        # TODO: implement note mapping as given in config file
        self.note_mapping: np.ndarray = np.array([28, 31, 33, 35, 38]).reshape(1,-1)
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