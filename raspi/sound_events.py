from abc import ABC


class SoundEvent(ABC):
    pass

class MidiNoteEvent(SoundEvent):
    value_range = range(128)
    def __init__(self, note: int, velocity: int):
        try:
            assert note in self.value_range
            assert velocity in self.value_range

            print("bleep")
        except:
            print("hdf")