import mido
from time import sleep

port = mido.open_output('Circuit MIDI 1')


song = [mido.Message('note_on', channel=2, velocity=64, time=100, note=i) for i in range(60, 66)]

song_off = [mido.Message('note_off', channel=2, note=i) for i in range(60, 66)]


for idx, msg in enumerate(song):
    port.send(msg)
    print(idx)
    sleep(0.5)
    port.send(song_off[idx])


