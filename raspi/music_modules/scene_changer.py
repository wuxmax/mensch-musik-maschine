import time
from collections import deque

import numpy as np

from sound_events import MidiControlEvent
from .base import MusicModule
from module_logger import ModuleLogger


class SceneChanger(MusicModule):
    def __init__(self, setup, sound, module_logger: ModuleLogger):
        super().__init__(setup, module_logger)
        self.scene_time = sound['scene_time']
        self.control = sound['control']
        self.time_step_size = sound['time_step_size']
        self.timer = time.time()

    def module_process(self, _):
        if time.time() - self.timer > self.time_step_size:
            return MidiControlEvent(
                channel=self.midi_channel,
                control=self.control,
                value=127)
        return []
