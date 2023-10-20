import socket
import json

from Src.BattleShipClient import BattleShipClient

def main():
    client = BattleShipClient("localhost", 8080)
    client.play()
if __name__ == "__main__":
    main()
