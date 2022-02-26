from time import sleep
from smbus2 import SMBus
import numpy

from note_player import NotePlayer

I2C_SLAVE_ADDRESS = 11

smbus = SMBus(1)

last_sounds = [0] * 4

SIGNAL_THRESHOLD = 50

DRUM_BEAT_NOTES = [60, 62, 64, 65]


noghteybois = [NotePlayer(channel=c, port='Circuit MIDI 1') for c in range(4)]
for baby in noghteybois:
    baby.reset()


while True:
    try:
        block_data = smbus.read_i2c_block_data(I2C_SLAVE_ADDRESS, 0x00, 8)
    except Exception as e:
        continue
    
    sensor_values = [int.from_bytes(block_data[idx:idx + 2], byteorder='little', signed=False) for idx in range(0, 8, 2)]
    

    # print(f"sensor values: {sensor_values}")

    for idx, sensor_value in enumerate(sensor_values):
        value_difference = sensor_value - last_sounds[idx]
        if abs(value_difference) > SIGNAL_THRESHOLD:
            print("----------------")
            print(idx)
            print(sensor_value)
            if idx > 1:
                if value_difference < 0:
                    noghteybois[2].play_note(DRUM_BEAT_NOTES[idx - 2], velocity=int(sensor_value / 10))
            else:
                noghteybois[idx].play_note(int(sensor_value / 20), velocity=64)

    last_sounds = sensor_values.copy()

