# from vidstream import StreamingServer

# class Stream:
#     def __init__(self, host_addr, port=8080) -> None:
#         self.host_addr = host_addr
#         self.port = port
#         self.service = None
#     def begin_stream(self):
#         self.service = StreamingServer(self.host_addr, 8080)
#         #th = threading.Thread(target=self.service.start_server)
#         #th.start()
#         self.service.start_server()
        
#     def stop_stream(self):
#         self.service.stop_server()

from socket import socket
from threading import Thread
from zlib import compress

from mss import mss

"""
RETRIEVED FROM https://newbedev.com/screen-sharing-in-python
"""

WIDTH = 1000
HEIGHT = 700

class Stream:
    def __init__(self, host) -> None:
        self.host = host
    def retreive_screenshot(self, conn):
        try:
            with mss() as sct:
                # The region to capture
                rect = {'top': 0, 'left': 0, 'width': WIDTH, 'height': HEIGHT}

                while 'recording':
                    # Capture the screen
                    img = sct.grab(rect)
                    # Tweak the compression level here (0-9)
                    pixels = compress(img.rgb, 6)

                    # Send the size of the pixels length
                    size = len(pixels)
                    size_len = (size.bit_length() + 7) // 8
                    conn.send(bytes([size_len]))

                    # Send the actual pixels length
                    size_bytes = size.to_bytes(size_len, 'big')
                    conn.send(size_bytes)

                    # Send pixels
                    conn.sendall(pixels)
        except ConnectionAbortedError: pass

    def start_stream(self, port=5000):
        sock = socket()
        sock.bind((self.host, port))
        try:
            sock.listen(5)
            print('Server started.')

            while 'connected':
                conn, addr = sock.accept()
                print('Client connected IP:', addr)
                thread = Thread(target=self.retreive_screenshot, args=(conn,))
                thread.start()
        except ConnectionAbortedError: pass
        finally:
            sock.close()

