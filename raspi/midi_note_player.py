import threading
from time import sleep
from datetime import datetime

import mido

from sound_events import MidiNoteEvent

class MidiNotePlayer:
    def __init__(self, channel: int, port: str, n_voices: int):
        self.channel: int = channel
        self.port = mido.open_output(port)
        self.reset()
        
        self.current_notes = [-1] * n_voices
        self.notes_started = [-1] * n_voices

    def play_note(self, note_event: MidiNoteEvent):
        voice = next((voice for voice, note in enumerate(self.current_notes) if note < 0), 0)

        if self.current_notes[voice] >= 0:
            self.stop_note(self.current_notes[voice])
        self.current_notes[voice] = note_event.note
        
        msg = mido.Message('note_on', 
            channel=self.channel, 
            note=note_event.note,
            velocity=note_event.velocity, 
            time=1)  # we do not really know, what time does
        self.port.send(msg)

        threading.Thread(target=self.time_switch, args=(voice, note_event.duration)).start()

    def time_switch(self, voice: int, duration: float):
        note_started = datetime.now()
        self.notes_started[voice] = note_started
        sleep(duration)
        
        if (self.notes_started[voice] == note_started):
            self.stop_note(self.current_notes[voice])
            self.current_notes[voice] = -1
            
    def stop_note(self, note: int):
        msg = mido.Message('note_off', note=note)
        self.port.send(msg)

    def reset(self):
        self.port.reset()
        # for note in MidiNoteEvent.value_range:
        #     self.stop_note(note)


if __name__=="__main__":
    print(f"MIDI outupt names: {mido.get_output_names()}")

    from utils import load_config

    config = load_config()['midi_player']
    player = MidiNotePlayer(**config)

    # while True:
        #player.play_note(MidiNoteEvent(note=34, velocity=100))
    
    for _ in range(5):
        for v in range(100):
            player.port.send(mido.Message('control_change', channel=1, control=2, value=v))
            print("sent")
            sleep(0.01)
