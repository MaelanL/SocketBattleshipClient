import tkinter as tk
from tkinter import simpledialog

# La fonction start_listening_to_server peut être définie ici ou avant la fonction main
import threading

from Src.client.Client import Client
from Src.interface.BattleShipInterface import BattleShipInterface
from Src.interface.GameManagerInterface import GameManagerInterface



def start_listening_to_server(game_manager_interface):
    threading.Thread(target=game_manager_interface.listen_to_server, daemon=True).start()


def mainClient1Interface():
    root = tk.Tk()
    client = Client("127.0.0.1", 1000)
    client.connect()

    # La fonction lambda est utilisée ici comme un exemple de callback pour mettre à jour l'UI
    game_manager_interface = GameManagerInterface(client, lambda message: print(message))

    app = BattleShipInterface(root, game_manager_interface)
    root.mainloop()

if __name__ == "__main__":
    mainClient1Interface()
