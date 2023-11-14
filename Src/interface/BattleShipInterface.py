import tkinter as tk
from tkinter import simpledialog

from Src.client.Client import Client
from GameManagerInterface import *


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
        # Appelle la méthode pour le placement manuel
        self.game_manager.initialize_game_interface(manual_placement=True)

    def random_placement(self):
        # Appelle la méthode pour le placement aléatoire
        self.game_manager.initialize_game_interface(manual_placement=False)

    def attack(self):
        # Ouvre une boîte de dialogue pour obtenir les coordonnées d'attaque de l'utilisateur
        x, y = self.get_user_attack_coordinates()
        if x is not None and y is not None:
            self.game_manager.make_attack_interface(x, y)

    def get_user_attack_coordinates(self):
        x = simpledialog.askinteger("Attaque", "Entrez la coordonnée x (0-9):", minvalue=0, maxvalue=9)
        y = simpledialog.askinteger("Attaque", "Entrez la coordonnée y (0-9):", minvalue=0, maxvalue=9)
        return x, y

    def update_status(self, message):
        self.status_label.config(text=message)


