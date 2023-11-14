import random

from Src.model.ShipCell import ShipCell


class GameManagerInterface:
    def __init__(self, client, update_ui_callback):
        self.client = client
        self.update_ui_callback = update_ui_callback

    def initialize_game_interface(self, manual_placement):
        if manual_placement:
            board = self.manual_ship_placement_interface()
        else:
            board = self.random_ship_placement_interface()

        board_dict = [cell.to_dict() for cell in board]
        request = {'board': board_dict, 'x': None, 'y': None}
        self.client.send_request(request)
        response = self.client.receive_response()
        self.update_ui_callback(response)

    def manual_ship_placement_interface(self):
        board = []
        for _ in range(5):  # Nombre de bateaux à placer
            x, y = self.get_ship_coordinates_from_user()
            board.append(ShipCell(x, y))
        return board

    def random_ship_placement_interface(self):
        board = []
        for _ in range(5):  # Nombre de bateaux à placer
            x, y = random.randint(0, 9), random.randint(0, 9)
            board.append(ShipCell(x, y))
        return board

    def make_attack_interface(self, x, y):
        request = {'board': None, 'x': x, 'y': y}
        self.client.send_request(request)
        response = self.client.receive_response()
        self.update_ui_callback(response)

    def listen_to_server(self):
        while True:
            response = self.client.receive_response()
            self.update_ui_callback(response)

    def get_ship_coordinates_from_user(self):
        # Cette méthode devrait être modifiée pour utiliser une boîte de dialogue Tkinter
        pass
