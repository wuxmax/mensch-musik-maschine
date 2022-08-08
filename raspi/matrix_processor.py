import datetime

import numpy as np

import sound_events
import midi_controller
import music_modules
from visualization import Interface
from utils import load_config


class MatrixProcessor:    
    def __init__(self, config: dict, printing=True, logging=False):
        self.matrix_shape = (config['matrix_shape']['vertical'], config['matrix_shape']['horizontal'])
        self.midi_note_player = midi_controller.MidiNotePlayer(**config['midi_controller'], **config['midi_note_player'])
        self.midi_control_changer = midi_controller.MidiControlChanger(**config['midi_controller'])

        self.modules = []
        for module in config['modules'].values():
            self.set_module(module)

        self.logging = logging
        if self.logging:
            self.log_file = 'logs/log_' + datetime.datetime.now().strftime('%d%m%Y-%H:%M:%S') + '.csv'

        self.printing = printing
        if self.printing:
            self.visualization = Interface(modules=self.modules, shape=self.matrix_shape)

    def set_module(self, config: dict):
        module_class = getattr(music_modules, config['module'])
        self.modules.append(module_class(config['setup'], config['sound']))
        
    def process(self, value_matrix: np.ndarray):
        assert value_matrix.shape == self.matrix_shape
        
        events = []
        for module in self.modules:
            events += module.process(value_matrix[module.top:module.bottom,module.left:module.right])
                
        for sound_event in events:
            # match type(sound_event):
            #     case MidiNoteEvent:
            if type(sound_event) == sound_events.MidiNoteEvent:
                    self.midi_note_player.play_note(sound_event)
            if type(sound_event) == sound_events.MidiControlEvent:
                    self.midi_control_changer.set_value(sound_event)
                    
        # render CLI output
        if self.printing:
            self.visualization.render()

        # logging
        if self.logging:
            with open(self.log_file, "ab") as file:
                np.savetxt(file, value_matrix, fmt='%.18e', delimiter=',', newline='\n',
                           header='', footer='', encoding=None)
