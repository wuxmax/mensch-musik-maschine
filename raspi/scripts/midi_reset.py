import sys
sys.path.append("..")

from sound_events import MidiControlEvent
from utils import load_config

def midi_reset(module_data, max_value):
    for channel, control in module_data:
       for activation in range(max_value + 1):
        return [MidiControlEvent(
                channel=channel,
                control=control,
                value=activation)]

if __name__ == "__main__":
    config = load_config(sys.argv[1])
    module_data = []

    for module in config['modules'].values():
        module_data.append((module['setup']['midi_channel'], module['sound']['control']))

    midi_reset(module_data, 127)