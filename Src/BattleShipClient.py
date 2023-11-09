import json
import socket
import random

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

    def place_ships(self):
        print("How would you like to place your ships?")
        print("1. Random placement")
        print("2. Manual placement")

        choice = input("Enter your choice (1 or 2): ")

        if choice == "1":
            self.place_ships_random()
        elif choice == "2":
            self.place_ships_manual()
        else:
            print("Invalid choice. Exiting.")

    def place_ships_random(self):
        board = [{"x": random.randint(0, 9), "y": random.randint(0, 9)} for _ in range(15)]
        request = ClientRequest(board=board)
        self.send_request(request)

    def place_ships_manual(self):
        print("Enter the coordinates to place your ships (e.g., 0 1)")
        board = [{"x": int(x), "y": int(y)} for x, y in [input("Enter coordinates: ").split() for _ in range(15)]]
        request = ClientRequest(board=board)
        self.send_request(request)


    def play(self):
        try:
            self.connect()
            self.place_ships()
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