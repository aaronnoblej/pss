# This module contains code for producing a "virtual monitor" on client screens that display the host's screen

# from vidstream import ScreenShareClient

# #WIDTH = root.winfo_screenwidth()
# #HEIGHT = root.winfo_screenheight()

# def stream_from(address, port=8080):
#     client = ScreenShareClient(address, port)
#     client.start_stream()

"""
RETRIEVED FROM https://newbedev.com/screen-sharing-in-python
"""
from socket import socket
from zlib import decompress

import pygame

WIDTH = 1000
HEIGHT = 700


def recvall(conn, length):
    """ Retreive all pixels. """

    buf = b''
    while len(buf) < length:
        data = conn.recv(length - len(buf))
        if not data:
            return data
        buf += data
    return buf


def stream_from(host, port=5000):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    watching = True

    sock = socket()
    sock.connect((host, port))
    try:
        while watching:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    watching = False
                    break

            # Retreive the size of the pixels length, the pixels length and pixels
            size_len = int.from_bytes(sock.recv(1), byteorder='big')
            size = int.from_bytes(sock.recv(size_len), byteorder='big')
            pixels = decompress(recvall(sock, size))

            # Create the Surface from raw pixels
            img = pygame.image.fromstring(pixels, (WIDTH, HEIGHT), 'RGB')

            # Display the picture
            screen.blit(img, (0, 0))
            pygame.display.flip()
            clock.tick(60)
    finally:
        sock.close()
