from abc import ABC


class SoundEvent(ABC):
    pass

class MidiNoteEvent(SoundEvent):
    value_range = range(128)
    def __init__(self, note: int, velocity: int):
        try:
            assert note in self.note_range
            assert velocity in self.note_range
        except:
            print("hdf")