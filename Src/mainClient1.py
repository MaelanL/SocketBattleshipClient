import socket
import json

from Src.client.Client import Client
from Src.gameHandler.GameManager import GameManager


def get_user_attack_coordinates():
    x = int(input("Entrez x : "))
    y = int(input("Entrez y : "))
    return x, y

def mainClient1():
    host = "127.0.0.1"
    port = 2000

    client = Client(host, port)
    client.connect()

    game_manager = GameManager(client)
    game_manager.initialize_game()

    game_over = False
    while not game_over:
        response = client.receive_response()
        game_over = game_manager.handle_response(response)

        if not game_over and game_manager.is_player_turn(response):
            x, y = get_user_attack_coordinates()
            game_manager.make_attack(x, y)

    client.close()

if __name__ == "__main__":
    mainClient1()
