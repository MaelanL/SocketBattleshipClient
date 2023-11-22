import re
import tkinter as tk
from tkinter import messagebox

class BattleShipInterface:
    def __init__(self, game_manager_interface):
        self.game_manager_interface = game_manager_interface
        self.root = tk.Tk()
        self.root.title("Bataille Navale")
        self.create_boards()
        self.create_abandon_button()
        self.turn_label = tk.Label(self.root, text="Votre tour")
        self.turn_label.pack()

    def create_boards(self):
        self.player_board_frame = tk.LabelFrame(self.root, text="Votre Plateau :")
        self.player_board_frame.pack(side="left", padx=10, pady=10)

        self.opponent_board_frame = tk.LabelFrame(self.root, text="Plateau de l'adversaire :")
        self.opponent_board_frame.pack(side="right", padx=10, pady=10)


        for i in range(10):
            tk.Label(self.player_board_frame, text=str(i)).grid(row=0, column=i+1)
            tk.Label(self.opponent_board_frame, text=str(i)).grid(row=0, column=i+1)


        for i in range(10):
            tk.Label(self.player_board_frame, text=str(i)).grid(row=i+1, column=0)
            tk.Label(self.opponent_board_frame, text=str(i)).grid(row=i+1, column=0)


            self.player_buttons = [[tk.Button(self.player_board_frame, text=" ", state="disabled", bg="lightblue")
                                    for _ in range(10)] for _ in range(10)]

            self.opponent_buttons = [[tk.Button(self.opponent_board_frame, text=" ", bg="lightblue",
                                                command=lambda x=i, y=j: self.attack(x, y))
                                      for j in range(10)] for i in range(10)]

            for i in range(10):
                for j in range(10):
                    self.player_buttons[i][j].grid(row=i + 1, column=j + 1)
                    self.opponent_buttons[i][j].grid(row=i + 1, column=j + 1)

    def create_abandon_button(self):
        self.abandon_button = tk.Button(self.root, text="Abandonner", command=self.abandon_game)
        self.abandon_button.pack(side="bottom", pady=10)

    def attack(self, x, y):
        self.game_manager_interface.make_request(1, x, y)  # 1 pour type PLAY
        self.opponent_buttons[x][y].config(text="O", state="disabled")
        self.receive_and_handle_response()
        self.receive_and_handle_response()



    def receive_and_handle_response(self):
        response = self.game_manager_interface.client.receive_response()
        self.game_manager_interface.handle_response(response)



        #self.update_turn_label(response.get('playerTurn', False))
        #self.update_interface(response)


    def abandon_game(self):
        self.game_manager_interface.make_request(2, None, None)  # 2 pour type ABANDON
        self.receive_and_handle_response()

    def end_game(self):
        messagebox.showinfo("Fin du jeu", "Le jeu est terminé.")
        self.root.destroy()

    def run(self):
        self.root.mainloop()
