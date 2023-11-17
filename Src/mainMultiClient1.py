import socket
import json

from Src.client.AuthenticationClient import AuthenticationClient
from Src.client.Client import Client
from Src.gameHandler.GameManager import *



def get_user_attack_coordinates():
    x = int(input("Entrez x : "))
    y = int(input("Entrez y : "))
    return x, y

def mainMultiClient1():
    auth_host = "127.0.0.1"
    auth_port = 9999  # Le même port que celui du AuthServer

    auth_client = AuthenticationClient(auth_host, auth_port)
    username = input("Nom d'utilisateur: ")
    password = input("Mot de passe: ")
    token = auth_client.authenticate(username, password)

    if len(token) == 36:  # Supposant que le token est un UUID
        host = "127.0.0.1"
        port = 2001
        print("Connexion au serveur de jeu...")
        client = Client(host, port)
        client.connect()

        game_manager = GameManager(client)
        game_manager.initialize_game()

        game_over = False
        while not game_over:
            response = client.receive_response()
            game_over = game_manager.handle_response(response)

            if not game_over:
                game_manager.update_board(game_manager.player_board, response.get('playerCellsAttacked', []),
                                          response.get('playerCellsDamaged', []))
                game_manager.update_board(game_manager.opponent_board, response.get('opponentCellsAttacked', []),
                                          response.get('opponentCellsDamaged', []))

                game_manager.print_boards()

                if game_manager.is_player_turn(response):
                    type = input("taper 2 si vous voulez abandonner, sinon taper 1: ")
                    # si type = 2, on abandonne la partie sinon on joue
                    if type == "2":
                        game_manager.make_request(type, None, None)
                        print("Vous avez abandonné la partie")


                    else:
                        x, y = get_user_attack_coordinates()
                        game_manager.make_request(type, x, y)

        client.close()
    else:
        print("Échec de l'authentification")



if __name__ == "__main__":
    mainMultiClient1()
