import random

from Src.model.ShipCell import ShipCell


class GameManager:
    def __init__(self, client):
        self.client = client

    def initialize_game(self):
        choice = input("Choisissez la configuration des bateaux (manuel/aleatoire) : ")
        if choice.lower() == "manuel":
            board = self.manual_ship_placement()
        else:
            board = self.random_ship_placement()
        board_dict = [cell.to_dict() for cell in board]
        request = {'board': board_dict, 'x': None, 'y': None}
        self.client.send_request(request)

    def manual_ship_placement(self):
        board = []
        print("Placez vos bateaux (saisissez les coordonnées x et y) :")
        for _ in range(5):  # Nombre de bateaux à placer
            while True:
                try:
                    x = int(input("x: "))
                    y = int(input("y: "))
                    if 0 <= x < 10 and 0 <= y < 10:  # Assurez-vous que les coordonnées sont dans la grille
                        board.append(ShipCell(x, y))
                        break
                    else:
                        print("Coordonnées hors de la grille. Réessayez.")
                except ValueError:
                    print("Entrée invalide. Veuillez saisir des nombres.")
        return board

    def random_ship_placement(self):
        board = []
        for _ in range(5):  # Nombre de bateaux à placer
            while True:
                x, y = random.randint(0, 9), random.randint(0, 9)
                if ShipCell(x, y) not in board:  # Vérifie si le bateau n'est pas déjà placé
                    board.append(ShipCell(x, y))
                    break
        return board

    def make_attack(self, x, y):
        request = {'board': None, 'x': x, 'y': y}
        self.client.send_request(request)

    def handle_response(self, response):
        print("Réponse du serveur :", response)

        if response.get("hasPlayerWon"):
            print("Vous avez gagné !")
            return True  # Indique que le jeu est terminé

        if response.get("hasOpponentWon"):
            print("Vous avez perdu !")
            return True  # Indique que le jeu est terminé

        return False  # Continue le jeu

    def is_player_turn(self, response):
        return response.get("isPlayerTurn", False)
