# README

## Raspi Setup
1. Clone/Pull repo
2. Start virtual MIDI device: `sudo modprobe snd-virmidi`
3. Get device ID of virtual MIDI device: `amidi -l` --> First entry in `Device` column (eg. `hw:2,0`)
4. Enter device ID in `raveloxmidi.conf` --> `alsa.input_device`
5. Get port name of virtual MIDI device: 
    * `cd $HOME/mensch-musik-maschine/raspi`
    * `python midi_controller.py` --> First entry in list thats starts with `Virtual Raw MIDI`
    * Copy full name and enter into `config.yml`--> `midi_controller` --> `port`

## Raspi Run
1. `cd $HOME/mensch-musik-maschine/raspi`
2. Start network MIDI service: `sudo raveloxmidi -d -N -c raveloxmidi.conf`
3. Stat main python script: `python main.py`