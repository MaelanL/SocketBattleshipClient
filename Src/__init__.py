# Exemple d'utilisation :
import socket
import json
from Src.Client import Client

def main():
    server_address = '127.0.0.1'  # Adresse IP du serveur
    server_port = 8080  # Port du serveur

    # Création de l'instance du client
    client = Client(server_address, server_port)
    client.connect()

    try:
        # Créez le message que vous souhaitez envoyer sous forme de dictionnaire
        message_to_send = {
            "action": "fire",
            "x": 3,
            "y": 4
        }

        # Envoi du message au serveur
        client.send_message(message_to_send)

        # Attente et réception de la réponse du serveur
        response = client.receive_message()
        if response:
            print(f"Server response: {response}")

    finally:
        # Fermeture de la connexion
        client.close()



if __name__ == "__main__":
    main()
