import sys
sys.path.append("..")

import midi_controller
from sound_events import MidiControlEvent
from utils import load_config

def get_input(channel, control, name):
    print(f"Awaiting Instructions for {name}...\nPress 'S' to send the signal, press 'N' to skip to the next module")
    x = input()
    if x == "S":
        midi_control_changer.set_value(MidiControlEvent(channel=channel, control=control, value=127))
        get_input(channel, control, name)
    elif x == "N":
        return
    else:
        get_input(channel, control, name)


if __name__ == "__main__":
    config = load_config(sys.argv[1])
    midi_control_changer = midi_controller.MidiControlChanger(**config['midi_controller'])
    module_data = []

    for module in config['modules'].values():
        module_data.append((module['setup']['midi_channel'], module['sound']['control'], module['setup']['name']))

    for channel, control, name in module_data:
        get_input(channel, control, name)
    
    print("Mapping finished!")