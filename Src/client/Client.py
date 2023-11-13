import socket
import json

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = None

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))

    def send_request(self, request):
        message = json.dumps(request)
        self.socket.sendall(message.encode('utf-8'))

    def receive_response(self):
        response = self.socket.recv(4096)
        return json.loads(response.decode('utf-8'))

    def close(self):
        self.socket.close()
