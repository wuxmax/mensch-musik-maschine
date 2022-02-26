import threading
from time import sleep
from datetime import datetime

import mido


class NotePlayer:
    current_note = 0
    last_note_started  = 0
    stopper_subroutine = None
    channel = 0
    note_range = range(128)

    def __init__(self, channel: int, port: str):
        self.channel = channel
        self.port = mido.open_output(port)

    def play_note(self, note: int, velocity: int):
        try:
            assert note in self.note_range
            assert velocity in self.note_range
        except AssertionError:
            return
        
        self.stop_note(self.current_note)
        self.current_note = note
        msg = mido.Message('note_on', channel=self.channel, velocity=velocity, time=1, note=note)
        self.port.send(msg)
        threading.Thread(target=self.time_switch, args=()).start()

    def time_switch(self):
        note_started = datetime.now()
        self.last_note_started = note_started
        sleep(1)
        if (self.last_note_started == note_started):
            self.stop_note(self.current_note)

    def stop_note(self, note: int):
        msg = mido.Message('note_off', note=note)
        self.port.send(msg)

    def reset(self):
        for note in self.note_range:
            self.stop_note(note)