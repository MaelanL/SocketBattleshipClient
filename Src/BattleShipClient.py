import json
import socket

from Src.ClientRequest import ClientRequest


class BattleShipClient:
    def __init__(self, server_host, server_port):
        self.server_host = server_host
        self.server_port = server_port
        self.socket = None

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.server_host, self.server_port))

    def send_request(self, client_request):
        message = client_request.to_json() + "\n"  # Adding newline as a delimiter
        self.socket.sendall(message.encode())

    def receive_response(self):
        data = self.socket.recv(1024)
        return json.loads(data.decode())

    def close(self):
        self.socket.close()

    def play(self):
        try:
            self.connect()
            while True:
                # Get user input for x and y coordinates
                x = int(input("Enter x-coordinate: "))
                y = int(input("Enter y-coordinate: "))

                # Create request and send to server
                request = ClientRequest(x, y)
                self.send_request(request)

                # Get server response and print
                response = self.receive_response()
                print("Server Response:", response)

                # Check for game over conditions
                if response["hasPlayerWon"] or response["hasOpponentWon"]:
                    break
        finally:
            self.close()
