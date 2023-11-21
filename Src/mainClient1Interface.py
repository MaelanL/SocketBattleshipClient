import sys
from pathlib import Path

from AuthentificationInterface import AuthenticationInterface
from client.AuthenticationClient import AuthenticationClient



# Assurez-vous que l'importation se fait après l'ajout du chemin au sys.path
from client.Client import Client
from GameModeSelectionInterface import GameModeSelectionInterface
from AuthentificationInterface import AuthenticationInterface
from client.AuthenticationClient import AuthenticationClient

import tkinter as tk

def mainClient1Interface():
    host = "127.0.0.1"
    port = 9999  # Le même port que celui du AuthServer
    auth_client = AuthenticationClient(host, port)
    auth_interface = AuthenticationInterface(auth_client)
    auth_interface.run()



if __name__ == "__main__":
    mainClient1Interface()
