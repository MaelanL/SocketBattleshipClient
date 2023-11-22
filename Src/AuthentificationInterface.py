import re
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
        response = self.auth_client.authenticate(username, password)
        token_match = re.search(r'token=([^)]+)', response)
        if token_match:
            token = token_match.group(1)
            status = re.search(r'status=(\d+)', response)

            if status:
                login = int(status.group(1))
                if login == 0:
                    messagebox.showinfo("Succès", "Authentification réussie")
                    self.root.destroy()  # Fermer la fenêtre d'authentification
                    self.launch_game_mode_selection(token)  # Lancer la sélection du mode de jeu
                else:
                    messagebox.showerror("Échec", "Authentification échouée")
            else:
                messagebox.showerror("Échec", "Le statut n a pas pu être extrait de la réponse")
        else:
            messagebox.showerror("Échec", "token non valide")

    def launch_game_mode_selection(self, token):
        # Créez un nouveau Tk root ici pour la nouvelle fenêtre
        new_root = tk.Tk()
        new_root.title("Sélection du Mode de Jeu")

        # Créer une nouvelle instance de Client
        client = self.create_client_instance()

        # Passez le client créé lors de l'authentification à la nouvelle interface
        game_mode_selection_interface = GameModeSelectionInterface(client, new_root, token)
        new_root.mainloop()

    def create_client_instance(self):
        host = "127.0.0.1"
        port = 9999  # Ou un autre port si nécessaire
        return Client(host, port)

    def run(self):
        self.root.mainloop()