import datetime

import numpy as np

from sound_events import MidiNoteEvent
from .base import MusicModule

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