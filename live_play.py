from pedalboard import Convolution, Pedalboard, Chorus, Compressor, Delay, Gain, Reverb, Phaser
from pedalboard.io import AudioStream

# Open up an audio stream:
with AudioStream(
  input_device_name="MacBook Pro Microphone",  # Guitar interface
  output_device_name="External Headphones"
) as stream:
  # Audio is now streaming through this pedalboard and out of your speakers!
  stream.plugins = Pedalboard([
      Compressor(threshold_db=-50, ratio=25),
      Gain(gain_db=30),
      Chorus(),
      Phaser(),
      Convolution("./demo.wav", 1.0),
      Reverb(room_size=0.25),
  ])
  input("Press enter to stop streaming...")

# The live AudioStream is now closed, and audio has stopped.