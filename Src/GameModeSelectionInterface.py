import tkinter as tk
from tkinter import messagebox

from BattleShipInterface import BattleShipInterface
from GameManagerInterface import GameManagerInterface
from client.Client import Client


class GameModeSelectionInterface:
    def __init__(self, client, root, token):
        self.client = client
        self.root = root
        self.token = token
        self.frame = tk.Frame(self.root)
        self.frame.pack()

        tk.Label(self.frame, text="Choisissez votre mode de jeu :").pack()

        self.solo_button = tk.Button(self.frame, text="Solo", command=lambda: self.select_mode('solo'))
        self.solo_button.pack(side="left", padx=10, pady=10)

        self.multi_button = tk.Button(self.frame, text="Multi", command=lambda: self.select_mode('multi'))
        self.multi_button.pack(side="right", padx=10, pady=10)

    def select_mode(self, mode):
        self.root.destroy()  # Destroy the current window
        port = 1001 if mode == 'solo' else 2001
        host = "127.0.0.1"
        client = Client(host, port)

        try:
            client.connect()
            self.launch_game_interface(client)
        except Exception as e:
            messagebox.showerror("Erreur de connexion", f"Impossible de se connecter au serveur: {e}")

    def launch_game_interface(self):
        # Lancer l'interface de jeu de la bataille navale
        game_manager_interface = GameManagerInterface(self.client, self.token)
        battle_ship_interface = BattleShipInterface(game_manager_interface)
        battle_ship_interface.run()