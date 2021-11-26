from vidstream import StreamingServer
import threading

host = StreamingServer('192.168.1.26', 8080)
th = threading.Thread(target=host.start_server)
th.start()

while input("") != "stop":
    continue

host.stop_server()
