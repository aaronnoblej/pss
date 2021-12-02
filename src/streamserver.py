from vidstream import StreamingServer
import threading

class Stream:
    def __init__(self, host_addr, port=8080) -> None:
        self.host_addr = host_addr
        self.port = port
        self.service = None
    def begin_stream(self):
        self.service = StreamingServer(self.host_addr, 8080)
        #th = threading.Thread(target=self.service.start_server)
        #th.start()
        self.service.start_server()
        
    def stop_stream(self):
        self.service.stop_server()
