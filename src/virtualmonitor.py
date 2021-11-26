# This module contains code for producing a "virtual monitor" on client screens that display the host's screen

import tkinter as tk
from vidstream import StreamingServer
import threading

#root = tk.Tk()

#WIDTH = root.winfo_screenwidth()
#HEIGHT = root.winfo_screenheight()

from vidstream import ScreenShareClient

sender = ScreenShareClient('192.168.1.26', 8080)
sender.start_stream()

