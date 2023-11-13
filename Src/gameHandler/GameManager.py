from Src.model.ShipCell import ShipCell


class GameManager:
    def __init__(self, client):
        self.client = client

    def initialize_game(self):
        initial_board = [
            ShipCell(0, 0), ShipCell(0, 1), ShipCell(0, 2),
            ShipCell(0, 3), ShipCell(0, 4)
        ]
        board_dict = [cell.to_dict() for cell in initial_board]
        request = {'board': board_dict, 'x': None, 'y': None}
        self.client.send_request(request)

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
