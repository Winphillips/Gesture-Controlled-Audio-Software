import mido

#The outPath should be the name of the port that leads to audio software to play MIDI.
outPath = ""

print(mido.get_output_names())
print(mido.get_input_names())


with mido.open_output(outPath) as midiOut:
    choice = 0
    newChoice = 0

    while choice < 128 and choice >= 0:

        #The input integer should be controlled by the gesture. This determines what note is being played.
        newChoice = int(input("Enter midi note:"))

        #The input float will determine the velocity (volume) of the note. It should be a float between 0.0 and 1.0.
        velChoice = int(float(input("Enter midi velocity:")) * 127)

        midiOut.send(mido.Message('note_off', note=choice))

        choice = newChoice

        if choice < 128 and choice >= 0 and velChoice < 128 and velChoice >= 0:
            midiOut.send(mido.Message('note_on', note=choice, velocity=velChoice))
