# This module contains all components for creating a network connection between two devices
# This includes LAN and bluetooth connections

import bluetooth as bt
import socket, time, ipaddress, os, subprocess
from threading import Thread

service_name = "PSS Service"
service_uuid  = "5feb8726-447b-42ed-b1f5-98570a97f5e5" #obtained from an online UUID generator
SCAN_PORT = 9184

class Server:
    def __init__(self, type, port) -> None:
        self.host = socket.gethostbyname(socket.gethostname())
        self.type = type
        self.port = port
        if type == 'Bluetooth':
            self.socket = bt.BluetoothSocket(bt.RFCOMM)
        else:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def get_subnet(self):
        sub = self.host.split(sep='.')
        return f'{sub[0]}.{sub[1]}.{sub[2]}.'

    def start(self):
        if self.type == 'Bluetooth':
            # Allow for devices to find this one
            self.socket.bind(('',self.port)) # NEEDS TO CHANGE TO A BLUETOOTH ADDRESS
            print("Listening for connections on port",self.port)
            self.socket.listen(1)

            #bt.advertise_service(bt_socket, service_name, service_uuid)
            client_socket,address = self.socket.accept()
            print('Accepted connection from', address)
            data = client_socket.recv(1024)
            print('Received [%s]' % data)
            client_socket.close()
            self.socket.close()
        elif self.type == 'LAN':
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #Bind socket to a port number and listen on that port
            self.socket.bind((self.host, self.port))
            print("Listening for connections on port",self.port)
            self.socket.listen(1)
            acceptor = Thread(target=self.accept_scans, daemon=True)
            acceptor.start()

    # Uses network adapters to find devices hosting the PSS service 
    def scan(self, duration=5):
        if self.type == "Bluetooth":
            active_services = bt.find_service(name=service_name, uuid=service_uuid)
            if len(active_services) == 0:
                print('No other users found')
                return None
            print(len(active_services),'found hosting PSS service.')
            return active_services
        elif self.type == "LAN":
            active_services = []
            time_begin = time.time()
            subnet = self.get_subnet()
            #Scan the port, add any found devices into active_services
            while True:            
                for i in range(2,255):
                    if time.time() - time_begin >= duration:
                        return active_services
                    addr = subnet+str(i)
                    print(addr)
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(1)
                    res = sock.connect_ex((addr,self.port))
                    sock.close()
                    print(res)
                    result = res == 0
                    if result:
                        print("Device found at", addr+":"+str(self.port))
                        active_services.append(socket.gethostbyaddr(addr))
        else:
            print("No connection.")
    
    def accept_scans(self):
        print('True!')
        while True:
            client_socket,address = self.socket.accept()
            print('Accepted connection from', address)
            data = client_socket.recv(1024)
            print('Received [%s]' % data)
            #client_socket.close()
            #self.socket.close()

def tester():
    net_addr = '192.168.1.0/24'
    ip_net = ipaddress.ip_network(net_addr)

    # Get all hosts on that network
    all_hosts = list(ip_net.hosts())
    print(all_hosts)

    # Configure subprocess to hide the console window
    info = subprocess.STARTUPINFO()
    info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    info.wShowWindow = subprocess.SW_HIDE

    # For each IP address in the subnet, 
    # run the ping command with subprocess.popen interface
    for i in range(len(all_hosts)):
        output = subprocess.Popen(['ping', '-n', '1', '-w', '10', str(all_hosts[i])], stdout=subprocess.PIPE, startupinfo=info).communicate()[0]
        
        if "Destination host unreachable" in output.decode('utf-8'):
            print(str(all_hosts[i]), "is Offline")
        elif "Request timed out" in output.decode('utf-8'):
            print(str(all_hosts[i]), "is Offline")
        else:
            print(str(all_hosts[i]), "is Online")

# DRIVER CODE

lan = Server('LAN', 14572)
lan.start()

lan.scan()



#test for retrieiving devices on LAN, refer to https://stackoverflow.com/questions/207234/list-of-ip-addresses-hostnames-from-local-network-in-python

#create_bluetooth_server(bt.PORT_ANY)


# NOW NEED TO SET UP A CLIENT SIDE, WHICH IS USED FOR SENDING THE SCANS (CLIENT WILL SEND PINGS TO THE HOST SERVERS, WHO SHOULD RESPOND IF CONNECTION IS SUCCESSFUL)
# DEVICE ADDED TO LIST AND SHOW UP ON GUI
# SET UP CONTINUOUS SCANNING, WHICH ENDS ONCE WE GO BACK