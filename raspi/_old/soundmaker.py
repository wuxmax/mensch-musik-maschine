# Generate a 440 Hz square waveform in Pygame by building an array of samples and play
# it for 5 seconds.  Change the hard-coded 440 to another value to generate a different
# pitch.
#
# Run with the following command:
#   python pygame-play-tone.py

from array import array
from time import sleep

import pygame
from pygame.mixer import Sound, get_init, pre_init

class Note(Sound):

    def __init__(self, frequency, volume=.1):
        self.frequency = frequency
        Sound.__init__(self, self.build_samples())
        self.set_volume(volume)

    def build_samples(self):
        period = int(round(get_init()[0] / self.frequency))
        samples = array("h", [0] * period)
        amplitude = 2 ** (abs(get_init()[1]) - 1) - 1
        for time in range(period):
            if time < period / 2:
                samples[time] = amplitude
            else:
                samples[time] = -amplitude
        return samples

# note = None

class SoundMaker():
    def __init__(self):
        pre_init(44100, -16, 1, 1024, allowedchanges=True)
        pygame.init()
        self.note = Note(440)
        self.note.play(-1)

    def make_sound(self, frequency):
        # self.note.queue(self.note.build_samples(frequency))
        self.note.stop()
        self.note.__init__([220, 242, 278, 330, 371, 440, 495, 556, 660, 742][int(frequency/100)])
        # if note:
        self.note.play(-1)


# def init_soundmaker():
#     pre_init(44100, -16, 1, 1024, allowedchanges=True)
#     pygame.init()
#     note = Note(440)


# def make_sound(frequency: int = 440, duration: int = 1):
#     note.__init__(frequency)
#     if note:
#         note.play(duration)


if __name__ == "__main__":
    pre_init(44100, -16, 1, 1024)
    pygame.init()
    Note(440).play(-1)
    sleep(1)
