from pedalboard import Pedalboard, Gain, Mix, Reverb, Distortion, HighpassFilter, LowpassFilter, Delay, PitchShift, Compressor
from pedalboard.io import AudioFile

# Read in a whole file, resampling to our desired sample rate:
samplerate = 44100.0
with AudioFile('base.wav').resampled_to(samplerate) as f:
  audio = f.read(f.frames)
  #print(f.samplerate)
  #print(f.num_channels)
  

# Effects Go here
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