# README

## Test Setup
1. apt-get install libasound2-dev
2. python3.8 -m pip install -r requirements.txt

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
3. In new terminal window: Start main python script: `python main.py`


## Mac Setup
1. Open 'Audio MDI Setup'
2. Go to 'Window -> MDI Studio'
3. Go to 'MIDI Studio -> MIDI Network Setup"
4. If not already done, under 'My Sessions' create a session
5. If not already done, activate the session by enabling the checkmark
6. If not already done, under 'Directory' create a device: 'Host' is the IPv4 of the raspi, Port should be 5004
7. If not already done, activate the device by enabling the checkmark
8. Connnect to the device by clicking on the connect button (red latency bars should appear in the latency display on the left)

## Ableton Midi Setup
* Changable in Ableton UserConfigurations.txt (https://help.ableton.com/hc/en-us/articles/206240184-Creating-your-own-Control-Surface-script)
* One Midi Channel per Module
** Track Volume is on CC1
** Effect are on CC2+ 

## Troubleshooting
* Check if all I2C devices are detected: `i2cdetect -y 1`
* Check if MIDI messages are send in the raveloxmidi terminal session on the raspi