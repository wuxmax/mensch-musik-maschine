from typing import Tuple, Dict
from abc import ABC
import sys
import yaml
import numpy as np

from utils import load_config
from sound_events import MidiNoteEvent

class MusicModule(ABC):
    def __init__(self, setup: Dict):
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

class MatrixProcessor:    
    def __init__(self, config_file: str = 'config.yaml'):
        config = load_config(config_file)
        self.matrix_shape = (config['matrix_shape']['vertical'], config['matrix_shape']['horizontal'])

        self.modules = []
        for module_name in config['modules']:
            self.set_module(config['modules'][module_name])

    def set_module(self, config: Dict):
        module_class = getattr(sys.modules[__name__], config['module'])
        self.modules.append(module_class(config['setup'], config['sound']))
        
    def process(self, value_matrix: np.ndarray):
        assert value_matrix.shape == self.matrix_shape
        
        for module in self.modules:
            module.process(value_matrix[module.top:module.bottom,module.left:module.right])