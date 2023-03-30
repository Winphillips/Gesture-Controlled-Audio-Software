import PySimpleGUI as sg



# Define the layout of the GUI
layout = [
    [sg.Text('SoundWave', font=('Courier New', 20), justification='center', size=(40, 1)),
     sg.Image(filename='logo.png', key='-IMAGE-', size=(25, 25),pad=(0,0))],
    [sg.Text('Gain:', size=(10, 1)), sg.Slider(range=(-24, 24), orientation='h', size=(20, 20), default_value=0)],
    [sg.Text('Reverb:', size=(10, 1)), sg.Slider(range=(0, 100), orientation='h', size=(20, 20), default_value=50)],
    [sg.Text('Delay Time:', size=(10, 1)),
     sg.Slider(range=(0, 1000), orientation='h', size=(20, 20), default_value=500)],
    [sg.Text('Delay Mix:', size=(10, 1)), sg.Slider(range=(0, 100), orientation='h', size=(20, 20), default_value=50)],
    [sg.Text('Distortion:', size=(10, 1)),
     sg.Slider(range=(0, 100), orientation='h', size=(20, 20), default_value=0)],
    [sg.Text('Lowpass:', size=(10, 1)), sg.Slider(range=(0, 100), orientation='h', size=(20, 20), default_value=0)],
    [sg.Image(filename='', background_color='turquoise', key='-IMAGE-', size=(400, 240))],
    [sg.Button('Start', size=(10, 1)), sg.Button('Stop', size=(10, 1)), sg.Button('Exit', size=(10, 1))]
]

# Create the window
window = sg.Window('SoundWave', layout)

# The event loop
while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    if event == '-GRAPH-':
        if values['-GRAPH-'] == (None, None):
            continue
        x, y = values['-GRAPH-']
        print(f'Clicked at x={x}, y={y}')
    if event == 'Start':
        window['-IMAGE-'].update(filename='sample_camera_image.png')
    if event == 'Stop':
        window['-IMAGE-'].update(filename='')

window.close()
