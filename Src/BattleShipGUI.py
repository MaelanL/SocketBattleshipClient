import tkinter as tk

# Configuration initiale pour la taille de la grille
GRID_SIZE = 10

class BattleShipGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Bataille Navale")

        # Création d'une frame pour la grille de jeu
        self.grid_frame = tk.Frame(self.root)
        self.grid_frame.pack()

        # Initialisation de la grille de boutons pour représenter le champ de bataille
        self.buttons = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                btn = tk.Button(self.grid_frame, text=' ', width=4, height=2,
                                command=lambda x=x, y=y: self.button_click(x, y))
                btn.grid(row=y+1, column=x+1)
                self.buttons[y][x] = btn

        # Ajout des numéros autour de la grille (en haut et à gauche)
        for i in range(1, GRID_SIZE+1):
            tk.Label(self.grid_frame, text=str(i)).grid(row=0, column=i)
            tk.Label(self.grid_frame, text=str(i)).grid(row=i, column=0)

    def button_click(self, x, y):
        print(f"Button clicked at {x}, {y}")
        # Ici, vous ajouterez la logique pour communiquer avec le serveur

        # Pour l'exemple, on marque simplement le bouton avec une 'X'
        self.buttons[y][x].config(text='X', state='disabled')

# Démarrer l'interface graphique
def main():
    root = tk.Tk()
    gui = BattleShipGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
