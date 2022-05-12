from abc import ABC


class SoundEvent(ABC):
    pass

class MidiNoteEvent(SoundEvent):
    value_range = range(128)
    def __init__(self, note: int, velocity: int, duration: float = 1.0):
        try:
            assert note in self.value_range
            assert velocity in self.value_range
        except AssertionError:
            print(f"Note and velocity must be within {self.value_range[0]} and {self.value_range[-1]}."
                f"Values: note: {note}, velocity: {velocity}")

        self.note = note
        self.velocity = velocity
        self.duration = duration



