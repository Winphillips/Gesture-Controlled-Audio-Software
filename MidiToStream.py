import mido
from mido import MidiFile

#The outPath should be the name of the port that leads to audio software to play MIDI.
outPath = ""

#The inFile should be the name of the starting midi file.
inFile = "test.mid"


print(mido.get_output_names())
print(mido.get_input_names())

midiStream = mido.open_output(outPath)

def adjust_note(messageIn):
    #TODO: Figure out how to have adjustment values set by external program. Will just be 0 for now.
    noteAdjust = 0
    velAdjust = 0
    
    #The adjusted values are held in these variables to check for boundary cases.
    noteTemp = noteAdjust + messageIn.note
    velTemp = velAdjust + messageIn.velocity

    if noteTemp > 127:
        noteTemp = 127
    elif noteTemp < 0:
        noteTemp = 0
    
    if velTemp > 127:
        velTemp = 127
    elif velTemp < 0:
        velTemp = 0
    
    #After checking for boundary cases, the new values are applied to the message.
    messageIn.note = noteTemp
    messageIn.velocity = velTemp

    #The adjust message is then returned.
    return messageIn

for message in MidiFile(inFile).play():
    midiStream.send(adjust_note(message))
    #midiStream.send(message)