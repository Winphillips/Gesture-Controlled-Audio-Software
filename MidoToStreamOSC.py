import pythonosc
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import AsyncIOOSCUDPServer
import mido
from mido import MidiFile
from typing import List, Any
import copy
import asyncio

#The IN_FILE should be the name of the starting midi file.
IN_FILE = "test.mid"

#The SOURCE_IP should be the IP address of the device sending the OSC messages.
SOURCE_IP = "127.0.0.1"

#The SOURCE_PORT should be the port the OSC message is being received through.
SOURCE_PORT = "1115"

#The ADDRESS should be the OSC address.
ADDRESS = "/MIDI/adjust"

#The MIDI_OUT should be the name of the MIDI port the program sends the notes to.
MIDI_OUT = "Midi Through:Midi Through Port-0 14:0"

#These variables will be used for note adjustment.
noteAdjust = 0
velAdjust = 0

#These prints are here for debugging purposes and for helping identify active ports.
print(mido.get_output_names())
print(mido.get_input_names())

midiStream = mido.open_output(MIDI_OUT)

#Method that returns modified MIDI message.
def adjust_note(messageIn, noteAdjustIn, velAdjustIn):
    #The adjusted values are held in these variables to check for boundary cases.
    noteTemp = noteAdjustIn + messageIn.note
    velTemp = velAdjustIn + messageIn.velocity

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

#Method that changes noteAdjust and velAdjust. Is put in the dispatcher.
def osc_note(address: str, *args: List[Any]):
    #Arguments should be integers. First element should be note, second should be velocity.
    global noteAdjust
    global velAdjust
    noteAdjust = int(args[0])
    velAdjust = int(args[1])

dispatcher = Dispatcher()
dispatcher.map(ADDRESS, osc_note)

#Method that sends MIDI messages.
async def async_message(messageIn):
    global noteAdjust
    global velAdjust
    midiStream.send(adjust_note(messageIn, copy.deepcopy(noteAdjust), copy.deepcopy(velAdjust)))
    await asyncio.sleep(0)

#Plays the MIDI file.
async def mido_play(fileName):
    server = AsyncIOOSCUDPServer((SOURCE_IP, SOURCE_PORT), dispatcher, asyncio.get_event_loop())
    trport, proto = await server.create_serve_endpoint()

    for message in MidiFile(fileName).play():
        await async_message(message)
    
    await asyncio.sleep(1)
    
    #This method disables any notes that are still playing after the file ended.
    midiStream.reset()
    
    trport.close()

asyncio.run(mido_play(IN_FILE))