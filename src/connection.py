# This module contains all components for creating a network connection between two devices
# This includes LAN and bluetooth connections

import bluetooth as bt
import socket, time, virtualmonitor
from threading import Thread
from streamserver import Stream

service_name = "PSS Service"
service_uuid  = "5feb8726-447b-42ed-b1f5-98570a97f5e5" #obtained from an online UUID generator

class Server:
    active = False
    def __init__(self, type, port) -> None:
        self.host = socket.gethostbyname(socket.gethostname())
        self.type = type
        self.port = port
        self.found_devices = []
        self.scanning = False
        self.requests = []
        self.stream = None
        if type == 'Bluetooth':
            self.socket = bt.BluetoothSocket(bt.RFCOMM)
        else:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        Server.active = True

        # Create a screen-share server so people can tune in
        streamer = Thread(target=self.start_stream_server, daemon=True)
        streamer.start()
    
    def get_subnet(self):
        sub = self.host.split(sep='.')
        return f'{sub[0]}.{sub[1]}.{sub[2]}.'

    def start(self):
        if self.type == 'Bluetooth':
            # Allow for devices to find this one
            self.socket.bind(('',self.port)) # NEEDS TO CHANGE TO A BLUETOOTH ADDRESS
            print("Listening for connections on port",self.port)
            self.socket.listen(5)
            
            bt.advertise_service(self.socket, service_name, service_uuid)
            client_socket,address = self.socket.accept()
            print('Accepted connection from', address)
            data = client_socket.recv(1024)
            print('Received [%s]' % data)
            client_socket.close()
            self.socket.close()
        elif self.type == 'LAN':
            #Bind socket to a port number and listen on that port
            self.socket.bind((self.host, self.port))
            print("Listening for connections on port",self.port)
            self.socket.listen(5)
            acceptor = Thread(target=self.accept_scans, daemon=True)
            acceptor.start()

    # Uses network adapters to find devices hosting the PSS service 
    def scan(self): #client
        self.scanning = True
        if self.type == "Bluetooth":
            self.found_devices = bt.find_service(name=service_name, uuid=service_uuid)
            if len(self.found_devices) == 0:
                print('No other users found')
                return None
            print(len(self.found_devices),'found hosting PSS service.')
            return self.found_devices
        elif self.type == "LAN":
            subnet = self.get_subnet()
            #Scan the port, add any found devices into active_services
            while True:            
                for i in range(2,255):
                    if not self.scanning or not Server.active:
                        # Clear the found devices
                        self.found_devices.clear()
                        print('No longer scanning.')
                        return
                    addr = subnet+str(i)
                    if addr == self.host:
                        continue
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(0.1)
                    res = sock.connect_ex((addr,self.port))
                    sock.close()
                    result = res == 0
                    if result:
                        dev = socket.gethostbyaddr(addr)[0]
                        if dev in self.found_devices:
                            continue
                        print("Device found at", addr+":"+str(self.port))
                        self.found_devices.append(dev)
        else:
            print("No connection.")
    
    def accept_scans(self): #server
        while Server.active:
            try:
                client_socket,address = self.socket.accept()
            except OSError: break
            print('Accepted connection from', address)
            msg = client_socket.recv(1024)
            if msg.decode() != '':
                print('YOU HAVE RECEIVED A REQUEST')
                self.requests.append(msg.decode())
            else:
                print('Scanned only, closing connection socket')
                client_socket.close()
        
        print('No longer accepting scans...')
    
    def stop(self):
        Server.active = False #causes all threads to stop
        self.socket.close()
        #self.stream.stop_stream()
    
    def start_stream_server(self):
        self.stream = Stream(self.host)
        self.stream.start_stream()

    def get_stream(self, server_addr):
        virtualmonitor.stream_from(server_addr)
    
    def send_request(self, client_ip): #server
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        result = s.connect_ex((client_ip, self.port))
        if result != 0:
            print(f'Cannot connect to {client_ip}')
            return -1
        msg = socket.gethostbyaddr(self.host)[0]
        s.send(msg.encode())
        print('Sent request!')
    
    def get_client_addr(self, client_name): #server
        return socket.gethostbyname(client_name)