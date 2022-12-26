import numpy as np

from sound_events import MidiNoteEvent
from .base import MusicModule
from module_logger import ModuleLogger


class Keyboard(MusicModule):
    def __init__(self, setup, sound, module_logger: ModuleLogger):
        super().__init__(setup, module_logger)
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
        return return_list