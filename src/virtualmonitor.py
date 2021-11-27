# This module contains code for producing a "virtual monitor" on client screens that display the host's screen

from vidstream import ScreenShareClient

#WIDTH = root.winfo_screenwidth()
#HEIGHT = root.winfo_screenheight()

def stream_from(address, port=8080):
    sender = ScreenShareClient(address, 8080)
    sender.start_stream()

