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

    def get_values(self) -> np.ndarray:
        return np.zeros((self.bottom, self.right))


class Keyboard(MusicModule):
    def __init__(self, setup, config):
        super().__init__(setup)

        self.note_mapping: np.ndarray = np.array([100, 110, 90, 40, 80]).reshape(1,-1)
        self.last_matrix: np.ndarray = np.zeros(self.note_mapping.shape)
        self.threshold: float = config['threshold']

    def process(self, matrix: np.ndarray):
        assert matrix.shape == self.note_mapping.shape
        
        sound_events = []
        
        for note_idx, difference in np.ndenumerate(np.abs(matrix - self.last_matrix)):
            if difference > self.threshold:
                sound_events.append(MidiNoteEvent(note=self.note_mapping[note_idx], velocity=difference))

        self.last_matrix = matrix
        return sound_events

    def get_values(self) -> np.ndarray:
        return self.last_matrix