import json
import socket

class AuthenticationClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def authenticate(self, username, password):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
            # Create a dictionary for the auth request with type set to LOGIN
            auth_request = {
                'type': 1,  # This represents LOGIN
                'name': username,
                'password': password
            }
            # Convert the dictionary to a JSON string
            message = json.dumps(auth_request).encode('utf-8')
            udp_socket.sendto(message, (self.host, self.port))
            response, _ = udp_socket.recvfrom(1024)
            return response.decode('utf-8')


