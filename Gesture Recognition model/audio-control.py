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
import time
import soundfile as sf
from gesture_recognition import GESTURE, HAND_LOCATION_X, HAND_LOCATION_Y  # Import the necessary variables

audio_finished = False

# Load audio file
audio_file = './demo.wav'
data, samplerate = sf.read(audio_file)

# Create empty pedalboard
pedalboard = Pedalboard()

# Add plugins to the pedalboard
gain_plugin = Gain(gain_db=-20)
compressor_plugin = Compressor(threshold_db=0, ratio=1.0, attack_ms=1, release_ms=100)
reverb_plugin = Reverb(room_size=0.0, wet_level=0.5, dry_level=0.5, width=0.5)
high_pass_plugin = HighpassFilter(cutoff_frequency_hz=20)
high_shelf_plugin = HighShelfFilter(gain_db=0, cutoff_frequency_hz=8000)
low_pass_plugin = LowpassFilter(cutoff_frequency_hz=20000)
low_shelf_plugin = LowShelfFilter(gain_db=0, cutoff_frequency_hz=200)
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
    global pedalboard, data, position
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
    
    outdata[:] = processed_data


# Get the default output device
output_device = sd.default.device[1]

# Initialize the position variable
position = 0

# Start the audio stream
with sd.OutputStream(device=output_device, samplerate=samplerate, channels=2, callback=callback):
    # Loop for updating effects during audio playback
    while not audio_finished:
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

        # Check if the audio has finished playing
        # TODO: CREATE WAY IN GUI TO CHANGE THIS TO BREAK OUT OF LOOP TO SAVE OUTPUT FILE
        if position >= len(data):
            audio_finished = True
        else:
            print("\n\nPedalboard:", pedalboard)
            time.sleep(0.1)

# Save the processed audio data to an output file
output_file = './output.wav'
sf.write(output_file, data, samplerate)
