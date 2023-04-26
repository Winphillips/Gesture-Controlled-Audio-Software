import sounddevice as sd
import numpy as np
from pedalboard import (
    Pedalboard,
    Gain,
    Compressor,
    Reverb,
    Delay,
    HighpassFilter,
    HighShelfFilter,
    LowpassFilter,
    LowShelfFilter,
    PitchShift,
)
from pedalboard.io import AudioStream
import time
import soundfile as sf
from gesture_recognition import GESTURE, HAND_LOCATION_X, HAND_LOCATION_Y  # Import the necessary variables
import PySimpleGUI as sg

# BOOLS for handling button controls
audio_finished = False
is_playing = False
is_paused = False

# Load audio file
audio_file = './clairdelune.wav'
data, samplerate = sf.read(audio_file)
LOGO_PATH = 'img/SoundWave-logo.png'
SAMPLE_PATH = 'img/Cam-feed.png'

#Input and output names can be different across computers, so defaults are attempted.
#The "STREAM" devices should be tied to a virtual audio device to loop audio output to input.
STREAM_INPUT_DEVICE = AudioStream.input_device_names[0]
STREAM_OUTPUT_DEVICE = AudioStream.output_device_names[0]

# Create an empty array to store the processed audio data
processed_audio_data = np.zeros_like(data)

# Create empty pedalboard
pedalboard = Pedalboard()

# Add plugins to the pedalboard
gain_plugin = Gain(gain_db=-20)
compressor_plugin = Compressor(threshold_db=0, ratio=1.0, attack_ms=1, release_ms=100)
reverb_plugin = Reverb(room_size=0.0, wet_level=0.5, dry_level=0.5, width=0.5)
high_pass_plugin = HighpassFilter(cutoff_frequency_hz=20)
high_shelf_plugin = HighShelfFilter(gain_db=3, cutoff_frequency_hz=8000)
low_pass_plugin = LowpassFilter(cutoff_frequency_hz=20000)
low_shelf_plugin = LowShelfFilter(gain_db=3, cutoff_frequency_hz=200)
delay_plugin = Delay(delay_seconds=0.0, mix=0.5)
pitch_shift_plugin = PitchShift(semitones=0)

plugins = [
    gain_plugin,
    compressor_plugin,
    reverb_plugin,
    high_pass_plugin,
    high_shelf_plugin,
    low_pass_plugin,
    low_shelf_plugin,
    delay_plugin,
    pitch_shift_plugin,
]

for plugin in plugins:
    pedalboard.append(plugin)

def callback(outdata, frames, time, status):
    global pedalboard, data, position, is_playing, is_paused
    if not is_playing or is_paused:
        outdata[:] = np.zeros_like(outdata)
        return

    indata_float32 = data[position : position + frames]
    position += frames
    if position >= len(data):
        position = 0
    processed_data = indata_float32
    for plugin in pedalboard:
        processed_data = plugin.process(processed_data, sample_rate=samplerate)
    
    # Pad the processed_data array with zeros if necessary
    if processed_data.shape[0] < outdata.shape[0]:
        processed_data = np.pad(processed_data, ((0, outdata.shape[0] - processed_data.shape[0]), (0, 0)), mode='constant')
    
    # Store the processed data in the processed_audio_data array only when playing and not paused
    if is_playing and not is_paused:
        processed_audio_data[position - frames : position] = processed_data[:frames]
    outdata[:] = processed_data


# Get the default output device
output_device = sd.default.device[1]

# Initialize the position variable
position = 0

# GUI layout
layout = [
    [sg.Image(filename=LOGO_PATH, key='-IMAGE-', size=(64, 50),pad=((620,0),(0,0)))],
    [sg.Text('SoundWave', font=('Courier New', 20, "bold"), justification='center', size=(40, 1))],
    [sg.Button('Play', size=(10, 1)), sg.Button('Pause', size=(10, 1)), sg.Button('Resume', size=(10, 1))],
    [sg.Text('Gain:', size=(10, 1)), sg.Slider(key='-GAIN-', range=(-24, 24), orientation='h', size=(20, 20), default_value=gain_plugin.gain_db)],
    [sg.Text('Reverb Wet level:', size=(10, 1)), sg.Slider(key='-REVERB-', range=(0.0, 100), orientation='h', size=(20, 20), default_value=reverb_plugin.wet_level)],
    [sg.Text('Reverb Room size:', size=(10, 1)), sg.Slider(key='-REVERB_ROOM-', range=(0.0, 10), orientation='h', size=(20, 20), default_value=reverb_plugin.room_size)],
    [sg.Text('Highpass Filter:', size=(10, 1)), sg.Slider(key='-HIGHPASS-', range=(1, 20000), orientation='h', size=(20, 20), default_value=high_pass_plugin.cutoff_frequency_hz)],
    [sg.Text('Lowpass Filter:', size=(10, 1)), sg.Slider(key='-LOWPASS-', range=(1, 20000), orientation='h', size=(20, 20), default_value=low_pass_plugin.cutoff_frequency_hz)],
    [sg.Text('High Shelf Filter:', size=(10, 1)), sg.Slider(key='-HIGHSHELF-', range=(1, 20000), orientation='h', size=(20, 20), default_value=high_shelf_plugin.cutoff_frequency_hz)],
    [sg.Text('Low Shelf Filter:', size=(10, 1)), sg.Slider(key='-LOWSHELF-', range=(1, 20000), orientation='h', size=(20, 20), default_value=low_shelf_plugin.cutoff_frequency_hz)],
    [sg.Text('Delay Time:', size=(10, 1)), sg.Slider(key='-DEL_TIME-', range=(0.0, 30.0), orientation='h', size=(20, 20), default_value=delay_plugin.delay_seconds)],
    [sg.Text('Delay Mix:', size=(10, 1)), sg.Slider(key='-DEL_MIX-', range=(0.0, 100), orientation='h', size=(20, 20), default_value=delay_plugin.mix)],
    [sg.Text('Pitch Shift:', size=(10, 1)), sg.Slider(key='-PITCH-', range=(-24, 24), orientation='h', size=(20, 20), default_value=pitch_shift_plugin.semitones)],
    [sg.Image(filename='', background_color='turquoise', key='-IMAGE-', size=(400, 240))],
    [sg.Button('Start', size=(10, 1)), sg.Button('Stop', size=(10, 1)), sg.Button('Exit', size=(10, 1))]
]

# Create the window
window = sg.Window('SoundWave', layout)

# Start the audio stream
with sd.OutputStream(device=output_device, samplerate=samplerate, channels=2, callback=callback):

    # Loop for updating effects during audio playback
    while not audio_finished:
        event, values = window.read(timeout=0.01)

        if event == 'Start':
            window['-IMAGE-'].update(filename=SAMPLE_PATH)

        if event == 'Stop':
            window['-IMAGE-'].update(filename='')

        if event == 'Play':
            is_playing = True

        if event =='Pause':
            is_paused = True

        if event == 'Resume':
            is_paused = False

        # Update the effects based on the gesture and hand location
        if GESTURE == "ThumbsUp":
            gain_plugin.gain_db=HAND_LOCATION_Y
            compressor_plugin.threshold_db=HAND_LOCATION_X
            compressor_plugin.ratio=HAND_LOCATION_X*1.5

        elif GESTURE == "OpenHand":
            reverb_plugin.wet_level = HAND_LOCATION_X
            reverb_plugin.width = HAND_LOCATION_Y
        
        elif GESTURE == "ClosedFist":
            delay_plugin.delay_seconds = HAND_LOCATION_Y
            delay_plugin.mix = HAND_LOCATION_X
            delay_plugin.feedback = HAND_LOCATION_X*0.5

        elif GESTURE == "PeaceSignUpwards":
            high_pass_plugin.cutoff_frequency_hz = HAND_LOCATION_X
            high_shelf_plugin.gain_db = HAND_LOCATION_Y

        elif GESTURE == "PeaceSignDownwards":
            low_pass_plugin.cutoff_frequency_hz = HAND_LOCATION_X
            low_shelf_plugin.gain_db = HAND_LOCATION_Y
        elif GESTURE == "PointingLeft":
            pitch_shift_plugin.semitones = HAND_LOCATION_Y
            
        else:
            print("\nNo Hand Detected\n")

        # GUI
        # Update the VARIABLES based on the SLIDERS value
        gain_plugin.gain_db = values['-GAIN-']
        reverb_plugin.wet_level = values['-REVERB-']/100
        reverb_plugin.room_size = values['-REVERB_ROOM-']/10
        high_pass_plugin.cutoff_frequency_hz = values["-HIGHPASS-"]
        high_shelf_plugin.cutoff_frequency_hz = values["-HIGHSHELF-"]
        low_pass_plugin.cutoff_frequency_hz = values["-LOWPASS-"]
        low_shelf_plugin.cutoff_frequency_hz = values["-LOWSHELF-"]
        delay_plugin.delay_seconds = values['-DEL_TIME-']
        delay_plugin.mix = values['-DEL_MIX-']/100
        pitch_shift_plugin.semitones = values['-PITCH-']


        # Update the SLIDERS based on the VARIABLES     
        window['-GAIN-'].update(value=gain_plugin.gain_db)
        window['-REVERB-'].update(value=reverb_plugin.wet_level*100)
        window['-REVERB_ROOM-'].update(value=reverb_plugin.room_size*10)
        window['-HIGHPASS-'].update(value=high_pass_plugin.cutoff_frequency_hz)
        window['-HIGHSHELF-'].update(value=high_shelf_plugin.cutoff_frequency_hz)
        window['-LOWPASS-'].update(value=low_pass_plugin.cutoff_frequency_hz)
        window['-LOWSHELF-'].update(value=low_shelf_plugin.cutoff_frequency_hz)
        window['-DEL_TIME-'].update(value=delay_plugin.delay_seconds)
        window['-DEL_MIX-'].update(value=delay_plugin.mix*100)
        window['-PITCH-'].update(value=pitch_shift_plugin.semitones)
        

        # Check if the audio has finished playing
        if position >= len(data) or event == "Exit" or event == sg.WINDOW_CLOSED:
            # Append the remaining unprocessed audio data to the processed_audio_data array
            if position < len(data):
                processed_audio_data[position:] = data[position:]
            audio_finished = True
        else:
            # print("\n\nPedalboard:", pedalboard)
            time.sleep(0.1)
    window.close()
# Save the processed audio data to an output file
output_file = './output.wav'
sf.write(output_file, processed_audio_data, samplerate)
