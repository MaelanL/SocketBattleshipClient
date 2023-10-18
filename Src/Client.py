import socket
import json

class Client:
    def __init__(self, server_address, server_port):
        self.server_address = server_address
        self.server_port = server_port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        try:
            self.socket.connect((self.server_address, self.server_port))
            print("Connected to the server.")
        except Exception as e:
            print(f"Error connecting to the server: {e}")

    def send_message(self, message):
        try:
            json_message = json.dumps(message)
            self.socket.send(json_message.encode())
        except Exception as e:
            print(f"Error sending message: {e}")

    def receive_message(self):
        try:
            data = self.socket.recv(1024)
            if data:
                message = json.loads(data.decode())
                return message
        except Exception as e:
            print(f"Error receiving message: {e}")
        return None

    def close(self):
        self.socket.close()
        print("Connection closed.")


