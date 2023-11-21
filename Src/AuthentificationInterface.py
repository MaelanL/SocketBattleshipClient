import tkinter as tk
from tkinter import messagebox

import sys
from pathlib import Path



from GameModeSelectionInterface import GameModeSelectionInterface
from client.Client import Client


class AuthenticationInterface:
    def __init__(self, auth_client):
        self.auth_client = auth_client
        self.root = tk.Tk()
        self.root.title("Authentification")

        # Création des éléments de l'interface
        tk.Label(self.root, text="Username :").grid(row=0, column=0, sticky="e")
        tk.Label(self.root, text="Password :").grid(row=1, column=0, sticky="e")

        self.username_entry = tk.Entry(self.root)
        self.password_entry = tk.Entry(self.root, show="*")

        self.username_entry.grid(row=0, column=1)
        self.password_entry.grid(row=1, column=1)

        tk.Button(self.root, text="Valider", command=self.authenticate).grid(row=2, column=0, columnspan=2)

    def authenticate(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        token = self.auth_client.authenticate(username, password)

        if len(token) == 36:  # Supposant que le token est un UUID
            messagebox.showinfo("Succès", "Authentification réussie")
            self.root.destroy()  # Fermer la fenêtre d'authentification
            self.launch_game_mode_selection()  # Lancer la sélection du mode de jeu
        else:
            messagebox.showerror("Échec", "Authentification échouée")

    def launch_game_mode_selection(self):
        # Créez un nouveau Tk root ici pour la nouvelle fenêtre
        new_root = tk.Tk()
        new_root.title("Sélection du Mode de Jeu")
        # Passez le client créé lors de l'authentification à la nouvelle interface
        game_mode_selection_interface = GameModeSelectionInterface(self.auth_client, new_root)
        game_mode_selection_interface.root.mainloop()

    def create_client_instance(self):
        # Ici, vous devez créer et retourner une instance de votre classe `Client`.
        # Vous pouvez utiliser les informations d'authentification ou d'autres paramètres nécessaires pour initialiser le client.
        host = "127.0.0.1"
        port = 9999  # Ou un autre port si nécessaire
        return Client(host, port)

    def run(self):
        self.root.mainloop()