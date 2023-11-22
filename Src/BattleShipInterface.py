import tkinter as tk
from tkinter import messagebox

class BattleShipInterface:
    def __init__(self, game_manager_interface):
        self.game_manager_interface = game_manager_interface
        self.root = tk.Tk()
        self.root.title("Bataille Navale")

        self.create_boards()
        self.create_attack_button()

    def create_boards(self):
        self.player_board_frame = tk.LabelFrame(self.root, text="Votre Plateau :", bg="blue")
        self.player_board_frame.pack(side="left", padx=10, pady=10)

        self.opponent_board_frame = tk.LabelFrame(self.root, text="Plateau de l'adversaire :", bg="blue")
        self.opponent_board_frame.pack(side="right", padx=10, pady=10)

        # Add column numbers above the boards
        for i in range(10):
            tk.Label(self.player_board_frame, text=str(i), bg="blue").grid(row=0, column=i+1)
            tk.Label(self.opponent_board_frame, text=str(i), bg="blue").grid(row=0, column=i+1)

        # Add row numbers to the side of the boards
        for i in range(10):
            tk.Label(self.player_board_frame, text=str(i), bg="blue").grid(row=i+1, column=0)
            tk.Label(self.opponent_board_frame, text=str(i), bg="blue").grid(row=i+1, column=0)

        # Create grids for the game boards
        self.player_buttons = [[tk.Button(self.player_board_frame, text=" ", state="disabled", bg="lightblue")
                                for _ in range(10)] for _ in range(10)]
        self.opponent_buttons = [[tk.Button(self.opponent_board_frame, text=" ", bg="lightblue")
                                  for _ in range(10)] for _ in range(10)]

        for i in range(10):
            for j in range(10):
                self.player_buttons[i][j].grid(row=i+1, column=j+1)
                self.opponent_buttons[i][j].grid(row=i+1, column=j+1)

    def create_attack_button(self):
        self.attack_button = tk.Button(self.root, text="Abandonner", command=self.abandon_game)
        self.attack_button.pack(side="bottom", pady=10)

    def attack(self, x, y):
        # Appel à GameManager pour exécuter l'attaque
        self.game_manager_interface.make_request(1, x, y)  # 1 pour type PLAY
        self.receive_and_handle_response()

    def receive_and_handle_response(self):
        response = self.game_manager_interface.client.receive_response()
        game_over = self.game_manager_interface.handle_response(response)
        self.game_manager_interface.update_interface()
        if game_over:
            self.end_game()

    def abandon_game(self):
        # Appel à GameManager pour abandonner le jeu
        self.game_manager_interface.make_request(2, None, None)  # 2 pour type ABANDON
        self.receive_and_handle_response()

    def end_game(self):
        # Afficher un message indiquant la fin du jeu et fermer l'application
        messagebox.showinfo("Fin du jeu", "Le jeu est terminé.")
        self.root.destroy()

    def run(self):
        self.root.mainloop()
