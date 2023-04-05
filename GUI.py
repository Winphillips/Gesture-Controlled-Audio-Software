import PySimpleGUI as sg
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import AsyncIOOSCUDPServer
import asyncio

#TROY: Paths to other files are stored in global constants for easier modification.
LOGO_PATH = 'img/logo.png'
SAMPLE_PATH = 'img/sample_camera_image.png'

#The SOURCE_IP should be the IP address of the device sending the OSC messages.
SOURCE_IP = "127.0.0.1"

#The SOURCE_PORT should be the port the OSC message is being received through.
SOURCE_PORT = "1115"

#The ADDRESS should be the OSC address.
ADDRESS_PREFIX = "/GESTURE/set/"
ADDRESS = "/GESTURE/set/*"

# Define the layout of the GUI
layout = [
    [sg.Text('SoundWave', font=('Courier New', 20), justification='center', size=(40, 1)),
     sg.Image(filename=LOGO_PATH, key='-IMAGE-', size=(25, 25),pad=(0,0))],
    [sg.Text('Gain:', size=(10, 1)), sg.Slider(key='-GAIN-', range=(-24, 24), orientation='h', size=(20, 20), default_value=0)],
    [sg.Text('Reverb:', size=(10, 1)), sg.Slider(key='-REVERB-', range=(0, 100), orientation='h', size=(20, 20), default_value=50)],
    [sg.Text('Delay Time:', size=(10, 1)),
     sg.Slider(key='-DEL_TIME-', range=(0, 1000), orientation='h', size=(20, 20), default_value=500)],
    [sg.Text('Delay Mix:', size=(10, 1)), sg.Slider(key='-DEL_MIX-', range=(0, 100), orientation='h', size=(20, 20), default_value=50)],
    [sg.Text('Distortion:', size=(10, 1)),
     sg.Slider(key='-DISTORTION-', range=(0, 100), orientation='h', size=(20, 20), default_value=0)],
    [sg.Text('Lowpass:', size=(10, 1)), sg.Slider(key='-LOWPASS-', range=(0, 100), orientation='h', size=(20, 20), default_value=0)],
    [sg.Image(filename='', background_color='turquoise', key='-IMAGE-', size=(400, 240))],
    [sg.Button('Start', size=(10, 1)), sg.Button('Stop', size=(10, 1)), sg.Button('Exit', size=(10, 1))]
]

queued_changes = {}
allow_change = True

#TROY: This method is in the dispatcher. The last phrase of the address gives the key. The args give the value.
def osc_set(address: str, *args):
    global queued_changes
    global allow_change
    if allow_change:
        queued_changes[address.removeprefix(ADDRESS_PREFIX)] = args[0]


#Troy: creates the dispatcher for the OSC server.
osc_dispatcher = Dispatcher()
osc_dispatcher.map(ADDRESS, osc_set)

async def gui_loop():
    global queued_changes
    global allow_change

    # Create the window
    window = sg.Window('SoundWave', layout)

    # The event loop
    while True:
        event, values = window.read(timeout=0.01)
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        #TROY: If queued_changes has any elements, this branch is taken.
        if queued_changes:
            allow_change = False
            for signal in queued_changes:
                #TROY: If for any reason the message from the OSC signal doesn't match up with a key, this WILL throw errors.
                window[signal].update(queued_changes[signal])
            queued_changes = {}
            allow_change = True
        if event == '-GRAPH-':
            if values['-GRAPH-'] == (None, None):
                continue
            x, y = values['-GRAPH-']
            print(f'Clicked at x={x}, y={y}')
        if event == 'Start':
            window['-IMAGE-'].update(filename=SAMPLE_PATH)
        if event == 'Stop':
            window['-IMAGE-'].update(filename='')
        await asyncio.sleep(0)

    window.close()

async def init_osc():
    server = AsyncIOOSCUDPServer((SOURCE_IP, SOURCE_PORT), osc_dispatcher, asyncio.get_event_loop())
    trport, proto = await server.create_serve_endpoint()

    await gui_loop()

    trport.close()

asyncio.run(init_osc())