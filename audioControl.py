from pedalboard import Pedalboard, Gain, Mix, Reverb, Distortion, HighpassFilter, LowpassFilter, Delay, PitchShift, Compressor
from pedalboard.io import AudioFile

# Read in a whole file, resampling to our desired sample rate:
samplerate = 44100.0
with AudioFile('base.wav').resampled_to(samplerate) as f:
  audio = f.read(f.frames)
  #print(f.samplerate)
  #print(f.num_channels)
  

'''
passthrough = Gain(gain_db=0)

delay_and_pitch_shift = Pedalboard([
  Delay(delay_seconds=0.25, mix=1.0),
  PitchShift(semitones=12),
  Gain(gain_db=-3),
])

delay_longer_and_more_pitch_shift = Pedalboard([
  Delay(delay_seconds=0.5, mix=1.0),
  PitchShift(semitones=-12),
  Gain(gain_db=-6),
])

board = Pedalboard([
  # Put a compressor at the front of the chain:
  Compressor(),
  # Run all of these pedalboards simultaneously with the Mix plugin:
  Mix([
    passthrough,
    delay_and_pitch_shift,
    delay_longer_and_more_pitch_shift,
  ]),
  # Add a reverb on the final mix:
  Reverb()
])
'''

# Make a pretty interesting sounding guitar pedalboard:
board = Pedalboard([
    #Reverb(room_size=0.30, wet_level=0.4, dry_level=0.2),
    #HighpassFilter(),
    #LowpassFilter(),
    Distortion(drive_db=20),
    Gain(gain_db=-15)
])

# Pedalboard objects behave like lists, so you can add plugins:
#board.append(Compressor(threshold_db=-25, ratio=10))
#board.append(Gain(gain_db=10))
#board.append(Limiter())


# Run the audio through board
effected = board(audio, samplerate)

# Write the audio back as a wav file:
with AudioFile('baseDist.wav', 'w', samplerate, effected.shape[0]) as f:
  f.write(effected)