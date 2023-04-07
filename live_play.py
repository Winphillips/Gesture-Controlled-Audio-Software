from pedalboard import Convolution, Pedalboard, Chorus, Compressor, Delay, Gain, Reverb, Phaser
from pedalboard.io import AudioStream

#TROY: Input and output names can be different across computers, so defaults are attempted.
INPUT_DEVICE = AudioStream.input_device_names[0]
OUTPUT_DEVICE = AudioStream.output_device_names[0]

# Open up an audio stream:
with AudioStream(
  input_device_name=INPUT_DEVICE,
  output_device_name=OUTPUT_DEVICE
) as stream:
  # Audio is now streaming through this pedalboard and out of your speakers!
  stream.plugins = Pedalboard([
      Compressor(threshold_db=-50, ratio=25),
      Gain(gain_db=30),
      Chorus(),
      Phaser(),
      Convolution(".audio/demo.wav", 1.0),
      Reverb(room_size=0.25),
  ])
  input("Press enter to stop streaming...")

# The live AudioStream is now closed, and audio has stopped.