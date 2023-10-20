import tkinter as tk
from tkinter import messagebox
from Src.BattleShipClient import BattleShipClient
import tkinter as tk
from tkinter import messagebox

from Src.ClientRequest import ClientRequest


class BattleshipGUI:
    def __init__(self, root, client):
        self.root = root
        self.client = client
        self.root.title("Battleship Game")

        # Ajout des numéros de lignes et de colonnes
        for i in range(10):
            tk.Label(self.root, text=str(i)).grid(row=i + 1, column=0)  # Numéros des lignes
            tk.Label(self.root, text=str(i)).grid(row=0, column=i + 1)  # Numéros des colonnes

        # Initialisation de la grille
        self.buttons = []
        for i in range(10):
            row = []
            for j in range(10):
                btn = tk.Button(self.root, text="", width=5, height=2, command=lambda i=i, j=j: self.attack_cell(i, j))
                btn.grid(row=i + 1, column=j + 1)  # Ajustement pour tenir compte des numéros
                row.append(btn)
            self.buttons.append(row)

    def attack_cell(self, x, y):
        self.client.connect()

        # Envoie de la requête au serveur
        request = ClientRequest(x, y)
        self.client.send_request(request)

        # Obtention de la réponse du serveur
        response = self.client.receive_response()

        # Mettre à jour l'interface en fonction de la réponse
        # Par exemple, vous pourriez changer la couleur du bouton pour indiquer si le tir a touché ou manqué
        if response["opponentCellsDamaged"]:
            self.buttons[x][y].config(bg='red')
        else:
            self.buttons[x][y].config(bg='blue')

        # Affichage des messages en fonction de la réponse
        if response["hasPlayerWon"]:
            messagebox.showinfo("Game Over", "You have won!")
            self.root.destroy()
        elif response["hasOpponentWon"]:
            messagebox.showinfo("Game Over", "Opponent has won!")
            self.root.destroy()

        self.client.close()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    client = BattleShipClient("localhost", 8080)  # Ajustez l'adresse et le port en fonction de votre configuration
    gui = BattleshipGUI(root, client)
    gui.run()
