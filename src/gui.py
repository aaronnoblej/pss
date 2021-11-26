#--------------------------------------------------------------------------------------
# THIS MODULE CONTAINS THE CODE THAT MAKES UP THE TITLE SCREEN GUI AND OTHER POPUPS
# THAT MAY OCCUR WHILE USING THE SOFTWARE - SEPARATE FROM THE LOGIC
#--------------------------------------------------------------------------------------

import PySimpleGUI as sg
import os

from PySimpleGUI.PySimpleGUI import LISTBOX_SELECT_MODE_BROWSE, LISTBOX_SELECT_MODE_EXTENDED, LISTBOX_SELECT_MODE_MULTIPLE, LISTBOX_SELECT_MODE_SINGLE

WIDTH = 500
HEIGHT = 350
BUTTON_WIDTH = 30
BUTTON_HEIGHT = 2 #This is not pixels, this is the default units provided by the pysimplegui interface

connection_type = 'Bluetooth'
selected_color = '#D3D3D3'
deselected_color = '#FFFFFF'

def get_image_path(filename):
    os.chdir(__file__+'\\..\\img')
    return os.getcwd()+'\\'+filename

def titleScreen():
    # Title screen appears upon running the software - user interface of the program
    global connection_type
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
        elif event == '-OPT_LAN-': #Updates colors if LAN is selected
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
        elif event == 'Send a Share Request':
            window.close()
            findDevicesScreen()
            return
        elif event == 'Settings':
            sg.Popup('Not yet implemented', title='Settings', background_color='white', text_color='black')
        
        print(connection_type)

    window.close()

def findDevicesScreen():
    global connection_type
    searchText = 'Searching for available devices on your network...' if connection_type == 'LAN' else 'Searching for nearby devices...'
    buttons = [
        [sg.Button('Send screen request', font='Century 12', button_color=('white', '#0083FF'), border_width=1, size=(30,1), disabled=True, disabled_button_color=('white','#BEBEBE'), use_ttk_buttons=True)],
        [sg.Button('Back', button_color=('black','white')), sg.Button('Quit', button_color=('black','white'))]
    ]
    layout = [
                [sg.Text(searchText, font='Century 12', background_color='white', text_color='black', key='-SEARCHING-')],
                [sg.Image(filename=get_image_path('loading.gif'), key='-LOADING-')],
                [sg.Listbox(['Aaron-Laptop', 'Molly-iPad', 'Sara Speaker'], size=(50,10), select_mode=LISTBOX_SELECT_MODE_EXTENDED)],
                [sg.Column(buttons, background_color='white', element_justification='c')]
            ]
    window = sg.Window("PSS", layout, background_color='white', size=(WIDTH,HEIGHT), element_justification='c')
    # Event loop for processing user inputs and values

    while True:
        event, values = window.read(timeout=100)
        if event in (sg.WIN_CLOSED, 'Quit'):
            break
        if event == 'Back':
            window.close()
            titleScreen()
            return

    window.close()

if __name__ == '__main__':
    titleScreen()
