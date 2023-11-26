import re
import socket
import json
import sys
from pathlib import Path

# Calculez le chemin du répertoire parent et imprimez-le pour le vérifier
#parent_dir = str(Path(__file__).parent.parent)
#sys.path.append(parent_dir)

from Src.client.AuthenticationClient import AuthenticationClient
from Src.client.Client import Client
from Src.gameHandler.GameManager import GameManager


def get_user_attack_coordinates():
    x = int(input("Entrez x : "))
    y = int(input("Entrez y : "))
    return x, y

def mainReconnexionClient3():
    auth_host = "127.0.0.1"
    auth_port = 9999  # Le même port que celui du AuthServer

    auth_client = AuthenticationClient(auth_host, auth_port)
    username = input("Nom d'utilisateur: ")
    password = input("Mot de passe: ")

    # Authenticate and get the full response
    response = auth_client.authenticate(username, password)
    # Convertir la chaîne JSON en dictionnaire Python
    print(response)

    # Utiliser les expressions régulières pour trouver le statut
    status = re.search(r'status=(\d+)', response)

    if status:
        login = int(status.group(1))
        print(login)
        if login == 0:
            print("Connexion réussie")
            # Extract the token from the response
            token_match = re.search(r"token=([^,]+)", response)

            if token_match:
                token = token_match.group(1)
                print("Extracted token:", token)
                mode = input("taper solo si vous voulez en solo, sinon taper multi: ")
                if mode =="solo":
                    host = "127.0.0.1"
                    port = 1001
                    print("Connexion au serveur de jeu solo...")
                else:
                    host = "127.0.0.1"
                    port = 2001
                    print("Connexion au serveur de jeu multi...")


                client = Client(host, port)
                client.connect()


                reconnexion = input("ecrire jouer si vous voulez commencer une partie sinon ecrire reconnexion: ")
                if reconnexion == "reconnexion":
                    # envoie requette avec le game idea , le type=3 et le token
                    type = "3"
                    game_id_search = re.search(r"gameId=([^\)]+)", response)

                    # Récupérer le gameId si trouvé
                    gameId = game_id_search.group(1)
                    print(gameId)
                    #message erreur si gameId est null
                    if gameId == "null":
                        print("pas de partie en cours")
                    request = {'type': type, 'token': token, 'gameId': gameId}
                    game_manager = GameManager(client)
                    print(request)
                    client.send_request(request)
                    game_over = False
                    roomId = "0"
                    while not game_over:
                        print("on est la")
                        response = client.receive_response()
                        print(response)
                        game_over = game_manager.handle_response(response)

                        if not game_over:
                            game_manager.update_board(game_manager.player_board,
                                                      response.get('playerCellsAttacked', []),
                                                      response.get('playerCellsDamaged', []))
                            game_manager.update_board(game_manager.opponent_board,
                                                      response.get('opponentCellsAttacked', []),
                                                      response.get('opponentCellsDamaged', []))

                            game_manager.print_boards()

                            if game_manager.is_player_turn(response):
                                type = input("taper 2 si vous voulez abandonner, sinon taper 1: ")
                                # si type = 2, on abandonne la partie sinon on joue
                                if type == "2":
                                    game_manager.make_request(type, token, roomId, None, None)
                                    print("Vous avez abandonné la partie")


                                else:
                                    x, y = get_user_attack_coordinates()
                                    game_manager.make_request(type, token, roomId, x, y)
                else :
                    if mode == "solo":
                        roomId = "0"
                    else:
                        roomId = input("Entrez le roomId: ")

                    game_manager = GameManager(client)
                    game_manager.initialize_game(mode, token, roomId)

                    game_over = False
                    while not game_over:
                        response = client.receive_response()
                        game_over = game_manager.handle_response(response)

                        if not game_over:
                            game_manager.update_board(game_manager.player_board,
                                                      response.get('playerCellsAttacked', []),
                                                      response.get('playerCellsDamaged', []))
                            game_manager.update_board(game_manager.opponent_board,
                                                      response.get('opponentCellsAttacked', []),
                                                      response.get('opponentCellsDamaged', []))

                            game_manager.print_boards()

                            if game_manager.is_player_turn(response):
                                type = input("taper 2 si vous voulez abandonner, sinon taper 1: ")
                                # si type = 2, on abandonne la partie sinon on joue
                                if type == "2":
                                    game_manager.make_request(type, token, roomId, None, None)
                                    print("Vous avez abandonné la partie")

                                else:
                                    x, y = get_user_attack_coordinates()
                                    game_manager.make_request(type, token, roomId, x, y)

                client.close()
            else:
                print("Échec de l'obtention du token")
        else:
            print("Échec de l'authentification")
    else:
        print("Le statut n'a pas pu être extrait de la réponse")

if __name__ == "__main__":
    mainReconnexionClient3()