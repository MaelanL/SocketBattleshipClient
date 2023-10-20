# Exemple d'utilisation :
import socket
import json
from time import sleep

from Src.Client import Client

def main():
    server_address = '127.0.0.1'  # Adresse IP du serveur
    server_port = 8080  # Port du serveur

    # Création de l'instance du client
    client = Client(server_address, server_port)
    client.connect()

    try:

            x = int(input("Saisissez la coordonnée X : "))
            y = int(input("Saisissez la coordonnée Y : "))

            # Créez un objet ShipCell avec les coordonnées X et Y
            ship_cell = {"x": x, "y": y}

            # Envoi du message au serveur
            client.send_message(ship_cell)
            print(f"Message sent: {ship_cell}\n")
            # Attente et réception de la réponse du serveur
            response = client.receive_message()
            if response:
                print(f"Server response: {response}")
                # Traitez la réponse du serveur selon les besoins


    finally:
        # Fermeture de la connexion
        client.close()

if __name__ == "__main__":
    main()
