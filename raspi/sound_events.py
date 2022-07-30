from abc import ABC

class SoundEvent(ABC):
    pass

class MidiEvent(SoundEvent):
    value_range = range(128)
    def __init__(self, channel: int):
        self.channel = channel

class MidiNoteEvent(MidiEvent):
    def __init__(self, channel: int, note: int, velocity: int, duration: float = 1.0):
        super().__init__(channel)
        try:
            assert note in self.value_range
            assert velocity in self.value_range
        except AssertionError:
            print(f"Note and velocity must be within {self.value_range[0]} and {self.value_range[-1]}. "
                f"Values: note: {note}, velocity: {velocity}")
            exit(1)

        self.note = note
        self.velocity = velocity
        self.duration = duration

class MidiControlEvent(MidiEvent):
    def __init__(self, channel: int, control: int, value: int):
        super().__init__(channel)
        try:
            assert control in self.value_range
            assert value in self.value_range
        except AssertionError:
            print(f"Control and value must be within {self.value_range[0]} and {self.value_range[-1]}. "
                f"Values: control: {control}, value: {value}")
            exit(1)

        self.control = control
        self.value = value    
