from abc import ABC

import numpy as np

import music_modules
from visualization import Interface
from sound_events import MidiNoteEvent
from midi_note_player import MidiNotePlayer
from utils import load_config


class MatrixProcessor:    
    def __init__(self, config_file: str = 'config.yaml'):
        config = load_config(config_file)
        self.matrix_shape = (config['matrix_shape']['vertical'], config['matrix_shape']['horizontal'])
        self.midi_player = MidiNotePlayer(**config['midi_player'])

        self.modules = []
        for module in config['modules'].values():
            self.set_module(module)

        self.log_file = config['log_file']
        open(self.log_file, 'w').close()

        self.visualization = Interface(modules=self.modules, shape=self.matrix_shape)

    def set_module(self, config: dict):
        module_class = getattr(music_modules, config['module'])
        self.modules.append(module_class(config['setup'], config['sound']))
        
    def process(self, value_matrix: np.ndarray):
        assert value_matrix.shape == self.matrix_shape
        
        sound_events = []
        for module in self.modules:
            sound_events += module.process(value_matrix[module.top:module.bottom,module.left:module.right])
                
        for sound_event in sound_events:
            # match type(sound_event):
            #     case MidiNoteEvent:
            if type(sound_event) == MidiNoteEvent:
                    self.midi_player.play_note(sound_event)

        # render CLI output
        self.visualization.render()

        # logging
        with open(self.log_file, "ab") as file:
            np.save(file, value_matrix)