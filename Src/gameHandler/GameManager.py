import random

import sys
from pathlib import Path

# Calculez le chemin du répertoire parent et imprimez-le pour le vérifier
parent_dir = str(Path(__file__).parent.parent)
sys.path.append(parent_dir)
from model.ShipCell import ShipCell


class GameManager:
    def __init__(self, client):
        self.client = client
        # Initialisation des plateaux du joueur et de l'adversaire
        self.player_board = [['O'] * 10 for _ in range(10)]
        self.opponent_board = [['O'] * 10 for _ in range(10)]
        self.computer_level = 1

    def initialize_game(self,mode,token):
        if mode =="solo":
            self.computer_level = input("Choisissez le niveau de l'ordinateur (1-3, laissez vide pour niveau 1): ") or '1'
            self.computer_level = int(self.computer_level)
        else :
            self.computer_level =0

        choice = input("Choisissez la configuration des bateaux (manuel/aleatoire) : ")
        if choice.lower() == "manuel":
            board = self.manual_ship_placement()
        else:
            board = self.random_ship_placement()

        board_dict = [cell.to_dict() for cell in board]
        request = {'token': token, 'board': board_dict, 'computerLevel': self.computer_level, 'x': None, 'y': None}
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

    def make_request(self, type,token, x, y):
        request = {
            'type': type,
            'token': token,
            'board': None,
            'x': x,
            'y': y}
        self.client.send_request(request)

    def handle_response(self, response):
        print("Réponse du serveur :", response)

        if response.get("playerWon"):
            print("Vous avez gagné !")
            return True  # Indique que le jeu est terminé

        if response.get("opponentWon"):
            print("Vous avez perdu !")
            return True  # Indique que le jeu est terminé

        return False  # Continue le jeu

    def is_player_turn(self, response):
        return response.get("playerTurn", False)

    def print_boards(self):
        # En-têtes pour les colonnes ajustées pour l'alignement
        cols = ' ' * 2 + '  '.join([f'{i}' for i in range(10)])  # Commencez par 0 à 9
        print("\n" + "Votre plateau:" + " " * 23 + "Plateau adverse:")
        print(cols + " " * 7 + cols)

        for i in range(10):
            player_row = ['•' if cell == 'O' else ('X' if cell == 'X' else 'O') for cell in self.player_board[i]]
            opponent_row = ['•' if cell == 'O' else ('X' if cell == 'X' else 'O') for cell in self.opponent_board[i]]
            # Ajoutez deux espaces entre chaque symbole pour une apparence de grille carrée
            player_row_formatted = '  '.join(player_row)
            opponent_row_formatted = '  '.join(opponent_row)
            # Alignez les numéros des lignes à droite et ajustez les espaces
            print(f'{i} {player_row_formatted}  ' + " " * 5 + f'{i} {opponent_row_formatted}')

    def update_board(self, board, cells_attacked, cells_damaged):
        for cell in cells_attacked:
            x, y = cell['x'], cell['y']
            board[y][x] = 'X'  # Marque le tir sans toucher de bateau
        for cell in cells_damaged:
            x, y = cell['x'], cell['y']
            board[y][x] = '1'  # Marque le coup réussi sur un bateau
