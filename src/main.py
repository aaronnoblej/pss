#--------------------------------------------------------------------------------------
# THIS MODULE CONTAINS THE CODE THAT MAKES UP THE TITLE SCREEN GUI AND OTHER POPUPS
# THAT MAY OCCUR WHILE USING THE SOFTWARE - SEPARATE FROM THE LOGIC
#--------------------------------------------------------------------------------------

import PySimpleGUI as sg
from threading import Thread
import os, connection, socket

WIDTH = 600 #500 orignally
HEIGHT = 420 #350 originally
BUTTON_WIDTH = 30
BUTTON_HEIGHT = 2 #This is not pixels, this is the default units provided by the pysimplegui interface

connection_type = 'Bluetooth'
selected_color = '#D3D3D3'
deselected_color = '#FFFFFF'

lan_port = 14572
bt_port = 4
server: connection.Server = None           

def get_image_path(filename):
    os.chdir(__file__+'\\..\\img')
    return os.getcwd()+'\\'+filename

def get_requests():
    if isinstance(server, connection.Server):
        if len(server.requests) > 0: 
            request = server.requests.pop(0)
            status = request_popup(request)
            if status: #if accepted
                server.get_stream(socket.gethostbyname(request))

def titleScreen():
    # Title screen appears upon running the software - user interface of the program
    global connection_type, server
    buttons = [
        [sg.Button('Send a Share Request', button_color=('black','white'), size=(BUTTON_WIDTH,BUTTON_HEIGHT), border_width=3)],
        [sg.Button('Settings', button_color=('black','white'), size=(BUTTON_WIDTH,BUTTON_HEIGHT), border_width=3)],
    ]
    bt_image = [
        [sg.Button(key='-OPT_BT-', image_filename=get_image_path('bluetooth.png'), button_color=(selected_color if connection_type == 'Bluetooth' else deselected_color), mouseover_colors=selected_color, border_width=0)],
        [sg.Text(key='-OPT_BT_TEXT-', text='Bluetooth', font='Century 8', text_color='black', background_color=(selected_color if connection_type == 'Bluetooth' else deselected_color))]
    ]
    lan_image = [
        [sg.Button(key='-OPT_LAN-', image_filename=get_image_path('lan.png'), button_color=(selected_color if connection_type == 'LAN' else deselected_color), mouseover_colors=deselected_color, border_width=0)],
        [sg.Text(key='-OPT_LAN_TEXT-', text='LAN', font='Century 8', text_color='black', background_color=(selected_color if connection_type == 'LAN' else deselected_color))]
    ]

    layout = [
                [sg.Text('PSS', font='Century 60', background_color='white', text_color='black', key='-TITLE-')], # TEST LAYOUT FROM https://pysimplegui.readthedocs.io/en/latest/
                [sg.Column(buttons, background_color='white')],
                [sg.Button('Quit', button_color=('black','white'))],
                [sg.Column(bt_image, element_justification='c', background_color=(selected_color if connection_type == 'Bluetooth' else deselected_color), key='-CONNECTION_OPTIONS_BT-'), sg.Column(lan_image, element_justification='c', background_color=(selected_color if connection_type == 'LAN' else deselected_color), key='-CONNECTION_OPTIONS_LAN-')]
            ]

    window = sg.Window("PSS", layout, background_color='white', size=(WIDTH,HEIGHT), element_justification='c')

    # Event loop for processing user inputs and values
    while True:
        event, values = window.read()
        #Close window
        if event in (sg.WIN_CLOSED, 'Quit'):
            break
        elif event == '-OPT_BT-': #Updates colors if Bluetooth is selected
            if connection_type != 'Bluetooth':
                if isinstance(server,connection.Server) and server.type == 'LAN':
                    print('Yep')
                    server = None #stop current server because we have now changed type
                connection_type = 'Bluetooth'
                window['-OPT_BT-'].update(button_color=selected_color)
                window['-OPT_BT-'].ParentRowFrame.config(background=selected_color)
                window['-OPT_BT_TEXT-'].update(background_color=selected_color)
                window['-OPT_BT_TEXT-'].ParentRowFrame.config(background=selected_color)
                window['-CONNECTION_OPTIONS_BT-'].Widget.config(background=selected_color)
                window['-OPT_LAN-'].update(button_color=deselected_color)
                window['-OPT_LAN-'].ParentRowFrame.config(background=deselected_color)
                window['-OPT_LAN_TEXT-'].update(background_color=deselected_color)
                window['-OPT_LAN_TEXT-'].ParentRowFrame.config(background=deselected_color)
                window['-CONNECTION_OPTIONS_LAN-'].Widget.config(background=deselected_color)
                # Create a Bluetooth server so others can see that this device is available
                #serv = connection.Server('Bluetooth', bt_port)
                #serv.start()
        elif event == '-OPT_LAN-': #Updates colors if LAN is selected, opens a LAN server
            if connection_type != 'LAN':
                connection_type = 'LAN'
                window['-OPT_LAN-'].update(button_color=selected_color)
                window['-OPT_LAN-'].ParentRowFrame.config(background=selected_color)
                window['-OPT_LAN_TEXT-'].update(background_color=selected_color)
                window['-OPT_LAN_TEXT-'].ParentRowFrame.config(background=selected_color)
                window['-CONNECTION_OPTIONS_LAN-'].Widget.config(background=selected_color)
                window['-OPT_BT-'].update(button_color=deselected_color)
                window['-OPT_BT-'].ParentRowFrame.config(background=deselected_color)
                window['-OPT_BT_TEXT-'].update(background_color=deselected_color)
                window['-OPT_BT_TEXT-'].ParentRowFrame.config(background=deselected_color)
                window['-CONNECTION_OPTIONS_BT-'].Widget.config(background=deselected_color)
                # Create a LAN server so others can see that this device is available
                server = connection.Server('LAN', lan_port)
                server.start()
        elif event == 'Send a Share Request':
            window.close()
            findDevicesScreen()
            return
        elif event == 'Settings':
            sg.Popup('Not yet implemented', title='Settings', background_color='white', text_color='black')
        
        # This must be put within each GUI loop - using another thread immensely slows down the program
        #get_requests()
        
        print(connection_type)
    window.close()

def findDevicesScreen():
    global connection_type
    searchText = 'Searching for available devices on your network...' if connection_type == 'LAN' else 'Searching for nearby devices...'
    buttons = [
        [sg.Button('Send screen request', key ='-SEND_BUTTON-', font='Century 12', button_color=('white', '#0083FF'), border_width=1, size=(30,1), disabled=True, disabled_button_color=('white','#BEBEBE'), use_ttk_buttons=True)],
        [sg.Button('Back', button_color=('black','white')), sg.Button('Quit', button_color=('black','white'))]
    ]
    layout = [
                [sg.Text(searchText, font='Century 12', background_color='white', text_color='black', key='-SEARCHING-')],
                [sg.Image(filename=get_image_path('loading.gif'), key='-LOADING-')],
                [sg.Listbox(server.found_devices, size=(50,10), select_mode=sg.LISTBOX_SELECT_MODE_EXTENDED, key='-DEVICES-')],
                [sg.Column(buttons, background_color='white', element_justification='c')]
            ]
    window = sg.Window("PSS", layout, background_color='white', size=(WIDTH,HEIGHT), element_justification='c')

    # Event loop for processing user inputs and values

    scanner = Thread(target=server.scan, daemon=True)
    scanner.start()

    device_length = 0

    while True:
        event, values = window.read(timeout=100)
        if(len(server.found_devices) != device_length):
            device_length = len(server.found_devices)
            window['-DEVICES-'].update(server.found_devices)
        if event in (sg.WIN_CLOSED, 'Quit'):
            break
        if event == 'Back':
            server.scanning = False #stop scanning, kills the scanner thread
            window.close()
            titleScreen()
            return
        if len(values['-DEVICES-']) > 0:
            window['-SEND_BUTTON-'].update(disabled=False)
        else:
            window['-SEND_BUTTON-'].update(disabled=True)
        if event == '-SEND_BUTTON-':
            for client in values['-DEVICES-']:
                server.send_request(server.get_client_addr(client))

        # This must be put within each GUI loop - using another thread immensely slows down the program
        get_requests()

    window.close()

def request_popup(requester_name):
    layout = [
                [sg.Text(text=requester_name, font='Century 14 bold', text_color='black', background_color='white')],
                [sg.Text(text='would like to share their screen with you.', font='Century 14', text_color='black', background_color='white')],
                [sg.Button('Accept', font='Century 12', button_color=('black', '#c7f2d2'), size=(10,1)), sg.Button('Deny', font='Century 12', button_color=('black','#d66f6f'), size=(10,1))]
            ]
    window = sg.Window("New screen share request!", layout, background_color='white', size=(WIDTH, HEIGHT//2), element_justification='c', force_toplevel=True,modal=True, margins=(10,10))
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Quit'):
            break
        if event == 'Accept':
            window.close()
            return True
        if event == 'Deny':
            window.close()
            return False
    window.close()
        

if __name__ == '__main__':
    titleScreen()
