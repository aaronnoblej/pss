from vidstream import StreamingServer
import threading

class Stream:
    def __init__(self, host_addr, port=8080) -> None:
        self.host_addr = host_addr
        self.port = port
    def begin_stream(self):
        host = StreamingServer(self.host_addr, 8080)
        th = threading.Thread(target=host.start_server)
        th.start()
        
        while input("") != "stop":
            continue

        host.stop_server()
