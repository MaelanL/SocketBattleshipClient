import random

from model.ShipCell import ShipCell


class GameManagerInterface:
    def __init__(self, client, token):
        self.client = client
        self.token = token
        self.player_board = [['O'] * 10 for _ in range(10)]
        self.opponent_board = [['O'] * 10 for _ in range(10)]
        self.initialize_game()

    def initialize_game(self,token):
        board = self.random_ship_placement()
        board_dict = [cell.to_dict() for cell in board]
        request = {'board': board_dict, 'computerLevel': 2, 'token': token, 'x': None, 'y': None}
        self.client.send_request(request)
        # Gérer la réponse initiale du serveur, si nécessaire

    def random_ship_placement(self):
        board = []
        for _ in range(5):  # Pour l'exemple, on place 5 bateaux
            while True:
                x, y = random.randint(0, 9), random.randint(0, 9)
                if not any(ship.x == x and ship.y == y for ship in board):
                    board.append(ShipCell(x, y))
                    break
        return board


    def make_request(self, request_type, x, y):
        request = {'type': request_type, 'token': self.token, 'x': x, 'y': y}
        self.client.send_request(request)

    def handle_response(self, response):
        pass
    def update_interface(self):
        # Utilisez self.player_board et self.opponent_board pour mettre à jour l'interface graphique
        # avec l'état actuel des plateaux de jeu
        pass
