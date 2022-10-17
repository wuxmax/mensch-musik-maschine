import sys
sys.path.append("..")


import midi_controller
from sound_events import MidiControlEvent
from utils import load_config

if __name__ == "__main__":
    config = load_config(sys.argv[1])
    midi_control_changer = midi_controller.MidiControlChanger(**config['midi_controller'])
    module_data = []
    events = []

    for module in config['modules'].values():
        module_data.append((module['setup']['midi_channel'], module['sound']['control']))

    for channel, control in module_data:
       for activation in range(127 + 1):
        events.append(MidiControlEvent(
                channel=channel,
                control=control,
                value=activation))
                
    for sound_event in events:
        midi_control_changer.set_value(sound_event)
