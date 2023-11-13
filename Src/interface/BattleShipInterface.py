import tkinter as tk
from tkinter import simpledialog

from Src.client.Client import Client
from Src.gameHandler.GameManager import GameManager


class BattleShipInterface:
    def __init__(self, master, game_manager):
        self.master = master
        self.game_manager = game_manager
        master.title("Bataille Navale")

        self.status_label = tk.Label(master, text="Bienvenue à la Bataille Navale!")
        self.status_label.pack()

        self.game_frame = tk.Frame(master)
        self.game_frame.pack()
        self.initialize_game_board()

        self.manual_placement_button = tk.Button(master, text="Placement Manuel", command=self.manual_placement)
        self.manual_placement_button.pack()

        self.random_placement_button = tk.Button(master, text="Placement Aléatoire", command=self.random_placement)
        self.random_placement_button.pack()

        self.attack_button = tk.Button(master, text="Attaquer", command=self.attack)
        self.attack_button.pack()

    def initialize_game_board(self):
        self.buttons = [[tk.Button(self.game_frame, text="", width=3, height=1) for _ in range(10)] for _ in range(10)]
        for i in range(10):
            for j in range(10):
                self.buttons[i][j].grid(row=i, column=j)

    def manual_placement(self):
        # Logique pour le placement manuel des bateaux
        pass

    def random_placement(self):
        # Logique pour le placement aléatoire des bateaux
        pass

    def attack(self):
        # Logique pour l'attaque
        pass

    def update_status(self, message):
        self.status_label.config(text=message)

def main():
    root = tk.Tk()
    client = Client("127.0.0.1", 1110)
    game_manager = GameManager(client)
    app = BattleShipInterface(root, game_manager)
    root.mainloop()

if __name__ == "__main__":
    main()
